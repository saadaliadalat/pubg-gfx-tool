import subprocess
import time
import psutil
import adbutils
from typing import Optional, List, Tuple
from .constants import GAMELOOP_PROCESSES, PUBG_VERSIONS

class AdbManager:
    """Manages ADB bridge connections to GameLoop emulator cleanly and reliably."""

    def __init__(self):
        self.device: Optional[adbutils.AdbDevice] = None
        self.is_connected: bool = False

    @staticmethod
    def kill_adb() -> bool:
        try:
            subprocess.run(["taskkill", "/F", "/IM", "adb.exe"], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            return True
        except Exception:
            return False

    @staticmethod
    def is_gameloop_running() -> bool:
        target_names = {p.lower() for p in GAMELOOP_PROCESSES}
        for proc in psutil.process_iter(['name']):
            try:
                pname = (proc.info.get('name') or '').lower()
                if pname in target_names or 'aow_exe' in pname or 'androidemulator' in pname:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def connect(self) -> Tuple[bool, str]:
        """
        Scans GameLoop ports and connects to active ADB interface.
        Returns (success: bool, message: str).
        """
        self.is_connected = False
        self.device = None

        if not self.is_gameloop_running():
            return False, "GameLoop is not currently running. Please start GameLoop first."

        # Start adb server if needed
        try:
            client = adbutils.AdbClient(host="127.0.0.1", port=5037)
        except Exception as e:
            return False, f"Failed to initialize ADB client: {e}"

        # Dynamic port discovery from GameLoop processes
        ports = [5555, 5554, 5565, 5575, 11223, 55555]
        try:
            target_proc_names = {'androidemulatorex.exe', 'androidemulatoren.exe', 'androidemulator.exe', 'aow_exe.exe', 'aow.exe'}
            for proc in psutil.process_iter(['name']):
                pname = (proc.info.get('name') or '').lower()
                if pname in target_proc_names:
                    try:
                        for conn in proc.net_connections(kind='inet'):
                            if conn.status == psutil.CONN_LISTEN and conn.laddr and conn.laddr.port:
                                p = conn.laddr.port
                                if p not in ports:
                                    ports.insert(0, p)
                    except Exception:
                        pass
        except Exception:
            pass

        # Try to find an existing device in adb device list first
        connected_device = None
        try:
            devices = client.device_list()
            for dev in devices:
                if self._verify_device(dev):
                    connected_device = dev
                    break
        except Exception:
            pass

        # Try connecting to discovered ports if no active device was verified
        if not connected_device:
            for port in ports:
                try:
                    client.connect(f"127.0.0.1:{port}", timeout=2.0)
                    for dev in client.device_list():
                        if self._verify_device(dev):
                            connected_device = dev
                            break
                    if connected_device:
                        break
                except Exception:
                    pass

        if connected_device and self._verify_device(connected_device):
            self.device = connected_device
            self.is_connected = True
            serial = getattr(connected_device, 'serial', 'GameLoop ADB')
            return True, f"Successfully connected to GameLoop ({serial})"
        else:
            self.kill_adb()
            return False, "Could not establish ADB connection with GameLoop. Ensure ADB is enabled."

    def _verify_device(self, dev: adbutils.AdbDevice) -> bool:
        """Helper to test if an ADB device actually responds to commands."""
        try:
            out = str(dev.shell("echo 1", timeout=3.0)).strip()
            return out == "1"
        except Exception:
            return False

    def detect_installed_pubg_versions(self) -> List[str]:
        """Returns list of installed PUBG package display names found on the device."""
        if not self.is_connected or not self.device:
            return []

        installed = []
        try:
            # Query installed packages via pm list packages
            pm_out = self.device.shell("pm list packages")
            installed_packages = set(line.replace("package:", "").strip() for line in pm_out.splitlines() if "package:" in line)
            
            for pkg, name in PUBG_VERSIONS.items():
                if pkg in installed_packages:
                    installed.append(name)
        except Exception:
            # Fallback check via ls /data/data/
            for pkg, name in PUBG_VERSIONS.items():
                try:
                    res = self.device.shell(f"ls /data/data/{pkg}")
                    if "No such file" not in res and res.strip():
                        installed.append(name)
                except Exception:
                    pass
        return installed
