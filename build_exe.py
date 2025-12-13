"""
Build script for MK PUBG Mobile Tool
This script creates an executable using PyInstaller
"""

import os
import sys
import subprocess

# PyInstaller command with all necessary options
pyinstaller_cmd = [
    'pyinstaller',
    '--noconfirm',
    '--onefile',
    '--windowed',
    '--icon=assets/icons/logo.ico',
    '--name=MK-PUBG-Mobile-Tool',
    '--add-data=assets;assets',
    '--add-data=images;images',
    '--hidden-import=adbutils',
    '--hidden-import=GPUtil',
    '--hidden-import=ping3',
    '--hidden-import=psutil',
    '--hidden-import=pywintypes',
    '--hidden-import=win32com.client',
    '--hidden-import=win32api',
    '--hidden-import=winshell',
    '--hidden-import=wmi',
    '--hidden-import=xmltodict',
    '--hidden-import=PyQt5',
    '--collect-all=adbutils',
    '--collect-all=PyQt5',
    'main.py'
]

print("Building MK PUBG Mobile Tool executable...")
print("This may take several minutes...")
print()

try:
    # Run PyInstaller
    result = subprocess.run(pyinstaller_cmd, check=True)

    if result.returncode == 0:
        print()
        print("=" * 60)
        print("BUILD SUCCESSFUL!")
        print("=" * 60)
        print("Executable location: dist/MK-PUBG-Mobile-Tool.exe")
        print()
    else:
        print("Build failed with errors.")
        sys.exit(1)

except subprocess.CalledProcessError as e:
    print(f"Error during build: {e}")
    sys.exit(1)
except FileNotFoundError:
    print("ERROR: PyInstaller not found!")
    print("Please install PyInstaller first:")
    print("  pip install pyinstaller")
    sys.exit(1)
