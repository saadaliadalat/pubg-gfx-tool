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

### Method 1: Simple Build (Recommended - Uses Spec File)

1. Open Command Prompt or PowerShell as Administrator
2. Navigate to the project directory:
   ```cmd
   cd path\to\pubg-gfx-tool
   ```

3. Run the simple build script:
   ```cmd
   build_simple.bat
   ```

4. The executable will be created in the `dist` folder:
   - Location: `dist\MK-PUBG-Mobile-Tool.exe`

**This method is most reliable!** It uses a PyInstaller spec file that properly includes all dependencies.

### Method 2: Quick Build (Alternative)

1. Navigate to project directory
2. Run:
   ```cmd
   build.bat
   ```

3. Check `dist\MK-PUBG-Mobile-Tool.exe`

### Method 3: Using Spec File (Manual)

1. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

2. Run PyInstaller with spec file:
   ```cmd
   pyinstaller MK-PUBG-Mobile-Tool.spec
   ```

3. Find the executable in `dist\MK-PUBG-Mobile-Tool.exe`

### Method 4: Using Python Script

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

### Runtime Errors (When Running EXE)

**"ModuleNotFoundError: No module named 'ping3'"** or similar
- This means PyInstaller didn't package the module correctly
- **Solution:** Use `build_simple.bat` which uses the spec file
- Or delete `build` and `dist` folders and rebuild:
  ```cmd
  rmdir /s /q build dist
  build_simple.bat
  ```

**"Failed to execute script"**
- Run from Command Prompt to see the actual error:
  ```cmd
  cd dist
  MK-PUBG-Mobile-Tool.exe
  ```
- Check `error.log` file for details

**"GameLoop not found"**
- Install Gameloop emulator
- Make sure it's running before connecting

**"ADB connection failed"**
- Restart Gameloop
- Enable ADB in Gameloop settings

## File Structure

```
pubg-gfx-tool/
├── main.py                        # Main entry point
├── requirements.txt               # Python dependencies
├── build.bat                      # Windows build script (CLI method)
├── build_simple.bat              # Simple build script (RECOMMENDED)
├── build_exe.py                  # Python build script
├── MK-PUBG-Mobile-Tool.spec      # PyInstaller spec file
├── BUILD_INSTRUCTIONS.md         # This file
├── src/
│   ├── app_functions.py          # Core functionality (UPDATED)
│   ├── gfx.py                    # Graphics UI logic (UPDATED)
│   ├── ui.py                     # UI definitions (UPDATED)
│   └── ...
├── assets/                        # Icons and resources
└── images/                        # Screenshots
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
