@echo off
cd /d "%~dp0"
where pyw.exe >nul 2>nul
if %errorlevel%==0 (
  start "Gai Desktop Pet" pyw.exe "%~dp0GaiDesktopPet.pyw"
  exit /b 0
)
where pythonw.exe >nul 2>nul
if %errorlevel%==0 (
  start "Gai Desktop Pet" pythonw.exe "%~dp0GaiDesktopPet.pyw"
  exit /b 0
)
echo Python 3 is required. Download it from https://www.python.org/downloads/windows/
pause
