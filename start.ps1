[CmdletBinding()]
param(
    [switch]$Stop
)

$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$backendDir = Join-Path $repoRoot 'backend'
$frontendDir = Join-Path $repoRoot 'frontend'
$runtimeDir = Join-Path $env:LOCALAPPDATA 'SaaS-O-Matic\run'
$stateFile = Join-Path $runtimeDir 'services.json'

function Write-Info([string]$Message) { Write-Host "[SaaS-O-Matic] $Message" }
function Write-Failure([string]$Message) { Write-Error "[SaaS-O-Matic] $Message" }

function Get-ListeningProcess([int]$Port) {
    return Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue |
        Select-Object -First 1
}

function Get-OwnedProcess($Record) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $($Record.pid)" -ErrorAction SilentlyContinue
    if (-not $process) { return $null }
    $expectedExe = [IO.Path]::GetFullPath([string]$Record.executable)
    $actualExe = [IO.Path]::GetFullPath([string]$process.ExecutablePath)
    $command = [string]$process.CommandLine
    if ($actualExe -ne $expectedExe -or $command -notlike "*$($Record.signature)*" -or $command -notlike "*$repoRoot*") {
        throw "El PID $($Record.pid) ya no coincide con el proceso de SaaS-O-Matic registrado. No se detendrá."
    }
    return $process
}

function Stop-OwnServices {
    if (-not (Test-Path -LiteralPath $stateFile)) {
        Write-Info 'No hay procesos propios registrados para detener.'
        return
    }
    $state = Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
    if ($state.repository -ne $repoRoot) { throw 'El registro de procesos pertenece a otra ruta; no se tocará.' }
    foreach ($record in @($state.services | Sort-Object port -Descending)) {
        $process = Get-OwnedProcess $record
        if ($process) {
            Stop-Process -Id $process.ProcessId -ErrorAction Stop
            $stopped = $false
            for ($attempt = 0; $attempt -lt 20; $attempt++) {
                if (-not (Get-CimInstance Win32_Process -Filter "ProcessId = $($record.pid)" -ErrorAction SilentlyContinue)) { $stopped = $true; break }
                Start-Sleep -Milliseconds 500
            }
            if (-not $stopped) { throw "El proceso propio PID $($record.pid) no terminó; queda preservado." }
            Write-Info "Servicio propio detenido (PID $($record.pid), puerto $($record.port))."
        }
    }
    Remove-Item -LiteralPath $stateFile -Force
    Write-Info 'Servicios detenidos. La base SQLite y los registros no se han borrado.'
}

if ($Stop) {
    try { Stop-OwnServices; exit 0 }
    catch { Write-Failure $_; exit 1 }
}

$started = [Collections.Generic.List[object]]::new()
$stateWritten = $false
try {
    if (-not (Test-Path -LiteralPath (Join-Path $backendDir 'pyproject.toml')) -or
        -not (Test-Path -LiteralPath (Join-Path $frontendDir 'package-lock.json'))) {
        throw 'No se reconoció la raíz del proyecto (faltan manifests backend/frontend).'
    }

    $pythonCommand = Get-Command py -ErrorAction SilentlyContinue
    if ($pythonCommand) {
        & $pythonCommand.Source -3.13 -c 'import sys; print(sys.executable)' *> $null
        if ($LASTEXITCODE -eq 0) { $pythonBase = $pythonCommand.Source; $pythonPrefix = @('-3.13') }
    }
    if (-not $pythonBase) {
        $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
        if (-not $pythonCommand) { throw 'No se encontró Python 3.13. Instálalo manualmente y vuelve a ejecutar; no se instalará software automáticamente.' }
        $pythonBase = $pythonCommand.Source
        $pythonPrefix = @()
    }
    $pythonVersionText = & $pythonBase @pythonPrefix --version 2>&1
    if ($LASTEXITCODE -ne 0 -or $pythonVersionText -notmatch '^Python 3\.13\.') {
        throw "Se requiere Python >=3.13,<3.14; se detectó '$pythonVersionText'."
    }

    $nodeCommand = Get-Command node -ErrorAction SilentlyContinue
    $npmCommand = Get-Command npm.cmd -ErrorAction SilentlyContinue
    if (-not $npmCommand) { $npmCommand = Get-Command npm -ErrorAction SilentlyContinue }
    if (-not $nodeCommand -or -not $npmCommand) { throw 'Se requieren Node.js 24 y npm 11 en PATH. No se instalarán automáticamente.' }
    $nodeVersion = (& $nodeCommand.Source --version).Trim()
    $npmVersion = (& $npmCommand.Source --version).Trim()
    if ($LASTEXITCODE -ne 0 -or $nodeVersion -notmatch '^v24\.(\d+)\.' -or [int]$Matches[1] -lt 15) {
        throw "Se requiere Node.js >=24.15,<25; se detectó '$nodeVersion'."
    }
    if ($npmVersion -notmatch '^11\.') { throw "Se requiere npm >=11,<12; se detectó '$npmVersion'." }

    if (Get-ListeningProcess 8000) { throw 'El puerto 8000 ya está ocupado en loopback. No se detuvo ni modificó el proceso existente; libéralo manualmente y reintenta.' }
    if (Get-ListeningProcess 4200) { throw 'El puerto 4200 ya está ocupado en loopback. No se detuvo ni modificó el proceso existente; libéralo manualmente y reintenta.' }
    if (Test-Path -LiteralPath $stateFile) { throw "Ya hay un estado de ejecución en '$stateFile'. Comprueba servicios y usa .\start.ps1 -Stop si pertenecen a esta copia." }

    $venvPython = Join-Path $backendDir '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $venvPython)) {
        Write-Info 'Creando backend/.venv con el Python 3.13 ya instalado...'
        & $pythonBase @pythonPrefix -m venv (Join-Path $backendDir '.venv')
        if ($LASTEXITCODE -ne 0) { throw 'Falló la creación de backend/.venv.' }
    }
    if (-not (Test-Path -LiteralPath $venvPython)) { throw 'No se encontró el Python esperado dentro de backend/.venv.' }
    $venvVersion = (& $venvPython --version 2>&1).ToString()
    if ($LASTEXITCODE -ne 0 -or $venvVersion -notmatch '^Python 3\.13\.') {
        throw "backend/.venv existe pero no usa Python 3.13 ('$venvVersion'). No se borró ni reemplazó; resuélvelo manualmente."
    }

    Write-Info 'Instalando/validando dependencias Python dentro de backend/.venv...'
    Push-Location $backendDir
    try {
        & $venvPython -m pip install -e . -c requirements.lock
        if ($LASTEXITCODE -ne 0) { throw 'Falló la instalación de dependencias Python en backend/.venv.' }
        & $venvPython -m pip check
        if ($LASTEXITCODE -ne 0) { throw 'pip check detectó dependencias incompatibles en backend/.venv.' }
        & $venvPython -m alembic upgrade head
        if ($LASTEXITCODE -ne 0) { throw 'Falló Alembic upgrade head. No se inició ningún servicio.' }
    }
    finally { Pop-Location }

    Write-Info 'Instalando frontend desde package-lock.json con npm ci --ignore-scripts...'
    Push-Location $frontendDir
    try {
        & $npmCommand.Source ci --ignore-scripts
        if ($LASTEXITCODE -ne 0) { throw 'Falló npm ci --ignore-scripts. No se inició ningún servicio.' }
    }
    finally { Pop-Location }

    New-Item -ItemType Directory -Path $runtimeDir -Force | Out-Null
    $pythonExe = [IO.Path]::GetFullPath($venvPython)
    $nodeExe = [IO.Path]::GetFullPath($nodeCommand.Source)
    $ngCli = [IO.Path]::GetFullPath((Join-Path $frontendDir 'node_modules\@angular\cli\bin\ng.js'))
    if (-not (Test-Path -LiteralPath $ngCli)) { throw 'No se encuentra Angular CLI local después de npm ci.' }

    $apiOut = Join-Path $runtimeDir 'api.log'
    $apiErr = Join-Path $runtimeDir 'api.err.log'
    $api = Start-Process -FilePath $pythonExe -ArgumentList @('-m','uvicorn','saas_o_matic.bootstrap.main:app','--host','127.0.0.1','--port','8000') -WorkingDirectory $backendDir -PassThru -RedirectStandardOutput $apiOut -RedirectStandardError $apiErr
    $started.Add([pscustomobject]@{name='backend';port=8000;pid=$api.Id;executable=$pythonExe;signature='uvicorn saas_o_matic.bootstrap.main:app --host 127.0.0.1 --port 8000'})

    $webOut = Join-Path $runtimeDir 'frontend.log'
    $webErr = Join-Path $runtimeDir 'frontend.err.log'
    $web = Start-Process -FilePath $nodeExe -ArgumentList @($ngCli,'serve','--host','127.0.0.1','--port','4200') -WorkingDirectory $frontendDir -PassThru -RedirectStandardOutput $webOut -RedirectStandardError $webErr
    $started.Add([pscustomobject]@{name='frontend';port=4200;pid=$web.Id;executable=$nodeExe;signature="$ngCli serve --host 127.0.0.1 --port 4200"})

    $state = [ordered]@{repository=$repoRoot;created_at_utc=[DateTime]::UtcNow.ToString('o');services=@($started)}
    $state | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $stateFile -Encoding utf8
    $stateWritten = $true

    $apiReady = $false
    $webReady = $false
    for ($attempt = 0; $attempt -lt 80; $attempt++) {
        foreach ($service in $started) {
            $process = Get-OwnedProcess $service
            if (-not $process) { throw "El servicio $($service.name) terminó durante el arranque. Revisa logs en '$runtimeDir'." }
        }
        if (-not $apiReady) {
            try { $health = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health' -TimeoutSec 2; $apiReady = $health.status -eq 'ok' } catch { }
        }
        if (-not $webReady) {
            try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:4200/' -TimeoutSec 2; $webReady = $response.StatusCode -eq 200 } catch { }
        }
        if ($apiReady -and $webReady) { break }
        Start-Sleep -Milliseconds 500
    }
    if (-not $apiReady) { throw "FastAPI no respondió en http://127.0.0.1:8000/health. Revisa '$apiErr'." }
    if (-not $webReady) { throw "Angular no respondió en http://127.0.0.1:4200/. Revisa '$webErr'." }

    Write-Info 'Backend: DISPONIBLE (http://127.0.0.1:8000/health).'
    Write-Info 'Frontend: DISPONIBLE (http://127.0.0.1:4200).'
    Write-Info 'Swagger/OpenAPI: http://127.0.0.1:8000/docs (schema: /openapi.json).'
    Write-Info "Datos SQLite: backend/var/saas_o_matic.sqlite3 (se preservan al detener/reiniciar)."
    Write-Info "Para detener únicamente estos procesos verificados: .\start.ps1 -Stop"
    Write-Info "Logs: $runtimeDir"
}
catch {
    Write-Failure $_
    if ($started.Count -gt 0) {
        foreach ($service in @($started | Sort-Object port -Descending)) {
            try {
                $process = Get-OwnedProcess $service
                if ($process) { Stop-Process -Id $process.ProcessId -ErrorAction Stop; Write-Info "Limpieza: detenido proceso propio PID $($service.pid)." }
            }
            catch { Write-Warning "No se pudo verificar/detener automáticamente PID $($service.pid): $_" }
        }
    }
    if ($stateWritten -and (Test-Path -LiteralPath $stateFile)) { Remove-Item -LiteralPath $stateFile -Force -ErrorAction SilentlyContinue }
    exit 1
}
