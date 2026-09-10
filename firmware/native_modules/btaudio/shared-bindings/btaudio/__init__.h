#ifndef MICROPY_INCLUDED_SHARED_BINDINGS_BTAUDIO___INIT___H
#define MICROPY_INCLUDED_SHARED_BINDINGS_BTAUDIO___INIT___H

#include "py/obj.h"

extern const mp_obj_type_t btaudio_type;

void common_hal_btaudio_init(void);
void common_hal_btaudio_deinit(void);
bool common_hal_btaudio_connect(const char *address);
void common_hal_btaudio_disconnect(void);
bool common_hal_btaudio_is_connected(void);
bool common_hal_btaudio_is_playing(void);
void common_hal_btaudio_play(mp_obj_t sample_obj);
void common_hal_btaudio_stop(void);
void common_hal_btaudio_pause(void);
void common_hal_btaudio_resume(void);
void common_hal_btaudio_set_volume(uint8_t volume);
const char *common_hal_btaudio_get_status(void);

#endif // MICROPY_INCLUDED_SHARED_BINDINGS_BTAUDIO___INIT___H
