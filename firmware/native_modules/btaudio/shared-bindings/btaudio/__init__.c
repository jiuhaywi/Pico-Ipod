#include "py/obj.h"
#include "py/runtime.h"
#include "shared-bindings/btaudio/__init__.h"

//| """Bluetooth A2DP Audio Streaming Module for Pico 2 W"""
//|

//| def init() -> None:
//|     """Initialize the BTstack A2DP Source and CYW43 Bluetooth controller."""
//|     ...
STATIC mp_obj_t btaudio_init_obj(void) {
    common_hal_btaudio_init();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(btaudio_init_fun_obj, btaudio_init_obj);

//| def deinit() -> None:
//|     """Deinitialize Bluetooth audio subsystem."""
//|     ...
STATIC mp_obj_t btaudio_deinit_obj(void) {
    common_hal_btaudio_deinit();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(btaudio_deinit_fun_obj, btaudio_deinit_obj);

//| def connect(address: Optional[str] = None) -> bool:
//|     """Connect to a Bluetooth audio sink / headphones (MAC address string or auto-discovery)."""
//|     ...
STATIC mp_obj_t btaudio_connect_obj(size_t n_args, const mp_obj_t *args) {
    const char *addr = NULL;
    if (n_args > 0 && args[0] != mp_const_none) {
        addr = mp_obj_str_get_str(args[0]);
    }
    bool res = common_hal_btaudio_connect(addr);
    return mp_obj_new_bool(res);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(btaudio_connect_fun_obj, 0, 1, btaudio_connect_obj);

//| def disconnect() -> None:
//|     """Disconnect from the active Bluetooth audio sink."""
//|     ...
STATIC mp_obj_t btaudio_disconnect_obj(void) {
    common_hal_btaudio_disconnect();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(btaudio_disconnect_fun_obj, btaudio_disconnect_obj);

//| def is_connected() -> bool:
//|     """Check if currently connected to a Bluetooth audio device."""
//|     ...
STATIC mp_obj_t btaudio_is_connected_obj(void) {
    return mp_obj_new_bool(common_hal_btaudio_is_connected());
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(btaudio_is_connected_fun_obj, btaudio_is_connected_obj);

//| def is_playing() -> bool:
//|     """Check if audio streaming is currently in progress."""
//|     ...
STATIC mp_obj_t btaudio_is_playing_obj(void) {
    return mp_obj_new_bool(common_hal_btaudio_is_playing());
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(btaudio_is_playing_fun_obj, btaudio_is_playing_obj);

//| def play(sample: Any) -> None:
//|     """Start streaming decoded audio samples to connected Bluetooth device."""
//|     ...
STATIC mp_obj_t btaudio_play_obj(mp_obj_t sample_obj) {
    common_hal_btaudio_play(sample_obj);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(btaudio_play_fun_obj, btaudio_play_obj);

//| def stop() -> None:
//|     """Stop Bluetooth audio streaming."""
//|     ...
STATIC mp_obj_t btaudio_stop_obj(void) {
    common_hal_btaudio_stop();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(btaudio_stop_fun_obj, btaudio_stop_obj);

//| def pause() -> None:
//|     """Pause Bluetooth audio streaming."""
//|     ...
STATIC mp_obj_t btaudio_pause_obj(void) {
    common_hal_btaudio_pause();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(btaudio_pause_fun_obj, btaudio_pause_obj);

//| def resume() -> None:
//|     """Resume Bluetooth audio streaming."""
//|     ...
STATIC mp_obj_t btaudio_resume_obj(void) {
    common_hal_btaudio_resume();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(btaudio_resume_fun_obj, btaudio_resume_obj);

//| def set_volume(volume: int) -> None:
//|     """Set Bluetooth streaming volume level (0-100)."""
//|     ...
STATIC mp_obj_t btaudio_set_volume_obj(mp_obj_t vol_obj) {
    mp_int_t vol = mp_obj_get_int(vol_obj);
    if (vol < 0) vol = 0;
    if (vol > 100) vol = 100;
    common_hal_btaudio_set_volume((uint8_t)vol);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(btaudio_set_volume_fun_obj, btaudio_set_volume_obj);

//| def get_status() -> str:
//|     """Get current Bluetooth status ('disconnected', 'connecting', 'streaming', etc.)."""
//|     ...
STATIC mp_obj_t btaudio_get_status_obj(void) {
    const char *status = common_hal_btaudio_get_status();
    return mp_obj_new_str(status, strlen(status));
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(btaudio_get_status_fun_obj, btaudio_get_status_obj);

STATIC const mp_rom_map_elem_t btaudio_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_btaudio) },
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&btaudio_init_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&btaudio_deinit_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_connect), MP_ROM_PTR(&btaudio_connect_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_disconnect), MP_ROM_PTR(&btaudio_disconnect_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_is_connected), MP_ROM_PTR(&btaudio_is_connected_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_is_playing), MP_ROM_PTR(&btaudio_is_playing_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_play), MP_ROM_PTR(&btaudio_play_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_stop), MP_ROM_PTR(&btaudio_stop_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_pause), MP_ROM_PTR(&btaudio_pause_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_resume), MP_ROM_PTR(&btaudio_resume_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_set_volume), MP_ROM_PTR(&btaudio_set_volume_fun_obj) },
    { MP_ROM_QSTR(MP_QSTR_get_status), MP_ROM_PTR(&btaudio_get_status_fun_obj) },
};

STATIC MP_DEFINE_CONST_DICT(btaudio_module_globals, btaudio_module_globals_table);

const mp_obj_module_t btaudio_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&btaudio_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_btaudio, btaudio_module);
