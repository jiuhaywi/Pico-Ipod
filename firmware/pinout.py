import board

# ==============================================================================
# Display: ILI9341 IPS LCD (SPI1)
# ==============================================================================
PIN_DISPLAY_CLK = board.GP14
PIN_DISPLAY_DIN = board.GP15
PIN_DISPLAY_CS  = board.GP13
PIN_DISPLAY_DC  = board.GP21
PIN_DISPLAY_RST = board.GP20
PIN_DISPLAY_BL  = board.GP22

# ==============================================================================
# Storage: MicroSD Card Slot (SPI0)
# ==============================================================================
PIN_SD_DAT3   = board.GP17
PIN_SD_CMD     = board.GP19
PIN_SD_CLK    = board.GP18
PIN_SD_DAT0   = board.GP16

# ==============================================================================
# User Inputs: EC11 Rotary Encoder & Directional Buttons
# ==============================================================================
PIN_ENC_A     = board.GP10
PIN_ENC_B     = board.GP11
PIN_ENC_SW    = board.GP12

PIN_BTN_UP    = board.GP2
PIN_BTN_DOWN  = board.GP3
PIN_BTN_LEFT  = board.GP4
PIN_BTN_RIGHT = board.GP5

# ==============================================================================
# Audio Output: Dual PWM Stage (PWM0 A/B)
# ==============================================================================
PIN_AUDIO_L   = board.GP0
PIN_AUDIO_R   = board.GP1
