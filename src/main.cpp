#include "pico/stdlib.h"
#include "display.hpp"
#include "input.hpp"

int main() {
  stdio_init_all();
  Display::init();
  InputHandler::init();

  Display::fill_screen(COLOR_DARK_GRAY);
  Display::draw_rect(0,0, LCD_WIDTH, 24, COLOR_IPOD_BLUE);

  int selected_row = 0;
  const int total_rows = 6;
  const int row_height = 36;
  const int start_y = 30;
  
  Display::draw_rect(0, start_y + (selected_row * row_height), LCD_WIDTH, row_height - 2, COLOR_CYAN);


  while (true) {
    InputEvent evt = InputHandler::poll();

    if (evt == InputEvent::SCROLL_UP || evt == InputEvent::BTN_UP) {
      if (selected_row > 0) {
        Display::draw_rect(0,start_y + (selected_row * row_height), LCD_WIDTH, row_height - 2, COLOR_DARK_GRAY);
        selected_row--;
        Display::draw_rect(0,start_y + (selected_row * row_height), LCD_WIDTH, row_height - 2, COLOR_CYAN);
      }
    } else if (evt == InputEvent::SCROLL_DOWN || evt == InputEvent::BTN_DOWN) {
      if (selected_row < total_rows - 1) {
        Display::draw_rect(0, start_y + (selected_row * row_height), LCD_WIDTH, row_height - 2, COLOR_DARK_GRAY);
        selected_row++;
        Display::draw_rect(0, start_y + (selected_row * row_height), LCD_WIDTH, row_height - 2, COLOR_CYAN);
      }
    }

    sleep_ms(5);
  }

  return 0;
}
