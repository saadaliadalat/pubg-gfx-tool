@echo off
echo ================================
echo MK PUBG Mobile Tool - Packager
echo ================================
echo.

REM Check if exe exists
if not exist dist\MK-PUBG-Mobile-Tool.exe (
    echo ERROR: Executable not found!
    echo Please run build_simple.bat first.
    pause
    exit /b 1
)

REM Create distribution folder
echo Creating distribution package...
if exist "MK-PUBG-Mobile-Tool-Release" rmdir /s /q "MK-PUBG-Mobile-Tool-Release"
mkdir "MK-PUBG-Mobile-Tool-Release"

REM Copy executable
echo Copying executable...
copy "dist\MK-PUBG-Mobile-Tool.exe" "MK-PUBG-Mobile-Tool-Release\"

REM Copy assets folder
echo Copying assets...
xcopy "assets" "MK-PUBG-Mobile-Tool-Release\assets\" /E /I /Y

REM Create README
echo Creating README...
(
echo MK PUBG Mobile Tool v1.0.8
echo ================================
echo.
echo INSTALLATION:
echo 1. Extract all files to a folder
echo 2. Run MK-PUBG-Mobile-Tool.exe
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
echo CONTACT:
echo GitHub: https://github.com/MohamedKVIP
echo Discord: https://discord.gg/PDPJM6e6PC
echo.
echo ================================
echo By Mohamed Kamal ^(MKvip^)
echo ================================
) > "MK-PUBG-Mobile-Tool-Release\README.txt"

REM Create ZIP archive (requires PowerShell)
echo.
echo Creating ZIP archive...
powershell -command "Compress-Archive -Path 'MK-PUBG-Mobile-Tool-Release\*' -DestinationPath 'MK-PUBG-Mobile-Tool-v1.0.8.zip' -Force"

echo.
echo ================================
echo Package created successfully!
echo.
echo Distribution folder: MK-PUBG-Mobile-Tool-Release\
echo ZIP archive: MK-PUBG-Mobile-Tool-v1.0.8.zip
echo.
echo You can now share the ZIP file with other gamers!
echo ================================
pause
