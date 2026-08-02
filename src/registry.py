import winreg
from typing import Any, Optional
from .constants import REG_PATH, REG_LOCAL_PATH

class RegistryManager:
    """Helper class for Windows Registry read/write operations for GameLoop."""
    
    @staticmethod
    def get_user_reg(name: str, subpath: str = "") -> Optional[Any]:
        target_path = rf"{REG_PATH}\{subpath}".strip('\\') if subpath else REG_PATH
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, target_path, 0, winreg.KEY_READ) as key:
                val, _ = winreg.QueryValueEx(key, name)
                return val
        except OSError:
            return None

    @staticmethod
    def get_local_reg(name: str, path: str = "AppMarket") -> Optional[Any]:
        target_path = rf"{REG_LOCAL_PATH}\{path}"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, target_path, 0, winreg.KEY_READ) as key:
                val, _ = winreg.QueryValueEx(key, name)
                return val
        except OSError:
            return None

    @staticmethod
    def set_user_dword(name: str, value: int, subpath: str = "") -> bool:
        target_path = rf"{REG_PATH}\{subpath}".strip('\\') if subpath else REG_PATH
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, target_path) as key:
                winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(value))
            return True
        except OSError:
            return False

    @staticmethod
    def set_user_string(name: str, value: str, subpath: str = "") -> bool:
        target_path = rf"{REG_PATH}\{subpath}".strip('\\') if subpath else REG_PATH
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, target_path) as key:
                winreg.SetValueEx(key, name, 0, winreg.REG_SZ, str(value))
            return True
        except OSError:
            return False
