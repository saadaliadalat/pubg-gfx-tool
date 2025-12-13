# Sensitivity settings structure for Active.sav
# Add to app_functions.py

def set_sensitivity(self, sensitivity_type, value):
    """
    Sets sensitivity settings in Active.sav

    Sensitivity types:
    - CameraSensitivity: 1-100
    - ADS_RedDot: 1-100
    - ADS_2x: 1-100
    - ADS_4x: 1-100
    - ADS_8x: 1-100
    - GyroSensitivity: 1-100
    """
    sensitivity_properties = {
        "CameraSensitivity": "CameraFreeV3",
        "ADS_RedDot": "AimingV3",
        "ADS_2x": "ScopeV3",
        "ADS_4x": "Scope4xV3",
        "ADS_8x": "Scope8xV3",
        "GyroSensitivity": "GyroV3"
    }

    property_name = sensitivity_properties.get(sensitivity_type)
    if property_name:
        # Convert value (1-100) to game value
        game_value = int((value / 100) * 255).to_bytes(1, 'little')
        self.change_graphics_file(property_name, game_value)

def get_sensitivity(self, sensitivity_type):
    """Gets current sensitivity value"""
    sensitivity_properties = {
        "CameraSensitivity": "CameraFreeV3",
        "ADS_RedDot": "AimingV3",
        "ADS_2x": "ScopeV3",
        "ADS_4x": "Scope4xV3",
        "ADS_8x": "Scope8xV3",
        "GyroSensitivity": "GyroV3"
    }

    property_name = sensitivity_properties.get(sensitivity_type)
    if property_name:
        value_bytes = self.read_hex(property_name)
        # Convert game value to 1-100 scale
        return int((int.from_bytes(value_bytes, 'little') / 255) * 100)
    return None
