# QUICK WIN #1: One-Click Preset Buttons
# Add to src/gfx.py

class QuickPresets:
    """One-click preset configurations for different use cases"""

    def __init__(self, app):
        self.app = app

    def apply_competitive_preset(self):
        """Optimized for competitive/ranked play"""
        self.app.set_graphics_quality("Smooth")  # Low graphics for max performance
        self.app.set_fps("Extreme+")  # 90 FPS
        self.app.set_graphics_style("Classic")  # Standard look
        # Clear visuals, high FPS
        self.app.show_status_message("✅ Competitive preset applied (Smooth + 90 FPS)")

    def apply_streaming_preset(self):
        """Best quality for streaming/recording"""
        self.app.set_graphics_quality("HDR")  # High quality graphics
        self.app.set_fps("High")  # 60 FPS (stable for streaming)
        self.app.set_graphics_style("Colorful")  # Vibrant for viewers
        self.app.show_status_message("✅ Streaming preset applied (HDR + 60 FPS)")

    def apply_battery_saver_preset(self):
        """Maximum battery life on mobile"""
        self.app.set_graphics_quality("Super Smooth")  # Lowest graphics
        self.app.set_fps("Low")  # 30 FPS
        self.app.set_graphics_style("Classic")
        self.app.show_status_message("✅ Battery Saver preset applied (Super Smooth + 30 FPS)")

    def apply_max_fps_preset(self):
        """Maximum FPS possible"""
        self.app.set_graphics_quality("Smooth")  # Low graphics
        self.app.set_fps("Ultra Extreme")  # 120 FPS
        self.app.set_graphics_style("Classic")
        # Disable shadows, effects for max performance
        self.app.show_status_message("✅ Max FPS preset applied (Smooth + 120 FPS)")

    def apply_balanced_preset(self):
        """Balanced graphics and performance"""
        self.app.set_graphics_quality("Balanced")
        self.app.set_fps("Ultra")  # 60 FPS
        self.app.set_graphics_style("Realistic")
        self.app.show_status_message("✅ Balanced preset applied (Balanced + 60 FPS)")

    def apply_pro_player_preset(self, player_name="default"):
        """Apply verified pro player settings"""
        pro_settings = {
            "default": {
                "graphics": "Smooth",
                "fps": "Extreme+",
                "style": "Classic"
            },
            "mortal": {  # Example: Mortal's settings
                "graphics": "Smooth",
                "fps": "Extreme",
                "style": "Colorful"
            },
            "scout": {  # Example: Scout's settings
                "graphics": "Balanced",
                "fps": "Extreme+",
                "style": "Classic"
            }
        }

        settings = pro_settings.get(player_name.lower(), pro_settings["default"])
        self.app.set_graphics_quality(settings["graphics"])
        self.app.set_fps(settings["fps"])
        self.app.set_graphics_style(settings["style"])
        self.app.show_status_message(f"✅ {player_name.title()}'s preset applied")


# Add to UI (src/ui.py)
"""
Add preset buttons to the GFX page:

self.preset_frame = QFrame(self.gfx_page)
self.preset_frame.setGeometry(QRect(20, 10, 1041, 51))

# Preset buttons
self.competitive_preset_btn = QPushButton("🎯 Competitive", self.preset_frame)
self.competitive_preset_btn.setGeometry(QRect(0, 0, 130, 40))

self.streaming_preset_btn = QPushButton("🎥 Streaming", self.preset_frame)
self.streaming_preset_btn.setGeometry(QRect(135, 0, 130, 40))

self.battery_preset_btn = QPushButton("🔋 Battery Saver", self.preset_frame)
self.battery_preset_btn.setGeometry(QRect(270, 0, 130, 40))

self.maxfps_preset_btn = QPushButton("⚡ Max FPS", self.preset_frame)
self.maxfps_preset_btn.setGeometry(QRect(405, 0, 130, 40))

self.balanced_preset_btn = QPushButton("⚖️ Balanced", self.preset_frame)
self.balanced_preset_btn.setGeometry(QRect(540, 0, 130, 40))
"""

# Connect in gfx.py
"""
self.presets = QuickPresets(self.app)

self.ui.competitive_preset_btn.clicked.connect(lambda: self.apply_preset('competitive'))
self.ui.streaming_preset_btn.clicked.connect(lambda: self.apply_preset('streaming'))
self.ui.battery_preset_btn.clicked.connect(lambda: self.apply_preset('battery'))
self.ui.maxfps_preset_btn.clicked.connect(lambda: self.apply_preset('maxfps'))
self.ui.balanced_preset_btn.clicked.connect(lambda: self.apply_preset('balanced'))

def apply_preset(self, preset_type):
    if preset_type == 'competitive':
        self.presets.apply_competitive_preset()
    elif preset_type == 'streaming':
        self.presets.apply_streaming_preset()
    elif preset_type == 'battery':
        self.presets.apply_battery_saver_preset()
    elif preset_type == 'maxfps':
        self.presets.apply_max_fps_preset()
    elif preset_type == 'balanced':
        self.presets.apply_balanced_preset()

    # Auto-submit after preset
    self.gfx_submit_button_click()
"""
