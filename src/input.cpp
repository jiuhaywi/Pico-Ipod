#include "input.hpp"
#include "pico/stdlib.h"

uint8_t InputHandler::last_encoder_state_ = 0;
uint32_t InputHandler::last_btn_time_ = 0;

void InputHandler::init() {
  gpio_init(PIN_ENC_A);
  gpio_init(PIN_ENC_B);
  gpio_init(PIN_ENC_SW);

  gpio_set_dir(PIN_ENC_A, GPIO_IN);
  gpio_set_dir(PIN_ENC_B, GPIO_IN);
  gpio_set_dir(PIN_ENC_SW, GPIO_IN);

  gpio_pull_up(PIN_ENC_A);
  gpio_pull_up(PIN_ENC_B);
  gpio_pull_up(PIN_ENC_SW);

  const uint btn_pins[] = { PIN_BTN_UP, PIN_BTN_DOWN, PIN_BTN_LEFT, PIN_BTN_RIGHT };
  for (uint pin : btn_pins) {
    gpio_init(pin);
    gpio_set_dir(pin, GPIO_IN);
    gpio_pull_up(pin);
  }

  last_encoder_state_ = (gpio_get(PIN_ENC_A) << 1) | gpio_get(PIN_ENC_B);

}

InputEvent InputHandler::poll() {
  uint8_t current_state = (gpio_get(PIN_ENC_A) << 1) | gpio_get(PIN_ENC_B);

  if (current_state != last_encoder_state_) {
    if (current_state == 0b11) {
      if (last_encoder_state_ == 0b01) {
        last_encoder_state_ = current_state;
        return InputEvent::SCROLL_UP;
      } else if (last_encoder_state_ == 0b10) {
        last_encoder_state_ = current_state;
        return InputEvent::SCROLL_DOWN;
      }
    }
    last_encoder_state_ = current_state;
  }

  uint32_t now = to_ms_since_boot(get_absolute_time());
  if (now - last_btn_time_ > 150) {
    if (!gpio_get(PIN_ENC_SW)) {
      last_btn_time_ = now;
      return InputEvent::CLICK_SELECT;
    }
    if (!gpio_get(PIN_BTN_UP)) {
      last_btn_time_ = now;
      return InputEvent::BTN_UP;
    }
    if (!gpio_get(PIN_BTN_DOWN)) {
      last_btn_time_ = now;
      return InputEvent::BTN_DOWN;
    }
    if (!gpio_get(PIN_BTN_LEFT)) {
      last_btn_time_ = now;
      return InputEvent::BTN_LEFT;
    }
    if (!gpio_get(PIN_BTN_RIGHT)) {
      last_btn_time_ = now;
      return InputEvent::BTN_RIGHT;
    }
  }
  return InputEvent::NONE;
}
