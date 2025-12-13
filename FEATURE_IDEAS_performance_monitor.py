# Performance Monitor Overlay
# Real-time FPS, ping, CPU/GPU usage

import psutil
import GPUtil
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class PerformanceOverlay(QWidget):
    """Transparent overlay showing performance metrics"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_timer()

    def init_ui(self):
        # Make window frameless and always on top
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Semi-transparent background
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 150);
                border-radius: 10px;
            }
            QLabel {
                color: #00FF00;
                font-family: 'Consolas';
                font-size: 14px;
                padding: 5px;
            }
        """)

        # Create labels
        layout = QVBoxLayout()
        self.fps_label = QLabel("FPS: --")
        self.cpu_label = QLabel("CPU: --%")
        self.gpu_label = QLabel("GPU: --%")
        self.ram_label = QLabel("RAM: -- MB")
        self.temp_label = QLabel("Temp: --°C")

        layout.addWidget(self.fps_label)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.gpu_label)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.temp_label)

        self.setLayout(layout)
        self.setGeometry(10, 10, 200, 150)  # Top-left corner

    def setup_timer(self):
        """Update metrics every second"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)  # Update every 1 second

    def update_metrics(self):
        """Fetch and display current metrics"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")

        # RAM usage
        ram = psutil.virtual_memory()
        ram_mb = (ram.total - ram.available) / (1024 * 1024)
        self.ram_label.setText(f"RAM: {ram_mb:.0f} MB")

        # GPU usage (if available)
        try:
            gpu = GPUtil.getGPUs()[0]
            self.gpu_label.setText(f"GPU: {gpu.load * 100:.1f}%")
            self.temp_label.setText(f"Temp: {gpu.temperature:.0f}°C")
        except:
            self.gpu_label.setText("GPU: N/A")
            self.temp_label.setText("Temp: N/A")

        # FPS (would need to hook into game process)
        # This is advanced - would require reading game memory
        # For now, show placeholder
        self.fps_label.setText("FPS: Monitor")

# Features to add:
# - Toggle on/off with hotkey (F11)
# - Draggable position
# - Customizable metrics (show/hide)
# - Different color schemes
# - Save position across sessions
