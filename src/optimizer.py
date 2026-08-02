import os
import sys
import shutil
import tempfile
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple
import psutil

from .constants import GAMELOOP_PROCESSES, get_app_data_dir
from .registry import RegistryManager

@dataclass
class OptimizationResult:
    success: bool
    message: str

def resource_path(relative_path: str) -> str:
    """Get path to bundled or standalone asset (PyInstaller compatible)."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base_path, relative_path)

class SystemOptimizer:
    """Provides system, registry, network, and GameLoop process optimizations."""

    def temp_cleaner(self) -> OptimizationResult:
        def clear_dir(path: str):
            try:
                if not os.path.exists(path):
                    return
                for entry in os.scandir(path):
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            shutil.rmtree(entry.path, ignore_errors=True)
                        else:
                            os.remove(entry.path)
                    except Exception:
                        pass
            except Exception:
                pass

        clear_dir(tempfile.gettempdir())
        clear_dir(r"C:\Windows\Temp")
        clear_dir(os.path.expandvars(r"%windir%\Prefetch"))

        # Clear GameLoop shader cache
        try:
            gameloop_ui_path = RegistryManager.get_local_reg('InstallPath', path='UI')
            if gameloop_ui_path:
                clear_dir(os.path.join(str(gameloop_ui_path), 'ShaderCache'))
        except Exception:
            pass

        # Memory working sets cleanup & Garbage collection
        try:
            subprocess.run(
                ["powershell", "-Command", "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False
            )
            subprocess.run(
                ["powershell", "-Command",
                 "Get-Process | Where-Object {$_.WorkingSet -gt 50MB} | ForEach-Object { $_.MinWorkingSet = 1MB }"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10, check=False
            )
        except Exception:
            pass

        # Flush DNS cache
        subprocess.run(["ipconfig", "/flushdns"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return OptimizationResult(True, "Temporary files and shader cache cleaned successfully.")

    def add_defender_exclusion(self) -> OptimizationResult:
        try:
            install_path = RegistryManager.get_local_reg("InstallPath")
            if not install_path:
                return OptimizationResult(False, "GameLoop installation path not found in registry.")
            gameloop_path = os.path.dirname(str(install_path))
            cmd = ["powershell", "-Command", f"Add-MpPreference -ExclusionPath '{gameloop_path}' -Force"]
            subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return OptimizationResult(True, f"Added Defender exclusion: {gameloop_path}")
        except Exception as e:
            return OptimizationResult(False, f"Defender exclusion error: {e}")

    def optimize_gameloop_registry(self) -> OptimizationResult:
        try:
            install_path = RegistryManager.get_local_reg("InstallPath", path="UI")
            registry_keys = ['AndroidEmulator.exe', 'AndroidEmulatorEn.exe', 'AndroidEmulatorEx.exe', 'aow_exe.exe']
            base_key = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options'
            
            for key in registry_keys:
                full_key = fr"{base_key}\{key}\PerfOptions"
                subprocess.run(['reg', 'ADD', full_key, '/v', 'CpuPriorityClass', '/t', 'REG_DWORD', '/d', '3', '/f'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

            if install_path:
                for key in registry_keys:
                    subprocess.run([
                        'reg', 'ADD', r'HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers',
                        '/v', fr'{install_path}\{key}', '/t', 'REG_SZ', '/d', '~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE', '/f'
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                    
                    subprocess.run([
                        'reg', 'ADD', r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\DirectX\UserGpuPreferences',
                        '/v', fr'{install_path}\{key}', '/t', 'REG_SZ', '/d', 'GpuPreference=2;', '/f'
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

            return OptimizationResult(True, "GameLoop execution options optimized in Windows Registry.")
        except Exception as e:
            return OptimizationResult(False, f"Registry optimization failed: {e}")

    def apply_latency_tweaks(self) -> OptimizationResult:
        reg_tweaks = [
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "NetworkThrottlingIndex", "REG_DWORD", "0xffffffff"),
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", "REG_DWORD", "0"),
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "GPU Priority", "REG_DWORD", "8"),
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "Priority", "REG_DWORD", "6"),
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "Scheduling Category", "REG_SZ", "High"),
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "SFIO Priority", "REG_SZ", "High"),
            (r"HKCU\System\GameConfigStore", "GameDVR_Enabled", "REG_DWORD", "0"),
            (r"HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR", "AppCaptureEnabled", "REG_DWORD", "0"),
            (r"HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR", "AllowGameDVR", "REG_DWORD", "0"),
            (r"HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerThrottling", "PowerThrottlingOff", "REG_DWORD", "1"),
            (r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpAckFrequency", "REG_DWORD", "1"),
            (r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TCPNoDelay", "REG_DWORD", "1"),
        ]

        try:
            for key, name, type_, val in reg_tweaks:
                subprocess.run(['reg', 'ADD', key, '/v', name, '/t', type_, '/d', val, '/f'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

            # Enable High Performance Power Scheme
            subprocess.run(["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            return OptimizationResult(True, "Latency and network response tweaks applied successfully.")
        except Exception as e:
            return OptimizationResult(False, f"Latency tweaks failed: {e}")

    def force_resource_allocation(self, aggressive: bool = False, target_ram_gb: Optional[int] = None, target_cores: Optional[int] = None) -> Tuple[int, int]:
        total_ram_mb = int(psutil.virtual_memory().total / (1024 ** 2))
        if target_ram_gb is not None:
            ram_val = max(2048, int(target_ram_gb) * 1024)
        elif aggressive:
            ram_val = max(2048, total_ram_mb - 2048)
        else:
            ram_val = max(2048, min(int(total_ram_mb * 0.75), total_ram_mb - 2048))

        total_cores = psutil.cpu_count(logical=True) or 1
        if target_cores is not None:
            cpu_val = max(1, min(int(target_cores), 64))
        elif aggressive:
            cpu_val = max(1, min(total_cores, 12))
        else:
            cpu_val = max(1, min(max(2, int(total_cores * 0.75)), 12))

        RegistryManager.set_user_dword("VMMemorySizeInMB", ram_val)
        RegistryManager.set_user_dword("VMCpuCount", cpu_val)
        return ram_val, cpu_val

    def boost_priority(self, priority: str = "high", target_cores: Optional[int] = None) -> Tuple[int, bool]:
        priority_map = {
            "high": getattr(psutil, "HIGH_PRIORITY_CLASS", None),
            "realtime": getattr(psutil, "REALTIME_PRIORITY_CLASS", None),
            "above_normal": getattr(psutil, "ABOVE_NORMAL_PRIORITY_CLASS", None),
        }
        p_class = priority_map.get(priority.lower(), priority_map["high"])
        if p_class is None:
            return 0, False

        cpu_cores = psutil.cpu_count(logical=True) or 1
        affinity_cores = max(1, min(target_cores or cpu_cores, cpu_cores))
        cpu_affinity = list(range(affinity_cores))

        boosted = 0
        applied_req = True
        target_names = {name.lower() for name in GAMELOOP_PROCESSES}

        for proc in psutil.process_iter(['name']):
            try:
                pname = (proc.info.get('name') or '').lower()
                if pname not in target_names and "renderer" not in pname and "aow_exe" not in pname:
                    continue
                proc.nice(p_class)
                try:
                    proc.cpu_affinity(cpu_affinity)
                except (AttributeError, psutil.AccessDenied, NotImplementedError):
                    pass
                boosted += 1
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                applied_req = False
                continue

        return boosted, applied_req

    def apply_full_resource_boost(self, target_cores: Optional[int] = None) -> OptimizationResult:
        total_ram_mb = int(psutil.virtual_memory().total / (1024 ** 2))
        gameloop_ram = max(2048, total_ram_mb - 2048)
        RegistryManager.set_user_dword("VMMemorySizeInMB", gameloop_ram)

        total_cores = psutil.cpu_count(logical=True) or 4
        gameloop_cores = max(1, min(int(target_cores), 64)) if target_cores else max(1, total_cores)
        RegistryManager.set_user_dword("VMCpuCount", gameloop_cores)

        RegistryManager.set_user_dword("RenderOptimizeEnabled", 0)
        RegistryManager.set_user_dword("GraphicsCardEnabled", 1)
        RegistryManager.set_user_dword("SetGraphicsCard", 1)
        RegistryManager.set_user_dword("ForceDirectX", 1)

        boosted, _ = self.boost_priority(priority="realtime", target_cores=gameloop_cores)
        return OptimizationResult(
            True, 
            f"Full Boost Applied: {gameloop_ram // 1024}GB RAM, {gameloop_cores} Cores, {boosted} processes boosted."
        )

    def apply_fps_stabilizer(self) -> OptimizationResult:
        visual_cmds = [
            ['reg', 'ADD', r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects', '/v', 'VisualFXSetting', '/t', 'REG_DWORD', '/d', '2', '/f'],
            ['reg', 'ADD', r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize', '/v', 'EnableTransparency', '/t', 'REG_DWORD', '/d', '0', '/f'],
        ]
        for cmd in visual_cmds:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

        fps_killers = ["SearchIndexer.exe", "MsMpEng.exe", "OneDrive.exe", "Teams.exe", "Slack.exe"]
        for proc_name in fps_killers:
            try:
                subprocess.run(["taskkill", "/F", "/IM", proc_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            except Exception:
                pass

        try:
            import ctypes
            ntdll = ctypes.WinDLL('ntdll.dll')
            ntdll.NtSetTimerResolution(5000, True, ctypes.byref(ctypes.c_ulong()))
        except Exception:
            pass

        return OptimizationResult(True, "FPS Stabilizer & high precision timer activated.")

    @staticmethod
    def kill_gameloop() -> OptimizationResult:
        killed_count = 0
        for proc_name in sorted(GAMELOOP_PROCESSES):
            res = subprocess.run(['taskkill', '/F', '/IM', proc_name, '/T'],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            if res.returncode == 0:
                killed_count += 1

        if killed_count > 0:
            return OptimizationResult(True, f"Terminated {killed_count} GameLoop background processes.")
        return OptimizationResult(False, "No running GameLoop processes were found.")

    @staticmethod
    def change_dns_servers(dns_servers: list) -> OptimizationResult:
        try:
            import pythoncom
            import wmi
            pythoncom.CoInitialize()
            wmi_api = wmi.WMI()
            adapters = wmi_api.Win32_NetworkAdapterConfiguration(IPEnabled=True)
            success = all(adapter.SetDNSServerSearchOrder(dns_servers)[0] == 0 for adapter in adapters)
            subprocess.run(['ipconfig', '/flushdns'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            if success:
                return OptimizationResult(True, f"DNS updated to {dns_servers[0]}")
            return OptimizationResult(False, "DNS update failed for one or more network adapters.")
        except Exception as e:
            return OptimizationResult(False, f"DNS update error: {e}")
