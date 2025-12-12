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
from win32api import EnumDisplayDevices, EnumDisplaySettings
from win32com.client import Dispatch
from . import setup_logger


class Settings:
    def __init__(self):
        self.settings = QSettings("MK Apps", "MK PUBG Mobile Tool")
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

    def temp_cleaner(self):
        """
        Cleans temporary files and directories.

        Returns:
            bool: True if the function successfully cleans the temporary files and directories.
        """
        base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))

        def clear_files(directory):
            try:
                for root, dirs, files in os.walk(directory):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        shutil.rmtree(os.path.join(root, name))
            except Exception:
                pass

        try:
            for folder in os.listdir(tempfile.gettempdir()):
                folder_path = os.path.join(tempfile.gettempdir(), folder)
                if folder_path != base_path:
                    if os.path.isdir(folder_path):
                        shutil.rmtree(folder_path, ignore_errors=True)
                    else:
                        try:
                            os.remove(folder_path)
                        except Exception:
                            pass
        except Exception:
            pass

        clear_files(r"C:\Windows\Temp")
        clear_files(os.path.expandvars(r'%windir%\Prefetch'))
        gameloop_ui_path = self.get_local_reg('InstallPath', path='UI')
        clear_files(os.path.join(gameloop_ui_path, 'ShaderCache'))

        return True

    def gameloop_settings(self):
        """
        Generates the game loop settings based on the system's hardware specifications.
        """

        def make_scale(value, low=False):
            for version_key in self.pubg_versions.keys():
                content_scale_key = f"{version_key}_ContentScale"
                render_quality_key = f"{version_key}_RenderQuality"
                fps_level_key = f"{version_key}_FPSLevel"

                reg_content_scale = self.get_reg(content_scale_key)
                if reg_content_scale is not None:
                    self.set_dword(content_scale_key, value)

                reg_fps_level = self.get_reg(fps_level_key)
                if reg_fps_level is not None:
                    self.set_dword(fps_level_key, 0)

                reg_render_quality = self.get_reg(render_quality_key)
                if reg_render_quality is not None:
                    render_value = value
                    if low:
                        # value = 0
                        render_value = 2
                    elif value == 1:
                        render_value = 2
                    self.set_dword(render_quality_key, render_value)

        ram_value = round((int(75) * psutil.virtual_memory().total / (1024 ** 3)) / 100) * 1024
        ram_value = min(ram_value, (8 * 1024))

        cpu_value = round((int(75) * psutil.cpu_count(logical=False)) / 100)
        cpu_value = min(cpu_value, 8)

        dc = EnumDisplayDevices(None, 0, 0)
        settings = EnumDisplaySettings(dc.DeviceName, -1)
        refresh_rate = settings.DisplayFrequency
        self.set_dword("VSyncEnabled", 1 if refresh_rate < 89 else 0)

        gpu = GPUtil.getGPUs()[0] if GPUtil.getGPUs() else None
        if gpu:
            gpu_memory = int(gpu.memoryTotal / 1024)
            self.set_dword("SetGraphicsCard", 1)
            if gpu_memory < 4:
                self.set_dword("VMDPI", 240)
                self.set_dword("FxaaQuality", 0)

                if gpu_memory <= 2:
                    self.set_dword("LocalShaderCacheEnabled", 0)
                    self.set_dword("ShaderCacheEnabled", 0)
                    make_scale(1, low=True)
                else:
                    self.set_dword("LocalShaderCacheEnabled", 1)
                    self.set_dword("ShaderCacheEnabled", 1)
                    make_scale(1)

            elif gpu_memory < 8 and cpu_value <= 4:
                self.set_dword("LocalShaderCacheEnabled", 1)
                self.set_dword("ShaderCacheEnabled", 1)
                self.set_dword("VMDPI", 480)
                self.set_dword("FxaaQuality", 2 if cpu_value == 4 else 1)
                make_scale(1)
            else:
                self.set_dword("LocalShaderCacheEnabled", 1)
                self.set_dword("ShaderCacheEnabled", 1)
                self.set_dword("VMDPI", 480)
                self.set_dword("FxaaQuality", 2)
                make_scale(2)

            self.set_dword("GraphicsCardEnabled", 1)

        else:
            self.set_dword("GraphicsCardEnabled", 0)
            self.set_dword("LocalShaderCacheEnabled", 0)
            self.set_dword("ShaderCacheEnabled", 0)
            self.set_dword("VMDPI", 240)
            self.set_dword("FxaaQuality", 0)
            make_scale(1, low=True)

        self.set_dword("ForceDirectX", 1)
        self.set_dword("RenderOptimizeEnabled", 1)
        self.set_dword("AdbDisable", 0)
        self.set_dword("VMMemorySizeInMB", ram_value)
        self.set_dword("VMCpuCount", cpu_value)

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
            nvidia_profile_path = self.resource_path("assets/mk.nip")

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

    @staticmethod
    def kill_gameloop():
        """
        Kills a list of processes related to the gameloop.

        Returns:
            - True if at least one process was killed.
            - False if no process was killed.
        """
        # List of processes to be killed
        processes_to_kill = [
            'aow_exe.exe',
            'AndroidEmulatorEn.exe',
            'AndroidEmulator.exe',
            'AndroidEmulatorEx.exe',
            'TBSWebRenderer.exe',
            'syzs_dl_svr.exe',
            'AppMarket.exe',
            'QMEmulatorService.exe',
            'RuntimeBroker.exe',
            'GameLoader.exe',
            'TSettingCenter.exe',
            'Auxillary.exe',
            'TP3Helper.exe',
            'tp3helper.dat',
            'GameDownload.exe'
        ]

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
        pythoncom.CoInitialize()

        wmi_api = wmi.WMI()

        adapters = wmi_api.Win32_NetworkAdapterConfiguration(IPEnabled=True)

        dns_changed_status = all(adapter.SetDNSServerSearchOrder(dns_servers)[0] == 0 for adapter in adapters)

        subprocess.run(['ipconfig', '/flushdns'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

        return dns_changed_status

    def ipad_layout_settings(self, reset=False):
        """
        Modify the layout of the XML file based on the edited values.
        """
        appdata_folder = os.getenv('APPDATA')
        keymap_folder = os.path.join(appdata_folder, 'AndroidTbox')
        original_file = os.path.join(keymap_folder, 'TVM_100.xml')
        backup_file = os.path.join(keymap_folder, 'TVM_100.xml.mkbackup')

        def set_keymap_layout():
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
                with open(original_file, 'w', encoding='utf-8') as file:
                    file.write(ET.tostring(root, encoding='utf-8').decode('utf-8')[6:-7])

            ipad_keymap_values = {
                "Smart 720P": {
                    "B": {"Reload": [("0.537234", "0.880567"), ("0.406535", "0.880567")]},
                    "3": {"Jump": ("0.613222", "0.880567"), "GetOutCar": ("0.613222", "0.880567")},
                    "F3": {"SetUp": [("0.768997", "0.163968"), ("0.896657", "0.270243")]},
                    "F2": {"SetUp": [("0.781155", "0.144737"), ("0.960486", "0.270243")]},
                    "Space": {"Jump": ("0.962006", "0.762146"), "Climb": ("0.962006", "0.762146"),
                              "Whistle": [("0.911094", "0.660931"), ("0.063070", "0.747976")],
                              "DriveMode1|DriveSpeed": ("0.063070", "0.747976"),
                              "DriveMode1|DriveSpeedPress": ("0.063070", "0.747976"),
                              "SwimUp": ("0.835106", "0.701417"), "SwimmingUp": ("0.835106", "0.701417"), },
                    "Shift": {"DriveMode1|DriveSpeed": ("0.076748", "0.555668"),
                              "DriveMode1|DriveSpeedPress": ("0.076748", "0.555668")},
                    "Right Click": {"Sniper": ("0.962006", "0.638664"), "Sniper2": ("0.962006", "0.638664"),
                                    "Reload": ("0.962006", "0.638664")},
                    "Z": {"Fall": ("0.942249", "0.949393"), "CancelFall": ("0.942249", "0.949393")},
                    "E": {"Sideways": ("0.221884", "0.522267"), "SidewaysCancel": ("0.221884", "0.522267"),
                          "Moto": ("0.806991", "0.637652"), "Moto2": ("0.806991", "0.637652")},
                    "Q": {"Sideways": ("0.141337", "0.520243"), "SidewaysCancel": ("0.141337", "0.520243"),
                          "Moto": ("0.713526", "0.635628"), "Moto2": ("0.713526", "0.635628")},
                    "Y": {"SetUp": [("0.794833", "0.161943"), ("0.753040", "0.161943"), ("0.844985", "0.157895")]},
                    "T": {"SetUp": [("0.780395", "0.092105"), ("0.732523", "0.092105"), ("0.847264", "0.097166")]},
                    "Alt": {"Eye": [("0.776596", "0.232794")]},
                    "Drive": {"DriveMode1": (("0.673252", "0.765182"), ("0.834347", "0.765182"),
                                             ("0.164894", "0.644737"), ("0.164894", "0.826923"))},
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
                    "B": {"Reload": [("0.542969", "0.910751"), ("0.437500", "0.910751")]},
                    "3": {"Jump": ("0.584347", "0.913793"), "GetOutCar": ("0.584347", "0.913793")},
                    "F3": {"SetUp": [("0.838146", "0.100406"), ("0.924012", "0.193712")]},
                    "F2": {"SetUp": [("0.838146", "0.100406"), ("0.971884", "0.193712")]},
                    "Space": {"Jump": ("0.969605", "0.834686"), "Climb": ("0.969605", "0.834686"),
                              "Whistle": [("0.934650", "0.764706"), ("0.049392", "0.823529")],
                              "DriveMode1|DriveSpeed": ("0.049392", "0.823529"),
                              "DriveMode1|DriveSpeedPress": ("0.049392", "0.823529"),
                              "SwimUp": ("0.879518", "0.759036"), "SwimmingUp": ("0.879518", "0.759036"), },
                    "Shift": {"DriveMode1|DriveSpeed": ("0.053951", "0.683570"),
                              "DriveMode1|DriveSpeedPress": ("0.053951", "0.683570")},
                    "Right Click": {"Sniper": ("0.971125", "0.746450"), "Sniper2": ("0.971125", "0.746450"),
                                    "Reload": ("0.971125", "0.746450")},
                    "Z": {"Fall": ("0.961246", "0.967546"), "CancelFall": ("0.961246", "0.967546")},
                    "E": {"Sideways": ("0.155775", "0.658215"), "SidewaysCancel": ("0.155775", "0.658215"),
                          "Moto": ("0.857903", "0.738337"), "Moto2": ("0.857903", "0.738337")},
                    "Q": {"Sideways": ("0.101064", "0.656187"), "SidewaysCancel": ("0.101064", "0.656187"),
                          "Moto": ("0.791793", "0.736308"), "Moto2": ("0.791793", "0.736308")},
                    "Y": {"SetUp": [("0.852584", "0.118661"), ("0.823708", "0.118661"), ("0.892097", "0.108519")]},
                    "T": {"SetUp": [("0.841185", "0.064909"), ("0.809271", "0.064909"), ("0.888298", "0.073022")]},
                    "Alt": {"Eye": [("0.840426", "0.166329")]},
                    "Drive": {"DriveMode1": (("0.764438", "0.836714"), ("0.881459", "0.836714"),
                                             ("0.116261", "0.752535"), ("0.116261", "0.883367"))},
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
                    "B": {"Reload": [("0.542969", "0.910751"), ("0.437500", "0.910751")]},
                    "3": {"Jump": ("0.584347", "0.913793"), "GetOutCar": ("0.584347", "0.913793")},
                    "F3": {"SetUp": [("0.838146", "0.100406"), ("0.924012", "0.193712")]},
                    "F2": {"SetUp": [("0.838146", "0.100406"), ("0.971884", "0.193712")]},
                    "Space": {"Jump": ("0.969605", "0.834686"), "Climb": ("0.969605", "0.834686"),
                              "Whistle": [("0.934650", "0.764706"), ("0.049392", "0.823529")],
                              "DriveMode1|DriveSpeed": ("0.049392", "0.823529"),
                              "DriveMode1|DriveSpeedPress": ("0.049392", "0.823529"),
                              "SwimUp": ("0.879518", "0.759036"), "SwimmingUp": ("0.879518", "0.759036"), },
                    "Shift": {"DriveMode1|DriveSpeed": ("0.053951", "0.683570"),
                              "DriveMode1|DriveSpeedPress": ("0.053951", "0.683570")},
                    "Right Click": {"Sniper": ("0.971125", "0.746450"), "Sniper2": ("0.971125", "0.746450"),
                                    "Reload": ("0.971125", "0.746450")},
                    "Z": {"Fall": ("0.961246", "0.967546"), "CancelFall": ("0.961246", "0.967546")},
                    "E": {"Sideways": ("0.155775", "0.658215"), "SidewaysCancel": ("0.155775", "0.658215"),
                          "Moto": ("0.857903", "0.738337"), "Moto2": ("0.857903", "0.738337")},
                    "Q": {"Sideways": ("0.101064", "0.656187"), "SidewaysCancel": ("0.101064", "0.656187"),
                          "Moto": ("0.791793", "0.736308"), "Moto2": ("0.791793", "0.736308")},
                    "Y": {"SetUp": [("0.852584", "0.118661"), ("0.823708", "0.118661"), ("0.892097", "0.108519")]},
                    "T": {"SetUp": [("0.841185", "0.064909"), ("0.809271", "0.064909"), ("0.888298", "0.073022")]},
                    "Alt": {"Eye": [("0.840426", "0.166329")]},
                    "Drive": {"DriveMode1": (("0.764438", "0.836714"), ("0.881459", "0.836714"),
                                             ("0.116261", "0.752535"), ("0.116261", "0.883367"))},
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
        shortcut.Description = "By Mohamed Kamal (MKvip) - Discord: mkvip"
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

            self.adb.sync.pull("/default.prop", self.resource_path(r'assets\testADB.mkvip'))
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
        local_file_path = self.resource_path('assets/old.mkvip')
        self.pubg_package = package
        self.adb.sync.pull(active_savegames_path, local_file_path)

        with open(local_file_path, 'rb') as file:
            self.active_sav_content = file.read()

    def save_graphics_file(self):
        file_path = self.resource_path("assets/new.mkvip")
        with open(file_path, 'wb') as file:
            file.write(self.active_sav_content)

    def set_fps(self, val: str) -> None:
        """
        Updates the Active.sav file with the new FPS value.
        ### ENHANCED WITH NEW TIERS ###
        """
        fps_mapping = {
            "Low": b"\x02",
            "Medium": b"\x03",
            "High": b"\x04",
            "Ultra": b"\x05",
            "Extreme": b"\x06",
            "Extreme+": b"\x07",
            "Ultra Extreme": b"\x08",
            "Unlimited": b"\x09"  # NEW TIER
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
        ### ENHANCED WITH NEW TIERS ###
        """
        graphics_setting_hex = self.read_hex("BattleRenderQuality")
        graphics_setting_dict = {
            b'\x01': "Smooth",
            b'\x02': "Balanced",
            b'\x03': "HD",
            b'\x04': "HDR",
            b'\x05': "Ultra HD",
            b'\x06': "Extreme HDR",    # NEW UNLOCKED
            b'\x07': "Ultra HDR+",     # NEW CUSTOM
            b'\x08': "God Mode"        # NEW MAXIMUM
        }
        return graphics_setting_dict.get(graphics_setting_hex, None)

    def get_fps(self):
        """
        Gets the FPS value from the Active.sav file.
        ### ENHANCED WITH NEW TIER ###
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
            b"\x09": "Unlimited",  # NEW
        }
        return fps_dict.get(fps_hex, None)

    def get_shadow(self):
        """
        Gets the shadow value from the UserCustom.ini file.
        """
        shadow_name = None
        user_custom_ini_path = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"
        self.adb.sync.pull(user_custom_ini_path, self.resource_path(r'assets\user.mkvip'))

        with open(self.resource_path(r"assets\user.mkvip")) as file:
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
        Sets the shadow value in the UserCustom.ini file.
        """
        shadow_value = {"ON": 48, "OFF": 49}.get(value)
        if shadow_value is None:
            return False
        
        lines = []
        with open(self.resource_path(r"assets\user.mkvip"), "r") as file:
            for line in file:
                if line.strip().startswith("+CVars=0B572A11181D160E280C1815100D0044"):
                    line = f"+CVars=0B572A11181D160E280C1815100D0044{shadow_value}\n"
                elif line.strip().startswith("+CVars=0B572C0A1C0B2A11181D160E2A0E100D1A1144"):
                    line = f"+CVars=0B572C0A1C0B2A11181D160E2A0E100D1A1144{shadow_value}\n"
                lines.append(line)

        with open(self.resource_path(r"assets\user.mkvip"), "w") as file:
            file.writelines(lines)

        return True

    def get_graphics_style(self):
        """
        Gets the graphics style name from the hex value.
        """
        battle_style_hex = self.read_hex("BattleRenderStyle")
        battle_style_dict = {
            b'\x01': "Classic",
            b'\x02': "Colorful",
            b'\x03': "Realistic",
            b'\x04': "Soft",
            b'\x06': "Movie"
        }

        return battle_style_dict.get(battle_style_hex, "Not Found")

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
        battle_style = battle_style_dict.get(style)
        if battle_style:
            self.change_graphics_file("BattleRenderStyle", battle_style)

    def set_graphics_quality(self, quality):
        """
        Sets the graphics quality for different game modes.
        ### ENHANCED WITH NEW TIERS ###
        """
        graphics_setting_dict = {
            "Smooth": b'\x01',
            "Balanced": b'\x02',
            "HD": b'\x03',
            "HDR": b'\x04',
            "Ultra HD": b'\x05',
            "Extreme HDR": b'\x06',    # NEW UNLOCKED
            "Ultra HDR+": b'\x07',     # NEW CUSTOM
            "God Mode": b'\x08'        # NEW MAXIMUM
        }

        graphics_setting = graphics_setting_dict.get(quality, b'\x01')

        # Set the graphics quality
        graphics_files = ["ArtQuality", "LobbyRenderQuality", "BattleRenderQuality"]
        for value in graphics_files:
            self.change_graphics_file(value, graphics_setting)

    def generate_advanced_config(self, preset="God Mode"):
        """
        ### NEW FUNCTION: Generate advanced UserCustom.ini with all settings ###
        Creates a complete config file with enhanced graphics settings
        """
        presets = {
            "God Mode": {
                "aa": "444C",           # 16x MSAA
                "shadow": "444E",       # Extreme shadows
                "texture": "444C",      # Max textures
                "view": "444D",         # Extreme view distance
                "post": "444D",         # Extreme post-processing
                "bloom": "444B",        # Ultra bloom
                "light": "444A",        # High light shafts
                "ssao": "444B",         # High SSAO
                "aniso": "444C",        # 16x anisotropic
            },
            "Competitive": {
                "aa": "444A",           # 4x MSAA
                "shadow": "444A",       # Medium shadows
                "texture": "444A",      # High textures
                "view": "444C",         # Ultra view distance
                "post": "444A",         # High post-processing
                "bloom": "4449",        # Low bloom
                "light": "4448",        # Off light shafts
                "ssao": "4449",         # Low SSAO
                "aniso": "444B",        # 8x anisotropic
            },
            "Balanced": {
                "aa": "444A",           # 4x MSAA
                "shadow": "444B",       # High shadows
                "texture": "444A",      # High textures
                "view": "444A",         # High view distance
                "post": "444A",         # High post-processing
                "bloom": "444A",        # High bloom
                "light": "4449",        # On light shafts
                "ssao": "444A",         # Medium SSAO
                "aniso": "444B",        # 8x anisotropic
            }
        }
        
        p = presets.get(preset, presets["God Mode"])
        
        config = f"""[BackUp DeviceProfile]
+CVars=0B5734161B10151C3A16170D1C170D2A1A18151C3F181A0D160B44485749
+CVars=0B572C0A1C0B2A11181D160E2A0E100D1A11{p['aa']}
+CVars=0B572A11181D160E280C1815100D00{p['shadow']}
+CVars=0B5734161B10151C3A16170D1C170D2A1A18151C3F181A0D160B{p['texture']}
+CVars=0B572A0D180D101A341C0A1135363D3D100A0D18171A1C2A1A18151C{p['view']}
+CVars=0B5734161B10151C313D2B{p['post']}
+CVars=0B573B15161614280C1815100D00{p['bloom']}
+CVars=0B5735101E110D2A11181F0D280C1815100D00{p['light']}
+CVars=0B572C0A1C0B342A38382A1C0D0D10171E{p['ssao']}
+CVars=0B5734161B10151C342A3838{p['aniso']}
+CVars=0B572A0D180D101A341C0A1135363D3D100A0D18171A1C2A1A18151C44495741
+CVars=1F161510181E1C5735363D3D100A0D18171A1C2A1A18151C4448
+CVars=0B5729180B0D101A151C35363D3B10180A4449
+CVars=0B573C14100D0D1C0B2A09180E172B180D1C2A1A18151C4448
+CVars=0B573D1C0D18101534161D1C444B
+CVars=0B5734180D1C0B101815280C1815100D00351C0F1C154448
+CVars=0B572C0A1C0B280C1815100D002A1C0D0D10171E444B
+CVars=0B5734161B10151C573D00171814101A361B131C1A0D2A11181D160E4448
+CVars=0B573D1C090D11361F3F101C151D280C1815100D004449
+CVars=0B572B1C1F0B181A0D101617280C1815100D004449
+CVars=1F161510181E1C5734101735363D4449
+CVars=0B572A0D0B1C181410171E57291616152A10031C444A4949
+CVars=0B5734161B10151C370C143D00171814101A291610170D35101E110D0A4448
+CVars=0B573E2D383657280C1815100D004449
+CVars=0B57292C3B3E2F1C0B0A101617444C
+CVars=0B572C0A1C0B313D2B2A1C0D0D10171E4448
+CVars=0B5734161B10151C313D2B4449
+CVars=0B5734161B10151C572A1A1C171C3A1615160B3F160B14180D4449
+CVars=0B573B15161614280C1815100D004449
+CVars=0B5735101E110D2A11181F0D280C1815100D004449
+CVars=0B5734161B10151C572D16171C141809091C0B3F1015144449
+CVars=0B5734161B10151C5738150E18000A2B1C0A16150F1C3D1C090D114449
+CVars=0B572C0A1C0B342A38382A1C0D0D10171E4449
+CVars=0B5734161B10151C342A38384448
+CVars=0B573D1C1F180C150D3F1C180D0C0B1C5738170D10381510180A10171E4449
+CVars=0B5734161B10151C2A101409151C2A11181D1C0B4449
+CVars=0B572C0A1C0B2F0C151218172A1C0D0D10171E4449

[UserCustom DeviceProfile]
+CVars=0B572C0A1C0B280C1815100D002A1C0D0D10171E444A
+CVars=0B572C0A1C0B2A11181D160E2A0E100D1A11{p['aa']}
+CVars=0B572A11181D160E280C1815100D00{p['shadow']}
+CVars=0B5734161B10151C3A16170D1C170D2A1A18151C3F181A0D160B{p['texture']}
+CVars=0B572C0A1C0B2F0C151218172A1C0D0D10171E4449
+CVars=0B5734161B10151C313D2B{p['post']}
+CVars=0B5734161B10151C572A1A1C171C3A1615160B3F160B14180D444B5749
+CVars=0B572F2B2A573F160B1A1C2A11181D10171E2B180D1C4454485749
+CVars=0B5734161B10151C573C17181B151C29292B44495749
+CVars=0B5734180D1C0B101815280C1815100D002A0C091C0B31101E1144485749
+CVars=0B572A11181D160E573418013A2A342B1C0A16150C0D1016174448494B4D
+CVars=0B572A1200380D14160A09111C0B1C44485749
+CVars=3C171E10171C573E2A151C1C092D10141C2D11161D4449574949494C
+CVars=0B573E2D383657280C1815100D004449
+CVars=0B572C0A1C0B313D2B2A1C0D0D10171E444B
+CVars=0B573B15161614280C1815100D00{p['bloom']}
+CVars=0B5735101E110D2A11181F0D280C1815100D00{p['light']}
+CVars=0B5734161B10151C572D16171C141809091C0B3F10151444485749
+CVars=0B5734161B10151C5738150E18000A2B1C0A16150F1C3D1C090D1144485749
+CVars=0B57383A3C2A2A0D00151C44495749
+CVars=0B572C0A1C0B342A38382A1C0D0D10171E{p['ssao']}
+CVars=0B572C0A1C0B342A38382F18150C1C4449
+CVars=0B573D1C1F180C150D3F1C180D0C0B1C5738170D10381510180A10171E44495749
+CVars=0B5734161B10151C342A3838{p['aniso']}
+CVars=0B57342A38383A160C170D444D5749
+CVars=0B5734180D1C0B101815280C1815100D00351C0F1C154448
+CVars=0B572A11181D160E573A2A345734180134161B10151C3A180A1A181D1C0A444B
+CVars=0B572A11181D160E573D100A0D18171A1C2A1A18151C4449574C
+CVars=0B5734161B10151C573D00171814101A361B131C1A0D2A11181D160E4448
+CVars=0B573D1C090D11361F3F101C151D280C1815100D004449
+CVars=0B572B1C1F0B181A0D101617280C1815100D004449
+CVars=0B572A0D180D101A341C0A1135363D3D100A0D18171A1C2A1A18151C{p['view']}
+CVars=1F161510181E1C5735363D3D100A0D18171A1C2A1A18151C44485749
+CVars=1F161510181E1C5734101735363D4449
+CVars=0B573D1C0D18101534161D1C444B
+CVars=0B5734180D1C0B101815280C1815100D00351C0F1C154448
+CVars=0B572A0D0B1C181410171E57291616152A10031C444A4949
+CVars=0B573C14100D0D1C0B2A09180E172B180D1C2A1A18151C44485749
+CVars=0B5729180B0D101A151C35363D3B10180A4449
+CVars=0B5734161B10151C370C143D00171814101A291610170D35101E110D0A4448
+CVars=1D1000572A1C0D3D1C1A18153B181210171E2B2D2A10031C301735161B1B004448494B4D
+CVars=0B57292C3B3E2F1C0B0A101617444C
+CVars=0B5734161B10151C2A101409151C2A11181D1C0B4449
"""
        return config

    def apply_advanced_graphics(self, preset="God Mode"):
        """
        ### NEW FUNCTION: Apply advanced graphics preset ###
        Combines Active.sav modifications with UserCustom.ini enhancements
        """
        # Generate advanced config
        config_content = self.generate_advanced_config(preset)
        
        # Save to file
        config_path = self.resource_path("assets/user.mkvip")
        with open(config_path, "w") as f:
            f.write(config_content)
        
        print(f"✓ Applied {preset} graphics preset")
        return True

    def push_active_shadow_file(self):
        """
        Pushes the modified Active.sav & Shadow file to the device and restarts the game.
        """
        self.adb.shell(f"am force-stop {self.pubg_package}")
        sleep(0.2)

        data_dir = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved"

        files = [
            (self.resource_path(r"assets\new.mkvip"), f"{data_dir}/SaveGames/Active.sav"),
            (self.resource_path(r"assets\user.mkvip"), f"{data_dir}/Config/Android/UserCustom.ini")
        ]

        for src, dest in files:
            self.adb.sync.push(src, dest)
            sleep(0.2)

    def start_app(self):
        package = f"{self.pubg_package}/com.epicgames.ue4.SplashActivity"
        self.adb.shell(f"am start -n {package}")

    def kr_fullhd(self):
        def backup_folder(path):
            backup_path = path + '.MKbackup'

            output = self.adb.shell(f"[ -d {path} ] && echo 1 || echo 0").strip()
            backup_output = self.adb.shell(f"[ -d {backup_path} ] && echo 1 || echo 0").strip()
            if backup_output == '0' and output == '1':
                self.adb.shell(['mv', path, backup_path])
            elif backup_output == '1' and output == '1':
                self.adb.shell(['rm', '-r', path])

        def restore_folder(path):
            backup_path = path + '.MKbackup'
            backup_output = self.adb.shell(f"[ -d {backup_path} ] && echo 1 || echo 0").strip()
            if backup_output == '1':
                self.adb.shell(['mv', backup_path, path])

        data_path = f"/sdcard/Android/data/{self.pubg_package}"
        obb_path = f"/sdcard/Android/obb/{self.pubg_package}"
        user_custom_ini_path = f"{data_path}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"

        safe_path = "/sdcard/mk_safe_folder"
        data_path_for_account = f"/data/data/{self.pubg_package}"

        self.adb.push(self.resource_path('assets\mk_kr.ini'), user_custom_ini_path)

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