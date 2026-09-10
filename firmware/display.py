import displayio
import busio
import terminalio
import digitalio
from adafruit_display_text import label
from adafruit_ili9341 import ILI9341
import pinout

try:
    from fourwire import FourWire
except (ImportError, AttributeError):
    from displayio import FourWire


# Preset Theme: Choose "dark" (Deep Black like Gemini) or "light" (Sleek Light Gray)
THEME = "dark"


def col(rgb_hex):
    """Convert RGB hex to BGR hex to match the ILI9341 panel order."""
    r = (rgb_hex >> 16) & 0xFF
    g = (rgb_hex >> 8) & 0xFF
    b = rgb_hex & 0xFF
    return (b << 16) | (g << 8) | r


THEMES = {
    "dark": {
        "bg": col(0x000000),           # Deep pitch black
        "header_bg": col(0x141416),    # Sleek dark charcoal
        "header_text": col(0xFFFFFF),  # Pure white
        "vol_text": col(0x38BDF8),     # Electric sky cyan
        "bat_text": col(0x4ADE80),     # Battery green
        "section_text": col(0x71717A), # Muted slate
        "selection": col(0x38BDF8),    # Highlight cyan
        "track_unsel": col(0xA1A1AA),  # Clean light gray
        "card_bg": col(0x141416),      # Dark charcoal card
        "card_title": col(0x71717A),   # Section gray
        "track_name": col(0xFFFFFF),   # Crisp white
        "track_state": col(0x4ADE80),  # Bright green
        "output_mode": col(0x38BDF8),  # Cyan
        "status_bg": col(0x000000),    # Deep pitch black
        "status_text": col(0xA1A1AA)   # Gray
    },
    "light": {
        "bg": col(0xF3F4F6),           # Soft light gray
        "header_bg": col(0xE5E7EB),    # Medium light gray
        "header_text": col(0x111827),  # Dark slate
        "vol_text": col(0x0284C7),     # Blue
        "bat_text": col(0x16A34A),     # Green
        "section_text": col(0x4B5563), # Slate
        "selection": col(0x0284C7),    # Blue highlight
        "track_unsel": col(0x374151),  # Dark slate
        "card_bg": col(0xFFFFFF),      # Clean white card
        "card_title": col(0x4B5563),   # Slate
        "track_name": col(0x111827),   # Black
        "track_state": col(0x16A34A),  # Green
        "output_mode": col(0x0284C7),  # Blue
        "status_bg": col(0xE5E7EB),    # Gray
        "status_text": col(0x374151)   # Dark slate
    }
}


def create_rect(width, height, color, x=0, y=0):
    bitmap = displayio.Bitmap(width, height, 1)
    palette = displayio.Palette(1)
    palette[0] = color
    return displayio.TileGrid(bitmap, pixel_shader=palette, x=x, y=y)


class DisplayManager:
    def __init__(self):
        self.init_vars()
        self.initialize_display()



    def init_vars(self):
        self.colors = THEMES.get(THEME, THEMES["dark"])
        self.display = None
        self.backlight = None
        self.group = displayio.Group()
        self.tracks = ["Song1.mp3", "Song2.mp3", "Song3.mp3"]
        self.selected_idx = 0
        self.scroll_offset = 0
        self.visible_count = 3
        self.volume = 70
        self.output_mode = "Audio-Jack"
        self.tab_labels = []
        self.vol_label = None
        self.bat_label = None
        self.now_playing_track = None
        self.now_playing_state = None
        self.now_playing_mode = None
        self.status_label = None
        self.selected_tab = "/"
        self.card_title = None
        self.menu_title = None
        self.root_tabs = ["settings", "music", "playlists"]
        self.settings = ["theme","output"]
        self.settings_theme = ["dark","light"]
        self.settings_output = ["Audio-Jack", "Bluetooth"]
        self.bt_devices = ["AirPods Pro", "Sony WH-1000XM4", "JBL Flip", "Scan for devices..."]
        self.playlists = ["playlist1"]



    def initialize_display(self):
        self.group = displayio.Group()
        self.tab_labels = []
        displayio.release_displays()
        spi = busio.SPI(clock=pinout.PIN_DISPLAY_CLK, MOSI=pinout.PIN_DISPLAY_DIN)
        display_bus = FourWire(
            spi,
            command=pinout.PIN_DISPLAY_DC,
            chip_select=pinout.PIN_DISPLAY_CS,
            reset=pinout.PIN_DISPLAY_RST,
            baudrate=40_000_000
        )
        
        # 240x240 native square resolution
        self.display = ILI9341(
            display_bus,
            width=240,
            height=240,
            rotation=0
        )

        self.backlight = digitalio.DigitalInOut(pinout.PIN_DISPLAY_BL)
        self.backlight.direction = digitalio.Direction.OUTPUT
        self.backlight.value = True

        # 1. Main Background
        bg = create_rect(240, 240, self.colors["bg"], 0, 0)
        self.group.append(bg)

        # 2. Header Bar (Height 32)
        header_bg = create_rect(240, 32, self.colors["header_bg"], 0, 0)
        self.group.append(header_bg)

        header_title = label.Label(
            terminalio.FONT,
            text="PicoPod",
            color=self.colors["header_text"],
            x=8,
            y=16,
            scale=2
        )
        self.group.append(header_title)

        # Volume level (to the left of the battery)
        self.vol_label = label.Label(
            terminalio.FONT,
            text="V: 70%",
            color=self.colors["vol_text"],
            x=116,
            y=16,
            scale=1
        )
        self.group.append(self.vol_label)

        # High-contrast Battery indicator
        self.bat_label = label.Label(
            terminalio.FONT,
            text="[###]",
            color=self.colors["bat_text"],
            x=185,
            y=16,
            scale=1
        )
        self.group.append(self.bat_label)

        # 3. Section Title
        self.menu_title = label.Label(
            terminalio.FONT,
            text=self.selected_tab,
            color=self.colors["section_text"],
            x=10,
            y=44,
            scale=1
        )
        self.group.append(self.menu_title)

        # 4. Track List Labels (3 tracks, 28px spacing)
        self.draw_tab()

        # 5. Now Playing Card (Y: 144 to 206)
        card_bg = create_rect(222, 62, self.colors["card_bg"], 9, 144)
        self.group.append(card_bg)

        self.card_title = label.Label(
            terminalio.FONT,
            text="NOW PLAYING",
            color=self.colors["card_title"],
            x=16,
            y=155,
            scale=1
        )
        self.group.append(self.card_title)

        self.now_playing_track = label.Label(
            terminalio.FONT,
            text="None",
            color=self.colors["track_name"],
            x=16,
            y=175,
            scale=2
        )
        self.group.append(self.now_playing_track)

        self.now_playing_state = label.Label(
            terminalio.FONT,
            text="Idle",
            color=self.colors["track_state"],
            x=16,
            y=195,
            scale=1
        )
        self.group.append(self.now_playing_state)

        self.now_playing_mode = label.Label(
            terminalio.FONT,
            text="Out: Audio-Jack",
            color=self.colors["output_mode"],
            x=110,
            y=195,
            scale=1
        )
        self.group.append(self.now_playing_mode)

        # 6. Status Bar (Y: 216 to 240)
        status_bg = create_rect(240, 24, self.colors["status_bg"], 0, 216)
        self.group.append(status_bg)

        self.status_label = label.Label(
            terminalio.FONT,
            text="System Ready",
            color=self.colors["status_text"],
            x=10,
            y=228,
            scale=1
        )
        self.group.append(self.status_label)

        self.display.root_group = self.group

    def update_selection(self, new_idx):
        items = self.get_items()
        if not items:
            return
        
        new_idx = max(0, min(len(items) - 1, new_idx))
        old_idx = self.selected_idx
        if old_idx == new_idx and len(self.tab_labels) > 0:
            return
        
        self.selected_idx = new_idx
        old_offset = self.scroll_offset

        if self.selected_idx < self.scroll_offset:
            self.scroll_offset = self.selected_idx
        elif self.selected_idx >= self.scroll_offset + self.visible_count:
            self.scroll_offset = self.selected_idx - self.visible_count + 1

        if self.scroll_offset != old_offset or len(self.tab_labels) == 0:
            self.draw_tab()
        else:
            self.display.auto_refresh = False
            for slot_i, lbl in enumerate(self.tab_labels):
                actual_idx = self.scroll_offset + slot_i
                if actual_idx < len(items):
                    if actual_idx == self.selected_idx:
                        lbl.text = "> " + str(actual_idx + 1) + ") " + items[actual_idx]
                        lbl.color = self.colors["selection"]
                    else:
                        lbl.text = "  " + str(actual_idx + 1) + ") " + items[actual_idx]
                        lbl.color = self.colors["track_unsel"]
            self.display.auto_refresh = True


    def set_volume(self, volume):
        self.volume = max(0, min(100, volume))
        self.vol_label.text = "V: {}%".format(self.volume)

    def set_output_mode(self, mode):
        self.output_mode = mode
        self.now_playing_mode.text = "Out: {}".format(mode)

    def set_now_playing(self, track_name):
        self.display.auto_refresh = False
        self.now_playing_track.text = track_name
        self.now_playing_state.text = "Playing"
        self.now_playing_state.color = self.colors["track_state"]
        self.display.auto_refresh = True

    def set_status(self, message):
        self.status_label.text = message
        msg_lower = message.lower()
        if "ready" in msg_lower:
            self.status_label.color = self.colors["track_state"]
        elif "no" in msg_lower or "unavail" in msg_lower:
            self.status_label.color = col(0xF87171)  # Red alert
        else:
            self.status_label.color = self.colors["status_text"]

    def set_selected_tab(self, new_tab):
        self.selected_tab = new_tab
        self.selected_idx = 0
        self.scroll_offset = 0
        self.draw_tab()

    def set_tracks(self, track_list):
        self.tracks = track_list if track_list else ["No songs found"]
        if self.selected_tab == "music":
            self.selected_idx = 0
            self.scroll_offset = 0
            self.draw_tab()

    def set_bt_devices(self, device_list):
        self.bt_devices = device_list if device_list else ["No devices found"]
        if self.selected_tab == "settings/output/bluetooth":
            self.selected_idx = 0
            self.scroll_offset = 0
            self.draw_tab()

    def get_items(self):
        #print(self.selected_tab)
        if self.selected_tab == "music":
            items = self.tracks
        elif self.selected_tab == "/":
            items = self.root_tabs
        elif self.selected_tab == "settings":
            items = self.settings
        elif self.selected_tab == "playlists":
            items = self.playlists
        elif self.selected_tab == "settings/theme":
            items = self.settings_theme
        elif self.selected_tab == "settings/output":
            items = self.settings_output
        elif self.selected_tab == "settings/output/bluetooth":
            items = self.bt_devices
        else:
            items = self.root_tabs
        return items

    def draw_tab(self):
        self.display.auto_refresh = False
        if self.selected_tab != "/":
            self.menu_title.text = ("/" + self.selected_tab + "/").upper()
        else:
            self.menu_title.text = self.selected_tab

        for lbl in self.tab_labels:
            if lbl in self.group:
                self.group.remove(lbl)
        self.tab_labels = []
        items = self.get_items()

        max_offset = max(0, len(items) - self.visible_count)
        self.scroll_offset = max(0, min(max_offset, self.scroll_offset))

        visible_items = items[self.scroll_offset : self.scroll_offset + self.visible_count]

        for slot_i, text_label in enumerate(visible_items):
            actual_idx = self.scroll_offset + slot_i
            is_selected = (actual_idx == self.selected_idx)
            prefix = "> " if is_selected else "  "
            col = self.colors["selection"] if is_selected else self.colors["track_unsel"]
            lbl = label.Label(
                terminalio.FONT,
                text=prefix + str(actual_idx + 1) + ") " + text_label,
                color=col,
                x=10,
                y=68 + (slot_i * 28),
                scale=2
            )
            self.group.append(lbl)
            self.tab_labels.append(lbl)
        
        self.display.auto_refresh = True