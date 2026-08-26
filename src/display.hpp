#pragma once
#include <cstdint>
#include <cstddef>
#include "pinout.hpp"

#define LCD_WIDTH   240
#define LCD_HEIGHT  320

// RGB to RGB565
constexpr uint16_t rgb(uint8_t r, uint8_t g, uint8_t b) {
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3);
}


#define COLOR_BLACK 0x0000
#define COLOR_WHITE 0xFFFF
#define COLOR_GRAY 0x7BEF
#define COLOR_DARK_GRAY 0x3186
#define COLOR_BLUE 0x001F
#define COLOR_CYAN 0x07FF
#define COLOR_IPOD_BLUE 0x035D




class Display {
  public:
    static void init();
    static void set_backlight(bool enable);
    static void fill_screen(uint16_t color);
    static void draw_rect(int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color);
    static void set_window(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1);

  private:
      static void write_cmd(uint8_t cmd);
      static void write_data(uint8_t data);
      static void write_data_buffer(const uint8_t *buffer, size_t len);
};
