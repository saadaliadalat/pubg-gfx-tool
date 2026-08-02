from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QSizePolicy, QButtonGroup
)

def _make_card(parent=None) -> QFrame:
    f = QFrame(parent)
    f.setObjectName("sectionCard")
    return f

def _make_section_title(text: str, parent=None) -> QLabel:
    lbl = QLabel(text, parent)
    lbl.setObjectName("sectionTitle")
    return lbl


class GfxPage(QWidget):
    """GFX Settings Page — modern card layout."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(12)

        # ── CONNECTION BANNER ──────────────────────────────────
        self.banner = QFrame()
        self.banner.setObjectName("bannerDisconnected")
        banner_row = QHBoxLayout(self.banner)
        banner_row.setContentsMargins(14, 10, 14, 10)
        banner_row.setSpacing(10)
        self.banner_icon_lbl = QLabel("⚠")
        self.banner_icon_lbl.setStyleSheet("font-size: 16px; color: #F59E0B;")
        self.banner_text_lbl = QLabel("Not connected — click Connect to GameLoop below")
        self.banner_text_lbl.setStyleSheet("color: #FCD34D; font-size: 12px; font-weight: 600;")
        banner_row.addWidget(self.banner_icon_lbl)
        banner_row.addWidget(self.banner_text_lbl, 1)
        root.addWidget(self.banner)

        # ── MAIN SETTINGS CARD ────────────────────────────────
        card = _make_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(16)

        # 1. Graphics Quality
        card_layout.addWidget(_make_section_title("GRAPHICS QUALITY"))
        q_row = QHBoxLayout()
        q_row.setSpacing(8)
        self.q_group = QButtonGroup(self)
        self.q_buttons = {}
        for label in ["Super Smooth", "Smooth", "Balanced", "HD", "HDR", "Ultra HD"]:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.q_group.addButton(btn)
            self.q_buttons[label] = btn
            q_row.addWidget(btn)
        card_layout.addLayout(q_row)

        # 2. Frame Rate
        card_layout.addWidget(_make_section_title("FRAME RATE"))
        fps_top = QHBoxLayout()
        fps_top.setSpacing(8)
        fps_bot = QHBoxLayout()
        fps_bot.setSpacing(8)
        self.fps_group = QButtonGroup(self)
        self.fps_buttons = {}
        for label in ["Low", "Medium", "High", "Ultra", "Extreme", "Extreme+"]:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.fps_group.addButton(btn)
            self.fps_buttons[label] = btn
            fps_top.addWidget(btn)
        btn_120 = QPushButton("Ultra Extreme  (120 FPS)")
        btn_120.setCheckable(True)
        btn_120.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.fps_group.addButton(btn_120)
        self.fps_buttons["Ultra Extreme"] = btn_120
        fps_bot.addWidget(btn_120)
        card_layout.addLayout(fps_top)
        card_layout.addLayout(fps_bot)

        # 3. Color Style
        card_layout.addWidget(_make_section_title("COLOR STYLE"))
        style_row = QHBoxLayout()
        style_row.setSpacing(10)
        self.style_group = QButtonGroup(self)
        self.style_buttons = {}
        style_emojis = {"Classic": "🏔", "Colorful": "🌈", "Realistic": "🌿", "Soft": "✨", "Movie": "🎬"}
        for label, emoji in style_emojis.items():
            btn = QPushButton(f"{emoji}\n{label}")
            btn.setProperty("btnStyle", "styleCard")
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(60)
            self.style_group.addButton(btn)
            self.style_buttons[label] = btn
            style_row.addWidget(btn)
        card_layout.addLayout(style_row)

        # 4. Shadow + KR row
        shadow_kr_row = QHBoxLayout()
        shadow_kr_row.setSpacing(12)

        # Shadow card
        shadow_card = _make_card()
        shadow_layout = QVBoxLayout(shadow_card)
        shadow_layout.setContentsMargins(14, 12, 14, 12)
        shadow_layout.setSpacing(8)
        shadow_layout.addWidget(_make_section_title("SHADOW"))
        s_btn_row = QHBoxLayout()
        s_btn_row.setSpacing(8)
        self.btn_shadow_off = QPushButton("Disable Shadow")
        self.btn_shadow_off.setCheckable(True)
        self.btn_shadow_on = QPushButton("Enable Shadow")
        self.btn_shadow_on.setCheckable(True)
        self.shadow_group = QButtonGroup(self)
        self.shadow_group.addButton(self.btn_shadow_off)
        self.shadow_group.addButton(self.btn_shadow_on)
        s_btn_row.addWidget(self.btn_shadow_off)
        s_btn_row.addWidget(self.btn_shadow_on)
        shadow_layout.addLayout(s_btn_row)

        # KR resolution card (hidden by default)
        self.kr_card = _make_card()
        kr_layout = QVBoxLayout(self.kr_card)
        kr_layout.setContentsMargins(14, 12, 14, 12)
        kr_layout.setSpacing(8)
        kr_layout.addWidget(_make_section_title("PUBG KR RESOLUTION"))
        self.btn_kr_1080p = QPushButton("Enable 1080p Fix")
        self.btn_kr_1080p.setCheckable(True)
        kr_layout.addWidget(self.btn_kr_1080p)
        self.kr_card.hide()

        shadow_kr_row.addWidget(shadow_card, 3)
        shadow_kr_row.addWidget(self.kr_card, 2)
        card_layout.addLayout(shadow_kr_row)

        root.addWidget(card, 1)

        # ── FOOTER ────────────────────────────────────────────
        footer = QHBoxLayout()
        footer.setSpacing(10)

        # Version chooser (hidden until multiple versions found)
        self.version_chooser_card = _make_card()
        vc_layout = QHBoxLayout(self.version_chooser_card)
        vc_layout.setContentsMargins(10, 6, 10, 6)
        vc_layout.setSpacing(8)
        vc_label = QLabel("Version:")
        vc_label.setStyleSheet("color: #9CA3AF; font-size: 11px;")
        self.version_combo = QComboBox()
        self.btn_use_version = QPushButton("Select")
        self.btn_use_version.setFixedWidth(70)
        vc_layout.addWidget(vc_label)
        vc_layout.addWidget(self.version_combo, 1)
        vc_layout.addWidget(self.btn_use_version)
        self.version_chooser_card.hide()

        self.btn_connect = QPushButton("🔗  Connect to GameLoop")
        self.btn_connect.setProperty("btnStyle", "success")
        self.btn_connect.setMinimumWidth(190)

        self.btn_apply = QPushButton("✅  Apply Graphics Settings")
        self.btn_apply.setProperty("btnStyle", "primary")
        self.btn_apply.setMinimumWidth(210)
        self.btn_apply.setEnabled(False)

        footer.addWidget(self.version_chooser_card, 1)
        footer.addStretch(1)
        footer.addWidget(self.btn_connect)
        footer.addWidget(self.btn_apply)

        root.addLayout(footer)

        # Default selections
        self.q_buttons["Smooth"].setChecked(True)
        self.fps_buttons["Extreme+"].setChecked(True)
        self.style_buttons["Colorful"].setChecked(True)
        self.btn_shadow_off.setChecked(True)

        # Start with controls disabled
        self.set_controls_enabled(False)

    def set_controls_enabled(self, enabled: bool):
        for btn in self.q_buttons.values():
            btn.setEnabled(enabled)
        for btn in self.fps_buttons.values():
            btn.setEnabled(enabled)
        for btn in self.style_buttons.values():
            btn.setEnabled(enabled)
        self.btn_shadow_off.setEnabled(enabled)
        self.btn_shadow_on.setEnabled(enabled)
        self.btn_apply.setEnabled(enabled)

    def update_connection_status(self, connected: bool, detail: str = ""):
        if connected:
            self.banner.setObjectName("bannerConnected")
            self.banner.style().unpolish(self.banner)
            self.banner.style().polish(self.banner)
            self.banner_icon_lbl.setText("✅")
            self.banner_icon_lbl.setStyleSheet("font-size: 16px; color: #10B981;")
            self.banner_text_lbl.setText(f"Connected to GameLoop  •  {detail}")
            self.banner_text_lbl.setStyleSheet("color: #6EE7B7; font-size: 12px; font-weight: 600;")
            self.btn_connect.setText("🔌  Disconnect")
            self.btn_connect.setProperty("btnStyle", "danger")
            self.btn_connect.style().unpolish(self.btn_connect)
            self.btn_connect.style().polish(self.btn_connect)
            self.set_controls_enabled(True)
        else:
            self.banner.setObjectName("bannerDisconnected")
            self.banner.style().unpolish(self.banner)
            self.banner.style().polish(self.banner)
            self.banner_icon_lbl.setText("⚠")
            self.banner_icon_lbl.setStyleSheet("font-size: 16px; color: #F59E0B;")
            self.banner_text_lbl.setText("Not connected — click Connect to GameLoop below")
            self.banner_text_lbl.setStyleSheet("color: #FCD34D; font-size: 12px; font-weight: 600;")
            self.btn_connect.setText("🔗  Connect to GameLoop")
            self.btn_connect.setProperty("btnStyle", "success")
            self.btn_connect.style().unpolish(self.btn_connect)
            self.btn_connect.style().polish(self.btn_connect)
            self.set_controls_enabled(False)
