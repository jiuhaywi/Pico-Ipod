import digitalio
import rotaryio
import pinout

class InputManager:
    def __init__(self):
        self.encoder = rotaryio.IncrementalEncoder(pinout.PIN_ENC_A, pinout.PIN_ENC_B)
        self.last_position = 0
        
        # Center click / encoder switch (SW)
        self.btn_encoder_sw = digitalio.DigitalInOut(pinout.PIN_ENC_SW)
        self.btn_encoder_sw.direction = digitalio.Direction.INPUT
        self.btn_encoder_sw.pull = digitalio.Pull.UP
        self._last_sw = True

        # Directional push buttons
        self.btn_up = digitalio.DigitalInOut(pinout.PIN_BTN_UP)
        self.btn_up.direction = digitalio.Direction.INPUT
        self.btn_up.pull = digitalio.Pull.UP
        self._last_up = True

        self.btn_down = digitalio.DigitalInOut(pinout.PIN_BTN_DOWN)
        self.btn_down.direction = digitalio.Direction.INPUT
        self.btn_down.pull = digitalio.Pull.UP
        self._last_down = True

        self.btn_left = digitalio.DigitalInOut(pinout.PIN_BTN_LEFT)
        self.btn_left.direction = digitalio.Direction.INPUT
        self.btn_left.pull = digitalio.Pull.UP
        self._last_left = True

        self.btn_right = digitalio.DigitalInOut(pinout.PIN_BTN_RIGHT)
        self.btn_right.direction = digitalio.Direction.INPUT
        self.btn_right.pull = digitalio.Pull.UP
        self._last_right = True

    def get_track_delta(self):
        """Only UP and DOWN buttons control song selection."""
        delta = 0
        curr_up = self.btn_up.value
        if self._last_up and not curr_up:
            delta -= 1
        self._last_up = curr_up

        curr_down = self.btn_down.value
        if self._last_down and not curr_down:
            delta += 1
        self._last_down = curr_down
        return delta

    def get_volume_delta(self):
        """Rotary encoder turning controls volume in steps of 10."""
        current_pos = self.encoder.position
        diff = current_pos - self.last_position
        if diff != 0:
            self.last_position = current_pos
            return diff * 10
        return 0

    def is_output_toggle_pressed(self):
        """Clicking encoder in (SW) toggles between Bluetooth and Audio-Jack."""
        curr = self.btn_encoder_sw.value
        pressed = self._last_sw and not curr
        self._last_sw = curr
        return pressed

    def is_play_pressed(self):
        """RIGHT button activates the selected tab."""
        curr = self.btn_right.value
        pressed = self._last_right and not curr
        self._last_right = curr
        return pressed

    def is_back_pressed(self):
        """LEFT button goes back to the previous tab."""
        curr = self.btn_left.value
        pressed = self._last_left and not curr
        self._last_left = curr
        return pressed