"""
MK PUBG Mobile Tool - God Mode Graphics Applier
Quick script to apply maximum graphics settings

Usage: python apply_god_mode.py [preset]
Presets: god, competitive, balanced (default: god)
"""

import sys
from time import sleep
from src.app_functions import Game

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        🎮 MK PUBG MOBILE TOOL - GOD MODE 🎮             ║
    ║                                                          ║
    ║              EXTREME HDR • UNLOCKED                      ║
    ║              ULTRA HDR+ • CUSTOM                         ║
    ║              GOD MODE • MAXIMUM                          ║
    ║                                                          ║
    ║     Anti-Aliasing: 16x | Shadows: Extreme               ║
    ║     Textures: 4K | View Distance: Extreme               ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_status(message, status="info"):
    symbols = {
        "info": "ℹ️",
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "loading": "⏳"
    }
    print(f"{symbols.get(status, 'ℹ️')} {message}")

def apply_graphics(preset_name="god"):
    """Apply graphics preset to PUBG Mobile"""
    
    # Map preset names
    preset_map = {
        "god": "God Mode",
        "competitive": "Competitive",
        "balanced": "Balanced"
    }
    
    preset = preset_map.get(preset_name.lower(), "God Mode")
    
    print_banner()
    print_status(f"Selected Preset: {preset}", "info")
    print()
    
    try:
        # Step 1: Initialize
        print_status("Initializing MK PUBG Tool...", "loading")
        game = Game()
        print_status("Tool initialized", "success")
        print()
        
        # Step 2: Connect to Gameloop
        print_status("Connecting to Gameloop emulator...", "loading")
        game.check_adb_connection()
        
        if not game.is_adb_working:
            print_status("Gameloop not running or ADB failed!", "error")
            print_status("Please start Gameloop and try again", "warning")
            return False
        
        print_status("Connected to Gameloop successfully", "success")
        print()
        
        # Step 3: Detect PUBG version
        print_status("Scanning for PUBG Mobile versions...", "loading")
        game.pubg_version_found()
        
        if not game.PUBG_Found:
            print_status("No PUBG Mobile version found!", "error")
            print_status("Please install PUBG Mobile in Gameloop", "warning")
            return False
        
        print_status(f"Found: {', '.join(game.PUBG_Found)}", "success")
        print()
        
        # Step 4: Choose package (use first found)
        package_map = {v: k for k, v in game.pubg_versions.items()}
        selected_version = game.PUBG_Found[0]
        selected_package = package_map[selected_version]
        
        print_status(f"Selected: {selected_version}", "info")
        print_status(f"Package: {selected_package}", "info")
        print()
        
        # Step 5: Load graphics config
        print_status("Loading current graphics configuration...", "loading")
        game.get_graphics_file(selected_package)
        print_status("Graphics config loaded", "success")
        
        # Display current settings
        current_graphics = game.get_graphics_setting()
        current_fps = game.get_fps()
        current_style = game.get_graphics_style()
        
        print()
        print("📊 CURRENT SETTINGS:")
        print(f"   Graphics: {current_graphics or 'Unknown'}")
        print(f"   FPS: {current_fps or 'Unknown'}")
        print(f"   Style: {current_style or 'Unknown'}")
        print()
        
        # Step 6: Apply new settings based on preset
        print_status(f"Applying {preset} settings...", "loading")
        
        if preset == "God Mode":
            game.set_graphics_quality("God Mode")
            game.set_fps("Unlimited")
            game.set_graphics_style("Colorful")
            game.apply_advanced_graphics("God Mode")
            
            print()
            print("🔥 GOD MODE SETTINGS:")
            print("   Graphics Tier: God Mode (0x08)")
            print("   FPS: Unlimited (Uncapped)")
            print("   Anti-Aliasing: 16x MSAA")
            print("   Shadows: Extreme Quality")
            print("   Textures: Max (4K)")
            print("   View Distance: Extreme")
            print("   Post-Processing: Extreme")
            print("   Bloom: Ultra")
            print("   Light Shafts: High")
            print("   SSAO: High")
            print("   Anisotropic: 16x")
            print("   Style: Colorful")
            
        elif preset == "Competitive":
            game.set_graphics_quality("Ultra HD")
            game.set_fps("Ultra Extreme")
            game.set_graphics_style("Colorful")
            game.apply_advanced_graphics("Competitive")
            
            print()
            print("⚡ COMPETITIVE SETTINGS:")
            print("   Graphics Tier: Ultra HD")
            print("   FPS: Ultra Extreme (High)")
            print("   Anti-Aliasing: 4x MSAA")
            print("   Shadows: Medium")
            print("   Textures: High")
            print("   View Distance: Ultra")
            print("   Effects: Minimal (Performance)")
            print("   Style: Colorful")
            
        elif preset == "Balanced":
            game.set_graphics_quality("Ultra HD")
            game.set_fps("Extreme")
            game.set_graphics_style("Colorful")
            game.apply_advanced_graphics("Balanced")
            
            print()
            print("⚖️ BALANCED SETTINGS:")
            print("   Graphics Tier: Ultra HD")
            print("   FPS: Extreme")
            print("   Anti-Aliasing: 4x MSAA")
            print("   Shadows: High")
            print("   Textures: High")
            print("   All Settings: High/Ultra")
            print("   Style: Colorful")
        
        print()
        print_status("Settings configured successfully", "success")
        print()
        
        # Step 7: Save changes
        print_status("Saving graphics configuration...", "loading")
        game.save_graphics_file()
        print_status("Configuration saved", "success")
        print()
        
        # Step 8: Push to device
        print_status("Pushing files to device...", "loading")
        print_status("Stopping PUBG Mobile...", "info")
        game.push_active_shadow_file()
        print_status("Files pushed successfully", "success")
        print()
        
        # Step 9: Launch game
        print_status("Launching PUBG Mobile...", "loading")
        sleep(2)
        game.start_app()
        print_status("PUBG Mobile launched!", "success")
        print()
        
        # Success message
        print("═" * 60)
        print()
        print(f"    🎉 {preset.upper()} GRAPHICS ACTIVATED! 🎉")
        print()
        print("    Your game is now running with enhanced graphics!")
        print("    Enjoy the PC-level visual experience!")
        print()
        print("═" * 60)
        print()
        
        # Performance expectations
        print("📈 EXPECTED PERFORMANCE (RX 580):")
        if preset == "God Mode":
            print("   FPS: 45-60 (Maximum Quality)")
            print("   GPU Usage: 90-100%")
            print("   Recommended for: Screenshots, Recording")
        elif preset == "Competitive":
            print("   FPS: 80-120 (High Performance)")
            print("   GPU Usage: 60-80%")
            print("   Recommended for: Competitive Gaming")
        elif preset == "Balanced":
            print("   FPS: 60-90 (Balanced)")
            print("   GPU Usage: 70-85%")
            print("   Recommended for: Daily Gaming")
        print()
        
        print_status("Monitor your GPU temperature!", "warning")
        print_status("If you experience lag, use 'balanced' preset", "info")
        print()
        
        return True
        
    except Exception as e:
        print()
        print_status(f"Error occurred: {str(e)}", "error")
        print_status("Check error.log for details", "info")
        return False

def show_help():
    help_text = """
    MK PUBG Mobile Tool - God Mode Graphics
    
    Usage:
        python apply_god_mode.py [preset]
    
    Available Presets:
        god          - God Mode (Maximum graphics, 16x AA, Extreme everything)
        competitive  - Competitive (High FPS, optimized for performance)
        balanced     - Balanced (Best of both worlds)
    
    Examples:
        python apply_god_mode.py god
        python apply_god_mode.py competitive
        python apply_god_mode.py balanced
        python apply_god_mode.py    # defaults to 'god'
    
    Requirements:
        - Gameloop emulator running
        - PUBG Mobile installed
        - ADB enabled
    
    Hardware Requirements:
        God Mode:
            - GPU: RX 580 / GTX 1060 or better
            - RAM: 16GB+
            - CPU: Ryzen 5 / i5 or better
        
        Competitive:
            - GPU: RX 570 / GTX 1050 Ti or better
            - RAM: 8GB+
        
        Balanced:
            - GPU: RX 560 / GTX 1050 or better
            - RAM: 8GB+
    
    Warning:
        ⚠️  These modifications may be detected by anti-cheat
        ⚠️  Use at your own risk
        ⚠️  Recommended for secondary accounts
    """
    print(help_text)

if __name__ == "__main__":
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        sys.exit(0)
    
    # Get preset from command line or default to 'god'
    preset = sys.argv[1] if len(sys.argv) > 1 else 'god'
    
    # Validate preset
    valid_presets = ['god', 'competitive', 'balanced']
    if preset.lower() not in valid_presets:
        print(f"❌ Invalid preset: {preset}")
        print(f"Valid presets: {', '.join(valid_presets)}")
        print("\nRun 'python apply_god_mode.py --help' for more info")
        sys.exit(1)
    
    # Apply graphics
    success = apply_graphics(preset)
    
    if success:
        print("✅ Done! Enjoy your enhanced graphics!")
        sys.exit(0)
    else:
        print("❌ Failed to apply graphics. Check the errors above.")
        sys.exit(1)