from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout
from ..constants import APP_NAME, APP_VERSION

class AboutPage(QWidget):
    """About Page Component."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        # Header Card
        header_card = QFrame()
        header_card.setProperty("class", "cardFrame")
        h_layout = QVBoxLayout(header_card)
        h_layout.setContentsMargins(20, 20, 20, 20)

        app_title = QLabel(f"{APP_NAME} {APP_VERSION}")
        app_title.setStyleSheet("font-size: 22px; font-weight: 800; color: #FFFFFF;")
        
        app_subtitle = QLabel("Ultimate GameLoop Optimization & PUBG Mobile GFX Tool")
        app_subtitle.setStyleSheet("font-size: 13px; color: #06B6D4; font-weight: 600;")

        desc = QLabel(
            "EX Tool v0.3 is completely rebuilt from the ground up for maximum GameLoop performance, "
            "zero input lag, high FPS stability, and automated dynamic ADB connection handling."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 12px; color: #9CA3AF; margin-top: 8px;")

        h_layout.addWidget(app_title)
        h_layout.addWidget(app_subtitle)
        h_layout.addWidget(desc)

        main_layout.addWidget(header_card)

        # Features Overview Grid
        feat_card = QFrame()
        feat_card.setProperty("class", "cardFrame")
        f_layout = QGridLayout(feat_card)
        f_layout.setContentsMargins(20, 20, 20, 20)
        f_layout.setSpacing(12)

        features = [
            ("⚡ Dynamic ADB Connection", "Auto-discovers GameLoop listening ports and establishes reliable bridge."),
            ("🎮 Active.sav Binary Editor", "Unlocks hidden PUBG graphics qualities, style presets, and 120 FPS modes."),
            ("🚀 Full PC & VM Boost", "Assigns dedicated CPU core affinity, max VMMemory, and real-time process priority."),
            ("🎯 FPS Stabilizer", "Enables Windows high-precision timer resolution and kills background throttlers."),
            ("🌐 Low-Ping DNS Switcher", "Configures fast DNS servers with real-time latency verification."),
            ("🖥️ VM View & Resolution", "Configures customized iPad aspect ratios and display density.")
        ]

        for idx, (title, detail) in enumerate(features):
            row = idx // 2
            col = idx % 2

            item_box = QVBoxLayout()
            t_lbl = QLabel(title)
            t_lbl.setStyleSheet("font-weight: 700; color: #7C3AED; font-size: 13px;")
            d_lbl = QLabel(detail)
            d_lbl.setStyleSheet("color: #9CA3AF; font-size: 11px;")
            d_lbl.setWordWrap(True)

            item_box.addWidget(t_lbl)
            item_box.addWidget(d_lbl)
            f_layout.addLayout(item_box, row, col)

        main_layout.addWidget(feat_card, 1)
