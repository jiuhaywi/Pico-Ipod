#pragma once

#include <cstdint>
#include "pinout.hpp"

enum class InputEvent {
  NONE,
  SCROLL_UP,
  SCROLL_DOWN,
  CLICK_SELECT,
  BTN_UP,
  BTN_DOWN,
  BTN_LEFT,
  BTN_RIGHT

};

class InputHandler {
  public:
    static void init();
    static InputEvent poll();

  private:
    static uint8_t last_encoder_state_;
    static uint32_t last_btn_time_;



};




