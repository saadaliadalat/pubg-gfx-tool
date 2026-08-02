"""
EX Tool v0.3 - Dark Glassmorphism Design System Theme
"""

THEME_QSS = """
QMainWindow, QWidget#centralWidget {
    background-color: #080B1A;
    color: #F3F4F6;
    font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
}

/* --- TITLE BAR --- */
#titleBar {
    background-color: #0F142A;
    border-bottom: 1px solid rgba(124, 58, 237, 0.3);
    min-height: 48px;
    max-height: 48px;
}

#appNameLabel {
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

#appBadgeLabel {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7C3AED, stop:1 #06B6D4);
    color: #FFFFFF;
    font-size: 10px;
    font-weight: bold;
    border-radius: 4px;
    padding: 2px 6px;
}

/* --- NAVIGATION BUTTONS --- */
QPushButton[role="nav"] {
    background: transparent;
    color: #9CA3AF;
    font-size: 13px;
    font-weight: 600;
    padding: 8px 18px;
    border: none;
    border-bottom: 3px solid transparent;
    border-radius: 0px;
}
QPushButton[role="nav"]:hover {
    color: #E5E7EB;
    background-color: rgba(255, 255, 255, 0.03);
}
QPushButton[role="nav"]:checked {
    color: #FFFFFF;
    border-bottom: 3px solid #06B6D4;
    font-weight: 700;
}

/* --- TITLE CONTROL BUTTONS --- */
QPushButton[role="titleControl"] {
    background-color: transparent;
    color: #9CA3AF;
    border: none;
    border-radius: 4px;
    font-size: 12px;
    min-width: 32px;
    max-width: 32px;
    min-height: 28px;
    max-height: 28px;
}
QPushButton[role="titleControl"]:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #FFFFFF;
}
QPushButton[role="titleControlClose"]:hover {
    background-color: #EF4444;
    color: #FFFFFF;
}

/* --- CARDS & PANELS --- */
QFrame.cardFrame {
    background-color: #11162B;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
}

QLabel.sectionHeader {
    color: #06B6D4;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* --- STANDARD BUTTONS --- */
QPushButton {
    background-color: #1A2035;
    color: #D1D5DB;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 600;
    min-height: 34px;
}
QPushButton:hover {
    background-color: #242C47;
    border-color: #7C3AED;
    color: #FFFFFF;
}
QPushButton:pressed {
    background-color: #1E1B4B;
}
QPushButton:checked {
    background-color: #7C3AED;
    color: #FFFFFF;
    border-color: #06B6D4;
    font-weight: 700;
}
QPushButton:disabled {
    background-color: #0D1120;
    color: #4B5563;
    border-color: rgba(255, 255, 255, 0.03);
}

/* --- PRIMARY ACTION BUTTONS --- */
QPushButton[class="primary"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7C3AED, stop:1 #6366F1);
    color: #FFFFFF;
    border: none;
    font-weight: 700;
    font-size: 13px;
    min-height: 40px;
}
QPushButton[class="primary"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8B5CF6, stop:1 #4F46E5);
}
QPushButton[class="primary"]:pressed {
    background: #6D28D9;
}

QPushButton[class="accent"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10B981);
    color: #FFFFFF;
    border: none;
    font-weight: 700;
    font-size: 13px;
    min-height: 40px;
}
QPushButton[class="accent"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10B981, stop:1 #34D399);
}

QPushButton[class="danger"] {
    background-color: rgba(239, 68, 68, 0.15);
    color: #FCA5A5;
    border: 1px solid rgba(239, 68, 68, 0.4);
    font-weight: 700;
}
QPushButton[class="danger"]:hover {
    background-color: #EF4444;
    color: #FFFFFF;
    border-color: #EF4444;
}

/* --- STYLE CARDS (GRAPHICS STYLE) --- */
QPushButton[role="styleCard"] {
    background-color: #161C33;
    border: 2px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 6px;
    min-height: 64px;
}
QPushButton[role="styleCard"]:hover {
    border-color: #06B6D4;
    background-color: #1E2646;
}
QPushButton[role="styleCard"]:checked {
    border: 2px solid #7C3AED;
    background-color: rgba(124, 58, 237, 0.2);
}

/* --- INPUTS & COMBOBOX --- */
QComboBox, QLineEdit {
    background-color: #161C33;
    color: #F3F4F6;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    min-height: 34px;
}
QComboBox:hover, QLineEdit:hover {
    border-color: #7C3AED;
}
QComboBox:focus, QLineEdit:focus {
    border-color: #06B6D4;
    outline: none;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    background-color: rgba(124, 58, 237, 0.3);
}
QComboBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #06B6D4;
    width: 0;
    height: 0;
}
QComboBox QAbstractItemView {
    background-color: #0F142A;
    color: #F3F4F6;
    border: 1px solid #7C3AED;
    border-radius: 8px;
    selection-background-color: #7C3AED;
    selection-color: #FFFFFF;
    padding: 4px;
    outline: none;
}

/* --- STATUS BAR --- */
#statusBarFrame {
    background-color: #0B0E20;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding: 6px 14px;
}
#statusLabel {
    font-size: 12px;
    color: #9CA3AF;
    font-weight: 500;
}
"""
