from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from . import resource_path
from .ui_images import resources_rc

THEME = """
QMainWindow, QWidget {
    background-color: #0f0f1a;
    color: #ffffff;
    font-family: 'Segoe UI', Arial;
}

#titleBar {
    background-color: #1a1a2e;
    border-bottom: 2px solid #e94560;
}

QPushButton[role="nav"] {
    background: transparent;
    color: #888888;
    font-size: 13px;
    font-weight: bold;
    padding: 8px 20px;
    border: none;
    border-bottom: 3px solid transparent;
}
QPushButton[role="nav"]:checked {
    color: #ffffff;
    border-bottom: 3px solid #e94560;
}
QPushButton[role="nav"]:hover {
    color: #cccccc;
}

#sectionLabel {
    color: #e94560;
    font-size: 14px;
    font-weight: bold;
    border-bottom: 1px solid #333355;
    padding-bottom: 4px;
}

QPushButton {
    background-color: #1e1e35;
    color: #cccccc;
    border: 1px solid #333355;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 12px;
    min-height: 35px;
}
QPushButton:hover {
    background-color: #2a2a4a;
    border-color: #e94560;
    color: #ffffff;
}
QPushButton:checked {
    background-color: #e94560;
    color: #ffffff;
    border-color: #e94560;
    font-weight: bold;
}
QPushButton:disabled {
    background-color: #111122;
    color: #444444;
    border-color: #222233;
}
QPushButton:pressed {
    background-color: #c73652;
}

#connectBtn {
    background-color: #1a4a1a;
    border: 1px solid #2a7a2a;
    color: #aaffaa;
    min-height: 40px;
    font-size: 13px;
}
#connectBtn:checked {
    background-color: #2a7a2a;
    color: #ffffff;
}

#submitBtn {
    background-color: #e94560;
    color: white;
    font-weight: bold;
    font-size: 13px;
    min-height: 40px;
    border: none;
}
#submitBtn:hover { background-color: #ff5577; }
#submitBtn:pressed { background-color: #c73652; }

#forceCloseBtn {
    background-color: #4a1a1a;
    border: 1px solid #7a2a2a;
    color: #ffaaaa;
    min-height: 45px;
    font-size: 13px;
    font-weight: bold;
}
#forceCloseBtn:hover {
    background-color: #7a2a2a;
    color: #ffffff;
}

QComboBox {
    background-color: #1e1e35;
    color: #ffffff;
    border: 1px solid #333355;
    border-radius: 6px;
    padding: 6px 35px 6px 12px;
    font-size: 12px;
    min-height: 32px;
    min-width: 120px;
}
QComboBox:hover {
    border-color: #e94560;
}
QComboBox:focus {
    border-color: #e94560;
    outline: none;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #333355;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    background-color: #e94560;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid white;
    width: 0;
    height: 0;
}
QComboBox QAbstractItemView {
    background-color: #1a1a2e;
    color: #ffffff;
    border: 1px solid #e94560;
    border-radius: 4px;
    selection-background-color: #e94560;
    selection-color: #ffffff;
    padding: 4px;
    outline: none;
}
QComboBox QAbstractItemView::item {
    min-height: 28px;
    padding: 4px 8px;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #2a2a4a;
}

QLineEdit {
    background-color: #1e1e35;
    color: #ffffff;
    border: 1px solid #333355;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
    min-height: 32px;
}
QLineEdit:hover {
    border-color: #e94560;
}
QLineEdit:focus {
    border-color: #e94560;
}

#statusBar {
    background-color: #1a1a2e;
    border-top: 1px solid #333355;
    color: #888888;
    padding: 5px 10px;
    font-size: 11px;
}

#sectionBox {
    background-color: #14142a;
    border: 1px solid #222244;
    border-radius: 8px;
    padding: 12px;
}

QPushButton[role="style"] {
    background-color: #1e1e35;
    border: 2px solid #333355;
    border-radius: 6px;
    padding: 4px;
    min-height: 72px;
}
QPushButton[role="style"]:checked {
    border: 2px solid #e94560;
}

QLabel#connection_banner_label {
    background-color: #4a2d00;
    border: 1px solid #aa6600;
    color: #ffd080;
    border-radius: 6px;
    padding: 8px;
    font-weight: bold;
}

QFrame#aboutHeaderCard {
    background-color: #1a1a2e;
    border: 1px solid #e94560;
    border-radius: 10px;
    padding: 20px;
}

QFrame#aboutFeaturesCard {
    background-color: #14142a;
    border: 1px solid #222244;
    border-radius: 10px;
}

QLabel#aboutFeatureName, QLabel#aboutFeatureDesc {
    color: #cccccc;
    font-size: 12px;
    padding: 8px 4px;
    border-bottom: 1px solid #1e1e35;
}

QLabel#aboutFeatureName {
    font-weight: bold;
}
"""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(760, 500)
        MainWindow.resize(1100, 700)
        MainWindow.setStyleSheet(THEME)

        font = QFont("Segoe UI", 10)
        MainWindow.setFont(font)

        icon = QIcon()
        icon.addFile(resource_path(r"assets\icons\logo.ico"))
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.rootLayout.setSpacing(0)

        self._build_title_bar()
        self._build_pages()
        self._build_status_bar()

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

    def _build_title_bar(self):
        self.titleBar = QFrame(self.centralwidget)
        self.titleBar.setObjectName("titleBar")
        self.titleBarLayout = QHBoxLayout(self.titleBar)
        self.titleBarLayout.setContentsMargins(12, 8, 12, 8)
        self.titleBarLayout.setSpacing(10)

        self.appname_label = QLabel(self.titleBar)
        self.appname_label.setObjectName("appname_label")
        app_font = QFont("Segoe UI", 12)
        app_font.setBold(True)
        self.appname_label.setFont(app_font)

        nav_host = QWidget(self.titleBar)
        nav_layout = QHBoxLayout(nav_host)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(4)

        self.gfx_button = QPushButton(nav_host)
        self.gfx_button.setObjectName("gfx_button")
        self.gfx_button.setProperty("role", "nav")
        self.gfx_button.setCheckable(True)
        self.gfx_button.setChecked(True)

        self.other_button = QPushButton(nav_host)
        self.other_button.setObjectName("other_button")
        self.other_button.setProperty("role", "nav")
        self.other_button.setCheckable(True)

        self.about_button = QPushButton(nav_host)
        self.about_button.setObjectName("about_button")
        self.about_button.setProperty("role", "nav")
        self.about_button.setCheckable(True)

        nav_layout.addWidget(self.gfx_button)
        nav_layout.addWidget(self.other_button)
        nav_layout.addWidget(self.about_button)

        self.zoom75_btn = QPushButton("75%", self.titleBar)
        self.zoom75_btn.setObjectName("zoom75_btn")
        self.zoom100_btn = QPushButton("100%", self.titleBar)
        self.zoom100_btn.setObjectName("zoom100_btn")
        self.zoom125_btn = QPushButton("125%", self.titleBar)
        self.zoom125_btn.setObjectName("zoom125_btn")
        for b in [self.zoom75_btn, self.zoom100_btn, self.zoom125_btn]:
            b.setMinimumWidth(46)

        self.minimize_btn = QPushButton("-", self.titleBar)
        self.minimize_btn.setObjectName("minimize_btn")
        self.minimize_btn.setMinimumWidth(30)
        self.close_btn = QPushButton("X", self.titleBar)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setMinimumWidth(30)

        self.titleBarLayout.addWidget(self.appname_label, 1)
        self.titleBarLayout.addWidget(nav_host, 0)
        self.titleBarLayout.addStretch(1)
        self.titleBarLayout.addWidget(self.zoom75_btn)
        self.titleBarLayout.addWidget(self.zoom100_btn)
        self.titleBarLayout.addWidget(self.zoom125_btn)
        self.titleBarLayout.addWidget(self.minimize_btn)
        self.titleBarLayout.addWidget(self.close_btn)

        self.rootLayout.addWidget(self.titleBar)

    def _build_pages(self):
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._build_gfx_page()
        self._build_optimizer_page()
        self._build_about_page()

        self.stackedWidget.addWidget(self.gfx_page)
        self.stackedWidget.addWidget(self.other_page)
        self.stackedWidget.addWidget(self.about_page)
        self.rootLayout.addWidget(self.stackedWidget, 1)

    def _section_frame(self, parent):
        frame = QFrame(parent)
        frame.setObjectName("sectionBox")
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return frame

    def _section_label(self, text, parent):
        label = QLabel(text, parent)
        label.setObjectName("sectionLabel")
        return label

    def _build_gfx_page(self):
        self.gfx_page = QWidget()
        self.gfx_page.setObjectName("gfx_page")
        page_layout = QVBoxLayout(self.gfx_page)
        page_layout.setContentsMargins(16, 16, 16, 16)
        page_layout.setSpacing(14)

        self.connection_banner_label = QLabel(self.gfx_page)
        self.connection_banner_label.setObjectName("connection_banner_label")
        page_layout.addWidget(self.connection_banner_label)

        self.frame = QWidget(self.gfx_page)
        self.frame.setObjectName("frame")
        self.frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(12)

        self.GraphicsFrame = self._section_frame(self.frame)
        g_layout = QVBoxLayout(self.GraphicsFrame)
        g_layout.setContentsMargins(12, 10, 12, 10)
        g_layout.setSpacing(10)
        self.graphics_label = self._section_label("Graphics Quality", self.GraphicsFrame)
        g_layout.addWidget(self.graphics_label)

        self.layoutWidget = QWidget(self.GraphicsFrame)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.GraphicsLayout = QHBoxLayout(self.layoutWidget)
        self.GraphicsLayout.setContentsMargins(0, 0, 0, 0)
        self.GraphicsLayout.setSpacing(10)
        self.smooth_graphics_btn = QPushButton("Super Smooth", self.layoutWidget)
        self.smooth_graphics_btn.setObjectName("smooth_graphics_btn")
        self.smooth_graphics_btn.setCheckable(True)
        self.balanced_graphics_btn = QPushButton("Smooth", self.layoutWidget)
        self.balanced_graphics_btn.setObjectName("balanced_graphics_btn")
        self.balanced_graphics_btn.setCheckable(True)
        self.hd_graphics_btn = QPushButton("Balanced", self.layoutWidget)
        self.hd_graphics_btn.setObjectName("hd_graphics_btn")
        self.hd_graphics_btn.setCheckable(True)
        self.hdr_graphics_btn = QPushButton("HD", self.layoutWidget)
        self.hdr_graphics_btn.setObjectName("hdr_graphics_btn")
        self.hdr_graphics_btn.setCheckable(True)
        self.ultrahd_graphics_btn = QPushButton("HDR", self.layoutWidget)
        self.ultrahd_graphics_btn.setObjectName("ultrahd_graphics_btn")
        self.ultrahd_graphics_btn.setCheckable(True)
        self.uhd_graphics_btn = QPushButton("Ultra HD", self.layoutWidget)
        self.uhd_graphics_btn.setObjectName("uhd_graphics_btn")
        self.uhd_graphics_btn.setCheckable(True)
        for btn in [
            self.smooth_graphics_btn,
            self.balanced_graphics_btn,
            self.hd_graphics_btn,
            self.hdr_graphics_btn,
            self.ultrahd_graphics_btn,
            self.uhd_graphics_btn,
        ]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.GraphicsLayout.addWidget(btn)
        g_layout.addWidget(self.layoutWidget)
        self.frame_layout.addWidget(self.GraphicsFrame)

        self.FramerateFrame = self._section_frame(self.frame)
        fps_layout = QVBoxLayout(self.FramerateFrame)
        fps_layout.setContentsMargins(12, 10, 12, 10)
        fps_layout.setSpacing(10)
        self.fps_label = self._section_label("Frame Rate", self.FramerateFrame)
        fps_layout.addWidget(self.fps_label)

        self.layoutWidget1 = QWidget(self.FramerateFrame)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.layoutWidget1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.FramerateLayout = QVBoxLayout(self.layoutWidget1)
        self.FramerateLayout.setContentsMargins(0, 0, 0, 0)
        self.FramerateLayout.setSpacing(8)

        self.FramerateRowTop = QHBoxLayout()
        self.FramerateRowTop.setContentsMargins(0, 0, 0, 0)
        self.FramerateRowTop.setSpacing(8)
        self.FramerateRowBottom = QHBoxLayout()
        self.FramerateRowBottom.setContentsMargins(0, 0, 0, 0)
        self.FramerateRowBottom.setSpacing(8)

        self.low_fps_btn = QPushButton("Low", self.layoutWidget1)
        self.low_fps_btn.setObjectName("low_fps_btn")
        self.low_fps_btn.setCheckable(True)
        self.medium_fps_btn = QPushButton("Medium", self.layoutWidget1)
        self.medium_fps_btn.setObjectName("medium_fps_btn")
        self.medium_fps_btn.setCheckable(True)
        self.high_fps_btn = QPushButton("High", self.layoutWidget1)
        self.high_fps_btn.setObjectName("high_fps_btn")
        self.high_fps_btn.setCheckable(True)
        self.ultra_fps_btn = QPushButton("Ultra", self.layoutWidget1)
        self.ultra_fps_btn.setObjectName("ultra_fps_btn")
        self.ultra_fps_btn.setCheckable(True)
        self.extreme_fps_btn = QPushButton("Extreme", self.layoutWidget1)
        self.extreme_fps_btn.setObjectName("extreme_fps_btn")
        self.extreme_fps_btn.setCheckable(True)
        self.fps90_fps_btn = QPushButton("Extreme+", self.layoutWidget1)
        self.fps90_fps_btn.setObjectName("fps90_fps_btn")
        self.fps90_fps_btn.setCheckable(True)
        self.fps120_fps_btn = QPushButton("Ultra Extreme", self.layoutWidget1)
        self.fps120_fps_btn.setObjectName("fps120_fps_btn")
        self.fps120_fps_btn.setCheckable(True)
        self.fps120_fps_btn.setMinimumWidth(140)

        for btn in [
            self.low_fps_btn,
            self.medium_fps_btn,
            self.high_fps_btn,
            self.ultra_fps_btn,
            self.extreme_fps_btn,
            self.fps90_fps_btn,
        ]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.FramerateRowTop.addWidget(btn)

        self.fps120_fps_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.FramerateRowBottom.addWidget(self.fps120_fps_btn)

        self.FramerateLayout.addLayout(self.FramerateRowTop)
        self.FramerateLayout.addLayout(self.FramerateRowBottom)
        fps_layout.addWidget(self.layoutWidget1)
        self.frame_layout.addWidget(self.FramerateFrame)

        self.StyleFrame = self._section_frame(self.frame)
        style_layout = QVBoxLayout(self.StyleFrame)
        style_layout.setContentsMargins(12, 10, 12, 10)
        style_layout.setSpacing(10)
        self.style_label = self._section_label("Style", self.StyleFrame)
        style_layout.addWidget(self.style_label)

        self.layoutWidget2 = QWidget(self.StyleFrame)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.layoutWidget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.StyleLayout = QHBoxLayout(self.layoutWidget2)
        self.StyleLayout.setContentsMargins(0, 0, 0, 0)
        self.StyleLayout.setSpacing(10)

        self.classic_style_btn = QPushButton("Classic", self.layoutWidget2)
        self.classic_style_btn.setObjectName("classic_style_btn")
        self.classic_style_btn.setCheckable(True)
        self.classic_style_btn.setProperty("role", "style")
        self.classic_style_btn.setIcon(QIcon(":/Graphics/Classic.png"))

        self.colorful_style_btn = QPushButton("Colorful", self.layoutWidget2)
        self.colorful_style_btn.setObjectName("colorful_style_btn")
        self.colorful_style_btn.setCheckable(True)
        self.colorful_style_btn.setProperty("role", "style")
        self.colorful_style_btn.setIcon(QIcon(":/Graphics/Colorful.png"))

        self.realistic_style_btn = QPushButton("Realistic", self.layoutWidget2)
        self.realistic_style_btn.setObjectName("realistic_style_btn")
        self.realistic_style_btn.setCheckable(True)
        self.realistic_style_btn.setProperty("role", "style")
        self.realistic_style_btn.setIcon(QIcon(":/Graphics/Realistic.png"))

        self.soft_style_btn = QPushButton("Soft", self.layoutWidget2)
        self.soft_style_btn.setObjectName("soft_style_btn")
        self.soft_style_btn.setCheckable(True)
        self.soft_style_btn.setProperty("role", "style")
        self.soft_style_btn.setIcon(QIcon(":/Graphics/Soft.png"))

        self.movie_style_btn = QPushButton("Movie", self.layoutWidget2)
        self.movie_style_btn.setObjectName("movie_style_btn")
        self.movie_style_btn.setCheckable(True)
        self.movie_style_btn.setProperty("role", "style")
        self.movie_style_btn.setIcon(QIcon(":/Graphics/Movie.png"))

        for btn in [
            self.classic_style_btn,
            self.colorful_style_btn,
            self.realistic_style_btn,
            self.soft_style_btn,
            self.movie_style_btn,
        ]:
            btn.setIconSize(QtCore.QSize(72, 72))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.StyleLayout.addWidget(btn)
        style_layout.addWidget(self.layoutWidget2)
        self.frame_layout.addWidget(self.StyleFrame)

        shadow_row = QHBoxLayout()
        shadow_row.setSpacing(12)

        self.ShadowFrame = self._section_frame(self.frame)
        shadow_layout = QVBoxLayout(self.ShadowFrame)
        shadow_layout.setContentsMargins(12, 10, 12, 10)
        shadow_layout.setSpacing(10)
        self.shadow_label = self._section_label("Shadow", self.ShadowFrame)
        shadow_layout.addWidget(self.shadow_label)
        self.layoutWidget_2 = QWidget(self.ShadowFrame)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.ShadowLayout = QHBoxLayout(self.layoutWidget_2)
        self.ShadowLayout.setContentsMargins(0, 0, 0, 0)
        self.ShadowLayout.setSpacing(8)
        self.disable_shadow_btn = QPushButton("Disable Shadow", self.layoutWidget_2)
        self.disable_shadow_btn.setObjectName("disable_shadow_btn")
        self.disable_shadow_btn.setCheckable(True)
        self.enable_shadow_btn = QPushButton("Enable Shadow", self.layoutWidget_2)
        self.enable_shadow_btn.setObjectName("enable_shadow_btn")
        self.enable_shadow_btn.setCheckable(True)
        self.ShadowLayout.addWidget(self.disable_shadow_btn)
        self.ShadowLayout.addWidget(self.enable_shadow_btn)
        shadow_layout.addWidget(self.layoutWidget_2)

        self.ResolutionkrFrame = self._section_frame(self.frame)
        res_layout = QVBoxLayout(self.ResolutionkrFrame)
        res_layout.setContentsMargins(12, 10, 12, 10)
        res_layout.setSpacing(10)
        self.resolution_label = self._section_label("Resolution PUBG KR", self.ResolutionkrFrame)
        self.resolution_btn = QPushButton("1080p", self.ResolutionkrFrame)
        self.resolution_btn.setObjectName("resolution_btn")
        self.resolution_btn.setCheckable(True)
        res_layout.addWidget(self.resolution_label)
        res_layout.addWidget(self.resolution_btn)

        shadow_row.addWidget(self.ShadowFrame, 3)
        shadow_row.addWidget(self.ResolutionkrFrame, 2)
        self.frame_layout.addLayout(shadow_row)

        page_layout.addWidget(self.frame, 1)

        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(12)

        self.PubgchooseFrame = self._section_frame(self.gfx_page)
        pubg_choose_layout = QVBoxLayout(self.PubgchooseFrame)
        pubg_choose_layout.setContentsMargins(10, 8, 10, 8)
        pubg_choose_layout.setSpacing(6)
        pubg_row = QHBoxLayout()
        self.pubgchoose_dropdown = QComboBox(self.PubgchooseFrame)
        self.pubgchoose_dropdown.setObjectName("pubgchoose_dropdown")
        self.pubgchoose_btn = QPushButton("Use", self.PubgchooseFrame)
        self.pubgchoose_btn.setObjectName("pubgchoose_btn")
        pubg_row.addWidget(self.pubgchoose_dropdown, 1)
        pubg_row.addWidget(self.pubgchoose_btn, 0)
        self.pubgchoose_label = QLabel("Select game version", self.PubgchooseFrame)
        self.pubgchoose_label.setObjectName("pubgchoose_label")
        pubg_choose_layout.addLayout(pubg_row)
        pubg_choose_layout.addWidget(self.pubgchoose_label)
        footer_layout.addWidget(self.PubgchooseFrame, 1)

        footer_layout.addStretch(1)

        self.connect_gameloop_btn = QPushButton("Connect to GameLoop", self.gfx_page)
        self.connect_gameloop_btn.setObjectName("connect_gameloop_btn")
        self.connect_gameloop_btn.setProperty("class", "action")
        self.connect_gameloop_btn.setProperty("id", "connectBtn")
        self.connect_gameloop_btn.setObjectName("connectBtn")
        self.connect_gameloop_btn.setCheckable(True)
        self.connect_gameloop_btn.setMinimumWidth(150)
        self.connect_gameloop_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.submit_gfx_btn = QPushButton("Submit Changes", self.gfx_page)
        self.submit_gfx_btn.setObjectName("submitBtn")
        self.submit_gfx_btn.setMinimumWidth(140)
        self.submit_gfx_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        footer_layout.addWidget(self.connect_gameloop_btn, 1)
        footer_layout.addWidget(self.submit_gfx_btn, 1)

        page_layout.addLayout(footer_layout)

    def _build_optimizer_page(self):
        self.other_page = QWidget()
        self.other_page.setObjectName("other_page")
        page_layout = QVBoxLayout(self.other_page)
        page_layout.setContentsMargins(14, 12, 14, 12)
        page_layout.setSpacing(10)

        top_grid = QHBoxLayout()
        top_grid.setSpacing(10)

        left_box = self._section_frame(self.other_page)
        left_layout = QVBoxLayout(left_box)
        left_layout.setContentsMargins(12, 10, 12, 10)
        left_layout.setSpacing(8)

        self.optimizer_label = self._section_label("PC Optimizer", left_box)
        left_layout.addWidget(self.optimizer_label)

        self.tempcleaner_other_btn = QPushButton("Temp Cleaner", left_box)
        self.tempcleaner_other_btn.setObjectName("tempcleaner_other_btn")
        left_layout.addWidget(self.tempcleaner_other_btn)

        self.gloptimizer_other_btn = QPushButton("Full Resource Boost", left_box)
        self.gloptimizer_other_btn.setObjectName("gloptimizer_other_btn")
        left_layout.addWidget(self.gloptimizer_other_btn)

        priority_row = QHBoxLayout()
        self.glpriority_dropdown = QComboBox(left_box)
        self.glpriority_dropdown.setObjectName("glpriority_dropdown")
        self.glpriority_dropdown.addItems(["High", "Realtime"])
        self.glcores_input = QLineEdit(left_box)
        self.glcores_input.setObjectName("glcores_input")
        self.glcores_input.setPlaceholderText("CPU Cores (Auto)")
        self.glcores_input.setClearButtonEnabled(True)
        self.glpriority_other_btn = QPushButton("Priority Boost", left_box)
        self.glpriority_other_btn.setObjectName("glpriority_other_btn")
        priority_row.addWidget(self.glpriority_other_btn, 2)
        priority_row.addWidget(self.glcores_input, 1)
        priority_row.addWidget(self.glpriority_dropdown, 1)
        left_layout.addLayout(priority_row)
        self.glcores_hint_label = QLabel("Leave empty for auto. Example: 10", left_box)
        self.glcores_hint_label.setObjectName("glcores_hint_label")
        self.glcores_hint_label.setStyleSheet("color: #8888aa; font-size: 11px;")
        left_layout.addWidget(self.glcores_hint_label)

        self.gllatency_other_btn = QPushButton("Latency Tweaks", left_box)
        self.gllatency_other_btn.setObjectName("gllatency_other_btn")
        left_layout.addWidget(self.gllatency_other_btn)

        self.fpsstabilizer_other_btn = QPushButton("FPS Stabilizer", left_box)
        self.fpsstabilizer_other_btn.setObjectName("fpsstabilizer_other_btn")
        left_layout.addWidget(self.fpsstabilizer_other_btn)

        engine_row = QHBoxLayout()
        self.engine_ini_mode_dropdown = QComboBox(left_box)
        self.engine_ini_mode_dropdown.setObjectName("engine_ini_mode_dropdown")
        self.engine_ini_mode_dropdown.addItems(["Competitive", "Balanced"])
        self.engine_ini_btn = QPushButton("Engine.ini Optimizer", left_box)
        self.engine_ini_btn.setObjectName("engine_ini_btn")
        engine_row.addWidget(self.engine_ini_btn, 2)
        engine_row.addWidget(self.engine_ini_mode_dropdown, 1)
        left_layout.addLayout(engine_row)

        self.headshot_tweaks_btn = QPushButton("Headshot Tweaks", left_box)
        self.headshot_tweaks_btn.setObjectName("headshot_tweaks_btn")
        left_layout.addWidget(self.headshot_tweaks_btn)

        exp_row = QHBoxLayout()
        self.experimental_fps_dropdown = QComboBox(left_box)
        self.experimental_fps_dropdown.setObjectName("experimental_fps_dropdown")
        self.experimental_fps_dropdown.addItems(["144fps [EXP]", "165fps [EXP]", "200fps [EXP]"])
        self.experimental_fps_btn = QPushButton("Experimental FPS", left_box)
        self.experimental_fps_btn.setObjectName("experimental_fps_btn")
        exp_row.addWidget(self.experimental_fps_btn, 2)
        exp_row.addWidget(self.experimental_fps_dropdown, 1)
        left_layout.addLayout(exp_row)

        self.experimental_fps_label = QLabel("? Experimental - may not work on all devices", left_box)
        self.experimental_fps_label.setObjectName("experimental_fps_label")
        self.experimental_fps_label.setStyleSheet("color: #ffaa44;")
        left_layout.addWidget(self.experimental_fps_label)

        self.all_other_btn = QPushButton("Apply ALL ??", left_box)
        self.all_other_btn.setObjectName("all_other_btn")
        left_layout.addWidget(self.all_other_btn)

        left_layout.addStretch(1)

        right_col = QVBoxLayout()
        right_col.setSpacing(10)

        network_box = self._section_frame(self.other_page)
        network_layout = QVBoxLayout(network_box)
        network_layout.setContentsMargins(12, 10, 12, 10)
        network_layout.setSpacing(8)
        self.dns_label = self._section_label("Network", network_box)
        network_layout.addWidget(self.dns_label)
        dns_row = QHBoxLayout()
        self.dns_dropdown = QComboBox(network_box)
        self.dns_dropdown.setObjectName("dns_dropdown")
        self.dns_dropdown.addItems([
            "Google DNS - 8.8.8.8",
            "Cloudflare DNS - 1.1.1.1",
            "Quad9 DNS - 9.9.9.9",
            "Cisco Umbrella - 208.67.222.222",
            "Yandex DNS - 77.88.8.1",
        ])
        self.dns_other_btn = QPushButton("Apply DNS", network_box)
        self.dns_other_btn.setObjectName("dns_other_btn")
        dns_row.addWidget(self.dns_dropdown, 2)
        dns_row.addWidget(self.dns_other_btn, 1)
        network_layout.addLayout(dns_row)
        self.dns_status_label = QLabel("Ping: --", network_box)
        self.dns_status_label.setObjectName("dns_status_label")
        network_layout.addWidget(self.dns_status_label)

        shortcut_box = self._section_frame(self.other_page)
        shortcut_layout = QVBoxLayout(shortcut_box)
        shortcut_layout.setContentsMargins(12, 10, 12, 10)
        shortcut_layout.setSpacing(8)
        self.shortcut_label = self._section_label("Game Shortcut", shortcut_box)
        shortcut_layout.addWidget(self.shortcut_label)
        shortcut_row = QHBoxLayout()
        self.shortcut_dropdown = QComboBox(shortcut_box)
        self.shortcut_dropdown.setObjectName("shortcut_dropdown")
        self.shortcut_dropdown.addItems([
            "PUBG Mobile Global",
            "PUBG Mobile VN",
            "PUBG Mobile TW",
            "PUBG Mobile KR",
            "Battlegrounds Mobile India",
        ])
        self.shortcut_other_btn = QPushButton("Create Desktop Icon", shortcut_box)
        self.shortcut_other_btn.setObjectName("shortcut_other_btn")
        shortcut_row.addWidget(self.shortcut_dropdown, 2)
        shortcut_row.addWidget(self.shortcut_other_btn, 1)
        shortcut_layout.addLayout(shortcut_row)

        right_col.addWidget(network_box)
        right_col.addWidget(shortcut_box)
        right_col.addStretch(1)

        top_grid.addWidget(left_box, 3)
        top_grid.addLayout(right_col, 2)
        page_layout.addLayout(top_grid, 1)

        ipad_box = self._section_frame(self.other_page)
        ipad_layout = QVBoxLayout(ipad_box)
        ipad_layout.setContentsMargins(12, 10, 12, 10)
        ipad_layout.setSpacing(8)
        self.ipad_label = self._section_label("iPad / Resolution", ipad_box)
        ipad_layout.addWidget(self.ipad_label)

        ipad_row = QHBoxLayout()
        self.ipad_dropdown = QComboBox(ipad_box)
        self.ipad_dropdown.setObjectName("ipad_dropdown")
        self.ipad_dropdown.addItems(["Smart 720P", "Smart 1080P", "Smart 2K", "Custom"])
        self.ipad_other_btn = QPushButton("Apply", ipad_box)
        self.ipad_other_btn.setObjectName("ipad_other_btn")
        self.ipad_rest_btn = QPushButton("Reset", ipad_box)
        self.ipad_rest_btn.setObjectName("ipad_rest_btn")
        ipad_row.addWidget(self.ipad_dropdown, 2)
        ipad_row.addWidget(self.ipad_other_btn, 1)
        ipad_row.addWidget(self.ipad_rest_btn, 1)
        ipad_layout.addLayout(ipad_row)

        self.ipad_code = QLineEdit(ipad_box)
        self.ipad_code.setObjectName("ipad_code")
        self.ipad_code.setReadOnly(True)
        self.ipad_code_label = QLabel("Current Code", ipad_box)
        self.ipad_code_label.setObjectName("ipad_code_label")
        ipad_layout.addWidget(self.ipad_code_label)
        ipad_layout.addWidget(self.ipad_code)

        page_layout.addWidget(ipad_box)

        self.forceclosegl_other_btn = QPushButton("Force Close GameLoop", self.other_page)
        self.forceclosegl_other_btn.setObjectName("forceCloseBtn")
        page_layout.addWidget(self.forceclosegl_other_btn)

        self.line = QFrame(self.other_page)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.NoFrame)

    def _build_about_page(self):
        self.about_page = QWidget()
        self.about_page.setObjectName("about_page")
        layout = QVBoxLayout(self.about_page)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        header_card = QFrame(self.about_page)
        header_card.setObjectName("aboutHeaderCard")
        header_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(20, 18, 20, 18)
        header_layout.setSpacing(4)

        self.about_title_label = QLabel("EX Tool v0.2", header_card)
        self.about_title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Segoe UI", 16)
        title_font.setBold(True)
        self.about_title_label.setFont(title_font)

        self.about_subtitle_label = QLabel("PUBG Mobile GameLoop Optimizer", header_card)
        self.about_subtitle_label.setAlignment(Qt.AlignCenter)

        self.about_link_label = QLabel("github.com/saadaliadalat", header_card)
        self.about_link_label.setAlignment(Qt.AlignCenter)
        self.about_link_label.setStyleSheet("color: #e94560;")

        header_layout.addWidget(self.about_title_label)
        header_layout.addWidget(self.about_subtitle_label)
        header_layout.addWidget(self.about_link_label)
        layout.addWidget(header_card)

        features_card = QFrame(self.about_page)
        features_card.setObjectName("aboutFeaturesCard")
        features_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        features_layout = QVBoxLayout(features_card)
        features_layout.setContentsMargins(16, 14, 16, 14)
        features_layout.setSpacing(8)

        section_title = self._section_label("What This Tool Does", features_card)
        features_layout.addWidget(section_title)

        feature_grid = QGridLayout()
        feature_grid.setContentsMargins(0, 0, 0, 0)
        feature_grid.setHorizontalSpacing(14)
        feature_grid.setVerticalSpacing(2)

        feature_rows = [
            ("GFX Unlocker", "Unlock Extreme HDR, Ultra HD, and locked graphics settings."),
            ("PC Optimizer", "Allocate more RAM/CPU to GameLoop and apply priority tweaks."),
            ("Headshot Tools", "Engine.ini optimization for sharper textures and visibility."),
            ("Network", "DNS changer and ping optimization for stable networking."),
            ("Resolution", "iPad view and custom resolution options for wider FOV."),
            ("FPS Tweaks", "Service and timer optimizations for smoother frame pacing."),
        ]

        for row, (name, description) in enumerate(feature_rows):
            name_label = QLabel(name, features_card)
            name_label.setObjectName("aboutFeatureName")
            desc_label = QLabel(description, features_card)
            desc_label.setObjectName("aboutFeatureDesc")
            desc_label.setWordWrap(True)
            feature_grid.addWidget(name_label, row, 0)
            feature_grid.addWidget(desc_label, row, 1)

        feature_grid.setColumnStretch(0, 1)
        feature_grid.setColumnStretch(1, 3)
        features_layout.addLayout(feature_grid)
        layout.addWidget(features_card, 1)

        links_row = QHBoxLayout()
        links_row.setSpacing(10)
        links_row.addStretch(1)
        self.github_btn = QPushButton("GitHub", self.about_page)
        self.github_btn.setObjectName("github_btn")
        self.report_bug_btn = QPushButton("Report Bug", self.about_page)
        self.report_bug_btn.setObjectName("report_bug_btn")
        self.discord_btn = QPushButton("Discord", self.about_page)
        self.discord_btn.setObjectName("discord_btn")
        links_row.addWidget(self.github_btn)
        links_row.addWidget(self.report_bug_btn)
        links_row.addWidget(self.discord_btn)
        links_row.addStretch(1)
        layout.addLayout(links_row)

        self.about_footer_label = QLabel("v0.2  -  All settings are reversible  -  No bans", self.about_page)
        self.about_footer_label.setAlignment(Qt.AlignCenter)
        self.about_footer_label.setStyleSheet("color: #aaaaaa;")
        layout.addWidget(self.about_footer_label)

        self.label_8 = QLabel(self.about_page)
        self.label_8.hide()

    def _build_status_bar(self):
        self.statusBarFrame = QFrame(self.centralwidget)
        self.statusBarFrame.setObjectName("statusBar")
        s_layout = QHBoxLayout(self.statusBarFrame)
        s_layout.setContentsMargins(10, 6, 10, 6)
        s_layout.setSpacing(8)

        self.appstatus_label = QLabel("Status:", self.statusBarFrame)
        self.appstatus_label.setObjectName("appstatus_label")
        self.appstatus_text_lable = QLabel("? Ready", self.statusBarFrame)
        self.appstatus_text_lable.setObjectName("appstatus_text_lable")

        s_layout.addWidget(self.appstatus_label)
        s_layout.addWidget(self.appstatus_text_lable, 1)
        self.rootLayout.addWidget(self.statusBarFrame)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("EX Tool v0.2")
        self.appname_label.setText("EX Tool v0.2")
        self.gfx_button.setText("GFX")
        self.other_button.setText("OPTIMIZER")
        self.about_button.setText("ABOUT")
        self.connection_banner_label.setText("Connect to GameLoop first to enable settings")

