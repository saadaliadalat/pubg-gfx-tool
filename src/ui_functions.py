from PyQt5 import QtCore, QtGui, QtWidgets

from .app_functions import Game
from .gfx import GFX
from .other import Other
from .ui import Ui_MainWindow


class Window(QtWidgets.QMainWindow, Game):
    def __init__(self, app_name, app_version):
        super().__init__()
        self.app_name = app_name
        self.app_version = app_version
        self.timer = None
        self._drag_start_position = None
        self._drag_origin = None

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(1280, 800)
        self.resize(1280, 800)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.appname_label.setText(f"{app_name} {app_version}")

        self._wire_core_ui()

        # Restore preferred zoom and center window.
        self._base_font_size = 10.0
        self._base_width = 1280
        self._base_height = 800
        zoom = float(self.settings.value("ui_zoom", 1.0))
        self.apply_zoom(zoom, save=False)
        self._center_on_screen()

        self.GFX = GFX(self)
        self.Other = Other(self)

        self.set_adb_buttons_state(False)
        self.show_status_message("Ready", msg_type="info")

    def _wire_core_ui(self):
        self.ui.gfx_button.clicked.connect(lambda: self.buttonClicked(self.ui.gfx_button, self.ui.gfx_page))
        self.ui.other_button.clicked.connect(lambda: self.buttonClicked(self.ui.other_button, self.ui.other_page))
        self.ui.about_button.clicked.connect(lambda: self.buttonClicked(self.ui.about_button, self.ui.about_page))

        self.ui.close_btn.clicked.connect(self.close)
        self.ui.minimize_btn.clicked.connect(lambda: self.setWindowState(QtCore.Qt.WindowMinimized))

        self.ui.zoom75_btn.clicked.connect(lambda: self.apply_zoom(0.75))
        self.ui.zoom100_btn.clicked.connect(lambda: self.apply_zoom(1.0))
        self.ui.zoom125_btn.clicked.connect(lambda: self.apply_zoom(1.25))
        for btn in [self.ui.zoom75_btn, self.ui.zoom100_btn, self.ui.zoom125_btn]:
            btn.setCheckable(True)

        self.ui.github_btn.clicked.connect(
            lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/"))
        )
        self.ui.report_bug_btn.clicked.connect(
            lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/issues"))
        )
        self.ui.discord_btn.clicked.connect(
            lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://discord.com/"))
        )

    def _center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        x = screen.x() + (screen.width() - self.width()) // 2
        y = screen.y() + (screen.height() - self.height()) // 2
        self.move(x, y)

    def buttonClicked(self, button, page):
        self.ui.gfx_button.setChecked(button == self.ui.gfx_button)
        self.ui.other_button.setChecked(button == self.ui.other_button)
        self.ui.about_button.setChecked(button == self.ui.about_button)
        self.ui.stackedWidget.setCurrentWidget(page)

    def apply_zoom(self, factor, save=True):
        """Scale UI for different screens."""
        factor = max(0.75, min(1.25, float(factor)))

        font = self.font()
        font.setPointSizeF(self._base_font_size * factor)
        self.setFont(font)

        width = int(self._base_width * factor)
        height = int(self._base_height * factor)
        self.resize(max(1280, width), max(800, height))

        if save:
            self.settings.setValue("ui_zoom", factor)

        self.ui.zoom75_btn.setChecked(abs(factor - 0.75) < 0.01)
        self.ui.zoom100_btn.setChecked(abs(factor - 1.0) < 0.01)
        self.ui.zoom125_btn.setChecked(abs(factor - 1.25) < 0.01)

    def show_status_message(self, message, duration=5, msg_type="info"):
        """Enhanced status with color coding."""
        colors = {
            "info": "#888888",
            "success": "#44ff44",
            "error": "#ff4444",
            "warning": "#ffaa44",
        }
        color = colors.get(msg_type, "#888888")
        self.ui.appstatus_text_lable.setStyleSheet(f"color: {color};")
        self.ui.appstatus_text_lable.setText(f"? {message}")

        if self.timer and self.timer.isActive():
            self.timer.stop()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.ui.appstatus_text_lable.setText("? Ready"))
        self.timer.start(duration * 1000)

    def set_adb_buttons_state(self, connected: bool):
        adb_required = [
            "engine_ini_btn",
            "engine_ini_mode_dropdown",
            "headshot_tweaks_btn",
            "experimental_fps_btn",
            "experimental_fps_dropdown",
            "submit_gfx_btn",
            "smooth_graphics_btn",
            "balanced_graphics_btn",
            "hd_graphics_btn",
            "hdr_graphics_btn",
            "ultrahd_graphics_btn",
            "uhd_graphics_btn",
            "low_fps_btn",
            "medium_fps_btn",
            "high_fps_btn",
            "ultra_fps_btn",
            "extreme_fps_btn",
            "fps90_fps_btn",
            "fps120_fps_btn",
            "classic_style_btn",
            "colorful_style_btn",
            "realistic_style_btn",
            "soft_style_btn",
            "movie_style_btn",
            "disable_shadow_btn",
            "enable_shadow_btn",
            "beast_mode_btn",
            "competitive_mode_btn",
            "streamer_mode_btn",
        ]

        for widget_name in adb_required:
            btn = getattr(self.ui, widget_name, None)
            if btn:
                btn.setEnabled(connected)
                if not connected:
                    btn.setToolTip("Connect to GameLoop first")
                else:
                    btn.setToolTip("")

        self.ui.connection_banner_label.setVisible(not connected)

    def _is_on_titlebar(self, pos):
        return self.ui.titleBar.geometry().contains(pos)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self._is_on_titlebar(event.pos()):
            self._drag_start_position = event.globalPos()
            self._drag_origin = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_start_position is None:
            return
        if event.buttons() & QtCore.Qt.LeftButton:
            delta = event.globalPos() - self._drag_start_position
            self.move(self._drag_origin + delta)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_start_position = None
            self._drag_origin = None
