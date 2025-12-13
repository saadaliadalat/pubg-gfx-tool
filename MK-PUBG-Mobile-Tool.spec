# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

<<<<<<< HEAD
datas = [('assets', 'assets'), ('images', 'images')]
binaries = []
hiddenimports = ['adbutils', 'GPUtil', 'ping3', 'psutil', 'pywintypes', 'win32com.client', 'win32api', 'winshell', 'wmi', 'xmltodict', 'PyQt5']
tmp_ret = collect_all('adbutils')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PyQt5')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

=======
block_cipher = None
>>>>>>> f0898754ec718c530178568b743dbb7281b5b8b8

# Collect all submodules for problematic packages
ping3_datas, ping3_binaries, ping3_hiddenimports = collect_all('ping3')
adbutils_datas, adbutils_binaries, adbutils_hiddenimports = collect_all('adbutils')
wmi_datas, wmi_binaries, wmi_hiddenimports = collect_all('wmi')

a = Analysis(
    ['main.py'],
    pathex=[],
<<<<<<< HEAD
<<<<<<< HEAD
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
=======
    binaries=[],
=======
    binaries=ping3_binaries + adbutils_binaries + wmi_binaries,
>>>>>>> ec40b436f206ef5eacdc379d4263a2d7fb91ec70
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
<<<<<<< HEAD
    ],
>>>>>>> f0898754ec718c530178568b743dbb7281b5b8b8
=======
    ] + ping3_hiddenimports + adbutils_hiddenimports + wmi_hiddenimports,
>>>>>>> ec40b436f206ef5eacdc379d4263a2d7fb91ec70
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
<<<<<<< HEAD
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
=======
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
>>>>>>> f0898754ec718c530178568b743dbb7281b5b8b8

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
<<<<<<< HEAD
=======
    a.zipfiles,
>>>>>>> f0898754ec718c530178568b743dbb7281b5b8b8
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
<<<<<<< HEAD
<<<<<<< HEAD
    icon=['assets\\icons\\logo.ico'],
=======
    icon='assets\\icons\\logo.ico',
>>>>>>> f0898754ec718c530178568b743dbb7281b5b8b8
=======
    icon='assets/icons/logo.ico'
>>>>>>> ec40b436f206ef5eacdc379d4263a2d7fb91ec70
)
