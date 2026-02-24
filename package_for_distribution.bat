@echo off
echo ================================
echo EX Tool - Packager
echo ================================
echo.

REM Check if exe exists
if not exist dist\EX-Tool.exe (
    echo ERROR: Executable not found!
    echo Please run build_simple.bat first.
    pause
    exit /b 1
)

REM Create distribution folder
echo Creating distribution package...
if exist "EX-Tool-Release" rmdir /s /q "EX-Tool-Release"
mkdir "EX-Tool-Release"

REM Copy executable
echo Copying executable...
copy "dist\EX-Tool.exe" "EX-Tool-Release\"

REM Copy assets folder
echo Copying assets...
xcopy "assets" "EX-Tool-Release\assets\" /E /I /Y

REM Create README
echo Creating README...
(
echo EX Tool v0.1
echo ================================
echo.
echo INSTALLATION:
echo 1. Extract all files to a folder
echo 2. Run EX-Tool.exe
echo.
echo REQUIREMENTS:
echo - Windows 7/8/10/11
echo - Gameloop Emulator installed
echo - PUBG Mobile installed in Gameloop
echo.
echo FEATURES:
echo - Fix graphics settings for all PUBG Mobile versions
echo - Unlock FPS limits
echo - Change graphics styles
echo - Gameloop optimizer
echo - iPad view support
echo.
echo USAGE:
echo 1. Open Gameloop and start PUBG Mobile
echo 2. Run this tool
echo 3. Click "Connect to Gameloop"
echo 4. Select your desired graphics settings
echo 5. Click "Submit"
echo.
echo ================================
echo EX Tool
echo ================================
) > "EX-Tool-Release\README.txt"

REM Create ZIP archive (requires PowerShell)
echo.
echo Creating ZIP archive...
powershell -command "Compress-Archive -Path 'EX-Tool-Release\*' -DestinationPath 'EX-Tool-v0.1.zip' -Force"

echo.
echo ================================
echo Package created successfully!
echo.
echo Distribution folder: EX-Tool-Release\
echo ZIP archive: EX-Tool-v0.1.zip
echo.
echo You can now share the ZIP file with other gamers!
echo ================================
pause
