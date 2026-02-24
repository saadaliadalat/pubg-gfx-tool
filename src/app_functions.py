import os
import shutil
import subprocess
import sys
import winreg
import xml.etree.ElementTree as ET
from shutil import copy
from time import sleep

import GPUtil
import adbutils
import psutil
import pythoncom
import tempfile
import winshell
import wmi
from PyQt5.QtCore import QSettings
from win32com.client import Dispatch
from . import setup_logger


class Settings:
    def __init__(self):
        self.settings = QSettings("EX Apps", "EX Tool")
        self.REG_PATH = r'SOFTWARE\Tencent\MobileGamePC'
        self.pubg_versions = {
            "com.tencent.ig": "PUBG Mobile Global",
            "com.vng.pubgmobile": "PUBG Mobile VN",
            "com.rekoo.pubgm": "PUBG Mobile TW",
            "com.pubg.krmobile": "PUBG Mobile KR",
            "com.pubg.imobile": "Battlegrounds Mobile India"}
        self.logger = setup_logger('error_logger', 'error.log')

    @staticmethod
    def kill_adb():
        """
        Kills the ADB (Android Debug Bridge) process if it is currently running.
        """
        try:
            subprocess.run(["taskkill", "/F", "/IM", "adb.exe"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    # Get Script Run Location
    @staticmethod
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
        return os.path.join(base_path, relative_path)


class Registry(Settings):
    def get_reg(self, name):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_PATH, 0, winreg.KEY_READ) as registry_key:
                value, regtype = winreg.QueryValueEx(registry_key, name)
                return value
        except FileNotFoundError:
            return None

    @staticmethod
    def get_local_reg(name, path="AppMarket"):
        """
        Get the value of a registry key in the local machine.
        """
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                rf'SOFTWARE\WOW6432Node\Tencent\MobileGamePC\{path}') as registry_key:
                value, regtype = winreg.QueryValueEx(registry_key, name)
                return value
        except OSError:
            return None

    def set_dword(self, name, value):
        """
        Set the value of a DWORD in the Windows registry.
        """
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.REG_PATH) as registry_key:
                winreg.SetValueEx(registry_key, name, 0, winreg.REG_DWORD, value)
            return True
        except WindowsError:
            return False


class Optimizer(Registry):
    gameloop_process_names = {
        'aow_exe.exe',
        'aow.exe',
        'AndroidEmulatorEn.exe',
        'AndroidEmulator.exe',
        'AndroidEmulatorEx.exe',
        'TBSWebRenderer.exe',
        'QtWebEngineProcess.exe',
        'syzs_dl_svr.exe',
        'AppMarket.exe',
        'QMEmulatorService.exe',
        'RuntimeBroker.exe',
        'GameLoader.exe',
        'TSettingCenter.exe',
        'Auxillary.exe',
        'TP3Helper.exe',
        'tp3helper.dat',
        'GameDownload.exe',
    }

    def temp_cleaner(self):
        import os
        import shutil
        import subprocess
        import tempfile
        import winreg

        def clear_dir(path):
            try:
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

        # Clear temp folders
        clear_dir(tempfile.gettempdir())
        clear_dir(r"C:\Windows\Temp")
        clear_dir(os.path.expandvars(r"%windir%\Prefetch"))

        # Clear GameLoop shader cache
        try:
            gameloop_ui_path = self.get_local_reg('InstallPath', path='UI')
            if gameloop_ui_path:
                clear_dir(os.path.join(gameloop_ui_path, 'ShaderCache'))
        except Exception:
            pass

        # Flush standby memory using RAMMap-style registry trick
        try:
            subprocess.run(
                ["powershell", "-Command",
                 "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

        # Empty working sets of background processes
        try:
            subprocess.run(
                ["powershell", "-Command",
                 "Get-Process | Where-Object {$_.WorkingSet -gt 50MB} | ForEach-Object { $_.MinWorkingSet = 1MB }"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10
            )
        except Exception:
            pass

        # Disable Windows Search indexing temporarily for gaming
        try:
            subprocess.run(["sc", "stop", "WSearch"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

        # Clear DNS cache
        subprocess.run(["ipconfig", "/flushdns"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

        return True

    def add_to_windows_defender_exclusion(self):
        """
        Adds the directory of the game loop to the Windows Defender exclusion list.
        """
        try:
            gameloop_path = os.path.dirname(self.get_local_reg("InstallPath"))
            command = ["powershell", "-Command", f"Add-MpPreference -ExclusionPath '{gameloop_path}' -Force"]
            subprocess.call(command)
        except Exception:
            return False
        return True

    def optimize_gameloop_registry(self):
        try:
            install_path = self.get_local_reg("InstallPath", path="UI")
            registry_keys = [
                'AndroidEmulator.exe',
                'AndroidEmulatorEn.exe',
                'AndroidEmulatorEx.exe',
                'aow_exe.exe',
            ]
            base_key = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options'
            value_name = 'CpuPriorityClass'
            value_data = '3'

            for key in registry_keys:
                full_key = fr"{base_key}\{key}\PerfOptions"
                command = [
                    'reg', 'ADD', full_key,
                    '/v', value_name,
                    '/t', 'REG_DWORD',
                    '/d', value_data,
                    '/f'
                ]
                subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            registry_entries = [
                (
                    r'HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers',
                    '~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE'
                ),
                (
                    r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\DirectX\UserGpuPreferences',
                    'GpuPreference=2;'
                )
            ]

            commands = [
                [
                    'reg', 'ADD', registry_key,
                    '/v', fr'{install_path}\{key}',
                    '/t', 'REG_SZ',
                    '/d', value,
                    '/f'
                ]
                for registry_key, value in registry_entries
                for key in registry_keys
            ]

            for command in commands:
                subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            self.logger.error(f"Exception occurred: {str(e)}", exc_info=True)

    def apply_latency_tweaks(self):
        import subprocess
        import winreg

        reg_tweaks = [
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
             "NetworkThrottlingIndex", "REG_DWORD", "0xffffffff"),
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
             "SystemResponsiveness", "REG_DWORD", "0"),
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
             "GPU Priority", "REG_DWORD", "8"),
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
             "Priority", "REG_DWORD", "6"),
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
             "Scheduling Category", "REG_SZ", "High"),
            (r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
             "SFIO Priority", "REG_SZ", "High"),
            (r"HKCU\System\GameConfigStore", "GameDVR_Enabled", "REG_DWORD", "0"),
            (r"HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR", "AppCaptureEnabled", "REG_DWORD", "0"),
            (r"HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR", "AllowGameDVR", "REG_DWORD", "0"),
            (r"HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerThrottling",
             "PowerThrottlingOff", "REG_DWORD", "1"),
            (r"HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Parameters",
             "Type", "REG_SZ", "NTP"),
            (r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
             "TcpAckFrequency", "REG_DWORD", "1"),
            (r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
             "TCPNoDelay", "REG_DWORD", "1"),
            (r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
             "LargeSystemCache", "REG_DWORD", "0"),
            (r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters",
             "EnablePrefetcher", "REG_DWORD", "0"),
            (r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters",
             "EnableSuperfetch", "REG_DWORD", "0"),
        ]

        try:
            for key, name, type_, value in reg_tweaks:
                subprocess.run(
                    ['reg', 'ADD', key, '/v', name, '/t', type_, '/d', value, '/f'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )

            services_to_disable = [
                "SysMain",
                "WSearch",
                "DiagTrack",
                "dmwappushservice",
                "lfsvc",
                "MapsBroker",
                "XblAuthManager",
                "XblGameSave",
                "XboxNetApiSvc",
            ]

            for service in services_to_disable:
                subprocess.run(["sc", "config", service, "start=", "disabled"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["sc", "stop", service],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            subprocess.run(
                ["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

            subprocess.run(
                ["powercfg", "-setacvalueindex", "SCHEME_CURRENT",
                 "54533251-82be-4824-96c1-47b60b740d00",
                 "0cc5b647-c1df-4637-891a-dec35c318583", "100"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            subprocess.run(["powercfg", "-SetActive", "SCHEME_CURRENT"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            return True
        except Exception as e:
            self.logger.error(f"Latency tweaks error: {str(e)}", exc_info=True)
            return False

    def force_gameloop_resource_allocation(self, aggressive: bool = False, target_ram_gb: int | None = None,
                                           target_cores: int | None = None):
        """
        Increase Gameloop VM CPU/RAM allocation to reduce lag.

        Returns:
            tuple[int, int]: Allocated RAM in MB and CPU core count.
        """
        total_ram_mb = int(psutil.virtual_memory().total / (1024 ** 2))
        if target_ram_gb is not None:
            ram_value = max(2048, int(target_ram_gb) * 1024)
        elif aggressive:
            ram_value = max(2048, total_ram_mb - 2048)
        else:
            ram_value = max(2048, min(int(total_ram_mb * 0.75), total_ram_mb - 2048))

        total_cores = psutil.cpu_count(logical=True) or 1
        if target_cores is not None:
            cpu_value = max(1, min(int(target_cores), total_cores))
        elif aggressive:
            cpu_value = max(1, min(total_cores, 12))
        else:
            cpu_value = max(1, min(max(2, int(total_cores * 0.75)), 12))

        self.set_dword("VMMemorySizeInMB", ram_value)
        self.set_dword("VMCpuCount", cpu_value)

        return ram_value, cpu_value

    def boost_gameloop_priority(self, priority="high", target_cores: int | None = None):
        """
        Boosts Gameloop processes to high priority and sets CPU affinity.

        Returns:
            tuple[int, bool]: Number of processes updated, and whether requested priority applied.
        """
        priority_map = {
            "high": getattr(psutil, "HIGH_PRIORITY_CLASS", None),
            "realtime": getattr(psutil, "REALTIME_PRIORITY_CLASS", None),
            "above_normal": getattr(psutil, "ABOVE_NORMAL_PRIORITY_CLASS", None),
        }
        priority_class = priority_map.get(str(priority).lower())
        if priority_class is None:
            priority_class = priority_map.get("high")
        if priority_class is None:
            return 0, False

        cpu_cores = psutil.cpu_count(logical=True) or 1
        if target_cores is None:
            target_cores = cpu_cores if str(priority).lower() == "realtime" else min(cpu_cores, 12)
        affinity_cores = max(1, min(int(target_cores), int(cpu_cores)))
        cpu_affinity = list(range(affinity_cores))
        boosted = 0
        applied_requested = True

        target_names = {name.lower() for name in self.gameloop_process_names}

        for process in psutil.process_iter(['name']):
            process_name = (process.info.get('name') or '').lower()
            if process_name not in target_names and "renderer" not in process_name and "aow_exe" not in process_name:
                continue
            try:
                process.nice(priority_class)
                if process.nice() != priority_class:
                    applied_requested = False
                try:
                    process.cpu_affinity(cpu_affinity)
                except (AttributeError, psutil.AccessDenied, NotImplementedError):
                    pass
                boosted += 1
            except psutil.AccessDenied:
                applied_requested = False
                continue
            except psutil.NoSuchProcess:
                continue

        return boosted, applied_requested

    def apply_full_resource_boost(self):
        """
        Gives Gameloop everything: max RAM, max CPU cores, real-time priority,
        and forces GPU preference via registry.
        """
        import psutil
        import subprocess

        total_ram_mb = int(psutil.virtual_memory().total / (1024 ** 2))
        gameloop_ram = max(2048, total_ram_mb - 2048)
        self.set_dword("VMMemorySizeInMB", gameloop_ram)

        total_cores = psutil.cpu_count(logical=True) or 4
        gameloop_cores = min(total_cores, 12)
        self.set_dword("VMCpuCount", gameloop_cores)

        self.set_dword("RenderOptimizeEnabled", 0)
        self.set_dword("GraphicsCardEnabled", 1)
        self.set_dword("SetGraphicsCard", 1)
        self.set_dword("ForceDirectX", 1)

        boosted, _ = self.boost_gameloop_priority(priority="realtime", target_cores=total_cores)

        subprocess.run(
            ["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["powercfg", "-setacvalueindex", "SCHEME_CURRENT",
             "54533251-82be-4824-96c1-47b60b740d00",
             "893dee8e-2bef-41e0-89c6-b55d0929964c", "100"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["powercfg", "-setacvalueindex", "SCHEME_CURRENT",
             "54533251-82be-4824-96c1-47b60b740d00",
             "0cc5b647-c1df-4637-891a-dec35c318583", "100"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["powercfg", "-SetActive", "SCHEME_CURRENT"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        for exe in ['AndroidEmulator.exe', 'AndroidEmulatorEn.exe', 'AndroidEmulatorEx.exe', 'aow_exe.exe']:
            key = (r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
                   rf"\Image File Execution Options\{exe}\PerfOptions")
            subprocess.run(
                ['reg', 'ADD', key, '/v', 'IoPriority', '/t', 'REG_DWORD', '/d', '3', '/f'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            subprocess.run(
                ['reg', 'ADD', key, '/v', 'CpuPriorityClass', '/t', 'REG_DWORD', '/d', '3', '/f'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

        return gameloop_ram, gameloop_cores, boosted

    def apply_fps_stabilizer(self):
        """
        Applies all tweaks to ensure FPS never drops:
        - Disables background processes
        - Sets GameLoop affinity to performance cores
        - Disables Windows visual effects
        - Prevents CPU frequency scaling
        """
        import psutil
        import subprocess

        visual_effects_commands = [
            ['reg', 'ADD', r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects',
             '/v', 'VisualFXSetting', '/t', 'REG_DWORD', '/d', '2', '/f'],
            ['reg', 'ADD', r'HKCU\Control Panel\Desktop',
             '/v', 'UserPreferencesMask', '/t', 'REG_BINARY', '/d', '9012038010000000', '/f'],
            ['reg', 'ADD', r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize',
             '/v', 'EnableTransparency', '/t', 'REG_DWORD', '/d', '0', '/f'],
        ]

        for cmd in visual_effects_commands:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        subprocess.run(
            ["powercfg", "-setacvalueindex", "SCHEME_CURRENT",
             "54533251-82be-4824-96c1-47b60b740d00",
             "893dee8e-2bef-41e0-89c6-b55d0929964c", "100"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        fps_killers = [
            "SearchIndexer.exe", "MsMpEng.exe",
            "OneDrive.exe", "Teams.exe", "Slack.exe",
            "discord.exe",
            "chrome.exe", "msedge.exe",
        ]
        for proc_name in fps_killers:
            try:
                subprocess.run(["taskkill", "/F", "/IM", proc_name],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass

        try:
            import ctypes
            ntdll = ctypes.WinDLL('ntdll.dll')
            ntdll.NtSetTimerResolution(5000, True, ctypes.byref(ctypes.c_ulong()))
        except Exception:
            pass

        subprocess.run(["powercfg", "-SetActive", "SCHEME_CURRENT"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return True

    def optimize_for_nvidia(self):
        def change_nvidia_profile():
            gameloop_ui_path = self.get_local_reg("InstallPath", path="UI").replace("\\", "/")

            tree = ET.parse(nvidia_profile_path, parser=ET.XMLParser(encoding='utf-16'))
            root = tree.getroot()

            profilename = root.find('.//ProfileName')
            executeables = root.find('.//Executeables')
            path_elem = executeables.find('string')

            path_elem.text = f"{gameloop_ui_path}/androidemulatoren.exe".lower()
            profilename.text = path_elem.text.replace('/', '\\')

            gpu = GPUtil.getGPUs()[0] if GPUtil.getGPUs() else None

            filter_setting = tree.find(".//ProfileSetting[SettingNameInfo='Enable FXAA']")
            if gpu and gpu.memoryTotal / 1024 < 3:
                filter_setting.find('SettingValue').text = '0'
            else:
                filter_setting.find('SettingValue').text = '1'

            tree.write(nvidia_profile_path, encoding='utf-16')

        try:
            nvidia_profile_path = self.resource_path("assets/ex.nip")

            def is_gpu_nvidia() -> bool:
                try:
                    gpu_provider = wmi.WMI().Win32_VideoController()[0].AdapterCompatibility
                    return "NVIDIA" in gpu_provider
                except:
                    return False

            if is_gpu_nvidia():
                change_nvidia_profile()

                args = [
                    self.resource_path("assets/nvidiaProfileInspector.exe"),
                    nvidia_profile_path,
                    "-silent"
                ]
                subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            self.logger.error(f"Exception occurred: {str(e)}", exc_info=True)

    def optimize_for_amd(self):
        """
        Forces Gameloop executables to use high-performance GPU on AMD systems.
        """
        try:
            def is_gpu_amd() -> bool:
                try:
                    gpu_provider = wmi.WMI().Win32_VideoController()[0].AdapterCompatibility
                    return "AMD" in gpu_provider or "Radeon" in gpu_provider
                except Exception:
                    return False

            if not is_gpu_amd():
                return False

            install_path = self.get_local_reg("InstallPath", path="UI")
            if not install_path:
                return False

            registry_keys = [
                'AndroidEmulator.exe',
                'AndroidEmulatorEn.exe',
                'AndroidEmulatorEx.exe',
                'aow_exe.exe',
            ]

            for key in registry_keys:
                command = [
                    'reg', 'ADD',
                    r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\DirectX\UserGpuPreferences',
                    '/v', fr'{install_path}\{key}',
                    '/t', 'REG_SZ',
                    '/d', 'GpuPreference=2;',
                    '/f'
                ]
                subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            self.logger.error(f"Exception occurred: {str(e)}", exc_info=True)
            return False

    @staticmethod
    def kill_gameloop():
        """
        Kills a list of processes related to the gameloop.

        Returns:
            - True if at least one process was killed.
            - False if no process was killed.
        """
        # List of processes to be killed
        processes_to_kill = sorted(Optimizer.gameloop_process_names)

        processes_killed = 0

        for process in processes_to_kill:
            result = subprocess.run(['taskkill', '/F', '/IM', process, '/T'], stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                processes_killed += 1

        return processes_killed >= 1

    @staticmethod
    def change_dns_servers(dns_servers):
        """
        Change the DNS servers for all network adapters.
        """
        pythoncom.CoInitialize()  # Initialize the COM library

        wmi_api = wmi.WMI()  # Create a WMI API object

        # Retrieve all network adapters
        adapters = wmi_api.Win32_NetworkAdapterConfiguration(IPEnabled=True)

        dns_changed_status = all(adapter.SetDNSServerSearchOrder(dns_servers)[0] == 0 for adapter in adapters)

        # Flush DNS cache
        subprocess.run(['ipconfig', '/flushdns'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

        return dns_changed_status

    def ipad_layout_settings(self, reset=False):
        """
        Modify the layout of the XML file based on the edited values.

        Parameters:
            reset (bool): If True, the XML file will be reset to its original state by copying the backup file. If False, the layout will be modified based on the edited values.
        """
        appdata_folder = os.getenv('APPDATA')
        keymap_folder = os.path.join(appdata_folder, 'AndroidTbox')
        original_file = os.path.join(keymap_folder, 'TVM_100.xml')
        backup_file = os.path.join(keymap_folder, 'TVM_100.xml.mkbackup')

        def set_keymap_layout():
            """
            Modify the layout of the XML file based on the edited values.
            """

            def update_xml(ipad_keymap):
                with open(original_file, 'r', encoding='utf-8') as file:
                    xml_code = file.read()

                root = ET.fromstring(f'<root>{xml_code}</root>')
                for pubg_version in self.pubg_versions:
                    if root.find(f".//Item[@ApkName='{pubg_version}']") is not None:
                        for query, values in ipad_keymap.items():
                            for button_name, switches in values.items():
                                for switch_name, points in switches.items():
                                    item_elem = root.find(f".//Item[@ApkName='{pubg_version}'].//KeyMapMode[@Name='{query}']")
                                    if item_elem is not None:
                                        key_mapping_ex = item_elem.find(f'.//KeyMappingEx[@ItemName="{button_name}"]')
                                        key_mapping = item_elem.find(f'.//KeyMapping[@ItemName="{button_name}"]')
                                        if key_mapping_ex is not None:
                                            if key_mapping_ex.findall(f'.//SwitchOperation[@EnablePositionSwitch]'):
                                                old_x, old_x2 = None, None
                                                for (new_y1, new_y2), point_val in zip(points, key_mapping_ex.findall(
                                                        f'.//SwitchOperation[@Description="{switch_name}"]')):
                                                    texture, points = point_val.get(f'EnablePositionSwitch').split(":")
                                                    x1, y1, x2, y2 = points.split(",")
                                                    old_x = x1 if old_x is None else old_x
                                                    old_x2 = x2 if old_x2 is None else old_x2
                                                    point_val.set('EnablePositionSwitch',
                                                                  f'{texture}:{old_x},{new_y1},{old_x2},{new_y2}')
                                            else:
                                                for _ in key_mapping_ex.findall(
                                                        f'.//SwitchOperation[@EnableSwitch="{switch_name}"]'):
                                                    if len(key_mapping_ex.findall(".//Point") or key_mapping_ex.findall(
                                                            ".//DriveKey") or key_mapping_ex.findall(
                                                        ".//SwitchOperation")) < len(
                                                        points):
                                                        zz = key_mapping_ex.findall(".//Point")
                                                        for _ in range(len(points) - len(zz)):
                                                            zz.append(ET.Element("Point"))
                                                    else:
                                                        zz = key_mapping_ex.findall(".//Point")

                                                    for (x, y), point_val in zip(points, (
                                                            zz or key_mapping_ex.findall(
                                                        ".//DriveKey") or key_mapping_ex.findall(
                                                        f'.//SwitchOperation[@EnableSwitch="{switch_name}"]'))):
                                                        # if main_value is not None:
                                                        if button_name == "Click with Scroll Wheel" and switch_name == "Backpage":
                                                            key_mapping_ex.set('Click_X', str(float(x) + 0.1))
                                                            key_mapping_ex.set('Click_Y', str(y))

                                                        key_mapping_ex.set('Point_X', str(x))
                                                        key_mapping_ex.set('Point_Y', str(y))

                                                        if point_val.get('Point_X') is not None:
                                                            point_val.set('Point_X', str(x))
                                                            point_val.set('Point_Y', str(y))
                                        elif key_mapping is not None:
                                            try:
                                                x, y = points
                                            except ValueError:
                                                print(switch_name, points, "Wrong format")
                                                modified_xml_code = ET.tostring(root, encoding='utf-8').decode('utf-8')
                                                return modified_xml_code.replace("<root>", "").replace("</root>", "")
                                            if key_mapping.get('Point_X') is not None:
                                                key_mapping.set('Point_X', str(x))
                                                key_mapping.set('Point_Y', str(y))

                                            if isinstance(points, list):
                                                for (x, y), point_element in zip(points, key_mapping.findall(
                                                        f'.//SwitchOperation[@EnableSwitch="{switch_name}"]')):
                                                    point_element.set('Point_X', str(x))
                                                    point_element.set('Point_Y', str(y))
                                            else:
                                                for point_element in key_mapping.findall(
                                                        f'.//SwitchOperation[@EnableSwitch="{switch_name}"]'):
                                                    point_element.set('Point_X', str(x))
                                                    point_element.set('Point_Y', str(y))
                # print(ET.tostring(root, encoding='utf-8').decode('utf-8')[6:-7])
                with open(original_file, 'w', encoding='utf-8') as file:
                    file.write(ET.tostring(root, encoding='utf-8').decode('utf-8')[6:-7])

            ipad_keymap_values = {
                "Smart 720P": {
                    "B": {"Reload": [("0.537234", "0.880567"), ("0.406535", "0.880567")]},  # Main
                    "3": {"Jump": ("0.613222", "0.880567"), "GetOutCar": ("0.613222", "0.880567")},  # Main
                    "F3": {"SetUp": [("0.768997", "0.163968"), ("0.896657", "0.270243")]},
                    "F2": {"SetUp": [("0.781155", "0.144737"), ("0.960486", "0.270243")]},  # Main 2 >> 1
                    "Space": {"Jump": ("0.962006", "0.762146"), "Climb": ("0.962006", "0.762146"),
                              "Whistle": [("0.911094", "0.660931"), ("0.063070", "0.747976")],
                              "DriveMode1|DriveSpeed": ("0.063070", "0.747976"),
                              "DriveMode1|DriveSpeedPress": ("0.063070", "0.747976"),
                              "SwimUp": ("0.835106", "0.701417"), "SwimmingUp": ("0.835106", "0.701417"), },
                    "Shift": {"DriveMode1|DriveSpeed": ("0.076748", "0.555668"),
                              "DriveMode1|DriveSpeedPress": ("0.076748", "0.555668")},
                    "Right Click": {"Sniper": ("0.962006", "0.638664"), "Sniper2": ("0.962006", "0.638664"),
                                    "Reload": ("0.962006", "0.638664")},  # Main
                    "Z": {"Fall": ("0.942249", "0.949393"), "CancelFall": ("0.942249", "0.949393")},  # Main
                    "E": {"Sideways": ("0.221884", "0.522267"), "SidewaysCancel": ("0.221884", "0.522267"),
                          "Moto": ("0.806991", "0.637652"), "Moto2": ("0.806991", "0.637652")},  # Main
                    "Q": {"Sideways": ("0.141337", "0.520243"), "SidewaysCancel": ("0.141337", "0.520243"),
                          "Moto": ("0.713526", "0.635628"), "Moto2": ("0.713526", "0.635628")},
                    "Y": {"SetUp": [("0.794833", "0.161943"), ("0.753040", "0.161943"), ("0.844985", "0.157895")]},
                    "T": {"SetUp": [("0.780395", "0.092105"), ("0.732523", "0.092105"), ("0.847264", "0.097166")]},
                    "Alt": {"Eye": [("0.776596", "0.232794")]},
                    "Drive": {"DriveMode1": (("0.673252", "0.765182"), ("0.834347", "0.765182"),
                                             ("0.164894", "0.644737"), ("0.164894", "0.826923"))},  # ADWS
                    "F": {"Pickup|NineBlock": ("0.144377", "0.683198"), "Pickup|SixBlock": ("0.341945", "0.682186"),
                          "Pickup|XBtn": ("0.319909", "0.281377"), "Pickup": ("0.658055", "0.281377"),
                          "Pickup|SkyBoxFlag|XBtn": ("0.144377", "0.683198")},
                    "G": {"Pickup|NineBlock": ("0.303191", "0.683198"), "Pickup|SixBlock": ("0.484043", "0.682186"),
                          "Pickup|XBtn": ("0.319909", "0.354251"), "Pickup": ("0.658055", "0.354251"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.303191", "0.683198"),
                          "Whistle": ("0.954407", "0.771255"),
                          "OutCarShoot": ("0.954407", "0.683198"), "OutCarShoot2": ("0.954407", "0.771255")},
                    "H": {"Pickup|NineBlock": ("0.144377", "0.769231"), "Pickup|SixBlock": ("0.649696", "0.682186"),
                          "Pickup|XBtn": ("0.319909", "0.429150"), "Pickup": ("0.658055", "0.429150"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.144377", "0.769231")},
                    "Slide with Scroll Wheel": {"Pickup": [("0.658055", "0.374251")],
                                                "Pickup|XBtn": [("0.319909", "0.374251")],
                                                "Pickup|XBtn|SkyBoxFlag": [("0.319909", "0.723198")],
                                                "Pickup|SkyBoxFlag": [("0.658055", "0.723198")]},
                    "4": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "5": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "6": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "X": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "7": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "8": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "9": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "0": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                },
                "Smart 1080P": {
                    "B": {"Reload": [("0.542969", "0.910751"), ("0.437500", "0.910751")]},  # Main
                    "3": {"Jump": ("0.584347", "0.913793"), "GetOutCar": ("0.584347", "0.913793")},  # Main
                    "F3": {"SetUp": [("0.838146", "0.100406"), ("0.924012", "0.193712")]},
                    "F2": {"SetUp": [("0.838146", "0.100406"), ("0.971884", "0.193712")]},  # Main 2 >> 1
                    "Space": {"Jump": ("0.969605", "0.834686"), "Climb": ("0.969605", "0.834686"),
                              "Whistle": [("0.934650", "0.764706"), ("0.049392", "0.823529")],
                              "DriveMode1|DriveSpeed": ("0.049392", "0.823529"),
                              "DriveMode1|DriveSpeedPress": ("0.049392", "0.823529"),
                              "SwimUp": ("0.879518", "0.759036"), "SwimmingUp": ("0.879518", "0.759036"), },
                    "Shift": {"DriveMode1|DriveSpeed": ("0.053951", "0.683570"),
                              "DriveMode1|DriveSpeedPress": ("0.053951", "0.683570")},
                    "Right Click": {"Sniper": ("0.971125", "0.746450"), "Sniper2": ("0.971125", "0.746450"),
                                    "Reload": ("0.971125", "0.746450")},  # Main
                    "Z": {"Fall": ("0.961246", "0.967546"), "CancelFall": ("0.961246", "0.967546")},  # Main
                    "E": {"Sideways": ("0.155775", "0.658215"), "SidewaysCancel": ("0.155775", "0.658215"),
                          "Moto": ("0.857903", "0.738337"), "Moto2": ("0.857903", "0.738337")},  # Main
                    "Q": {"Sideways": ("0.101064", "0.656187"), "SidewaysCancel": ("0.101064", "0.656187"),
                          "Moto": ("0.791793", "0.736308"), "Moto2": ("0.791793", "0.736308")},
                    "Y": {"SetUp": [("0.852584", "0.118661"), ("0.823708", "0.118661"), ("0.892097", "0.108519")]},
                    "T": {"SetUp": [("0.841185", "0.064909"), ("0.809271", "0.064909"), ("0.888298", "0.073022")]},
                    "Alt": {"Eye": [("0.840426", "0.166329")]},
                    "Drive": {"DriveMode1": (("0.764438", "0.836714"), ("0.881459", "0.836714"),
                                             ("0.116261", "0.752535"), ("0.116261", "0.883367"))},  # ADWS
                    "F": {"Pickup|NineBlock": ("0.353906", "0.763889"), "Pickup|SixBlock": ("0.482031", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.199393"), "Pickup": ("0.721094", "0.199393"),
                          "Pickup|SkyBoxFlag|XBtn": ("0.353906", "0.763889")},
                    "G": {"Pickup|NineBlock": ("0.732812", "0.767206"), "Pickup|SixBlock": ("0.607812", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.251616"), "Pickup": ("0.721094", "0.251616"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.476563", "0.763889"),
                          "Whistle": ("0.966565", "0.835700"),
                          "OutCarShoot": ("0.965625", "0.839167"), "OutCarShoot2": ("0.965625", "0.839167")},
                    "H": {"Pickup|NineBlock": ("0.353906", "0.847761"), "Pickup|SixBlock": ("0.732031", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.303839"), "Pickup": ("0.721094", "0.303839"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.353906", "0.847761")},
                    "1": {"Jump": ("0.453906", "0.947333"), "Climb": ("0.453906", "0.947333"),
                          "GetOutCar": ("0.453906", "0.947333")},
                    "2": {"Jump": ("0.544531", "0.947333"), "Climb": ("0.544531", "0.947333"),
                          "GetOutCar": ("0.544531", "0.9472333")},
                    "Click with Scroll Wheel": {"Backpage": [("0.453906", "0.947333")]},
                    "Slide with Scroll Wheel": {"Pickup": [("0.739844", "0.199393")],
                                                "Pickup|XBtn": [("0.467187", "0.199393")]},
                    "4": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "5": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "6": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "X": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "7": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "8": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "9": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "0": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                },
                "Smart 2K": {
                    "B": {"Reload": [("0.542969", "0.910751"), ("0.437500", "0.910751")]},  # Main
                    "3": {"Jump": ("0.584347", "0.913793"), "GetOutCar": ("0.584347", "0.913793")},  # Main
                    "F3": {"SetUp": [("0.838146", "0.100406"), ("0.924012", "0.193712")]},
                    "F2": {"SetUp": [("0.838146", "0.100406"), ("0.971884", "0.193712")]},  # Main 2 >> 1
                    "Space": {"Jump": ("0.969605", "0.834686"), "Climb": ("0.969605", "0.834686"),
                              "Whistle": [("0.934650", "0.764706"), ("0.049392", "0.823529")],
                              "DriveMode1|DriveSpeed": ("0.049392", "0.823529"),
                              "DriveMode1|DriveSpeedPress": ("0.049392", "0.823529"),
                              "SwimUp": ("0.879518", "0.759036"), "SwimmingUp": ("0.879518", "0.759036"), },
                    "Shift": {"DriveMode1|DriveSpeed": ("0.053951", "0.683570"),
                              "DriveMode1|DriveSpeedPress": ("0.053951", "0.683570")},
                    "Right Click": {"Sniper": ("0.971125", "0.746450"), "Sniper2": ("0.971125", "0.746450"),
                                    "Reload": ("0.971125", "0.746450")},  # Main
                    "Z": {"Fall": ("0.961246", "0.967546"), "CancelFall": ("0.961246", "0.967546")},  # Main
                    "E": {"Sideways": ("0.155775", "0.658215"), "SidewaysCancel": ("0.155775", "0.658215"),
                          "Moto": ("0.857903", "0.738337"), "Moto2": ("0.857903", "0.738337")},  # Main
                    "Q": {"Sideways": ("0.101064", "0.656187"), "SidewaysCancel": ("0.101064", "0.656187"),
                          "Moto": ("0.791793", "0.736308"), "Moto2": ("0.791793", "0.736308")},
                    "Y": {"SetUp": [("0.852584", "0.118661"), ("0.823708", "0.118661"), ("0.892097", "0.108519")]},
                    "T": {"SetUp": [("0.841185", "0.064909"), ("0.809271", "0.064909"), ("0.888298", "0.073022")]},
                    "Alt": {"Eye": [("0.840426", "0.166329")]},
                    "Drive": {"DriveMode1": (("0.764438", "0.836714"), ("0.881459", "0.836714"),
                                             ("0.116261", "0.752535"), ("0.116261", "0.883367"))},  # ADWS
                    "F": {"Pickup|NineBlock": ("0.353906", "0.763889"), "Pickup|SixBlock": ("0.482031", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.199393"), "Pickup": ("0.721094", "0.199393"),
                          "Pickup|SkyBoxFlag|XBtn": ("0.353906", "0.763889")},
                    "G": {"Pickup|NineBlock": ("0.732812", "0.767206"), "Pickup|SixBlock": ("0.607812", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.251616"), "Pickup": ("0.721094", "0.251616"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.476563", "0.763889"),
                          "Whistle": ("0.966565", "0.835700"),
                          "OutCarShoot": ("0.965625", "0.839167"), "OutCarShoot2": ("0.965625", "0.839167")},
                    "H": {"Pickup|NineBlock": ("0.353906", "0.847761"), "Pickup|SixBlock": ("0.732031", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.303839"), "Pickup": ("0.721094", "0.303839"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.353906", "0.847761")},
                    "1": {"Jump": ("0.453906", "0.947333"), "Climb": ("0.453906", "0.947333"),
                          "GetOutCar": ("0.453906", "0.947333")},
                    "2": {"Jump": ("0.544531", "0.947333"), "Climb": ("0.544531", "0.947333"),
                          "GetOutCar": ("0.544531", "0.9472333")},
                    "Click with Scroll Wheel": {"Backpage": [("0.453906", "0.947333")]},
                    "Slide with Scroll Wheel": {"Pickup": [("0.739844", "0.199393")],
                                                "Pickup|XBtn": [("0.467187", "0.199393")]},
                    "4": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "5": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "6": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "X": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "7": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "8": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "9": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "0": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                }
            }


            update_xml(ipad_keymap_values)


        if reset:
            shutil.copy2(backup_file, original_file)
            os.remove(backup_file)
        else:
            if not os.path.exists(backup_file):
                shutil.copy2(original_file, backup_file)
            set_keymap_layout()


    def ipad_settings(self, width: int, height: int) -> None:
        """
        Update iPad settings with the given width and height.
        """
        _width = self.settings.value("VMResWidth")
        _height = self.settings.value("VMResHeight")

        if _width is None or _height is None:
            vm_res_width = self.get_reg("VMResWidth")
            vm_res_height = self.get_reg("VMResHeight")
            self.settings.setValue("VMResWidth", vm_res_width)
            self.settings.setValue("VMResHeight", vm_res_height)

        self.ipad_layout_settings()
        self.set_dword("VMResWidth", width)
        self.set_dword("VMResHeight", height)

    def reset_ipad(self):
        """
        Resets the resolution of the iPad to its default values.
        """
        width = self.settings.value("VMResWidth")
        height = self.settings.value("VMResHeight")

        if width and height:
            self.settings.setValue("VMResWidth", None)
            self.settings.setValue("VMResHeight", None)
            self.ipad_layout_settings(reset=True)
            self.set_dword("VMResWidth", width)
            self.set_dword("VMResHeight", height)
            return width, height
        else:
            return None, None


class Game(Optimizer):

    def __init__(self):
        super().__init__()
        self.is_adb_working = None

    def gen_game_icon(self, game_name):
        gameloop_market_path = self.get_local_reg("InstallPath") or r"C:\Program Files\TxGameAssistant\AppMarket"
        pythoncom.CoInitialize()
        desktop = winshell.desktop()

        version_id = next((key for key, value in self.pubg_versions.items() if value == game_name), None)
        path_icon = os.path.join(desktop, f"{game_name}.lnk")
        target = rf"{gameloop_market_path}\AppMarket.exe"

        icon = self.resource_path(fr"assets\icons\{version_id}.ico")
        copy(icon, fr"{gameloop_market_path}\{version_id}.ico")

        shortcut = Dispatch('WScript.Shell').CreateShortCut(path_icon)
        shortcut.Targetpath = target
        shortcut.Arguments = f"-startpkg {version_id}  -from DesktopLink"
        shortcut.Description = "EX Tool desktop shortcut"
        shortcut.IconLocation = fr"{gameloop_market_path}\{version_id}.ico"
        shortcut.save()

    def check_adb_status(self):
        adb_status = self.get_reg("AdbDisable")

        if adb_status == 0:
            self.adb_enabled = True
            return
        elif adb_status == 1:
            self.set_dword("AdbDisable", 0)
            self.adb_enabled = False
            return
        elif adb_status is None:
            raise ValueError("Could not get AdbDisable status from registry.")

        raise ValueError("Unknown AdbDisable status.")

    @staticmethod
    def is_gameloop_running():
        running_process_list = subprocess.check_output(["tasklist"])
        emulator_processes = [b"AndroidEmulatorEx.exe", b"AndroidEmulatorEn.exe", b"AndroidEmulator.exe"]
        return any(process in running_process_list for process in emulator_processes)

    def check_adb_connection(self, first_check=True):
        try:
            client = adbutils.AdbClient()
            self.adb = client.device(serial="emulator-5554")

            while not self.adb.shell("getprop dev.bootcomplete"):
                pass

            self.adb.sync.pull("/default.prop", self.resource_path(r'assets\device_probe.bin'))
            self.is_adb_working = True

        except Exception as e:
            self.kill_adb()
            self.is_adb_working = False

            if first_check:
                self.check_adb_connection(False)

    def pubg_version_found(self):
        """
        Checks if any version of PUBG is installed on the device.
        """
        while not self.adb.shell("getprop dev.bootcomplete"):
            pass
        self.PUBG_Found = [version_name for package_name, version_name in self.pubg_versions.items()
                           if self.adb.shell(f"pm list packages {package_name}")]

    def get_graphics_file(self, package: str):
        active_savegames_path = f"/sdcard/Android/data/{package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/Active.sav"
        local_file_path = self.resource_path('assets/active_original.bin')
        self.pubg_package = package
        self.adb.sync.pull(active_savegames_path, local_file_path)

        with open(local_file_path, 'rb') as file:
            self.active_sav_content = file.read()

    def save_graphics_file(self):
        file_path = self.resource_path("assets/active_modified.bin")
        with open(file_path, 'wb') as file:
            file.write(self.active_sav_content)

    def set_fps(self, val: str) -> None:
        """
        Updates the Active.sav file with the new FPS value.
        """
        fps_mapping = {
            "Low": b"\x02",
            "Medium": b"\x03",
            "High": b"\x04",
            "Ultra": b"\x05",
            "Extreme": b"\x06",
            "Extreme+": b"\x07",
            "Ultra Extreme": b"\x08"
        }
        fps_value = fps_mapping.get(val)

        fps_properties = ["FPSLevel", "BattleFPS", "LobbyFPS"]
        if fps_value is not None:
            for prop in fps_properties:
                header = prop.encode(
                    'utf-8') + b'\x00\x0c\x00\x00\x00IntProperty\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00'
                before, _, after = self.active_sav_content.partition(header)
                after = after[:1].replace(after[:1], fps_value) + after[1:]
                self.active_sav_content = before + _ + after

    def set_fps_experimental(self, val: str) -> bool:
        """
        Try to unlock FPS beyond 120 using undocumented values.
        """
        fps_mapping = {
            "Low": b"\x02",
            "Medium": b"\x03",
            "High": b"\x04",
            "Ultra": b"\x05",
            "Extreme": b"\x06",
            "Extreme+": b"\x07",
            "Ultra Extreme": b"\x08",
            "144fps [EXP]": b"\x09",
            "165fps [EXP]": b"\x0A",
            "200fps [EXP]": b"\x0B",
        }
        fps_value = fps_mapping.get(val)
        if fps_value is None:
            return False

        fps_properties = ["FPSLevel", "BattleFPS", "LobbyFPS"]
        for prop in fps_properties:
            header = (
                prop.encode('utf-8') +
                b'\x00\x0c\x00\x00\x00IntProperty\x00'
                b'\x04\x00\x00\x00\x00\x00\x00\x00\x00'
            )
            before, sep, after = self.active_sav_content.partition(header)
            if sep:
                after = fps_value + after[1:]
                self.active_sav_content = before + sep + after
        return True

    def set_high_dpi_rendering(self, dpi=560):
        """Increase emulator DPI for sharper game rendering."""
        valid_dpis = [240, 320, 480, 560, 640]
        dpi = min(valid_dpis, key=lambda x: abs(x - int(dpi)))
        self.set_dword("VMDPI", dpi)
        self.set_dword("HardwareAcceleration", 1)
        self.set_dword("SoftwareDecoder", 0)
        self.set_dword("RenderOptimizeEnabled", 0)
        return dpi

    def push_engine_ini(self, mode="competitive"):
        """
        Push optimized Engine.ini for headshot clarity and visibility.
        """
        engine_ini_path = (
            f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/"
            f"ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/Engine.ini"
        )

        if mode == "competitive":
            content = """\
[SystemSettings]
; === EX Tool Competitive Engine Settings ===
r.MipMapLODBias=-2
r.SkeletalMeshLODBias=-2
r.StaticMeshLODBias=-1
r.ViewDistanceScale=4
r.MaxAnisotropy=16
r.TemporalAACurrentFrameWeight=1
r.TemporalAASamples=1
r.Streaming.PoolSize=3000
r.DefaultFeature.MotionBlur=False
r.Fog=0
r.VolumetricFog=0
r.TonemapperGamma=2.2
r.Tonemapper.Sharpen=1.5
foliage.DensityScale=0.3
r.DepthOfFieldQuality=0
"""
        else:
            content = """\
[SystemSettings]
; === EX Tool Balanced Engine Settings ===
r.MipMapLODBias=-1
r.SkeletalMeshLODBias=-1
r.StaticMeshLODBias=0
r.ViewDistanceScale=3
r.MaxAnisotropy=8
r.TemporalAACurrentFrameWeight=0.5
r.Streaming.PoolSize=2048
r.DefaultFeature.MotionBlur=False
r.Fog=1
foliage.DensityScale=0.6
"""

        local_path = self.resource_path(r'assets\engine_custom.ini')
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.adb.sync.push(local_path, engine_ini_path)
        return True

    def reset_engine_ini(self):
        """Reset Engine.ini to default."""
        engine_ini_path = (
            f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/"
            f"ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/Engine.ini"
        )
        local_path = self.resource_path(r'assets\engine_custom.ini')
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write("[SystemSettings]\n; Reset by EX Tool\n")
        self.adb.sync.push(local_path, engine_ini_path)
        return True

    def push_game_user_settings(self, resolution_x=1280, resolution_y=720, fps_limit=120):
        """
        Optimize GameUserSettings.ini for PC GameLoop.
        """
        path = (
            f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/"
            f"ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/GameUserSettings.ini"
        )

        content = f"""\
[/Script/Engine.GameUserSettings]
bUseVSync=False
bUseDynamicResolution=False
ResolutionSizeX={resolution_x}
ResolutionSizeY={resolution_y}
LastUserConfirmedResolutionSizeX={resolution_x}
LastUserConfirmedResolutionSizeY={resolution_y}
FullscreenMode=1
LastConfirmedFullscreenMode=1
PreferredFullscreenMode=1
FrameRateLimit={float(fps_limit):.6f}
DefaultFeature.AntiAliasing=4
DefaultFeature.AmbientOcclusion=False
DefaultFeature.MotionBlur=False
"""

        local_path = self.resource_path(r'assets\game_user_settings.ini')
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.adb.sync.push(local_path, path)
        return True

    def read_hex(self, name):
        """
        Reads the value of the specified property from the Active.sav file.
        """
        header = name.encode('utf-8') + b'\x00\x0c\x00\x00\x00IntProperty\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00'
        _, _, content = self.active_sav_content.partition(header)
        return content[:1]

    def change_graphics_file(self, name, val):
        """
        Updates the Active.sav file with the new graphics setting value.
        """
        header = name.encode('utf-8') + b'\x00\x0c\x00\x00\x00IntProperty\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00'
        a, b, c = self.active_sav_content.partition(header)
        c = val + c[1:]
        self.active_sav_content = a + b + c

    def get_graphics_setting(self):
        """
        Gets the graphics setting name from the hex value.
        """
        graphics_setting_hex = self.read_hex("BattleRenderQuality")
        graphics_setting_dict = {
            b'\x01': "Super Smooth",
            b'\x02': "Smooth",
            b'\x03': "Balanced",
            b'\x04': "HD",
            b'\x05': "HDR",
            b'\x06': "Ultra HD",
            b'\x07': "Extreme HDR"
        }
        return graphics_setting_dict.get(graphics_setting_hex, None)

    def get_fps(self):
        """
        Gets the FPS value from the Active.sav file.
        """
        fps_hex = self.read_hex("BattleFPS")
        fps_dict = {
            b"\x02": "Low",
            b"\x03": "Medium",
            b"\x04": "High",
            b"\x05": "Ultra",
            b"\x06": "Extreme",
            b"\x07": "Extreme+",
            b"\x08": "Ultra Extreme",
            b"\x09": "144fps [EXP]",
            b"\x0A": "165fps [EXP]",
            b"\x0B": "200fps [EXP]",
        }
        return fps_dict.get(fps_hex, None)

    def get_shadow(self):
        """
        Gets the shadow value from the UserCustom.ini file.
        """
        shadow_name = None
        user_custom_ini_path = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"
        self.adb.sync.pull(user_custom_ini_path, self.resource_path(r'assets\user_custom.ini'))

        with open(self.resource_path(r"assets\user_custom.ini")) as file:
            for line in file:
                line = line.strip()
                if line.startswith("+CVars=0B572A11181D160E280C1815100D0044"):
                    if int(line[-2:]) == 49:
                        shadow_name = "Disable"
                    elif int(line[-2:]) == 48:
                        shadow_name = "Enable"
                    break

        return shadow_name

    def set_shadow(self, value):
        """
        Set PUBG shadow preference by editing UserCustom.ini and pushing it via ADB.
        """
        normalized = str(value).strip().lower()
        shadow_value = {
            "on": 48,
            "off": 49,
            "enable": 48,
            "disable": 49,
        }.get(normalized)
        if shadow_value is None:
            return False

        user_custom_ini_path = (
            f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/"
            f"ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"
        )
        local_ini_path = self.resource_path(r"assets\user_custom.ini")

        try:
            self.adb.sync.pull(user_custom_ini_path, local_ini_path)
        except Exception:
            return False

        key_1 = "+CVars=0B572A11181D160E280C1815100D0044"
        key_2 = "+CVars=0B572C0A1C0B2A11181D160E2A0E100D1A1144"
        found_1 = False
        found_2 = False
        lines = []

        try:
            with open(local_ini_path, "r", encoding="utf-8", errors="ignore") as file:
                for line in file:
                    stripped = line.strip()
                    if stripped.startswith(key_1):
                        line = f"{key_1}{shadow_value}\n"
                        found_1 = True
                    elif stripped.startswith(key_2):
                        line = f"{key_2}{shadow_value}\n"
                        found_2 = True
                    lines.append(line)
        except Exception:
            return False

        if not found_1:
            lines.append(f"{key_1}{shadow_value}\n")
        if not found_2:
            lines.append(f"{key_2}{shadow_value}\n")

        try:
            with open(local_ini_path, "w", encoding="utf-8", errors="ignore") as file:
                file.writelines(lines)
            self.adb.sync.push(local_ini_path, user_custom_ini_path)
            return True
        except Exception:
            return False

    def get_graphics_style(self):
        """
        Gets the graphics style name from the hex value.
        :return: name of the graphics style
        """
        battle_style_hex = self.read_hex("BattleRenderStyle")
        battle_style_dict = {
            b'\x01': "Classic",
            b'\x02': "Colorful",
            b'\x03': "Realistic",
            b'\x04': "Soft",
            b'\x06': "Movie"
        }

        return battle_style_dict.get(battle_style_hex, "Not Found, It Will Be Added In A Future Release")

    def set_graphics_style(self, style):
        """
        Sets the graphics style.
        """
        battle_style_dict = {
            "Classic": b'\x01',
            "Colorful": b'\x02',
            "Realistic": b'\x03',
            "Soft": b'\x04',
            "Movie": b'\x06'
        }
        battle_style = battle_style_dict.get(style, "Not Found, It Will Be Added In A Future Release")
        self.change_graphics_file("BattleRenderStyle", battle_style)

    def set_graphics_quality(self, quality):
        """
        Sets the graphics quality for different game modes.
        """
        graphics_setting_dict = {
            "Super Smooth": b'\x01',
            "Smooth": b'\x02',
            "Balanced": b'\x03',
            "HD": b'\x04',
            "HDR": b'\x05',
            "Ultra HD": b'\x06',
            "Extreme HDR": b'\x07'
        }

        graphics_setting = graphics_setting_dict.get(quality, b'\x02')

        # Set the graphics quality
        graphics_files = ["ArtQuality", "LobbyRenderQuality", "BattleRenderQuality"]
        for value in graphics_files:
            self.change_graphics_file(value, graphics_setting)

    def apply_pc_ultra_cvars(self):
        """Apply PC-specific ultra graphics CVars to UserCustom.ini"""
        user_custom_path = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"

        # Pull current file
        self.adb.sync.pull(user_custom_path, self.resource_path(r'assets\user_custom.ini'))

        # PC Ultra CVars for maximum graphics
        pc_ultra_cvars = [
            "; === PC BEAST MODE GRAPHICS (EX Tool) ===",
            "+CVars=r.ViewDistanceScale=3",  # 3x view distance
            "+CVars=r.Streaming.PoolSize=3000",  # 3GB texture pool
            "+CVars=r.Shadow.MaxResolution=2048",  # 2K shadows
            "+CVars=r.PostProcessAAQuality=6",  # Ultra AA
            "+CVars=r.SkeletalMeshLODBias=-1",  # Better character models
            "+CVars=r.StaticMeshLODBias=-1",  # Better building models
            "+CVars=r.MaxAnisotropy=16",  # 16x anisotropic filtering
            "+CVars=r.BloomQuality=5",  # Max bloom
            "+CVars=r.ReflectionCaptureResolution=256",  # High-res reflections
            "+CVars=r.MotionBlurQuality=0",  # Disable motion blur
            "+CVars=fx.MaxCPUParticlesPerEmitter=2000",  # More particles
        ]

        # Read existing content
        with open(self.resource_path(r'assets\user_custom.ini'), 'r') as f:
            content = f.read()

        # Remove old PC CVars if they exist
        if "; === PC BEAST MODE GRAPHICS" in content:
            lines = content.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if "; === PC BEAST MODE GRAPHICS" in line:
                    skip = True
                elif skip and (line.startswith('[') or (line and not line.startswith('+CVars=') and not line.startswith(';'))):
                    skip = False
                if not skip:
                    new_lines.append(line)
            content = '\n'.join(new_lines)

        # Add PC CVars at the end
        with open(self.resource_path(r'assets\user_custom.ini'), 'w') as f:
            f.write(content.rstrip() + '\n\n')
            for cvar in pc_ultra_cvars:
                f.write(cvar + '\n')

        # Push back to device
        self.adb.sync.push(self.resource_path(r'assets\user_custom.ini'), user_custom_path)

    def apply_competitive_cvars(self):
        """Apply competitive visibility CVars (grass reduction, fog removal)"""
        user_custom_path = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"

        # Pull current file
        self.adb.sync.pull(user_custom_path, self.resource_path(r'assets\user_custom.ini'))

        # Competitive CVars for maximum visibility
        competitive_cvars = [
            "; === COMPETITIVE MODE (EX Tool) ===",
            "+CVars=foliage.DensityScale=0.2",  # Reduced grass
            "+CVars=r.Shadow.MaxResolution=512",  # Low shadows
            "+CVars=r.Fog=0",  # No fog
            "+CVars=r.VolumetricFog=0",  # No volumetric fog
            "+CVars=r.TonemapperGamma=2.5",  # Brighter
            "+CVars=r.Tonemapper.Sharpen=2",  # Very sharp
            "+CVars=r.MotionBlurQuality=0",  # No motion blur
            "+CVars=r.DepthOfFieldQuality=0",  # No depth of field
            "+CVars=r.ViewDistanceScale=3",  # Max view distance
        ]

        # Read existing content
        with open(self.resource_path(r'assets\user_custom.ini'), 'r') as f:
            content = f.read()

        # Remove old competitive CVars if they exist
        if "; === COMPETITIVE MODE" in content:
            lines = content.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if "; === COMPETITIVE MODE" in line:
                    skip = True
                elif skip and (line.startswith('[') or (line and not line.startswith('+CVars=') and not line.startswith(';'))):
                    skip = False
                if not skip:
                    new_lines.append(line)
            content = '\n'.join(new_lines)

        # Add competitive CVars at the end
        with open(self.resource_path(r'assets\user_custom.ini'), 'w') as f:
            f.write(content.rstrip() + '\n\n')
            for cvar in competitive_cvars:
                f.write(cvar + '\n')

        # Push back to device
        self.adb.sync.push(self.resource_path(r'assets\user_custom.ini'), user_custom_path)

    def set_pc_ultra_graphics(self):
        """PC-only ultra graphics settings via Gameloop registry"""
        # DirectX optimizations
        self.set_dword("ForceDirectX", 1)
        self.set_dword("FxaaQuality", 3)  # Max FXAA (mobile max is 2)
        self.set_dword("RenderOptimizeEnabled", 0)  # Disable optimization = max quality
        self.set_dword("LocalShaderCacheEnabled", 1)
        self.set_dword("ShaderCacheEnabled", 1)
        self.set_dword("VSyncEnabled", 0)  # Let GPU run free for max FPS

        # Content Scale - 3x for PC (mobile max is 2x)
        for version_key in self.pubg_versions.keys():
            content_scale_key = f"{version_key}_ContentScale"
            reg_content_scale = self.get_reg(content_scale_key)
            if reg_content_scale is not None:
                self.set_dword(content_scale_key, 3)  # 3x = Ultra sharp

    def set_ultra_resolution(self, width, height):
        """Set custom resolution for PC (1080p, 2K, 4K)"""
        self.set_dword("VMResWidth", width)
        self.set_dword("VMResHeight", height)

        # Set DPI based on resolution
        if width >= 3840:  # 4K
            dpi = 640
        elif width >= 2560:  # 2K
            dpi = 560
        else:  # 1080p
            dpi = 480

        self.set_dword("VMDPI", dpi)

    def apply_beast_mode(self):
        """BEAST MODE: Maximum graphics + Ultra Extreme FPS + 4K"""
        # Set Extreme HDR graphics
        self.set_graphics_quality("Extreme HDR")

        # Set max FPS
        self.set_fps("Ultra Extreme")

        # PC Ultra graphics registry settings
        self.set_pc_ultra_graphics()

        # 4K resolution
        self.set_ultra_resolution(3840, 2160)

        # Apply PC ultra CVars
        self.apply_pc_ultra_cvars()

    def apply_competitive_mode(self):
        """COMPETITIVE MODE: Max visibility + Ultra Extreme FPS"""
        # Low graphics for max FPS
        self.set_graphics_quality("Smooth")

        # Max FPS
        self.set_fps("Ultra Extreme")

        # 1080p for performance
        self.set_ultra_resolution(1920, 1080)

        # Disable VSync
        self.set_dword("VSyncEnabled", 0)

        # Apply competitive CVars
        self.apply_competitive_cvars()

    def apply_streamer_mode(self):
        """STREAMER MODE: High quality + Stable 60 FPS"""
        # High graphics
        self.set_graphics_quality("HDR")

        # Stable 60 FPS
        self.set_fps("High")

        # 1080p for streaming
        self.set_ultra_resolution(1920, 1080)

        # 2x content scale
        for version_key in self.pubg_versions.keys():
            content_scale_key = f"{version_key}_ContentScale"
            reg_content_scale = self.get_reg(content_scale_key)
            if reg_content_scale is not None:
                self.set_dword(content_scale_key, 2)

    def push_active_shadow_file(self):
        """
        Pushes the modified Active.sav & Shadow file to the device and restarts the game.
        """
        self.adb.shell(f"am force-stop {self.pubg_package}")
        sleep(0.2)

        data_dir = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved"

        files = [
            (self.resource_path(r"assets\active_modified.bin"), f"{data_dir}/SaveGames/Active.sav"),
            (self.resource_path(r"assets\user_custom.ini"), f"{data_dir}/Config/Android/UserCustom.ini")
        ]

        for src, dest in files:
            self.adb.sync.push(src, dest)
            sleep(0.2)

    def start_app(self):
        package = f"{self.pubg_package}/com.epicgames.ue4.SplashActivity"
        self.adb.shell(f"am start -n {package}")

    def kr_fullhd(self):
        def backup_folder(path):
            backup_path = path + '.backup'

            output = self.adb.shell(f"[ -d {path} ] && echo 1 || echo 0").strip()
            backup_output = self.adb.shell(f"[ -d {backup_path} ] && echo 1 || echo 0").strip()
            if backup_output == '0' and output == '1':
                self.adb.shell(['mv', path, backup_path])
            elif backup_output == '1' and output == '1':
                self.adb.shell(['rm', '-r', path])

        def restore_folder(path):
            backup_path = path + '.backup'
            backup_output = self.adb.shell(f"[ -d {backup_path} ] && echo 1 || echo 0").strip()
            if backup_output == '1':
                self.adb.shell(['mv', backup_path, path])

        data_path = f"/sdcard/Android/data/{self.pubg_package}"
        obb_path = f"/sdcard/Android/obb/{self.pubg_package}"
        user_custom_ini_path = f"{data_path}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"

        safe_path = "/sdcard/ex_safe_folder"
        data_path_for_account = f"/data/data/{self.pubg_package}"

        self.adb.push(self.resource_path('assets/ex_kr.ini'), user_custom_ini_path)

        self.adb.shell(f"mkdir -p {safe_path}")
        self.adb.shell(f"cp -r {data_path_for_account}/shared_prefs {safe_path}/shared_prefs")
        self.adb.shell(f"cp -r {data_path_for_account}/databases {safe_path}/databases")

        backup_folder(data_path)
        backup_folder(obb_path)

        self.adb.shell(['pm', 'clear', self.pubg_package])
        self.adb.shell(['pm', 'grant', self.pubg_package, 'android.permission.READ_EXTERNAL_STORAGE'])
        self.adb.shell(['pm', 'grant', self.pubg_package, 'android.permission.WRITE_EXTERNAL_STORAGE'])

        restore_folder(data_path)
        restore_folder(obb_path)

        self.adb.shell(f"cp -r {safe_path}/shared_prefs {data_path_for_account}/shared_prefs")
        self.adb.shell(f"cp -r {safe_path}/databases {data_path_for_account}/databases")

        self.start_app()

        self.adb.shell(f"rm -r {safe_path}")
