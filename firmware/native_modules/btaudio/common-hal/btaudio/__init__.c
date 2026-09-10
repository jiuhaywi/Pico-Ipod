#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#include "py/runtime.h"
#include "shared-bindings/btaudio/__init__.h"

// Note: When compiled into CircuitPython with Pico SDK + BTstack:
// #include "btstack.h"
// #include "pico/cyw43_arch.h"

static bool s_bt_initialized = false;
static bool s_bt_connected = false;
static bool s_bt_playing = false;
static uint8_t s_bt_volume = 70;
static char s_bt_status[32] = "disconnected";

void common_hal_btaudio_init(void) {
    if (s_bt_initialized) {
        return;
    }
    // Initialize CYW43 architecture with BTstack
    // cyw43_arch_init();
    // a2dp_source_init();
    s_bt_initialized = true;
    strncpy(s_bt_status, "ready", sizeof(s_bt_status) - 1);
}

void common_hal_btaudio_deinit(void) {
    if (!s_bt_initialized) {
        return;
    }
    common_hal_btaudio_stop();
    common_hal_btaudio_disconnect();
    s_bt_initialized = false;
    strncpy(s_bt_status, "disabled", sizeof(s_bt_status) - 1);
}

bool common_hal_btaudio_connect(const char *address) {
    if (!s_bt_initialized) {
        common_hal_btaudio_init();
    }
    strncpy(s_bt_status, "connecting", sizeof(s_bt_status) - 1);
    
    // In full BTstack implementation:
    // bd_addr_t remote_addr;
    // sscanf_bd_addr(address, remote_addr);
    // a2dp_source_establish_stream(remote_addr, &local_stream_endpoint);
    
    s_bt_connected = true;
    strncpy(s_bt_status, "connected", sizeof(s_bt_status) - 1);
    return true;
}

void common_hal_btaudio_disconnect(void) {
    s_bt_connected = false;
    s_bt_playing = false;
    strncpy(s_bt_status, "disconnected", sizeof(s_bt_status) - 1);
}

bool common_hal_btaudio_is_connected(void) {
    return s_bt_connected;
}

bool common_hal_btaudio_is_playing(void) {
    return s_bt_playing;
}

void common_hal_btaudio_play(mp_obj_t sample_obj) {
    if (!s_bt_initialized) {
        common_hal_btaudio_init();
    }
    // Stream PCM buffers from audiomp3.MP3Decoder into SBC encoder packet queue
    s_bt_playing = true;
    strncpy(s_bt_status, "streaming", sizeof(s_bt_status) - 1);
}

void common_hal_btaudio_stop(void) {
    s_bt_playing = false;
    if (s_bt_connected) {
        strncpy(s_bt_status, "connected", sizeof(s_bt_status) - 1);
    } else {
        strncpy(s_bt_status, "disconnected", sizeof(s_bt_status) - 1);
    }
}

void common_hal_btaudio_pause(void) {
    s_bt_playing = false;
    strncpy(s_bt_status, "paused", sizeof(s_bt_status) - 1);
}

void common_hal_btaudio_resume(void) {
    s_bt_playing = true;
    strncpy(s_bt_status, "streaming", sizeof(s_bt_status) - 1);
}

void common_hal_btaudio_set_volume(uint8_t volume) {
    s_bt_volume = volume;
}

const char *common_hal_btaudio_get_status(void) {
    return s_bt_status;
}
