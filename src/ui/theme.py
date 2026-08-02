"""
EX Tool v0.3 — Premium Dark Theme
Uses only Qt-valid QSS selectors: #objectName or [property="value"]
"""

THEME_QSS = """
/* ============================================================
   BASE
   ============================================================ */
QMainWindow, QWidget {
    background-color: #080B1A;
    color: #E5E7EB;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}

/* ============================================================
   TITLE BAR
   ============================================================ */
QFrame#titleBar {
    background-color: #0C1022;
    border-bottom: 2px solid #7C3AED;
    min-height: 50px;
    max-height: 50px;
}

QLabel#appNameLabel {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

QLabel#appBadgeLabel {
    background-color: #7C3AED;
    color: #FFFFFF;
    font-size: 10px;
    font-weight: 700;
    border-radius: 4px;
    padding: 2px 8px;
}

/* ============================================================
   NAV BUTTONS
   ============================================================ */
QPushButton[role="nav"] {
    background: transparent;
    color: #6B7280;
    font-size: 13px;
    font-weight: 600;
    padding: 10px 22px;
    border: none;
    border-bottom: 3px solid transparent;
    border-radius: 0px;
    min-height: 46px;
}
QPushButton[role="nav"]:hover {
    color: #D1D5DB;
    background-color: rgba(124, 58, 237, 0.08);
}
QPushButton[role="nav"]:checked {
    color: #FFFFFF;
    border-bottom: 3px solid #7C3AED;
    font-weight: 700;
}

/* ============================================================
   TITLE CONTROL BUTTONS
   ============================================================ */
QPushButton[role="titleControl"] {
    background: transparent;
    color: #9CA3AF;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    min-width: 36px;
    max-width: 36px;
    min-height: 36px;
    max-height: 36px;
    font-weight: 600;
}
QPushButton[role="titleControl"]:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #FFFFFF;
}
QPushButton[role="closeBtn"] {
    background: transparent;
    color: #9CA3AF;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    min-width: 36px;
    max-width: 36px;
    min-height: 36px;
    max-height: 36px;
    font-weight: 600;
}
QPushButton[role="closeBtn"]:hover {
    background-color: #EF4444;
    color: #FFFFFF;
}

/* ============================================================
   SECTION CARDS
   ============================================================ */
QFrame#sectionCard {
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
}

QFrame#sectionCard:hover {
    border: 1px solid #374151;
}

/* ============================================================
   SECTION LABELS
   ============================================================ */
QLabel#sectionTitle {
    color: #06B6D4;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

/* ============================================================
   STANDARD BUTTONS
   ============================================================ */
QPushButton {
    background-color: #1F2937;
    color: #D1D5DB;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
    min-height: 36px;
}
QPushButton:hover {
    background-color: #374151;
    border-color: #7C3AED;
    color: #FFFFFF;
}
QPushButton:pressed {
    background-color: #111827;
    border-color: #6D28D9;
}
QPushButton:checked {
    background-color: #7C3AED;
    color: #FFFFFF;
    border-color: #06B6D4;
    font-weight: 700;
}
QPushButton:disabled {
    background-color: #0F1629;
    color: #374151;
    border-color: #1F2937;
}

/* PRIMARY: violet gradient */
QPushButton[btnStyle="primary"] {
    background-color: #7C3AED;
    color: #FFFFFF;
    border: none;
    font-weight: 700;
    font-size: 13px;
    min-height: 42px;
    border-radius: 9px;
}
QPushButton[btnStyle="primary"]:hover {
    background-color: #8B5CF6;
}
QPushButton[btnStyle="primary"]:pressed {
    background-color: #6D28D9;
}
QPushButton[btnStyle="primary"]:disabled {
    background-color: #3B1A6B;
    color: #7C6B99;
}

/* SUCCESS: green */
QPushButton[btnStyle="success"] {
    background-color: #059669;
    color: #FFFFFF;
    border: none;
    font-weight: 700;
    font-size: 13px;
    min-height: 42px;
    border-radius: 9px;
}
QPushButton[btnStyle="success"]:hover {
    background-color: #10B981;
}
QPushButton[btnStyle="success"]:pressed {
    background-color: #047857;
}

/* DANGER: red */
QPushButton[btnStyle="danger"] {
    background-color: rgba(239, 68, 68, 0.15);
    color: #FCA5A5;
    border: 1px solid rgba(239, 68, 68, 0.4);
    font-weight: 700;
    min-height: 36px;
}
QPushButton[btnStyle="danger"]:hover {
    background-color: #EF4444;
    color: #FFFFFF;
    border-color: #EF4444;
}

/* STYLE CARD: graphics style buttons with icon */
QPushButton[btnStyle="styleCard"] {
    background-color: #161C33;
    border: 2px solid #1F2937;
    border-radius: 10px;
    padding: 6px;
    min-height: 60px;
    color: #D1D5DB;
    font-size: 11px;
    font-weight: 600;
}
QPushButton[btnStyle="styleCard"]:hover {
    border-color: #06B6D4;
    background-color: #1E2646;
    color: #FFFFFF;
}
QPushButton[btnStyle="styleCard"]:checked {
    border: 2px solid #7C3AED;
    background-color: rgba(124, 58, 237, 0.25);
    color: #FFFFFF;
}

/* ============================================================
   CONNECTION BANNER
   ============================================================ */
QFrame#bannerDisconnected {
    background-color: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 8px;
}
QFrame#bannerConnected {
    background-color: rgba(5, 150, 105, 0.1);
    border: 1px solid rgba(5, 150, 105, 0.35);
    border-radius: 8px;
}

/* ============================================================
   COMBOBOX
   ============================================================ */
QComboBox {
    background-color: #1F2937;
    color: #F3F4F6;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 6px 34px 6px 12px;
    font-size: 12px;
    min-height: 34px;
    selection-background-color: #7C3AED;
}
QComboBox:hover {
    border-color: #7C3AED;
}
QComboBox:focus {
    border-color: #06B6D4;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid #374151;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    background-color: rgba(124, 58, 237, 0.4);
}
QComboBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #06B6D4;
    width: 0;
    height: 0;
}
QComboBox QAbstractItemView {
    background-color: #111827;
    color: #F3F4F6;
    border: 1px solid #7C3AED;
    border-radius: 8px;
    selection-background-color: #7C3AED;
    selection-color: #FFFFFF;
    padding: 4px;
    outline: none;
}
QComboBox QAbstractItemView::item {
    min-height: 30px;
    padding: 4px 10px;
}
QComboBox QAbstractItemView::item:hover {
    background-color: rgba(124, 58, 237, 0.3);
}

/* ============================================================
   LINE EDIT
   ============================================================ */
QLineEdit {
    background-color: #1F2937;
    color: #F3F4F6;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    min-height: 34px;
}
QLineEdit:hover {
    border-color: #7C3AED;
}
QLineEdit:focus {
    border-color: #06B6D4;
}

/* ============================================================
   STATUS BAR
   ============================================================ */
QFrame#statusBar {
    background-color: #0A0D1A;
    border-top: 1px solid #1F2937;
    min-height: 30px;
    max-height: 30px;
}

QLabel#statusLabel {
    font-size: 12px;
    color: #6B7280;
    font-weight: 500;
}

/* ============================================================
   SCROLL AREA
   ============================================================ */
QScrollBar:vertical {
    background: #0F1629;
    width: 6px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #374151;
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #7C3AED;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""
