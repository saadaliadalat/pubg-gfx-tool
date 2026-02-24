# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Collect all dependencies for problematic modules
ping3_datas, ping3_binaries, ping3_hiddenimports = collect_all('ping3')
adbutils_datas, adbutils_binaries, adbutils_hiddenimports = collect_all('adbutils')
wmi_datas, wmi_binaries, wmi_hiddenimports = collect_all('wmi')

# Build datas list separately
datas = []
datas.extend(ping3_datas)
datas.extend(adbutils_datas)
datas.extend(wmi_datas)
datas.append(('assets', 'assets'))

# Build binaries list separately
binaries = []
binaries.extend(ping3_binaries)
binaries.extend(adbutils_binaries)
binaries.extend(wmi_binaries)

# Build hiddenimports list separately
hiddenimports = []
hiddenimports.extend(ping3_hiddenimports)
hiddenimports.extend(adbutils_hiddenimports)
hiddenimports.extend(wmi_hiddenimports)
hiddenimports.extend([
    'win32com',
    'win32com.client',
    'win32com.client.gencache',
    'win32com.gen_py',
    'win32com.shell',
    'win32com.shell.shell',
    'pythoncom',
    'pywintypes',
    'win32timezone',
    'win32api',
    'win32con',
    'winreg',
    'GPUtil',
    'psutil',
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'winshell',
    'xmltodict',
    'adbutils._deprecated',
    'adbutils._utils',
    'adbutils._proto',
])

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EX-Tool',
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
    icon='assets/icons/logo.ico',
)
