from PyQt5.QtCore import QThread, pyqtSignal
from typing import Optional, List
import ping3

from .adb_manager import AdbManager
from .graphics import GraphicsManager
from .optimizer import SystemOptimizer, OptimizationResult

class ConnectWorker(QThread):
    """Background worker for ADB port scan & GameLoop connection."""
    finished = pyqtSignal(bool, str, list)

    def __init__(self, adb_mgr: AdbManager):
        super().__init__()
        self.adb_mgr = adb_mgr

    def run(self):
        success, msg = self.adb_mgr.connect()
        installed_versions = []
        if success:
            installed_versions = self.adb_mgr.detect_installed_pubg_versions()
        self.finished.emit(success, msg, installed_versions)


class SubmitGfxWorker(QThread):
    """Background worker for saving & pushing GFX settings to GameLoop."""
    finished = pyqtSignal(bool, str)

    def __init__(self, gfx_mgr: GraphicsManager, adb_mgr: AdbManager, 
                 quality: str, fps: str, style: str, disable_shadow: bool,
                 restart_game: bool = True):
        super().__init__()
        self.gfx_mgr = gfx_mgr
        self.adb_mgr = adb_mgr
        self.quality = quality
        self.fps = fps
        self.style = style
        self.disable_shadow = disable_shadow
        self.restart_game = restart_game

    def run(self):
        if not self.adb_mgr.is_connected or not self.adb_mgr.device:
            self.finished.emit(False, "Not connected to GameLoop.")
            return

        try:
            self.gfx_mgr.set_graphics_quality(self.quality)
            self.gfx_mgr.set_fps(self.fps)
            self.gfx_mgr.set_style(self.style)
            self.gfx_mgr.save_graphics_file()
            
            pushed_gfx = self.gfx_mgr.push_graphics_to_device(self.adb_mgr.device)
            pushed_shadow = self.gfx_mgr.push_shadow_config(self.adb_mgr.device, self.disable_shadow)

            if self.restart_game:
                self.gfx_mgr.restart_pubg(self.adb_mgr.device)

            if pushed_gfx:
                self.finished.emit(True, "Graphics settings applied successfully!")
            else:
                self.finished.emit(False, "Failed to push graphics file to GameLoop.")
        except Exception as e:
            self.finished.emit(False, f"Error applying graphics: {e}")


class SystemOptimizeWorker(QThread):
    """Background worker for system / GameLoop optimizations."""
    finished = pyqtSignal(bool, str)

    def __init__(self, action_name: str, optimizer: SystemOptimizer, target_cores: Optional[int] = None):
        super().__init__()
        self.action_name = action_name
        self.optimizer = optimizer
        self.target_cores = target_cores

    def run(self):
        try:
            if self.action_name == "temp_cleaner":
                res = self.optimizer.temp_cleaner()
            elif self.action_name == "full_boost":
                self.optimizer.add_defender_exclusion()
                self.optimizer.optimize_gameloop_registry()
                res = self.optimizer.apply_full_resource_boost(target_cores=self.target_cores)
            elif self.action_name == "latency_tweaks":
                res = self.optimizer.apply_latency_tweaks()
            elif self.action_name == "fps_stabilizer":
                res = self.optimizer.apply_fps_stabilizer()
            elif self.action_name == "apply_all":
                self.optimizer.temp_cleaner()
                self.optimizer.add_defender_exclusion()
                self.optimizer.optimize_gameloop_registry()
                self.optimizer.apply_latency_tweaks()
                self.optimizer.apply_fps_stabilizer()
                res = self.optimizer.apply_full_resource_boost(target_cores=self.target_cores)
            else:
                res = OptimizationResult(False, "Unknown optimization action.")

            self.finished.emit(res.success, res.message)
        except Exception as e:
            self.finished.emit(False, f"Optimization error: {e}")


class PingWorker(QThread):
    """Background worker for testing DNS ping latency."""
    finished = pyqtSignal(str, int)

    def __init__(self, dns_name: str, primary_ip: str):
        super().__init__()
        self.dns_name = dns_name
        self.primary_ip = primary_ip

    def run(self):
        try:
            pings = [ping3.ping(self.primary_ip, timeout=1, unit='ms', size=56) or float('inf') for _ in range(3)]
            valid = [p for p in pings if p != float('inf')]
            if valid:
                self.finished.emit(self.dns_name, int(min(valid)))
            else:
                self.finished.emit(self.dns_name, -1)
        except Exception:
            self.finished.emit(self.dns_name, -1)
