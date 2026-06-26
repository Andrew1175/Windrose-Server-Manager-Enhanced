param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

$LocalPython = Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"
$Python = $null

if (Test-Path $LocalPython) {
    $Python = $LocalPython
}
else {
    $PythonCommand = Get-Command python -ErrorAction SilentlyContinue
    $Python = if ($PythonCommand) { $PythonCommand.Source } else { $null }
}

if (-not $Python) {
    Write-Error "Python was not found. Install Python 3.11+ on the build machine, then run this script again."
    exit 1
}

if ($Clean) {
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ".\build", ".\dist"
}

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    & $Python -m venv .venv
}

$VenvPython = ".\.venv\Scripts\python.exe"
$VenvPip = ".\.venv\Scripts\pip.exe"

& $VenvPython -m pip install --upgrade pip
& $VenvPip install -r requirements.txt pyinstaller
& $VenvPython -m PyInstaller --clean --noconfirm ".\pyinstaller-manager.spec"

$Exe = ".\dist\Windrose-Server-Manager\Windrose-Server-Manager.exe"
if (-not (Test-Path $Exe)) {
    Write-Error "Build completed, but expected EXE was not found: $Exe"
    exit 1
}

Write-Host "Build complete:"
Write-Host (Resolve-Path ".\dist\Windrose-Server-Manager")
