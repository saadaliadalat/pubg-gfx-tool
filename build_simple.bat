@echo off
echo ============================================
echo MK PUBG Mobile Tool - Simple Build
echo ============================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo Step 2: Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist MK-PUBG-Mobile-Tool.spec.backup del MK-PUBG-Mobile-Tool.spec.backup
echo.

echo Step 3: Building executable using spec file...
pyinstaller MK-PUBG-Mobile-Tool.spec
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo BUILD SUCCESSFUL!
echo ============================================
echo.
echo Executable created: dist\MK-PUBG-Mobile-Tool.exe
echo.
echo You can now run the exe file!
echo.
pause
