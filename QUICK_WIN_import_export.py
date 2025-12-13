# QUICK WIN #2: Settings Import/Export
# Add to src/app_functions.py

import json
import base64
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog

class SettingsManager:
    """Import/Export settings to share with friends"""

    def export_settings(self):
        """Export current settings to JSON file"""
        settings_data = {
            "version": "1.0.8",
            "timestamp": datetime.now().isoformat(),
            "graphics": self.get_graphics_setting(),
            "fps": self.get_fps(),
            "style": self.get_graphics_style(),
            "shadow": self.get_shadow(),
            # Add more settings as needed
        }

        # Save to file
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Export Settings",
            f"PUBG_Settings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)"
        )

        if file_path:
            with open(file_path, 'w') as f:
                json.dump(settings_data, f, indent=4)
            return True, file_path
        return False, None

    def import_settings(self):
        """Import settings from JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Import Settings",
            "",
            "JSON Files (*.json)"
        )

        if file_path:
            try:
                with open(file_path, 'r') as f:
                    settings_data = json.load(f)

                # Validate version compatibility
                if settings_data.get("version") != "1.0.8":
                    return False, "Incompatible settings version"

                # Apply settings
                if "graphics" in settings_data:
                    self.set_graphics_quality(settings_data["graphics"])
                if "fps" in settings_data:
                    self.set_fps(settings_data["fps"])
                if "style" in settings_data:
                    self.set_graphics_style(settings_data["style"])

                return True, "Settings imported successfully"
            except Exception as e:
                return False, f"Import failed: {str(e)}"

        return False, "No file selected"

    def generate_share_code(self):
        """Generate a short code to share settings (like a URL shortener)"""
        settings_data = {
            "g": self.get_graphics_setting()[:2],  # First 2 letters
            "f": self.get_fps()[:2],
            "s": self.get_graphics_style()[:2],
        }

        # Encode to base64 for short code
        json_str = json.dumps(settings_data)
        code = base64.b64encode(json_str.encode()).decode()[:12]  # First 12 chars

        return code

    def apply_share_code(self, code):
        """Apply settings from share code"""
        try:
            # Decode (this is simplified - you'd need a mapping)
            # Full implementation would decode base64 and apply settings
            pass
        except:
            return False, "Invalid share code"


# Add to UI - Export/Import buttons
"""
In src/ui.py, add buttons:

self.export_btn = QPushButton("📤 Export", self.gfx_page)
self.export_btn.setGeometry(QRect(850, 580, 100, 51))

self.import_btn = QPushButton("📥 Import", self.gfx_page)
self.import_btn.setGeometry(QRect(740, 580, 100, 51))

self.share_code_btn = QPushButton("🔗 Share Code", self.gfx_page)
self.share_code_btn.setGeometry(QRect(630, 580, 100, 51))
"""

# Connect in gfx.py
"""
self.ui.export_btn.clicked.connect(self.export_settings)
self.ui.import_btn.clicked.connect(self.import_settings)
self.ui.share_code_btn.clicked.connect(self.show_share_code)

def export_settings(self):
    success, path = self.app.export_settings()
    if success:
        self.app.show_status_message(f"✅ Settings exported to {path}")
    else:
        self.app.show_status_message("❌ Export failed")

def import_settings(self):
    success, message = self.app.import_settings()
    if success:
        self.app.show_status_message(f"✅ {message}")
        # Refresh UI to show imported settings
        self.connect_gameloop_task_completed()
    else:
        self.app.show_status_message(f"❌ {message}")

def show_share_code(self):
    code = self.app.generate_share_code()
    # Show dialog with code
    from PyQt5.QtWidgets import QMessageBox, QApplication
    dialog = QMessageBox()
    dialog.setWindowTitle("Share Settings")
    dialog.setText(f"Share this code with friends:\\n\\n{code}")
    dialog.setStandardButtons(QMessageBox.Ok)

    # Add copy to clipboard button
    copy_btn = dialog.addButton("📋 Copy Code", QMessageBox.ActionRole)
    copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(code))

    dialog.exec_()
"""

# BONUS: Save profiles to database
"""
import sqlite3

class ProfileManager:
    def __init__(self):
        self.db_path = "profiles.db"
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                graphics TEXT,
                fps TEXT,
                style TEXT,
                shadow TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def save_profile(self, name, settings):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO profiles (name, graphics, fps, style, shadow)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, settings['graphics'], settings['fps'], settings['style'], settings.get('shadow')))
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            conn.close()

    def load_profile(self, name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM profiles WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'graphics': row[2],
                'fps': row[3],
                'style': row[4],
                'shadow': row[5]
            }
        return None

    def get_all_profiles(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM profiles ORDER BY created_at DESC')
        profiles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return profiles
"""
