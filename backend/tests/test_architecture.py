"""Comprobaciones de las reglas de dependencia entre capas."""

import ast
from pathlib import Path

import saas_o_matic.domain as domain_package

PROJECT_PACKAGE = "saas_o_matic"
FRAMEWORKS = {"alembic", "fastapi", "pydantic", "sqlalchemy", "starlette", "uvicorn"}
LAYERS = {"application", "bootstrap", "domain", "infrastructure", "presentation"}
FORBIDDEN_BY_LAYER: dict[str, set[str]] = {
    "domain": LAYERS - {"domain"},
    "application": {"bootstrap", "infrastructure", "presentation"},
    "infrastructure": {"application", "bootstrap", "presentation"},
    "presentation": {"bootstrap", "domain", "infrastructure"},
}


def _package_root() -> Path:
    """Devuelve el directorio del paquete raíz del backend."""

    package_file = domain_package.__file__
    if package_file is None:
        raise RuntimeError("No se pudo localizar el paquete de dominio.")
    return Path(package_file).parent.parent


def _package_name(path: Path, package_root: Path) -> str:
    """Obtiene el paquete Python al que pertenece un archivo."""

    package_parts = path.relative_to(package_root).parent.parts
    return ".".join((PROJECT_PACKAGE, *package_parts))


def _resolve_import_from(node: ast.ImportFrom, package_name: str) -> str | None:
    """Resuelve un `from ... import ...` absoluto o relativo."""

    if node.level == 0:
        return node.module

    package_parts = package_name.split(".")
    if node.level > len(package_parts):
        return None

    base_parts = package_parts[: len(package_parts) - node.level + 1]
    if node.module:
        base_parts.extend(node.module.split("."))
    return ".".join(base_parts) if base_parts else None


def _imported_modules_from_source(source: str, package_name: str) -> set[str]:
    """Extrae los módulos importados por un fragmento de código.

    El análisis es estático: no detecta imports dinámicos como
    `importlib.import_module` o `__import__`.
    """

    tree = ast.parse(source)
    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = _resolve_import_from(node, package_name)
            if base is None:
                continue
            modules.add(base)
            modules.update(f"{base}.{alias.name}" for alias in node.names if alias.name != "*")

    return modules


def _imported_modules(path: Path, package_root: Path) -> set[str]:
    """Extrae los módulos importados por un archivo del proyecto."""

    source = path.read_text(encoding="utf-8")
    return _imported_modules_from_source(source, _package_name(path, package_root))


def _forbidden_modules(layer: str, modules: set[str]) -> set[str]:
    """Filtra los módulos que la capa no puede importar."""

    forbidden = FORBIDDEN_BY_LAYER[layer]
    findings: set[str] = set()

    for module in modules:
        parts = module.split(".")
        if (layer == "domain" and parts[0] in FRAMEWORKS) or (
            parts[0] == PROJECT_PACKAGE and len(parts) > 1 and parts[1] in forbidden
        ):
            findings.add(module)

    return findings


def _forbidden_imports(layer: str) -> list[tuple[Path, str]]:
    """Devuelve las importaciones prohibidas encontradas en una capa."""

    package_root = _package_root()
    package_dir = package_root / layer
    findings: list[tuple[Path, str]] = []

    for path in sorted(package_dir.rglob("*.py")):
        modules = _imported_modules(path, package_root)
        for module in sorted(_forbidden_modules(layer, modules)):
            findings.append((path, module))

    return findings


def test_domain_has_no_framework_or_outer_layer_dependencies() -> None:
    """El dominio no importa frameworks ni capas exteriores."""

    assert _forbidden_imports("domain") == []


def test_layer_dependencies_follow_the_allowed_direction() -> None:
    """Cada capa respeta las dependencias permitidas por el ADR 0002."""

    for layer in FORBIDDEN_BY_LAYER:
        assert _forbidden_imports(layer) == [], layer


def test_presentation_forbids_domain_imports() -> None:
    """La capa de presentación no puede importar el dominio."""

    modules = _imported_modules_from_source(
        "from saas_o_matic.domain import entity\n",
        "saas_o_matic.presentation",
    )

    assert "saas_o_matic.domain" in _forbidden_modules("presentation", modules)


def test_analyzer_detects_absolute_and_from_package_imports() -> None:
    """El analizador cubre las formas absolutas documentadas."""

    modules = _imported_modules_from_source(
        "import saas_o_matic.application\n"
        "from saas_o_matic.application import use_case\n"
        "from saas_o_matic import application\n",
        "saas_o_matic.domain",
    )

    assert "saas_o_matic.application" in modules
    assert "saas_o_matic.application" in _forbidden_modules("domain", modules)


def test_analyzer_resolves_relative_imports() -> None:
    """El analizador resuelve imports relativos según el paquete del archivo."""

    modules = _imported_modules_from_source(
        "from .. import application\nfrom ..application import use_case\n",
        "saas_o_matic.domain",
    )

    assert "saas_o_matic.application" in modules
    assert "saas_o_matic.application" in _forbidden_modules("domain", modules)


def test_analyzer_resolves_single_dot_import() -> None:
    """El analizador resuelve un import relativo de un solo punto."""

    modules = _imported_modules_from_source(
        "from . import application\n",
        "saas_o_matic",
    )

    assert "saas_o_matic.application" in modules


def test_analyzer_does_not_flag_local_relative_import() -> None:
    """Un submódulo local llamado `application` no es una capa exterior."""

    modules = _imported_modules_from_source(
        "from . import application\n",
        "saas_o_matic.domain",
    )

    assert "saas_o_matic.domain.application" in modules
    assert _forbidden_modules("domain", modules) == set()
