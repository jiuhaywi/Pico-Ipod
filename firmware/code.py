import time
time.sleep(1)
print("BOOT: code.py started")

import board
import busio
import digitalio
import sdcardio
import storage
import os
import pinout
from input import InputManager
from display import DisplayManager
from audio import AudioPlayer
from settings import SettingsManager

print("BOOT: imports complete")

def mount_sd_card():
    spi = busio.SPI(
        clock=pinout.PIN_SD_CLK,
        MOSI=pinout.PIN_SD_CMD,
        MISO=pinout.PIN_SD_DAT0,
    )
    card = sdcardio.SDCard(spi, pinout.PIN_SD_DAT3)
    storage.mount(storage.VfsFat(card), "/sd")

def scan_songs():
    supported_exts = (".mp3", ".wav")
    found_tracks = []
    search_dirs = ["/sd/songs", "/sd", "/songs"]
    for dir_path in search_dirs:
        try:
            for item in os.listdir(dir_path):
                if item.startswith(".") or item.startswith("._"):
                    continue
                lower = item.lower()
                if any(lower.endswith(ext) for ext in supported_exts):
                    found_tracks.append(item)
            if found_tracks:
                print("Discovered {} tracks in {}".format(len(found_tracks), dir_path))
                break
        except (OSError, RuntimeError):
            pass
            
    if not found_tracks:
        found_tracks = ["Song1.mp3", "Song2.mp3", "Song3.mp3"]
    else:
        found_tracks.sort()
    return found_tracks

def resolve_song_path(filename):
    candidate_paths = [
        "/sd/songs/{}".format(filename),
        "/sd/{}".format(filename),
        "/songs/{}".format(filename),
        "/{}".format(filename),
    ]
    for path in candidate_paths:
        try:
            with open(path, "rb") as f:
                return path
        except (OSError, RuntimeError):
            pass
    return "/sd/songs/{}".format(filename)

inputs = InputManager()
print("BOOT: input ready")
ui = DisplayManager()
print("BOOT: display ready")
player = AudioPlayer()
print("BOOT: audio ready")

try:
    mount_sd_card()
    ui.set_status("SD ready")
    print("SD card mounted successfully")
except (OSError, RuntimeError) as error:
    print("SD card unavailable:", error)
    ui.set_status("No SD card")

settings = SettingsManager()
print("BOOT: settings ready")

tracks = scan_songs()
ui.set_tracks(tracks)
selected_idx = 0
volume = 70
output_modes = ["Audio-Jack", "Bluetooth"]
output_mode_idx = 0

ui.update_selection(selected_idx)
ui.set_volume(volume)
ui.set_output_mode(output_modes[output_mode_idx])
print("Ready: UP/DOWN for songs, RIGHT to play, Encoder turn for Volume, Encoder click for Audio output")

while True:
    track_delta = inputs.get_track_delta()
    if track_delta != 0:
        items = ui.get_items()
        new_idx = max(0, min(len(items) - 1, selected_idx + track_delta))
        if new_idx != selected_idx:
            selected_idx = new_idx
            ui.update_selection(selected_idx)
            print("Selected: " + items[selected_idx])

    vol_delta = inputs.get_volume_delta()
    if vol_delta != 0:
        new_vol = max(0, min(100, volume + vol_delta))
        if new_vol != volume:
            volume = new_vol
            ui.set_volume(volume)
            player.set_volume(volume)
            print("Volume:", volume)

    if inputs.is_output_toggle_pressed():
        output_mode_idx = (output_mode_idx + 1) % len(output_modes)
        mode = output_modes[output_mode_idx]
        ui.set_output_mode(mode)
        player.set_output_mode(mode)
        print("Output mode:", mode)

    if inputs.is_play_pressed():
        items = ui.get_items()
        print("Interact for:", items[selected_idx])
        
        if ui.selected_tab == "music":
            track_name = tracks[selected_idx]
            ui.set_now_playing(track_name)
            try:
                filepath = resolve_song_path(track_name)
                player.play(filepath)
                print("Playing:", filepath)
            except (OSError, RuntimeError) as error:
                print("Unable to play track:", error)
                ui.set_status("Track unavailable")
        elif ui.selected_tab == "settings":
            ui.set_selected_tab("settings/" + items[selected_idx])
            selected_idx = 0
            print("Toggled setting: ", items[selected_idx])
        elif ui.selected_tab == "playlists":
            print("Opened playlist: ", items[selected_idx])
        elif ui.selected_tab == "/":
            ui.set_selected_tab(items[selected_idx])
            selected_idx = 0
            print("Opened tab: ", items[selected_idx])
        elif ui.selected_tab == "settings/theme":
            settings.update_settings("theme", items[selected_idx])
            print("Updated setting 'theme': ", items[selected_idx])
        elif ui.selected_tab == "settings/output":
            choice = items[selected_idx]
            if choice == "Bluetooth":
                ui.set_selected_tab("settings/output/bluetooth")
                selected_idx = 0
                print("Opened Bluetooth device list")
            else:
                settings.update_settings("output", choice)
                ui.set_output_mode(choice)
                player.set_output_mode(choice)
                ui.set_status("Output: " + choice)
                print("Updated setting 'output': ", choice)
        elif ui.selected_tab == "settings/output/bluetooth":
            chosen_device = items[selected_idx]
            if chosen_device == "Scan for devices...":
                ui.set_status("Scanning...")
                print("Scanning for Bluetooth devices...")
                ui.set_status("Scan complete")
            else:
                ui.set_status("Connecting...")
                success = player.connect_bluetooth(chosen_device)
                if success:
                    settings.update_settings("output", "Bluetooth")
                    ui.set_output_mode("Bluetooth")
                    ui.set_status("Connected: " + chosen_device)
                    print("Connected to Bluetooth device:", chosen_device)
                else:
                    ui.set_status("BT Connect Failed")

    if inputs.is_back_pressed():
        print(ui.selected_tab)
        if ui.selected_tab=="/":
            print("Error: back key on root")
        elif ui.selected_tab=="settings":
            settings.save_settings()
            ui.set_selected_tab("/")
            selected_idx = 0
            print("Returned to tab: /")
        elif ui.selected_tab=="music":
            ui.set_selected_tab("/")
            selected_idx = 0
            print("Returned to tab: /")
        elif ui.selected_tab=="playlists":
            ui.set_selected_tab("/")
            selected_idx = 0
            print("Returned to tab: /")
        elif ui.selected_tab=="settings/theme":
            ui.set_selected_tab("settings")
            selected_idx = 0
            print("Returned to tab: settings")
        elif ui.selected_tab=="settings/output/bluetooth":
            ui.set_selected_tab("settings/output")
            selected_idx = 0
            print("Returned to tab: settings/output")
        elif ui.selected_tab=="settings/output":
            ui.set_selected_tab("settings")
            selected_idx = 0
            print("Returned to tab: settings")
        else:
            ui.set_selected_tab("/")
            selected_idx = 0
            print("Back to root tab")
        

    time.sleep(0.005)