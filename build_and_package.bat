@echo off
echo ================================
echo EX Tool
echo Build ^& Package for Distribution
echo ================================
echo.

REM Step 1: Build
echo [1/2] Building executable...
call build_simple.bat

REM Check if build was successful
if not exist dist\EX-Tool.exe (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ================================
echo.

REM Step 2: Package
echo [2/2] Creating distribution package...
call package_for_distribution.bat
