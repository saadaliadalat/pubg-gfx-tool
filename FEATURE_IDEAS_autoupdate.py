# Auto-update system
# Add to app_functions.py

import requests
import json
from packaging import version

class AutoUpdater:
    def __init__(self):
        self.current_version = "1.0.8"
        self.github_repo = "YourUsername/pubg-gfx-tool"
        self.update_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"

    def check_for_updates(self):
        """Check if a newer version is available"""
        try:
            response = requests.get(self.update_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest_version = data['tag_name'].replace('v', '')

                if version.parse(latest_version) > version.parse(self.current_version):
                    return {
                        'available': True,
                        'version': latest_version,
                        'download_url': data['assets'][0]['browser_download_url'],
                        'changelog': data['body']
                    }
        except Exception as e:
            print(f"Update check failed: {e}")

        return {'available': False}

    def download_update(self, download_url):
        """Download the latest version"""
        try:
            response = requests.get(download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            with open('MK-PUBG-Mobile-Tool-Update.exe', 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress = (downloaded / total_size) * 100
                        print(f"Downloading: {progress:.1f}%")

            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False

# In main UI, add update notification:
# - Check on startup (async, non-blocking)
# - Show notification bar if update available
# - One-click update button
