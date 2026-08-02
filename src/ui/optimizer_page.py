from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QLineEdit, QSizePolicy
)

def _make_card(parent=None) -> QFrame:
    f = QFrame(parent)
    f.setObjectName("sectionCard")
    return f

def _make_section_title(text: str, parent=None) -> QLabel:
    lbl = QLabel(text, parent)
    lbl.setObjectName("sectionTitle")
    return lbl


class OptimizerPage(QWidget):
    """PC & GameLoop Optimizer Page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(12)

        # Two-column grid
        cols = QHBoxLayout()
        cols.setSpacing(12)

        # ── LEFT: System Optimizer ────────────────────────────
        left_card = _make_card()
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(18, 16, 18, 16)
        left_layout.setSpacing(10)

        left_layout.addWidget(_make_section_title("SYSTEM & GAMELOOP OPTIMIZER"))

        # Temp Cleaner
        self.btn_temp_cleaner = QPushButton("🧹  Temp & Shader Cache Cleaner")
        left_layout.addWidget(self.btn_temp_cleaner)

        # Full Resource Boost
        self.btn_full_boost = QPushButton("🚀  Full Resource Boost  (RAM + CPU + GPU)")
        self.btn_full_boost.setProperty("btnStyle", "primary")
        self.btn_full_boost.style().unpolish(self.btn_full_boost)
        self.btn_full_boost.style().polish(self.btn_full_boost)
        left_layout.addWidget(self.btn_full_boost)

        # Priority boost row
        prio_row = QHBoxLayout()
        prio_row.setSpacing(8)
        self.btn_priority_boost = QPushButton("⚡  Priority Boost")
        self.cores_input = QLineEdit()
        self.cores_input.setPlaceholderText("CPU Cores (Auto)")
        self.cores_input.setMaximumWidth(130)
        self.prio_combo = QComboBox()
        self.prio_combo.addItems(["High", "Realtime"])
        self.prio_combo.setMaximumWidth(100)
        prio_row.addWidget(self.btn_priority_boost, 2)
        prio_row.addWidget(self.cores_input)
        prio_row.addWidget(self.prio_combo)
        left_layout.addLayout(prio_row)

        self.btn_latency_tweaks = QPushButton("🌐  Latency & Network Tweaks")
        left_layout.addWidget(self.btn_latency_tweaks)

        self.btn_fps_stabilizer = QPushButton("🎯  FPS Stabilizer + High-Precision Timer")
        left_layout.addWidget(self.btn_fps_stabilizer)

        # Engine.ini row
        engine_row = QHBoxLayout()
        engine_row.setSpacing(8)
        self.btn_engine_ini = QPushButton("⚙  Engine.ini Clarity Optimizer")
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Competitive", "Balanced"])
        self.engine_combo.setMaximumWidth(120)
        engine_row.addWidget(self.btn_engine_ini, 2)
        engine_row.addWidget(self.engine_combo)
        left_layout.addLayout(engine_row)

        self.btn_headshot_tweaks = QPushButton("🎯  Headshot & Sharpness Tweaks")
        left_layout.addWidget(self.btn_headshot_tweaks)

        # Experimental FPS row
        exp_row = QHBoxLayout()
        exp_row.setSpacing(8)
        self.btn_exp_fps = QPushButton("🔥  Experimental FPS Unlock")
        self.exp_combo = QComboBox()
        self.exp_combo.addItems(["144fps [EXP]", "165fps [EXP]", "200fps [EXP]"])
        self.exp_combo.setMaximumWidth(140)
        exp_row.addWidget(self.btn_exp_fps, 2)
        exp_row.addWidget(self.exp_combo)
        left_layout.addLayout(exp_row)

        exp_hint = QLabel("⚠  Experimental — may not work on all devices")
        exp_hint.setStyleSheet("color: #F59E0B; font-size: 11px;")
        left_layout.addWidget(exp_hint)

        # Apply ALL
        self.btn_apply_all = QPushButton("⚡  Apply ALL Recommended Optimizations")
        self.btn_apply_all.setProperty("btnStyle", "success")
        self.btn_apply_all.style().unpolish(self.btn_apply_all)
        self.btn_apply_all.style().polish(self.btn_apply_all)
        left_layout.addWidget(self.btn_apply_all)

        # Force close
        self.btn_kill_gl = QPushButton("🚫  Force Close GameLoop Processes")
        self.btn_kill_gl.setProperty("btnStyle", "danger")
        self.btn_kill_gl.style().unpolish(self.btn_kill_gl)
        self.btn_kill_gl.style().polish(self.btn_kill_gl)
        left_layout.addWidget(self.btn_kill_gl)
        left_layout.addStretch(1)

        # ── RIGHT: Network, Shortcut, iPad ────────────────────
        right_col = QVBoxLayout()
        right_col.setSpacing(12)

        # Network
        net_card = _make_card()
        net_layout = QVBoxLayout(net_card)
        net_layout.setContentsMargins(16, 14, 16, 14)
        net_layout.setSpacing(10)
        net_layout.addWidget(_make_section_title("GAMING DNS OPTIMIZER"))
        dns_row = QHBoxLayout()
        dns_row.setSpacing(8)
        self.dns_combo = QComboBox()
        self.dns_combo.addItems([
            "Google DNS - 8.8.8.8",
            "Cloudflare DNS - 1.1.1.1",
            "Quad9 DNS - 9.9.9.9",
            "Cisco Umbrella - 208.67.222.222",
            "Yandex DNS - 77.88.8.1",
        ])
        self.btn_apply_dns = QPushButton("Apply")
        self.btn_apply_dns.setFixedWidth(76)
        dns_row.addWidget(self.dns_combo, 1)
        dns_row.addWidget(self.btn_apply_dns)
        net_layout.addLayout(dns_row)
        self.lbl_dns_ping = QLabel("Ping: Checking...")
        self.lbl_dns_ping.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 600;")
        net_layout.addWidget(self.lbl_dns_ping)

        # Desktop shortcut
        sc_card = _make_card()
        sc_layout = QVBoxLayout(sc_card)
        sc_layout.setContentsMargins(16, 14, 16, 14)
        sc_layout.setSpacing(10)
        sc_layout.addWidget(_make_section_title("GAME SHORTCUT GENERATOR"))
        sc_row = QHBoxLayout()
        sc_row.setSpacing(8)
        self.shortcut_combo = QComboBox()
        self.shortcut_combo.addItems([
            "PUBG Mobile Global",
            "PUBG Mobile VN",
            "PUBG Mobile TW",
            "PUBG Mobile KR",
            "Battlegrounds Mobile India",
        ])
        self.btn_create_shortcut = QPushButton("Create")
        self.btn_create_shortcut.setFixedWidth(76)
        sc_row.addWidget(self.shortcut_combo, 1)
        sc_row.addWidget(self.btn_create_shortcut)
        sc_layout.addLayout(sc_row)

        # iPad resolution
        ipad_card = _make_card()
        ipad_layout = QVBoxLayout(ipad_card)
        ipad_layout.setContentsMargins(16, 14, 16, 14)
        ipad_layout.setSpacing(10)
        ipad_layout.addWidget(_make_section_title("IPAD VIEW & VM RESOLUTION"))
        ipad_row = QHBoxLayout()
        ipad_row.setSpacing(8)
        self.ipad_combo = QComboBox()
        self.ipad_combo.addItems([
            "Smart 720P (1280×720)",
            "Smart 1080P (1920×1080)",
            "Smart 2K (2560×1440)",
        ])
        self.btn_apply_ipad = QPushButton("Apply")
        self.btn_apply_ipad.setFixedWidth(76)
        self.btn_reset_ipad = QPushButton("Reset")
        self.btn_reset_ipad.setFixedWidth(60)
        ipad_row.addWidget(self.ipad_combo, 1)
        ipad_row.addWidget(self.btn_apply_ipad)
        ipad_row.addWidget(self.btn_reset_ipad)
        ipad_layout.addLayout(ipad_row)

        right_col.addWidget(net_card)
        right_col.addWidget(sc_card)
        right_col.addWidget(ipad_card)
        right_col.addStretch(1)

        cols.addWidget(left_card, 3)
        cols.addLayout(right_col, 2)
        root.addLayout(cols, 1)
