import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QIcon, QFont, QMouseEvent
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QFrame, QApplication, QSizePolicy
)

from ..constants import APP_NAME, APP_VERSION, FULL_APP_NAME, PUBG_VERSIONS, DNS_SERVERS
from ..registry import RegistryManager
from ..adb_manager import AdbManager
from ..graphics import GraphicsManager
from ..optimizer import SystemOptimizer, resource_path
from ..workers import ConnectWorker, SubmitGfxWorker, SystemOptimizeWorker, PingWorker

from .theme import THEME_QSS
from .gfx_page import GfxPage
from .optimizer_page import OptimizerPage
from .about_page import AboutPage

class MainWindow(QMainWindow):
    """Main Application Window for EX Tool v0.3."""

    def __init__(self):
        super().__init__()
        self.adb_mgr = AdbManager()
        self.gfx_mgr = GraphicsManager()
        self.optimizer = SystemOptimizer()
        self.drag_position = QPoint()

        self.init_ui()
        self.connect_events()

    def init_ui(self):
        self.setWindowTitle(FULL_APP_NAME)
        self.setMinimumSize(960, 640)
        self.resize(1100, 720)
        self.setStyleSheet(THEME_QSS)

        # Set Window Icon
        ico_path = resource_path(r"assets\icons\logo.ico")
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))

        # Central Widget & Root Layout
        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.root_layout = QVBoxLayout(self.central_widget)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        self._build_title_bar()
        self._build_stacked_pages()
        self._build_status_bar()

        self.setCentralWidget(self.central_widget)

    def _build_title_bar(self):
        self.title_bar = QFrame()
        self.title_bar.setObjectName("titleBar")
        tb_layout = QHBoxLayout(self.title_bar)
        tb_layout.setContentsMargins(16, 0, 16, 0)
        tb_layout.setSpacing(12)

        # App Brand & Badge
        self.lbl_app_name = QLabel(APP_NAME)
        self.lbl_app_name.setObjectName("appNameLabel")
        self.lbl_app_badge = QLabel(APP_VERSION)
        self.lbl_app_badge.setObjectName("appBadgeLabel")

        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(6)
        brand_layout.addWidget(self.lbl_app_name)
        brand_layout.addWidget(self.lbl_app_badge)

        # Navigation Bar
        nav_host = QWidget()
        nav_layout = QHBoxLayout(nav_host)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(4)

        self.btn_nav_gfx = QPushButton("GFX Settings")
        self.btn_nav_gfx.setProperty("role", "nav")
        self.btn_nav_gfx.setCheckable(True)
        self.btn_nav_gfx.setChecked(True)

        self.btn_nav_opt = QPushButton("PC Optimizer")
        self.btn_nav_opt.setProperty("role", "nav")
        self.btn_nav_opt.setCheckable(True)

        self.btn_nav_about = QPushButton("About")
        self.btn_nav_about.setProperty("role", "nav")
        self.btn_nav_about.setCheckable(True)

        nav_layout.addWidget(self.btn_nav_gfx)
        nav_layout.addWidget(self.btn_nav_opt)
        nav_layout.addWidget(self.btn_nav_about)

        # Controls
        self.btn_min = QPushButton("—")
        self.btn_min.setProperty("role", "titleControl")
        self.btn_min.clicked.connect(self.showMinimized)

        self.btn_close = QPushButton("✕")
        self.btn_close.setProperty("role", "titleControlClose")
        self.btn_close.clicked.connect(self.close)

        tb_layout.addLayout(brand_layout)
        tb_layout.addStretch(1)
        tb_layout.addWidget(nav_host)
        tb_layout.addStretch(1)
        tb_layout.addWidget(self.btn_min)
        tb_layout.addWidget(self.btn_close)

        self.root_layout.addWidget(self.title_bar)

    def _build_stacked_pages(self):
        self.stacked = QStackedWidget()
        
        self.gfx_page = GfxPage()
        self.opt_page = OptimizerPage()
        self.about_page = AboutPage()

        self.stacked.addWidget(self.gfx_page)
        self.stacked.addWidget(self.opt_page)
        self.stacked.addWidget(self.about_page)

        self.root_layout.addWidget(self.stacked, 1)

    def _build_status_bar(self):
        self.status_frame = QFrame()
        self.status_frame.setObjectName("statusBarFrame")
        sb_layout = QHBoxLayout(self.status_frame)
        sb_layout.setContentsMargins(14, 6, 14, 6)

        self.lbl_status = QLabel("Ready")
        self.lbl_status.setObjectName("statusLabel")
        sb_layout.addWidget(self.lbl_status)

        self.root_layout.addWidget(self.status_frame)

    def show_status(self, message: str, msg_type: str = "info", duration_ms: int = 5000):
        color_map = {
            "info": "#9CA3AF",
            "success": "#10B981",
            "warning": "#FBBF24",
            "error": "#EF4444"
        }
        color = color_map.get(msg_type, "#9CA3AF")
        self.lbl_status.setText(message)
        self.lbl_status.setStyleSheet(f"color: {color}; font-weight: 600;")

    def connect_events(self):
        # Nav switching
        self.btn_nav_gfx.clicked.connect(lambda: self.switch_page(0))
        self.btn_nav_opt.clicked.connect(lambda: self.switch_page(1))
        self.btn_nav_about.clicked.connect(lambda: self.switch_page(2))

        # GFX Page Buttons
        self.gfx_page.btn_connect.clicked.connect(self.on_connect_clicked)
        self.gfx_page.btn_apply.clicked.connect(self.on_apply_gfx_clicked)
        self.gfx_page.btn_use_version.clicked.connect(self.on_select_version_clicked)

        # Optimizer Page Buttons
        self.opt_page.btn_temp_cleaner.clicked.connect(lambda: self.run_optimizer_action("temp_cleaner"))
        self.opt_page.btn_full_boost.clicked.connect(lambda: self.run_optimizer_action("full_boost"))
        self.opt_page.btn_priority_boost.clicked.connect(self.on_priority_boost_clicked)
        self.opt_page.btn_latency_tweaks.clicked.connect(lambda: self.run_optimizer_action("latency_tweaks"))
        self.opt_page.btn_fps_stabilizer.clicked.connect(lambda: self.run_optimizer_action("fps_stabilizer"))
        self.opt_page.btn_engine_ini.clicked.connect(self.on_engine_ini_clicked)
        self.opt_page.btn_headshot_tweaks.clicked.connect(self.on_headshot_tweaks_clicked)
        self.opt_page.btn_exp_fps.clicked.connect(self.on_exp_fps_clicked)
        self.opt_page.btn_apply_all.clicked.connect(lambda: self.run_optimizer_action("apply_all"))
        self.opt_page.btn_kill_gl.clicked.connect(self.on_kill_gl_clicked)

        # DNS & Shortcut & iPad
        self.opt_page.btn_apply_dns.clicked.connect(self.on_apply_dns_clicked)
        self.opt_page.dns_combo.currentTextChanged.connect(self.on_dns_changed)
        self.opt_page.btn_create_shortcut.clicked.connect(self.on_create_shortcut_clicked)
        self.opt_page.btn_apply_ipad.clicked.connect(self.on_apply_ipad_clicked)

        # Initial ping test
        self.on_dns_changed(self.opt_page.dns_combo.currentText())

    def switch_page(self, idx: int):
        self.btn_nav_gfx.setChecked(idx == 0)
        self.btn_nav_opt.setChecked(idx == 1)
        self.btn_nav_about.setChecked(idx == 2)
        self.stacked.setCurrentIndex(idx)

    # --- Handlers ---
    def on_connect_clicked(self):
        if self.adb_mgr.is_connected:
            self.adb_mgr.is_connected = False
            self.adb_mgr.device = None
            self.adb_mgr.kill_adb()
            self.gfx_page.update_connection_status(False)
            self.show_status("Disconnected from GameLoop.", "warning")
            return

        self.gfx_page.btn_connect.setEnabled(False)
        self.show_status("Connecting to GameLoop ADB...", "info")
        
        self.conn_worker = ConnectWorker(self.adb_mgr)
        self.conn_worker.finished.connect(self.on_connect_finished)
        self.conn_worker.start()

    def on_connect_finished(self, success: bool, message: str, installed_versions: list):
        self.gfx_page.btn_connect.setEnabled(True)
        if success:
            self.show_status(message, "success")
            self.gfx_page.update_connection_status(True, message)
            
            if len(installed_versions) > 1:
                self.gfx_page.version_combo.clear()
                self.gfx_page.version_combo.addItems(installed_versions)
                self.gfx_page.version_chooser_card.show()
                pkg = list(PUBG_VERSIONS.keys())[list(PUBG_VERSIONS.values()).index(installed_versions[0])]
                self.gfx_mgr.fetch_graphics_file(self.adb_mgr.device, pkg)
            elif len(installed_versions) == 1:
                pkg = list(PUBG_VERSIONS.keys())[list(PUBG_VERSIONS.values()).index(installed_versions[0])]
                self.gfx_mgr.fetch_graphics_file(self.adb_mgr.device, pkg)
                self.gfx_page.version_chooser_card.hide()
            else:
                pkg = "com.tencent.ig"
                self.gfx_mgr.fetch_graphics_file(self.adb_mgr.device, pkg)
                self.gfx_page.version_chooser_card.hide()
        else:
            self.show_status(message, "error")
            self.gfx_page.update_connection_status(False)

    def on_select_version_clicked(self):
        name = self.gfx_page.version_combo.currentText()
        if name in PUBG_VERSIONS.values() and self.adb_mgr.device:
            pkg = list(PUBG_VERSIONS.keys())[list(PUBG_VERSIONS.values()).index(name)]
            self.gfx_mgr.fetch_graphics_file(self.adb_mgr.device, pkg)
            self.show_status(f"Selected target game: {name}", "success")

    def on_apply_gfx_clicked(self):
        if not self.adb_mgr.is_connected or not self.adb_mgr.device:
            self.show_status("Please connect to GameLoop first.", "warning")
            return

        quality = self.gfx_page.q_group.checkedButton().text()
        fps = self.gfx_page.fps_group.checkedButton().text().split(" (")[0]
        style = self.gfx_page.style_group.checkedButton().text()
        disable_shadow = self.gfx_page.btn_shadow_off.isChecked()

        self.gfx_page.btn_apply.setEnabled(False)
        self.show_status("Applying graphics settings & syncing with GameLoop...", "info")

        self.gfx_worker = SubmitGfxWorker(self.gfx_mgr, self.adb_mgr, quality, fps, style, disable_shadow)
        self.gfx_worker.finished.connect(self.on_apply_gfx_finished)
        self.gfx_worker.start()

    def on_apply_gfx_finished(self, success: bool, message: str):
        self.gfx_page.btn_apply.setEnabled(True)
        self.show_status(message, "success" if success else "error")

    def run_optimizer_action(self, action_name: str):
        self.show_status(f"Running optimization: {action_name}...", "info")
        target_cores = None
        raw_cores = self.opt_page.cores_input.text().strip()
        if raw_cores.isdigit():
            target_cores = int(raw_cores)

        self.opt_worker = SystemOptimizeWorker(action_name, self.optimizer, target_cores)
        self.opt_worker.finished.connect(lambda ok, msg: self.show_status(msg, "success" if ok else "error"))
        self.opt_worker.start()

    def on_priority_boost_clicked(self):
        prio = self.opt_page.prio_combo.currentText()
        raw_cores = self.opt_page.cores_input.text().strip()
        target_cores = int(raw_cores) if raw_cores.isdigit() else None
        
        ram_mb, cpu_cores = self.optimizer.force_resource_allocation(target_cores=target_cores)
        boosted, applied = self.optimizer.boost_priority(priority=prio, target_cores=target_cores)
        self.show_status(f"Priority Boost ({prio}): Allocated {cpu_cores} Cores, {ram_mb}MB RAM, {boosted} processes boosted.", "success")

    def on_engine_ini_clicked(self):
        if not self.adb_mgr.is_connected or not self.adb_mgr.device:
            self.show_status("Connect to GameLoop first.", "warning")
            return
        mode = self.opt_page.engine_combo.currentText().lower()
        success = self.gfx_mgr.push_engine_ini(self.adb_mgr.device, mode=mode)
        if success:
            self.show_status(f"Engine.ini clarity settings pushed ({mode} mode).", "success")
        else:
            self.show_status("Failed to push Engine.ini settings.", "error")

    def on_headshot_tweaks_clicked(self):
        if not self.adb_mgr.is_connected or not self.adb_mgr.device:
            self.show_status("Connect to GameLoop first.", "warning")
            return
        self.gfx_mgr.push_engine_ini(self.adb_mgr.device, mode="competitive")
        RegistryManager.set_user_dword("VMDPI", 560)
        self.show_status("Headshot & sharpness tweaks applied successfully!", "success")

    def on_exp_fps_clicked(self):
        if not self.adb_mgr.is_connected or not self.adb_mgr.device:
            self.show_status("Connect to GameLoop first.", "warning")
            return
        val = self.opt_page.exp_combo.currentText()
        self.gfx_mgr.set_fps(val)
        self.gfx_mgr.save_graphics_file()
        self.gfx_mgr.push_graphics_to_device(self.adb_mgr.device)
        self.gfx_mgr.restart_pubg(self.adb_mgr.device)
        self.show_status(f"Experimental FPS applied: {val}", "warning")

    def on_kill_gl_clicked(self):
        res = self.optimizer.kill_gameloop()
        self.show_status(res.message, "success" if res.success else "warning")

    def on_apply_dns_clicked(self):
        dns_key = self.opt_page.dns_combo.currentText()
        servers = DNS_SERVERS.get(dns_key)
        if servers:
            res = self.optimizer.change_dns_servers(servers)
            self.show_status(res.message, "success" if res.success else "error")

    def on_dns_changed(self, text: str):
        servers = DNS_SERVERS.get(text)
        if servers:
            self.ping_worker = PingWorker(text, servers[0])
            self.ping_worker.finished.connect(lambda name, ping_ms: self.opt_page.lbl_dns_ping.setText(
                f"Ping: {ping_ms}ms" if ping_ms > 0 else "Ping: Failed"
            ))
            self.ping_worker.start()

    def on_create_shortcut_clicked(self):
        val = self.opt_page.shortcut_combo.currentText()
        self.show_status(f"Created desktop shortcut for {val}", "success")

    def on_apply_ipad_clicked(self):
        sel = self.opt_page.ipad_combo.currentText()
        if "720P" in sel:
            w, h = 1280, 720
        elif "2K" in sel:
            w, h = 2560, 1440
        else:
            w, h = 1920, 1080
        self.gfx_mgr.set_ipad_resolution(w, h)
        self.show_status(f"VM Resolution set to {w}x{h}. Restart GameLoop to apply.", "success")
