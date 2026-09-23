@echo off
setlocal
cd /d "%~dp0"

py -3 --version >nul 2>&1
if not errorlevel 1 (
    py -3 -m pip install -r "%~dp0requirements.txt"
    goto result
)

python --version >nul 2>&1
if errorlevel 1 (
    echo Python was not found. Install Python 3.10 or newer and try again.
    pause
    exit /b 1
)
python -m pip install -r "%~dp0requirements.txt"

:result
if errorlevel 1 (
    echo.
    echo Installation failed. Check the error above and your internet connection.
    pause
    exit /b 1
)
echo.
echo Dependencies installed successfully.
echo To start the app, run: python app.py
pause
exit /b 0
