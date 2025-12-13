# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect all submodules for problematic packages
ping3_datas, ping3_binaries, ping3_hiddenimports = collect_all('ping3')
adbutils_datas, adbutils_binaries, adbutils_hiddenimports = collect_all('adbutils')
wmi_datas, wmi_binaries, wmi_hiddenimports = collect_all('wmi')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=ping3_binaries + adbutils_binaries + wmi_binaries,
    datas=[
        ('assets', 'assets'),
        ('images', 'images'),
    ] + ping3_datas + adbutils_datas + wmi_datas,
    hiddenimports=[
        'adbutils',
        'GPUtil',
        'ping3',
        'psutil',
        'pywintypes',
        'pythoncom',
        'win32com.client',
        'win32com.shell',
        'win32api',
        'win32timezone',
        'winshell',
        'wmi',
        'xmltodict',
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
    ] + ping3_hiddenimports + adbutils_hiddenimports + wmi_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='MK-PUBG-Mobile-Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/logo.ico'
)
