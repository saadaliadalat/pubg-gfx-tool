@echo off
echo ============================================
echo MK PUBG Mobile Tool - Build Script
echo ============================================
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Building executable with PyInstaller...
pyinstaller --noconfirm --onefile --windowed --icon=assets/icons/logo.ico --name=MK-PUBG-Mobile-Tool --add-data="assets;assets" --add-data="images;images" --hidden-import=adbutils --hidden-import=GPUtil --hidden-import=ping3 --hidden-import=psutil --hidden-import=pywintypes --hidden-import=win32com.client --hidden-import=win32api --hidden-import=winshell --hidden-import=wmi --hidden-import=xmltodict --hidden-import=PyQt5 --collect-all=adbutils --collect-all=PyQt5 main.py

echo.
echo ============================================
echo BUILD COMPLETE!
echo ============================================
echo Executable location: dist\MK-PUBG-Mobile-Tool.exe
echo.
pause
