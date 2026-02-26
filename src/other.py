import ping3
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import re
from . import setup_logger


class IPADWorkerThread(QThread):
    task_completed = pyqtSignal()

    def __init__(self, window, ui, gfx):
        super(IPADWorkerThread, self).__init__()
        self.app = window
        self.ui = ui
        self.gfx = gfx

    def run(self):
        width, height = self.extract_dimensions(self.ui.ipad_dropdown.currentText())
        self.app.ipad_settings(width, height)
        self.task_completed.emit()

    @staticmethod
    def extract_dimensions(string):
        pattern = r'(\d+)\s*x\s*(\d+)'
        match = re.search(pattern, string)

        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            return width, height
        else:
            return None


class Other(QObject):
    def __init__(self, window):
        super(Other, self).__init__()
        from .ui import Ui_MainWindow
        from .ui_functions import Window
        self.ui: Ui_MainWindow = window.ui
        self.app: Window = window
        self.dns_servers = {
            "Google DNS - 8.8.8.8": ['8.8.8.8', '8.8.4.4'],
            "Cloudflare DNS - 1.1.1.1": ['1.1.1.1', '1.0.0.1'],
            "Quad9 DNS - 9.9.9.9": ['9.9.9.9', '149.112.112.112'],
            "Cisco Umbrella - 208.67.222.222": ['208.67.222.222', '208.67.220.220'],
            "Yandex DNS - 77.88.8.1": ['77.88.8.1', '77.88.8.8']
        }
        self.function()
        self.logger = setup_logger('error_logger', 'error.log')

    def function(self):
        ui = self.ui

        ui.tempcleaner_other_btn.clicked.connect(self.temp_cleaner_button_click)
        ui.gloptimizer_other_btn.clicked.connect(self.gameloop_optimizer_button_click)
        ui.glpriority_other_btn.clicked.connect(self.gameloop_priority_button_click)
        ui.gllatency_other_btn.clicked.connect(self.gameloop_latency_button_click)
        ui.fpsstabilizer_other_btn.clicked.connect(self.fps_stabilizer_button_click)
        ui.engine_ini_btn.clicked.connect(self.engine_ini_button_click)
        ui.headshot_tweaks_btn.clicked.connect(self.headshot_tweaks_button_click)
        ui.experimental_fps_btn.clicked.connect(self.experimental_fps_button_click)
        ui.all_other_btn.clicked.connect(self.all_recommended_button_click)
        ui.forceclosegl_other_btn.clicked.connect(self.kill_gameloop_processes_button_click)
        ui.shortcut_other_btn.clicked.connect(self.shortcut_submit_button_click)
        ui.dns_dropdown.currentTextChanged.connect(self.dns_dropdown)
        ui.dns_other_btn.clicked.connect(self.dns_submit_button_click)
        ui.ipad_other_btn.clicked.connect(self.ipad_submit_button_click)
        ui.ipad_rest_btn.clicked.connect(self.ipad_reset_button_click)

        saved_cores = str(self.app.settings.value("GLCustomCpuCores", "") or "").strip()
        if saved_cores:
            ui.glcores_input.setText(saved_cores)

        ui.ipad_code.hide()
        ui.ipad_code_label.hide()

        _width = self.app.settings.value("VMResWidth")
        _height = self.app.settings.value("VMResHeight")

        if _width is None or _height is None:
            ui.ipad_rest_btn.hide()

    def _handle_error(self, e, user_message="Operation failed. Check error.log for details."):
        self.logger.error(f"Exception occurred: {str(e)}", exc_info=True)
        self.app.show_status_message(user_message, msg_type="error")

    def _require_adb(self):
        if not self.app.is_adb_working:
            self.app.show_status_message("Connect to GameLoop first.", 4, "warning")
            return False
        if not getattr(self.app, "pubg_package", None):
            self.app.show_status_message("Select PUBG version first.", 4, "warning")
            return False
        return True

    def _parse_custom_cores(self):
        raw_value = self.ui.glcores_input.text().strip()
        if not raw_value:
            self.app.settings.setValue("GLCustomCpuCores", "")
            return None
        if not raw_value.isdigit():
            self.app.show_status_message("CPU cores must be a positive whole number.", 5, "warning")
            return "invalid"
        cores = int(raw_value)
        if cores < 1:
            self.app.show_status_message("CPU cores must be at least 1.", 5, "warning")
            return "invalid"
        if cores > 0xFFFFFFFF:
            self.app.show_status_message("CPU cores value is too large.", 5, "warning")
            return "invalid"
        self.app.settings.setValue("GLCustomCpuCores", str(cores))
        return cores

    @staticmethod
    def _detect_gpu_provider():
        gpu_provider = ""
        try:
            import wmi
            controllers = wmi.WMI().Win32_VideoController()
            if controllers:
                gpu_provider = controllers[0].AdapterCompatibility or ""
        except Exception:
            pass
        return gpu_provider

    def _apply_gpu_optimization(self):
        gpu_provider = self._detect_gpu_provider()
        if "NVIDIA" in gpu_provider:
            self.app.optimize_for_nvidia()
        elif "AMD" in gpu_provider or "Radeon" in gpu_provider:
            self.app.optimize_for_amd()

    def temp_cleaner_button_click(self, e):
        """ Temp Cleaner Button On Click Function """
        try:
            self.app.temp_cleaner()
            self.app.show_status_message("System performance improved.", msg_type="success")
        except Exception as e:
            self._handle_error(e)

    def gameloop_optimizer_button_click(self, e):
        """ Full Resource Boost Button On Click Function """
        try:
            target_cores = self._parse_custom_cores()
            if target_cores == "invalid":
                return
            self.app.add_to_windows_defender_exclusion()
            self.app.optimize_gameloop_registry()
            self._apply_gpu_optimization()
            ram_mb, cpu_cores, boosted = self.app.apply_full_resource_boost(target_cores=target_cores)
            self.app.show_status_message(
                f"GameLoop fully optimized: {ram_mb // 1024}GB RAM, {cpu_cores} cores, {boosted} processes.",
                6,
                "success",
            )
        except Exception as e:
            self._handle_error(e)

    def gameloop_priority_button_click(self, e):
        """ Gameloop Priority Boost Button On Click Function """
        try:
            target_cores = self._parse_custom_cores()
            if target_cores == "invalid":
                return
            priority_value = self.ui.glpriority_dropdown.currentText().lower()
            ram_mb, cpu_cores = self.app.force_gameloop_resource_allocation(target_cores=target_cores)
            boosted, applied_requested = self.app.boost_gameloop_priority(
                priority=priority_value,
                target_cores=target_cores,
            )
            if boosted:
                message = (
                    f"Gameloop boosted ({priority_value}): {cpu_cores} CPU cores, {ram_mb}MB RAM, "
                    f"{boosted} processes."
                )
                if not applied_requested:
                    message += " Some processes may need admin rights."
            else:
                message = f"Resource allocation updated ({priority_value}): {cpu_cores} CPU cores, {ram_mb}MB RAM."
                if not self.app.is_gameloop_running():
                    message += " Start Gameloop to apply priority boost."
            self.app.show_status_message(message, msg_type="success")
        except Exception as e:
            self._handle_error(e)

    def gameloop_latency_button_click(self, e):
        """ Gameloop Latency Tweaks Button On Click Function """
        try:
            applied = self.app.apply_latency_tweaks()
            if applied:
                message = "Latency tweaks applied. Restart Windows for full effect."
            else:
                message = "Latency tweaks failed. Try running as admin."
            self.app.show_status_message(message, msg_type="success" if applied else "warning")
        except Exception as e:
            self._handle_error(e)

    def fps_stabilizer_button_click(self, e):
        """ FPS Stabilizer Button On Click Function """
        try:
            self.app.apply_fps_stabilizer()
            self.app.show_status_message("FPS Stabilizer applied. Restart Windows for full effect.", msg_type="success")
        except Exception as e:
            self._handle_error(e)

    def engine_ini_button_click(self, e):
        try:
            if not self._require_adb():
                return
            mode = self.ui.engine_ini_mode_dropdown.currentText().strip().lower()
            mode = "competitive" if mode not in {"competitive", "balanced"} else mode
            self.app.push_engine_ini(mode=mode)
            self.app.show_status_message(f"Engine.ini optimized ({mode}).", msg_type="success")
        except Exception as ex:
            self._handle_error(ex)

    def headshot_tweaks_button_click(self, e):
        try:
            if not self._require_adb():
                return
            self.app.push_engine_ini(mode="competitive")
            dpi = self.app.set_high_dpi_rendering(560)
            self.app.show_status_message(f"Headshot tweaks applied. DPI set to {dpi}.", msg_type="success")
        except Exception as ex:
            self._handle_error(ex)

    def experimental_fps_button_click(self, e):
        try:
            if not self._require_adb():
                return
            if not getattr(self.app, "pubg_package", None):
                self.app.show_status_message("Select and connect PUBG version first.", 5, "warning")
                return
            choice = self.ui.experimental_fps_dropdown.currentText().strip()
            applied = self.app.set_fps_experimental(choice)
            if not applied:
                self.app.show_status_message("Experimental FPS value is invalid.", 5, "warning")
                return
            self.app.save_graphics_file()
            self.app.push_active_shadow_file()
            self.app.start_app()
            self.app.show_status_message(f"Applied {choice}. This is experimental.", 6, "warning")
        except Exception as ex:
            self._handle_error(ex)

    def all_recommended_button_click(self, e):
        """ All Recommended Button On Click Function """
        try:
            target_cores = self._parse_custom_cores()
            if target_cores == "invalid":
                return
            self.app.temp_cleaner()
            self.app.add_to_windows_defender_exclusion()
            self.app.optimize_gameloop_registry()
            self._apply_gpu_optimization()
            self.app.apply_full_resource_boost(target_cores=target_cores)
            self.app.apply_latency_tweaks()
            self.app.apply_fps_stabilizer()
            if self.app.is_adb_working:
                self.app.push_engine_ini(mode="competitive")
                self.app.set_high_dpi_rendering(560)
            self.app.show_status_message(
                "All optimizations applied! Restart GameLoop for full effect.",
                7,
                "success",
            )
        except Exception as e:
            self._handle_error(e)

    def kill_gameloop_processes_button_click(self, e):
        """Terminates Gameloop processes when the button is clicked."""
        try:
            if self.app.kill_gameloop():
                message = "All Gameloop processes terminated."
            else:
                message = "No processes found to terminate."
            self.app.show_status_message(message, msg_type="warning")
        except Exception as ex:
            self._handle_error(ex)

    def shortcut_submit_button_click(self, e):
        """ Shortcut Submit Button On Click Function """
        try:
            version_value = self.ui.shortcut_dropdown.currentText()
            self.app.gen_game_icon(version_value)
            self.app.show_status_message("Shortcut generated successfully.", msg_type="success")
        except Exception as ex:
            self._handle_error(ex)

    def dns_submit_button_click(self, e):
        """ DNS Submit Button On Click Function """
        try:
            dns_key = self.ui.dns_dropdown.currentText()
            dns_server = self.dns_servers.get(dns_key)

            if dns_server and self.app.change_dns_servers(dns_server):
                self.dns_dropdown(dns_key)
                self.app.show_status_message("DNS server changed successfully.", msg_type="success")
            else:
                self.app.show_status_message("Could not change DNS server.", msg_type="warning")
        except Exception as ex:
            self._handle_error(ex)

    def dns_dropdown(self, value):
        try:
            server, _ = self.dns_servers[value]
            pings = [ping3.ping(server, timeout=1, unit='ms', size=56) or float('inf') for _ in range(5)]
            lowest_ping = min(pings)
            if lowest_ping != float('inf'):
                ping_result = f"{str(value).split(' -')[0]} Ping: {int(lowest_ping)}ms"
            else:
                ping_result = "No response from DNS servers"
            self.ui.dns_status_label.setText(ping_result)
        except Exception:
            self.ui.dns_status_label.setText("Ping check unavailable.")

    def ipad_submit_button_click(self, e):
        try:
            if self.app.is_gameloop_running():
                self.app.show_status_message(f"Close Gameloop to use this button. (Force Close Gameloop)", 5, "warning")
                return
            self.app.show_status_message("Please wait, working on it...", 15)
            self.ui.ipad_other_btn.setEnabled(False)
            self.ui.ipad_rest_btn.setEnabled(False)
            self.worker_ipad_submit = IPADWorkerThread(self.app, self.ui, self)
            self.worker_ipad_submit.task_completed.connect(self.submit_ipad_done)
            self.worker_ipad_submit.start()
        except Exception as ex:
            self._handle_error(ex, "Invalid iPad settings values.")

    def submit_ipad_done(self):
        try:
            self.ui.ipad_other_btn.setEnabled(True)
            self.ui.ipad_rest_btn.setEnabled(True)
            self.ui.ipad_rest_btn.show()
            gameloop_status = "Restart" if self.app.is_gameloop_running() else "Start"
            self.app.show_status_message(f"{gameloop_status} Gameloop and enjoy with iPad settings.", 7, "success")
        except Exception as ex:
            self._handle_error(ex)

    def ipad_reset_button_click(self, e):
        try:
            if self.app.is_gameloop_running():
                self.app.show_status_message(
                    "Close Gameloop to use this button. (Force Close Gameloop)", 5, "warning"
                )
                return

            width, height = self.app.reset_ipad()
            self.ui.ipad_rest_btn.hide()

            message = f"Start Gameloop to Utilize Resolution ({width} x {height})."
            self.app.show_status_message(message, 7, "success")
        except Exception as ex:
            self._handle_error(ex)
