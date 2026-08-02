from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QComboBox, QSizePolicy, QButtonGroup
)
from typing import Callable, Optional

class GfxPage(QWidget):
    """GFX Settings Page Component."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        # Connection Banner
        self.banner = QFrame()
        self.banner.setFrameShape(QFrame.StyledPanel)
        banner_layout = QHBoxLayout(self.banner)
        banner_layout.setContentsMargins(14, 10, 14, 10)
        self.banner_icon = QLabel("⚠️")
        self.banner_label = QLabel("GameLoop status: Disconnected. Click 'Connect to GameLoop' below.")
        self.banner_label.setStyleSheet("color: #FBBF24; font-weight: 600; font-size: 12px;")
        banner_layout.addWidget(self.banner_icon)
        banner_layout.addWidget(self.banner_label, 1)
        self.banner.setStyleSheet("""
            QFrame {
                background-color: rgba(245, 158, 11, 0.12);
                border: 1px solid rgba(245, 158, 11, 0.3);
                border-radius: 8px;
            }
        """)
        main_layout.addWidget(self.banner)

        # GFX Options Container
        options_card = QFrame()
        options_card.setProperty("class", "cardFrame")
        options_layout = QVBoxLayout(options_card)
        options_layout.setContentsMargins(16, 16, 16, 16)
        options_layout.setSpacing(16)

        # 1. Graphics Quality
        q_label = QLabel("GRAPHICS QUALITY")
        q_label.setProperty("class", "sectionHeader")
        options_layout.addWidget(q_label)

        q_layout = QHBoxLayout()
        q_layout.setSpacing(8)
        self.q_buttons = {}
        self.q_group = QButtonGroup(self)

        qualities = ["Super Smooth", "Smooth", "Balanced", "HD", "HDR", "Ultra HD"]
        for q in qualities:
            btn = QPushButton(q)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.q_group.addButton(btn)
            self.q_buttons[q] = btn
            q_layout.addWidget(btn)
        options_layout.addLayout(q_layout)

        # 2. Frame Rate
        fps_label = QLabel("FRAME RATE (FPS)")
        fps_label.setProperty("class", "sectionHeader")
        options_layout.addWidget(fps_label)

        fps_top_layout = QHBoxLayout()
        fps_top_layout.setSpacing(8)
        fps_bottom_layout = QHBoxLayout()
        fps_bottom_layout.setSpacing(8)

        self.fps_buttons = {}
        self.fps_group = QButtonGroup(self)

        fps_top = ["Low", "Medium", "High", "Ultra", "Extreme", "Extreme+"]
        for f in fps_top:
            btn = QPushButton(f)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.fps_group.addButton(btn)
            self.fps_buttons[f] = btn
            fps_top_layout.addWidget(btn)

        btn_120 = QPushButton("Ultra Extreme (120 FPS)")
        btn_120.setCheckable(True)
        btn_120.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.fps_group.addButton(btn_120)
        self.fps_buttons["Ultra Extreme"] = btn_120
        fps_bottom_layout.addWidget(btn_120)

        options_layout.addLayout(fps_top_layout)
        options_layout.addLayout(fps_bottom_layout)

        # 3. Graphics Style
        style_label = QLabel("COLOR STYLE")
        style_label.setProperty("class", "sectionHeader")
        options_layout.addWidget(style_label)

        style_layout = QHBoxLayout()
        style_layout.setSpacing(10)
        self.style_buttons = {}
        self.style_group = QButtonGroup(self)

        styles = ["Classic", "Colorful", "Realistic", "Soft", "Movie"]
        for s in styles:
            btn = QPushButton(s)
            btn.setProperty("role", "styleCard")
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.style_group.addButton(btn)
            self.style_buttons[s] = btn
            style_layout.addWidget(btn)
        options_layout.addLayout(style_layout)

        # 4. Shadow & KR Extra
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(14)

        # Shadow Group
        shadow_box = QVBoxLayout()
        s_label = QLabel("SHADOW PREFERENCE")
        s_label.setProperty("class", "sectionHeader")
        shadow_box.addWidget(s_label)
        s_btn_row = QHBoxLayout()

        self.btn_shadow_off = QPushButton("Disable Shadow")
        self.btn_shadow_off.setCheckable(True)
        self.btn_shadow_on = QPushButton("Enable Shadow")
        self.btn_shadow_on.setCheckable(True)

        self.shadow_group = QButtonGroup(self)
        self.shadow_group.addButton(self.btn_shadow_off)
        self.shadow_group.addButton(self.btn_shadow_on)

        s_btn_row.addWidget(self.btn_shadow_off)
        s_btn_row.addWidget(self.btn_shadow_on)
        shadow_box.addLayout(s_btn_row)

        # KR Resolution Group
        self.kr_box = QVBoxLayout()
        kr_label = QLabel("PUBG KR RESOLUTION")
        kr_label.setProperty("class", "sectionHeader")
        self.kr_box.addWidget(kr_label)
        self.btn_kr_1080p = QPushButton("1080p Resolution Fix")
        self.btn_kr_1080p.setCheckable(True)
        self.kr_box.addWidget(self.btn_kr_1080p)

        self.kr_widget = QWidget()
        self.kr_widget.setLayout(self.kr_box)
        self.kr_widget.hide()

        bottom_row.addLayout(shadow_box, 3)
        bottom_row.addWidget(self.kr_widget, 2)
        options_layout.addLayout(bottom_row)

        main_layout.addWidget(options_card, 1)

        # Footer Action Bar
        footer = QHBoxLayout()
        footer.setSpacing(12)

        # Version selection dropdown (visible when multiple versions detected)
        self.version_chooser_card = QFrame()
        vc_layout = QHBoxLayout(self.version_chooser_card)
        vc_layout.setContentsMargins(8, 4, 8, 4)
        vc_layout.setSpacing(8)
        vc_label = QLabel("Game Version:")
        vc_label.setStyleSheet("font-size: 11px; color: #9CA3AF;")
        self.version_combo = QComboBox()
        self.btn_use_version = QPushButton("Select")
        self.btn_use_version.setStyleSheet("min-height: 30px; padding: 4px 10px;")
        vc_layout.addWidget(vc_label)
        vc_layout.addWidget(self.version_combo, 1)
        vc_layout.addWidget(self.btn_use_version)
        self.version_chooser_card.hide()

        footer.addWidget(self.version_chooser_card, 1)
        footer.addStretch(1)

        self.btn_connect = QPushButton("Connect to GameLoop")
        self.btn_connect.setProperty("class", "accent")
        self.btn_connect.setMinimumWidth(180)

        self.btn_apply = QPushButton("Apply Graphics Settings")
        self.btn_apply.setProperty("class", "primary")
        self.btn_apply.setMinimumWidth(200)
        self.btn_apply.setEnabled(False)

        footer.addWidget(self.btn_connect)
        footer.addWidget(self.btn_apply)

        main_layout.addLayout(footer)

        # Set default selections
        self.q_buttons["Smooth"].setChecked(True)
        self.fps_buttons["Extreme+"].setChecked(True)
        self.style_buttons["Colorful"].setChecked(True)
        self.btn_shadow_off.setChecked(True)

    def set_controls_enabled(self, enabled: bool):
        for btn in self.q_buttons.values():
            btn.setEnabled(enabled)
        for btn in self.fps_buttons.values():
            btn.setEnabled(enabled)
        for btn in self.style_buttons.values():
            btn.setEnabled(enabled)
        self.btn_shadow_off.setEnabled(enabled)
        self.btn_shadow_on.setEnabled(enabled)
        self.btn_kr_1080p.setEnabled(enabled)
        self.btn_apply.setEnabled(enabled)

    def update_connection_status(self, connected: bool, device_info: str = ""):
        if connected:
            self.banner.setStyleSheet("""
                QFrame {
                    background-color: rgba(16, 185, 129, 0.12);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 8px;
                }
            """)
            self.banner_icon.setText("✅")
            self.banner_label.setText(f"GameLoop Connected! {device_info}")
            self.banner_label.setStyleSheet("color: #10B981; font-weight: 600; font-size: 12px;")
            self.btn_connect.setText("Disconnect GameLoop")
            self.set_controls_enabled(True)
        else:
            self.banner.setStyleSheet("""
                QFrame {
                    background-color: rgba(245, 158, 11, 0.12);
                    border: 1px solid rgba(245, 158, 11, 0.3);
                    border-radius: 8px;
                }
            """)
            self.banner_icon.setText("⚠️")
            self.banner_label.setText("GameLoop status: Disconnected. Click 'Connect to GameLoop' below.")
            self.banner_label.setStyleSheet("color: #FBBF24; font-weight: 600; font-size: 12px;")
            self.btn_connect.setText("Connect to GameLoop")
            self.set_controls_enabled(False)
