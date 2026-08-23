@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title App Electrica - Departamento Electrico

set "PYTHON_CMD="

where py >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=py -3"

if not defined PYTHON_CMD (
  where python >nul 2>&1
  if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
  for /f "usebackq delims=" %%P in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "$p=Get-ChildItem -Path $env:LOCALAPPDATA\Programs\Python -Filter python.exe -Recurse -ErrorAction SilentlyContinue ^| Sort-Object FullName -Descending ^| Select-Object -First 1; if($p){$p.FullName}"`) do set "PYTHON_CMD=%%P"
)

if not defined PYTHON_CMD goto NO_PYTHON

echo.
echo ==========================================
echo   APP ELECTRICA - DEPARTAMENTO ELECTRICO
echo ==========================================
echo.
echo Python detectado: !PYTHON_CMD!
echo.

echo Comprobando dependencias del backend...
!PYTHON_CMD! -c "import requests, bs4, pypdf" >nul 2>&1
if errorlevel 1 (
  echo Instalando dependencias necesarias por primera vez...
  !PYTHON_CMD! -m pip install --user -r "%~dp0requirements.txt"
  if errorlevel 1 (
    echo.
    echo No se pudieron instalar las dependencias.
    echo La app puede abrirse en modo local, pero sin busqueda web automatica.
    choice /C LS /N /M "Pulsa L para abrir modo local o S para salir: "
    if errorlevel 2 exit /b 1
    start "" "%~dp0index.html"
    exit /b 0
  )
)

echo.
echo Iniciando backend local en http://127.0.0.1:8765
echo El navegador se abrira automaticamente.
echo Para cerrar el backend, cierra esta ventana.
echo.
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Milliseconds 900; Start-Process 'http://127.0.0.1:8765'"
!PYTHON_CMD! "%~dp0backend.py"
if errorlevel 1 (
  echo.
  echo El backend se ha cerrado con un error.
  pause
)
exit /b 0

:NO_PYTHON
echo.
echo ==========================================
echo   PYTHON NO ESTA INSTALADO
echo ==========================================
echo.
echo El backend permite buscar datasheets y enriquecer articulos automaticamente.
echo Puedes instalar Python ahora o abrir la app sin backend.
echo.
echo [I] Instalar Python automaticamente con winget
echo [L] Abrir en modo local sin busqueda web automatica
echo [S] Salir
echo.
choice /C ILS /N /M "Selecciona una opcion: "
if errorlevel 3 exit /b 0
if errorlevel 2 (
  start "" "%~dp0index.html"
  exit /b 0
)
call "%~dp0instalar_python.bat"
exit /b %errorlevel%
