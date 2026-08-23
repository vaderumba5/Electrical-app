@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo.
echo ==========================================
echo   APP ELECTRICA - INSTALAR PYTHON
echo ==========================================
echo.

where winget >nul 2>&1
if errorlevel 1 (
  echo No se ha encontrado winget en este equipo.
  echo Abriendo la pagina oficial de Python para Windows...
  start "" "https://www.python.org/downloads/windows/"
  echo.
  echo Instala Python 3 y marca la opcion "Add Python to PATH".
  echo Despues vuelve a ejecutar start_windows.bat.
  pause
  exit /b 1
)

echo Se instalara Python 3.12 para el usuario actual.
echo.
winget install -e --id Python.Python.3.12 --scope user --accept-source-agreements --accept-package-agreements
if errorlevel 1 (
  echo.
  echo No se pudo completar la instalacion automaticamente.
  echo Puedes instalar Python desde https://www.python.org/downloads/windows/
  pause
  exit /b 1
)

echo.
echo Python instalado. Continuando con la app...
call "%~dp0start_windows.bat"
