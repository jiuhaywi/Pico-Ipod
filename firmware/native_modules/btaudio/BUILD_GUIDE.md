# PicoPod Build Guide

This guide explains how to compile the PicoPod **CircuitPython** firmware, with **btaudio** compiled into the uf2.



## Prerequisites

### Arch Distros:
```bash
sudo pacman -S --needed \
    base-devel \
    arm-none-eabi-gcc \
    arm-none-eabi-binutils \
    arm-none-eabi-newlib \
    cmake \
    ninja \
    python \
    git \
    pkgconf
```

### Debian/Ubuntu Distros:
```bash
sudo apt-get update && sudo apt-get install -y \
    build-essential \
    gcc-arm-none-eabi \
    binutils-arm-none-eabi \
    libnewlib-arm-none-eabi \
    cmake \
    ninja-build \
    python3 \
    git \
    pkg-config
```

---

## Layout

The native module files are found in `firmware/native_modules/btaudio/`:
```
firmware/native_modules/btaudio/
├── shared-bindings/
│   └── btaudio/
│       ├── __init__.c      
│       └── __init__.h      
├── common-hal/
│   └── btaudio/
│       └── __init__.c      
├── build_circuitpython_uf2.sh 
└── BUILD_GUIDE.md          
```

---

## Building

Run the build script:
```bash
chmod +x firmware/native_modules/btaudio/build_circuitpython_uf2.sh
./firmware/native_modules/btaudio/build_circuitpython_uf2.sh
```

Or:
1. **Clone CircuitPython:**
   ```bash
   git clone https://github.com/adafruit/circuitpython.git
   cd circuitpython
   make fetch-submodules
   ```
2. **Copy the `btaudio` module into CircuitPython:**
   ```bash
   cp -r ../native_modules/btaudio/shared-bindings/btaudio shared-bindings/
   cp -r ../native_modules/btaudio/common-hal/btaudio ports/raspberrypi/common-hal/
   ```
3. **Build `mpy-cross`:**
   ```bash
   make -C mpy-cross
   ```
4. **Compile for Pico 2 W:**
   ```bash
   cd ports/raspberrypi
   make BOARD=raspberry_pi_pico2_w -j$(nproc)
   ```

---

## 4. Flashing

1. Hold the **BOOTSEL** button and plug the pico in with USB.
2. Drag and drop `firmware.uf2` onto the `RPI-RP2` drive.
3. Copy all Python files (`code.py`, `display.py`, `input.py`, `audio.py`, `settings.py`, `pinout.py`) and `/songs/` onto the `CIRCUITPY` drive.
