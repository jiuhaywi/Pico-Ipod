#!/usr/bin/env bash
set -e

command -v arm-none-eabi-gcc >/dev/null 2>&1 || { echo >&2 "Error: arm-none-eabi-gcc required."; exit 1; }
command -v cmake >/dev/null 2>&1 || { echo >&2 "Error: cmake required."; exit 1; }
command -v ninja >/dev/null 2>&1 || { echo >&2 "Error: ninja required."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo >&2 "Error: python3 required."; exit 1; }

BUILD_DIR="circuitpython_build"
BOARD_TARGET="raspberry_pi_pico2_w"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "$BUILD_DIR" ]; then
    git clone --depth 1 https://github.com/adafruit/circuitpython.git "$BUILD_DIR"
    cd "$BUILD_DIR"
    make fetch-submodules
    cd ..
fi

mkdir -p "$BUILD_DIR/shared-bindings/btaudio"
cp "$SCRIPT_DIR/shared-bindings/btaudio/"* "$BUILD_DIR/shared-bindings/btaudio/"

mkdir -p "$BUILD_DIR/ports/raspberrypi/common-hal/btaudio"
cp "$SCRIPT_DIR/common-hal/btaudio/"* "$BUILD_DIR/ports/raspberrypi/common-hal/btaudio/"

make -C "$BUILD_DIR/mpy-cross" -j$(nproc)
make -C "$BUILD_DIR/ports/raspberrypi" BOARD="$BOARD_TARGET" -j$(nproc)

echo "Firmware: $BUILD_DIR/ports/raspberrypi/build-$BOARD_TARGET/firmware.uf2"
