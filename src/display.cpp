#include "display.hpp"
#include "pico/stdlib.h"
#include "hardware/spi.h"

static inline void cs_select() {
  gpio_put(PIN_DIS_CS, 0);
}

static inline void cs_deselect() {
  gpio_put(PIN_DIS_CS, 1);
}

void Display::write_cmd(uint8_t cmd) {
  gpio_put(PIN_DIS_CS, 0);
  cs_select();
  spi_write_blocking(DISPLAY_SPI_PORT, &cmd, 1);
  cs_deselect();
}

void Display::write_data(uint8_t data) {
  gpio_put(PIN_DIS_CS, 1);
  cs_select();
  spi_write_blocking(DISPLAY_SPI_PORT, &data, 1);
  cs_deselect();
}

void Display::write_data_buffer(const uint8_t *buffer, size_t len) {
  gpio_put(PIN_DIS_DC, 1);
  cs_select();
  spi_write_blocking(DISPLAY_SPI_PORT, buffer, len);
  cs_deselect();
}

void Display::set_window(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1) {
  write_cmd(0x2A);
  write_cmd(x0 >> 8);
  write_cmd(x0 & 0xFF);
  write_cmd(x1 >> 8);
  write_cmd(x1 & 0xFF);

  write_cmd(0x2B);
  write_cmd(y0 >> 8);
  write_cmd(y0 & 0xFF);
  write_cmd(y1 >> 8);
  write_cmd(y1 & 0xFF);
  
  write_cmd(0x2C);
}

void Display::set_backlight(bool enable) {
  gpio_put(PIN_DIS_LED, enable ? 1 : 0);
}

void Display::init() {
  spi_init(DISPLAY_SPI_PORT, 40*1000*1000);
  gpio_set_function(PIN_DIS_SCK, GPIO_FUNC_SPI);
  gpio_set_function(PIN_DIS_MOSI, GPIO_FUNC_SPI);

  gpio_init(PIN_DIS_CS);
  gpio_init(PIN_DIS_DC);
  gpio_init(PIN_DIS_RESET);
  gpio_init(PIN_DIS_LED);

  gpio_set_dir(PIN_DIS_CS, GPIO_OUT);
  gpio_set_dir(PIN_DIS_DC, GPIO_OUT);
  gpio_set_dir(PIN_DIS_RESET, GPIO_OUT);
  gpio_set_dir(PIN_DIS_LED, GPIO_OUT);

  cs_deselect();
  set_backlight(false);

  gpio_put(PIN_DIS_RESET, 1);
  sleep_ms(10);
  gpio_put(PIN_DIS_RESET, 0);
  sleep_ms(20);
  gpio_put(PIN_DIS_RESET, 1);
  sleep_ms(120);

  write_cmd(0x01);
  sleep_ms(150);

  write_cmd(0x11);
  sleep_ms(120);

  write_cmd(0x3A);
  write_data(0x55);

  write_cmd(0x36);
  write_data(0x00);

  write_cmd(0x21);
  write_cmd(0x13);

  write_cmd(0x29);
  sleep_ms(50);

  set_backlight(true);
}

void Display::fill_screen(uint16_t color) {
  draw_rect(0,0,LCD_WIDTH, LCD_HEIGHT, color);
}

void Display::draw_rect(int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color) {
  if (x >= LCD_WIDTH || y >= LCD_HEIGHT || w <= 0 || h <=0) return;
  if (x + w > LCD_WIDTH) w = LCD_HEIGHT - x;
  if (y + h > LCD_HEIGHT) h = LCD_HEIGHT - y;

  set_window(x,y,x+w-1,y+h-1);

  uint8_t high = color >> 8;
  uint8_t low = color & 0xFF;

  uint8_t scanline[w * 2];
  for (int i=0; i<w; i++) {
    scanline[i*2] = high;
    scanline[i*2+1] = low;
  }

  for (int row = 0; row < h; row++) {
    write_data_buffer(scanline, sizeof(scanline));
  }

}
