@echo off
echo ================================
echo MK PUBG Mobile Tool - Build Script
echo ================================
echo.

REM Clean previous build
echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo Building executable with PyInstaller...
pyinstaller --clean MK-PUBG-Mobile-Tool.spec

echo.
if exist dist\MK-PUBG-Mobile-Tool.exe (
    echo ================================
    echo Build completed successfully!
    echo Executable location: dist\MK-PUBG-Mobile-Tool.exe
    echo ================================
) else (
    echo ================================
    echo Build failed! Check the errors above.
    echo ================================
)

pause
