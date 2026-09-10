


class SettingsManager:
    def __init__(self):
        self.theme = "dark"
        self.output_mode = "Audio-Jack"
        self.load_settings()
    
    def update_settings(self, setting, value):
        key = setting.lower()
        if key == "theme":
            self.theme = value
        elif key == "output":
            self.output_mode = value
        
    def get_settings(self):
        return self.theme, self.output_mode
    
    def save_settings(self):
        print("Saved settings:", self.theme, self.output_mode)
        try:
            with open("/sd/settings.cfg", "w") as f:
                f.write("Theme: " + self.theme + "\n")
                f.write("Output: " + self.output_mode + "\n")
        except (OSError, RuntimeError) as error:
            print("Warning: Could not save settings to SD card (Read-Only or unmounted):", error)
    
    def load_settings(self):
        try:
            with open("/sd/settings.cfg", "r") as f:
                for line in f:
                    if line.startswith("Theme: "):
                        self.theme = line.strip().split("Theme: ")[1]
                    elif line.startswith("Output: "):
                        self.output_mode = line.strip().split("Output: ")[1]
        except:
            pass