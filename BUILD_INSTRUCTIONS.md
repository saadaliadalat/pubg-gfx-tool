# Build Instructions for MK PUBG Mobile Tool

## Changes Made

### Graphics Settings Fix
The tool has been updated to support the new **Super Smooth** graphics setting introduced by PUBG Mobile. The graphics mapping is now:

- **Super Smooth** (new)
- **Smooth** (previously mapped to Super Smooth)
- **Balanced** (previously mapped to Smooth)
- **HD** (previously mapped to Balanced)
- **HDR** (previously mapped to HD)
- **Ultra HD** (previously mapped to HDR)

## Building the Executable

### Prerequisites
1. **Windows PC** (required - this tool is Windows-only)
2. **Python 3.7+** installed
3. **Git** (optional, for cloning)

### Method 1: Quick Build (Recommended)

1. Open Command Prompt or PowerShell as Administrator
2. Navigate to the project directory:
   ```cmd
   cd path\to\pubg-gfx-tool
   ```

3. Run the build script:
   ```cmd
   build.bat
   ```

4. The executable will be created in the `dist` folder:
   - Location: `dist\MK-PUBG-Mobile-Tool.exe`

### Method 2: Manual Build

1. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

2. Run PyInstaller:
   ```cmd
   pyinstaller --noconfirm --onefile --windowed ^
     --icon=assets/icons/logo.ico ^
     --name=MK-PUBG-Mobile-Tool ^
     --add-data="assets;assets" ^
     --add-data="images;images" ^
     --hidden-import=adbutils ^
     --hidden-import=GPUtil ^
     --hidden-import=ping3 ^
     --hidden-import=psutil ^
     --hidden-import=pywintypes ^
     --hidden-import=win32com.client ^
     --hidden-import=win32api ^
     --hidden-import=winshell ^
     --hidden-import=wmi ^
     --hidden-import=xmltodict ^
     --hidden-import=PyQt5 ^
     --collect-all=adbutils ^
     --collect-all=PyQt5 ^
     main.py
   ```

3. Find the executable in `dist\MK-PUBG-Mobile-Tool.exe`

### Method 3: Using Python Script

1. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```cmd
   python build_exe.py
   ```

## Testing the Executable

1. Make sure Gameloop emulator is installed on your PC
2. Run `MK-PUBG-Mobile-Tool.exe`
3. Test the new graphics settings:
   - Click "Connect to Gameloop"
   - Select your PUBG version
   - Choose "Super Smooth" or any other graphics option
   - Click "Apply" and verify the settings in-game

## Troubleshooting

### Build Errors

**"PyInstaller not found"**
```cmd
pip install pyinstaller
```

**"Module not found" errors**
```cmd
pip install -r requirements.txt --upgrade
```

**Missing DLL errors**
- Install Microsoft Visual C++ Redistributable
- Install all Windows updates

### Runtime Errors

**"GameLoop not found"**
- Install Gameloop emulator
- Make sure it's running before connecting

**"ADB connection failed"**
- Restart Gameloop
- Enable ADB in Gameloop settings

## File Structure

```
pubg-gfx-tool/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── build.bat              # Windows build script
├── build_exe.py           # Python build script
├── BUILD_INSTRUCTIONS.md  # This file
├── src/
│   ├── app_functions.py   # Core functionality (UPDATED)
│   ├── gfx.py            # Graphics UI logic (UPDATED)
│   ├── ui.py             # UI definitions (UPDATED)
│   └── ...
├── assets/               # Icons and resources
└── images/              # Screenshots
```

## What Was Changed

1. **src/app_functions.py**
   - Added `b'\x00': "Super Smooth"` to graphics mapping
   - Updated `set_graphics_quality()` to support Super Smooth

2. **src/ui.py**
   - Enabled the 6th graphics button (`uhd_graphics_btn`)
   - Updated all button labels to reflect new mapping

3. **src/gfx.py**
   - Added `uhd_graphics_btn` to all button lists
   - Connected new button to event handlers

4. **requirements.txt**
   - Fixed encoding issues
   - Added PyInstaller

## Version

Current version: **v1.0.8** (with Super Smooth support)

## Notes

- The executable will be around 50-100 MB in size
- First run may be slow while Windows Defender scans it
- Consider adding Gameloop to Windows Defender exclusions for better performance
