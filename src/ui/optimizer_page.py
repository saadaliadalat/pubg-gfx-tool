from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QComboBox, QLineEdit, QGridLayout, QSizePolicy
)

class OptimizerPage(QWidget):
    """PC & GameLoop Optimizer Page Component."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(14)

        # LEFT COLUMN: System Optimizer
        left_card = QFrame()
        left_card.setProperty("class", "cardFrame")
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(10)

        opt_title = QLabel("SYSTEM & GAMELOOP OPTIMIZER")
        opt_title.setProperty("class", "sectionHeader")
        left_layout.addWidget(opt_title)

        self.btn_temp_cleaner = QPushButton("🧹 Temp & Cache Cleaner")
        left_layout.addWidget(self.btn_temp_cleaner)

        self.btn_full_boost = QPushButton("🚀 Full Resource Boost (RAM + CPU + GPU)")
        self.btn_full_boost.setProperty("class", "primary")
        left_layout.addWidget(self.btn_full_boost)

        # Priority & Core config row
        prio_row = QHBoxLayout()
        self.btn_priority_boost = QPushButton("⚡ Priority Boost")
        self.cores_input = QLineEdit()
        self.cores_input.setPlaceholderText("CPU Cores (Auto)")
        self.prio_combo = QComboBox()
        self.prio_combo.addItems(["High", "Realtime"])
        prio_row.addWidget(self.btn_priority_boost, 2)
        prio_row.addWidget(self.cores_input, 1)
        prio_row.addWidget(self.prio_combo, 1)
        left_layout.addLayout(prio_row)

        self.btn_latency_tweaks = QPushButton("🌐 Latency & Network Tweaks")
        left_layout.addWidget(self.btn_latency_tweaks)

        self.btn_fps_stabilizer = QPushButton("🎯 FPS Stabilizer & High-Precision Timer")
        left_layout.addWidget(self.btn_fps_stabilizer)

        # Engine.ini row
        engine_row = QHBoxLayout()
        self.btn_engine_ini = QPushButton("⚙️ Engine.ini Clarity Optimizer")
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Competitive", "Balanced"])
        engine_row.addWidget(self.btn_engine_ini, 2)
        engine_row.addWidget(self.engine_combo, 1)
        left_layout.addLayout(engine_row)

        self.btn_headshot_tweaks = QPushButton("🎯 Headshot & Sharpness Tweaks")
        left_layout.addWidget(self.btn_headshot_tweaks)

        # Experimental FPS row
        exp_row = QHBoxLayout()
        self.btn_exp_fps = QPushButton("🔥 Experimental FPS Unlock")
        self.exp_combo = QComboBox()
        self.exp_combo.addItems(["144fps [EXP]", "165fps [EXP]", "200fps [EXP]"])
        exp_row.addWidget(self.btn_exp_fps, 2)
        exp_row.addWidget(self.exp_combo, 1)
        left_layout.addLayout(exp_row)

        # Apply ALL & Kill buttons
        self.btn_apply_all = QPushButton("⚡ Apply ALL Recommended Optimizations")
        self.btn_apply_all.setProperty("class", "accent")
        left_layout.addWidget(self.btn_apply_all)

        self.btn_kill_gl = QPushButton("🚫 Force Close GameLoop Processes")
        self.btn_kill_gl.setProperty("class", "danger")
        left_layout.addWidget(self.btn_kill_gl)

        left_layout.addStretch(1)

        # RIGHT COLUMN: Network, Shortcut, iPad
        right_col = QVBoxLayout()
        right_col.setSpacing(14)

        # Network Panel
        net_card = QFrame()
        net_card.setProperty("class", "cardFrame")
        net_layout = QVBoxLayout(net_card)
        net_layout.setContentsMargins(16, 14, 16, 14)
        net_layout.setSpacing(10)

        net_title = QLabel("GAMING DNS OPTIMIZER")
        net_title.setProperty("class", "sectionHeader")
        net_layout.addWidget(net_title)

        dns_row = QHBoxLayout()
        self.dns_combo = QComboBox()
        self.dns_combo.addItems([
            "Google DNS - 8.8.8.8",
            "Cloudflare DNS - 1.1.1.1",
            "Quad9 DNS - 9.9.9.9",
            "Cisco Umbrella - 208.67.222.222",
            "Yandex DNS - 77.88.8.1",
        ])
        self.btn_apply_dns = QPushButton("Apply DNS")
        dns_row.addWidget(self.dns_combo, 2)
        dns_row.addWidget(self.btn_apply_dns, 1)
        net_layout.addLayout(dns_row)

        self.lbl_dns_ping = QLabel("Ping: Checking...")
        self.lbl_dns_ping.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: bold;")
        net_layout.addWidget(self.lbl_dns_ping)

        # Desktop Shortcut Panel
        sc_card = QFrame()
        sc_card.setProperty("class", "cardFrame")
        sc_layout = QVBoxLayout(sc_card)
        sc_layout.setContentsMargins(16, 14, 16, 14)
        sc_layout.setSpacing(10)

        sc_title = QLabel("GAME SHORTCUT GENERATOR")
        sc_title.setProperty("class", "sectionHeader")
        sc_layout.addWidget(sc_title)

        sc_row = QHBoxLayout()
        self.shortcut_combo = QComboBox()
        self.shortcut_combo.addItems([
            "PUBG Mobile Global",
            "PUBG Mobile VN",
            "PUBG Mobile TW",
            "PUBG Mobile KR",
            "Battlegrounds Mobile India",
        ])
        self.btn_create_shortcut = QPushButton("Create Shortcut")
        sc_row.addWidget(self.shortcut_combo, 2)
        sc_row.addWidget(self.btn_create_shortcut, 1)
        sc_layout.addLayout(sc_row)

        # iPad / Resolution Panel
        ipad_card = QFrame()
        ipad_card.setProperty("class", "cardFrame")
        ipad_layout = QVBoxLayout(ipad_card)
        ipad_layout.setContentsMargins(16, 14, 16, 14)
        ipad_layout.setSpacing(10)

        ipad_title = QLabel("IPAD VIEW & VM RESOLUTION")
        ipad_title.setProperty("class", "sectionHeader")
        ipad_layout.addWidget(ipad_title)

        ipad_row = QHBoxLayout()
        self.ipad_combo = QComboBox()
        self.ipad_combo.addItems(["Smart 720P (1280x720)", "Smart 1080P (1920x1080)", "Smart 2K (2560x1440)"])
        self.btn_apply_ipad = QPushButton("Apply Resolution")
        self.btn_reset_ipad = QPushButton("Reset")
        ipad_row.addWidget(self.ipad_combo, 2)
        ipad_row.addWidget(self.btn_apply_ipad, 1)
        ipad_row.addWidget(self.btn_reset_ipad, 1)
        ipad_layout.addLayout(ipad_row)

        right_col.addWidget(net_card)
        right_col.addWidget(sc_card)
        right_col.addWidget(ipad_card)
        right_col.addStretch(1)

        grid_layout.addWidget(left_card, 3)
        grid_layout.addLayout(right_col, 2)

        main_layout.addLayout(grid_layout)
