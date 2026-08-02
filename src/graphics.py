import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Tuple, Dict, List
import adbutils

from .constants import get_app_data_dir, PUBG_VERSIONS
from .registry import RegistryManager

class GraphicsManager:
    """Handles PUBG Mobile binary active.sav editing, config inis, and ADB sync."""

    def __init__(self):
        self.pubg_package: Optional[str] = None
        self.active_sav_content: bytes = b""

    def get_writable_path(self, filename: str) -> str:
        return str(get_app_data_dir() / filename)

    def fetch_graphics_file(self, adb_device: adbutils.AdbDevice, package: str) -> bool:
        """Pulls Active.sav from device for target PUBG package."""
        self.pubg_package = package
        active_remote_path = f"/sdcard/Android/data/{package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/Active.sav"
        local_original_path = self.get_writable_path("active_original.bin")
        try:
            adb_device.sync.pull(active_remote_path, local_original_path)
            with open(local_original_path, 'rb') as f:
                self.active_sav_content = f.read()
            return True
        except Exception:
            return False

    def save_graphics_file(self) -> bool:
        """Saves current modified buffer to active_modified.bin."""
        file_path = self.get_writable_path("active_modified.bin")
        try:
            with open(file_path, 'wb') as f:
                f.write(self.active_sav_content)
            return True
        except Exception:
            return False

    def push_graphics_to_device(self, adb_device: adbutils.AdbDevice) -> bool:
        """Pushes active_modified.bin back to GameLoop device."""
        if not self.pubg_package or not adb_device:
            return False
        local_file_path = self.get_writable_path("active_modified.bin")
        remote_file_path = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/Active.sav"
        try:
            if os.path.exists(local_file_path):
                adb_device.sync.push(local_file_path, remote_file_path)
                return True
        except Exception:
            pass
        return False

    def set_graphics_quality(self, val: str) -> None:
        quality_mapping = {
            "Super Smooth": b"\x01",
            "Smooth": b"\x02",
            "Balanced": b"\x03",
            "HD": b"\x04",
            "HDR": b"\x05",
            "Ultra HD": b"\x06",
            "Extreme HDR": b"\x07"
        }
        val_byte = quality_mapping.get(val)
        if val_byte and self.active_sav_content:
            header = b'BattleRenderQuality\x00\x0c\x00\x00\x00IntProperty\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00'
            before, sep, after = self.active_sav_content.partition(header)
            if sep:
                after = val_byte + after[1:]
                self.active_sav_content = before + sep + after

    def set_fps(self, val: str) -> None:
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
        val_byte = fps_mapping.get(val)
        if val_byte and self.active_sav_content:
            for prop in ["FPSLevel", "BattleFPS", "LobbyFPS"]:
                header = prop.encode('utf-8') + b'\x00\x0c\x00\x00\x00IntProperty\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00'
                before, sep, after = self.active_sav_content.partition(header)
                if sep:
                    after = val_byte + after[1:]
                    self.active_sav_content = before + sep + after

    def set_style(self, style_name: str) -> None:
        style_mapping = {
            "Classic": b"\x01",
            "Colorful": b"\x02",
            "Realistic": b"\x03",
            "Soft": b"\x04",
            "Movie": b"\x06"
        }
        val_byte = style_mapping.get(style_name)
        if val_byte and self.active_sav_content:
            header = b'BattleRenderStyle\x00\x0c\x00\x00\x00IntProperty\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00'
            before, sep, after = self.active_sav_content.partition(header)
            if sep:
                after = val_byte + after[1:]
                self.active_sav_content = before + sep + after

    def _read_hex_property(self, name: str) -> bytes:
        if not self.active_sav_content:
            return b""
        header = name.encode('utf-8') + b'\x00\x0c\x00\x00\x00IntProperty\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00'
        _, _, content = self.active_sav_content.partition(header)
        return content[:1]

    def get_graphics_setting(self) -> Optional[str]:
        val_hex = self._read_hex_property("BattleRenderQuality")
        return {
            b'\x01': "Super Smooth",
            b'\x02': "Smooth",
            b'\x03': "Balanced",
            b'\x04': "HD",
            b'\x05': "HDR",
            b'\x06': "Ultra HD",
        }.get(val_hex, "Smooth")

    def get_fps(self) -> Optional[str]:
        val_hex = self._read_hex_property("BattleFPS")
        return {
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
        }.get(val_hex, "Extreme+")

    def get_style(self) -> Optional[str]:
        val_hex = self._read_hex_property("BattleRenderStyle")
        return {
            b'\x01': "Classic",
            b'\x02': "Colorful",
            b'\x03': "Realistic",
            b'\x04': "Soft",
            b'\x06': "Movie",
        }.get(val_hex, "Colorful")

    def push_engine_ini(self, adb_device: adbutils.AdbDevice, mode: str = "competitive") -> bool:
        if not self.pubg_package or not adb_device:
            return False
        remote_path = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/Engine.ini"
        
        if mode == "competitive":
            ini_content = """[SystemSettings]
; === EX Tool v0.3 Competitive Engine Settings ===
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
            ini_content = """[SystemSettings]
; === EX Tool v0.3 Balanced Engine Settings ===
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
        local_path = self.get_writable_path("engine_custom.ini")
        try:
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(ini_content)
            adb_device.sync.push(local_path, remote_path)
            return True
        except Exception:
            return False

    def push_shadow_config(self, adb_device: adbutils.AdbDevice, disable_shadow: bool) -> bool:
        if not self.pubg_package or not adb_device:
            return False
        remote_path = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"
        local_path = self.get_writable_path("user_custom.ini")
        
        try:
            try:
                adb_device.sync.pull(remote_path, local_path)
            except Exception:
                pass

            target_val = 49 if disable_shadow else 48
            key_1 = "+CVars=0B572A11181D160E280C1815100D0044"
            key_2 = "+CVars=0B572C0A1C0B2A11181D160E2A0E100D1A1144"
            
            lines = []
            if os.path.exists(local_path):
                with open(local_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

            new_lines = []
            f1, f2 = False, False
            for line in lines:
                if line.startswith(key_1):
                    new_lines.append(f"{key_1}={target_val}\n")
                    f1 = True
                elif line.startswith(key_2):
                    new_lines.append(f"{key_2}={target_val}\n")
                    f2 = True
                else:
                    new_lines.append(line)

            if not f1:
                new_lines.append(f"{key_1}={target_val}\n")
            if not f2:
                new_lines.append(f"{key_2}={target_val}\n")

            with open(local_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            adb_device.sync.push(local_path, remote_path)
            return True
        except Exception:
            return False

    def set_ipad_resolution(self, width: int = 1920, height: int = 1080) -> bool:
        """Sets GameLoop VM Resolution in Registry."""
        RegistryManager.set_user_dword("VMResWidth", width)
        RegistryManager.set_user_dword("VMResHeight", height)
        RegistryManager.set_user_dword("VMResDpi", 240)
        return True

    def restart_pubg(self, adb_device: adbutils.AdbDevice) -> bool:
        """Force stops PUBG package and re-launches it via ADB."""
        if not self.pubg_package or not adb_device:
            return False
        try:
            adb_device.shell(f"am force-stop {self.pubg_package}")
            adb_device.shell(f"monkey -p {self.pubg_package} -c android.intent.category.LAUNCHER 1")
            return True
        except Exception:
            return False
