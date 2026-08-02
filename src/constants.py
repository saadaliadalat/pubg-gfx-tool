import os
from pathlib import Path

APP_NAME = "EX Tool"
APP_VERSION = "v0.3"
FULL_APP_NAME = f"{APP_NAME} {APP_VERSION}"

REG_PATH = r'SOFTWARE\Tencent\MobileGamePC'
REG_LOCAL_PATH = r'SOFTWARE\WOW6432Node\Tencent\MobileGamePC'

PUBG_VERSIONS = {
    "com.tencent.ig": "PUBG Mobile Global",
    "com.vng.pubgmobile": "PUBG Mobile VN",
    "com.rekoo.pubgm": "PUBG Mobile TW",
    "com.pubg.krmobile": "PUBG Mobile KR",
    "com.pubg.imobile": "Battlegrounds Mobile India"
}

GAMELOOP_PROCESSES = {
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

DNS_SERVERS = {
    "Google DNS - 8.8.8.8": ['8.8.8.8', '8.8.4.4'],
    "Cloudflare DNS - 1.1.1.1": ['1.1.1.1', '1.0.0.1'],
    "Quad9 DNS - 9.9.9.9": ['9.9.9.9', '149.112.112.112'],
    "Cisco Umbrella - 208.67.222.222": ['208.67.222.222', '208.67.220.220'],
    "Yandex DNS - 77.88.8.1": ['77.88.8.1', '77.88.8.8']
}

def get_app_data_dir() -> Path:
    app_data_root = os.getenv("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    data_dir = Path(app_data_root) / "EX Tool" / "assets"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
