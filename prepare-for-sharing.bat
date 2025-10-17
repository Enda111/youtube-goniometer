@echo off
echo ========================================
echo  Preparing YouTube Goniometer for Sharing
echo ========================================
echo.

echo Checking files...
echo.

REM Check if executable exists
if exist "dist\YouTube-Goniometer.exe" (
    echo ✓ Executable found: YouTube-Goniometer.exe
    for %%A in ("dist\YouTube-Goniometer.exe") do echo   Size: %%~zA bytes
) else (
    echo ✗ Executable not found. Run: pyinstaller --onefile --windowed app.py
    goto :end
)

REM Check if distribution packages exist
if exist "dist\*.whl" (
    echo ✓ Python packages found
) else (
    echo ✗ Python packages not found. Run: python -m build
)

echo.
echo Files ready for sharing:
echo.
dir /b dist\*
echo.

echo ========================================
echo  SHARING OPTIONS:
echo ========================================
echo.
echo 1. GITHUB (Recommended):
echo    - Create repository at github.com
echo    - Upload all files
echo    - Create release with YouTube-Goniometer.exe
echo.
echo 2. DIRECT SHARING:
echo    - Zip the 'dist' folder
echo    - Share via Google Drive, Dropbox, etc.
echo.
echo 3. SIMPLE SHARING:
echo    - Just share YouTube-Goniometer.exe
echo    - Recipients can run it immediately
echo.
echo ========================================
echo  WHAT USERS NEED:
echo ========================================
echo.
echo - FFmpeg installed (for YouTube audio)
echo - Audio device connected
echo - Windows computer
echo.
echo That's it! No Python installation needed.
echo.

:end
pause