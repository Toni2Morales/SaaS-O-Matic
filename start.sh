#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
backend_dir="$repo_root/backend"
frontend_dir="$repo_root/frontend"
runtime_base="${XDG_RUNTIME_DIR:-${TMPDIR:-/tmp}}"
runtime_dir="$runtime_base/saas-o-matic-${UID:-$(id -u)}"
state_file="$runtime_dir/services"
started_pids=()
state_written=0

info() { printf '[SaaS-O-Matic] %s\n' "$*"; }
fail() { printf '[SaaS-O-Matic] ERROR: %s\n' "$*" >&2; }

listening() {
  local port="$1"
  "$python_exe" -c 'import socket,sys; s=socket.socket(); s.settimeout(.25); result=s.connect_ex(("127.0.0.1",int(sys.argv[1]))); s.close(); raise SystemExit(0 if result == 0 else 1)' "$port" >/dev/null 2>&1
}

process_command() {
  local pid="$1"
  if command -v ps >/dev/null 2>&1; then ps -p "$pid" -o args= 2>/dev/null || true; fi
}

verify_owned() {
  local pid="$1" signature="$2" command
  command="$(process_command "$pid")"
  [[ -n "$command" && "$command" == *"$signature"* && "$command" == *"$repo_root"* ]]
}

stop_services() {
  if [[ ! -f "$state_file" ]]; then info 'No hay procesos propios registrados para detener.'; return 0; fi
  local saved_root saved_pids pid signature remaining
  IFS=$'\t' read -r saved_root saved_pids < "$state_file"
  [[ "$saved_root" == "$repo_root" ]] || { fail 'El registro pertenece a otra ruta; no se tocará.'; return 1; }
  IFS=',' read -r -a pids <<< "$saved_pids"
  IFS=',' read -r -a signatures <<< "$(sed -n '2p' "$state_file")"
  for ((i=${#pids[@]}-1; i>=0; i--)); do
    pid="${pids[$i]}"
    signature="${signatures[$i]:-}"
    if kill -0 "$pid" 2>/dev/null; then
      if ! verify_owned "$pid" "$signature"; then
        fail "PID $pid no coincide con el comando registrado; no se detendrá."
        return 1
      fi
      kill -TERM "$pid" || { fail "No se pudo solicitar parada segura para PID $pid."; return 1; }
      remaining=0
      for _ in {1..40}; do
        if ! kill -0 "$pid" 2>/dev/null; then remaining=1; break; fi
        sleep 0.25
      done
      if [[ "$remaining" -eq 0 ]]; then fail "PID propio $pid no terminó con SIGTERM; se preserva y requiere revisión manual."; return 1; fi
      info "Servicio propio detenido (PID $pid)."
    fi
  done
  rm -- "$state_file"
  info 'Servicios detenidos; SQLite y registros se preservan.'
}

cleanup_on_error() {
  local exit_code=$?
  if [[ "$exit_code" -ne 0 && ${#started_pids[@]} -gt 0 ]]; then
    for ((i=${#started_pids[@]}-1; i>=0; i--)); do
      local pid="${started_pids[$i]}" signature="${started_signatures[$i]}"
      if kill -0 "$pid" 2>/dev/null; then
        if verify_owned "$pid" "$signature"; then
          kill -TERM "$pid" 2>/dev/null || true
          info "Limpieza solicitada para el proceso propio PID $pid."
        else
          fail "No se pudo verificar PID $pid; no se detuvo."
        fi
      fi
    done
  fi
  if [[ "$state_written" -eq 1 && "$exit_code" -ne 0 ]]; then rm -f -- "$state_file"; fi
  exit "$exit_code"
}
trap cleanup_on_error EXIT

if [[ "${1:-}" == "--stop" || "${1:-}" == "-s" ]]; then
  python_exe="$(command -v python3.13 || true)"
  if [[ -z "$python_exe" ]]; then fail 'Python 3.13 se necesita para comprobar puertos/parada.'; exit 1; fi
  stop_services
  trap - EXIT
  exit 0
fi
if [[ $# -ne 0 ]]; then fail 'Uso: bash start.sh [--stop]'; exit 2; fi

[[ -f "$backend_dir/pyproject.toml" && -f "$frontend_dir/package-lock.json" ]] || { fail 'No se reconoce la raíz del proyecto (faltan manifests).'; exit 1; }
python_exe="$(command -v python3.13 || true)"
[[ -n "$python_exe" ]] || { fail 'Se requiere Python 3.13 disponible como python3.13; no se instalará automáticamente.'; exit 1; }
python_version="$("$python_exe" --version 2>&1)"
[[ "$python_version" =~ ^Python\ 3\.13\. ]] || { fail "Se requiere Python >=3.13,<3.14; detectado: $python_version"; exit 1; }
node_exe="$(command -v node || true)"
npm_exe="$(command -v npm || true)"
[[ -n "$node_exe" && -n "$npm_exe" ]] || { fail 'Se requieren Node.js 24.15+ y npm 11 en PATH; no se instalarán automáticamente.'; exit 1; }
node_version="$("$node_exe" --version)"
npm_version="$("$npm_exe" --version)"
[[ "$node_version" =~ ^v24\.([0-9]+)\. && ${BASH_REMATCH[1]} -ge 15 ]] || { fail "Se requiere Node.js >=24.15,<25; detectado: $node_version"; exit 1; }
[[ "$npm_version" =~ ^11\. ]] || { fail "Se requiere npm >=11,<12; detectado: $npm_version"; exit 1; }

if listening 8000; then fail 'Puerto 8000 ocupado en loopback. Libéralo manualmente; no se detendrá el proceso.'; exit 1; fi
if listening 4200; then fail 'Puerto 4200 ocupado en loopback. Libéralo manualmente; no se detendrá el proceso.'; exit 1; fi
[[ ! -e "$state_file" ]] || { fail "Existe estado previo en $state_file; comprueba procesos y usa bash start.sh --stop si son de esta copia."; exit 1; }

venv_python="$backend_dir/.venv/bin/python"
if [[ ! -x "$venv_python" ]]; then
  info 'Creando backend/.venv con el Python 3.13 ya instalado...'
  "$python_exe" -m venv "$backend_dir/.venv"
fi
venv_version="$("$venv_python" --version 2>&1)"
[[ "$venv_version" =~ ^Python\ 3\.13\. ]] || { fail "backend/.venv existe pero no usa Python 3.13 ($venv_version); no se borrará ni reemplazará."; exit 1; }

info 'Instalando/validando dependencias Python únicamente en backend/.venv...'
(cd -- "$backend_dir" && "$venv_python" -m pip install -e . -c requirements.lock)
(cd -- "$backend_dir" && "$venv_python" -m pip check)
(cd -- "$backend_dir" && "$venv_python" -m alembic upgrade head)

info 'Instalando frontend desde package-lock.json con npm ci --ignore-scripts...'
(cd -- "$frontend_dir" && "$npm_exe" ci --ignore-scripts)

mkdir -p -- "$runtime_dir"
api_log="$runtime_dir/api.log"
frontend_log="$runtime_dir/frontend.log"
api_signature="$repo_root/backend/.venv/bin/python -m uvicorn saas_o_matic.bootstrap.main:app --host 127.0.0.1 --port 8000"
frontend_signature="$repo_root/frontend/node_modules/.bin/ng serve --host 127.0.0.1 --port 4200"
(cd -- "$backend_dir" && exec "$venv_python" -m uvicorn saas_o_matic.bootstrap.main:app --host 127.0.0.1 --port 8000) >>"$api_log" 2>&1 &
api_pid=$!
started_pids+=("$api_pid")
started_signatures+=("$api_signature")
(cd -- "$frontend_dir" && exec "$frontend_dir/node_modules/.bin/ng" serve --host 127.0.0.1 --port 4200) >>"$frontend_log" 2>&1 &
frontend_pid=$!
started_pids+=("$frontend_pid")
started_signatures+=("$frontend_signature")
printf '%s\t%s,%s\n%s,%s\n' "$repo_root" "$api_pid" "$frontend_pid" "$api_signature" "$frontend_signature" > "$state_file"
state_written=1

api_ready=0
frontend_ready=0
for _ in {1..120}; do
  if ! kill -0 "$api_pid" 2>/dev/null; then fail "FastAPI terminó; revisa $api_log"; exit 1; fi
  if ! kill -0 "$frontend_pid" 2>/dev/null; then fail "Angular terminó; revisa $frontend_log"; exit 1; fi
  if [[ "$api_ready" -eq 0 ]] && "$venv_python" -c 'import json,sys,urllib.request; data=json.load(urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=2)); raise SystemExit(0 if data.get("status")=="ok" else 1)' >/dev/null 2>&1; then api_ready=1; fi
  if [[ "$frontend_ready" -eq 0 ]] && "$venv_python" -c 'import urllib.request; r=urllib.request.urlopen("http://127.0.0.1:4200/", timeout=2); raise SystemExit(0 if r.status==200 else 1)' >/dev/null 2>&1; then frontend_ready=1; fi
  [[ "$api_ready" -eq 1 && "$frontend_ready" -eq 1 ]] && break
  sleep 0.5
done
[[ "$api_ready" -eq 1 ]] || { fail "FastAPI no respondió en /health; revisa $api_log"; exit 1; }
[[ "$frontend_ready" -eq 1 ]] || { fail "Angular no respondió; revisa $frontend_log"; exit 1; }

info 'Backend: DISPONIBLE (http://127.0.0.1:8000/health).'
info 'Frontend: DISPONIBLE (http://127.0.0.1:4200).'
info 'Swagger/OpenAPI: http://127.0.0.1:8000/docs (schema: /openapi.json).'
info 'Datos SQLite: backend/var/saas_o_matic.sqlite3; se conservan al detener/reiniciar.'
info 'Para detener únicamente estos procesos verificados: bash start.sh --stop'
info "Logs: $runtime_dir"
trap - EXIT
