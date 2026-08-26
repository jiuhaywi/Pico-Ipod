 #ifndef PINOUT_H
#define PINOUT_H

#include "hardware/spi.h"
#include "hardware/pwm.h"

// ==============================================================================
// Display Interface: ST7789 IPS LCD (SPI1)
// ==============================================================================
#define DISPLAY_SPI_PORT    spi1
#define PIN_DIS_CS          13   // Chip Select (Active Low)
#define PIN_DIS_SCK         14   // SPI1 Clock
#define PIN_DIS_MOSI        15   // SPI1 TX / SDA / DIN
#define PIN_DIS_DC          20   // Data / Command Mode Selection
#define PIN_DIS_RESET       21   // Hardware Reset (Active Low)
#define PIN_DIS_LED         22   // Backlight Enable / PWM Brightness

// ==============================================================================
// Storage Interface: MicroSD Card Slot (SPI0)
// ==============================================================================
#define SD_SPI_PORT         spi0
#define PIN_SD_DAT0         16   // SPI0 RX (MISO / Data Out)
#define PIN_SD_CD           17   // Card Detect Switch (Active Low, Pull-Up)
#define PIN_SD_CLK          18   // SPI0 Clock (SCK)
#define PIN_SD_CMD          19   // SPI0 TX (MOSI / Data In)
// Note: If using a dedicated SD Chip Select pin, define PIN_SD_CS here.

// ==============================================================================
// User Inputs: EC11 Rotary Encoder & Directional Buttons
// ==============================================================================
#define PIN_ENC_A           10   // Rotary Encoder Phase A
#define PIN_ENC_B           11   // Rotary Encoder Phase B
#define PIN_ENC_SW          12   // Rotary Encoder Push Switch (Active Low)

#define PIN_BTN_UP          6    // Directional Button: Up / Play
#define PIN_BTN_DOWN        7    // Directional Button: Down / Menu
#define PIN_BTN_LEFT        8    // Directional Button: Left / Prev
#define PIN_BTN_RIGHT       9    // Directional Button: Right / Next

// ==============================================================================
// Audio Output: Dual PWM + RC Filter (PWM Slice 0)
// ==============================================================================
#define PIN_AUDIO_L         0    // Left Audio Channel (PWM0 A)
#define PIN_AUDIO_R         1    // Right Audio Channel (PWM0 B)

#endif // PINOUT_H
