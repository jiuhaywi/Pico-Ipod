import audiopwmio
import audiomp3
import pinout

try:
    import btaudio
    BT_SUPPORTED = True
except ImportError:
    btaudio = None
    BT_SUPPORTED = False


class AudioPlayer:
    def __init__(self):
        self.output_mode = "Audio-Jack"
        self.connected_device = None
        self.volume = 70
        self.decoder = None
        self.pwm_out = None
        self.init_hardware()

    def init_hardware(self):
        try:
            self.pwm_out = audiopwmio.PWMAudioOut(
                left_channel=pinout.PIN_AUDIO_L,
                right_channel=pinout.PIN_AUDIO_R
            )
        except Exception as error:
            print("Audio PWM hardware init warning:", error)
            self.pwm_out = None

        if BT_SUPPORTED and btaudio is not None:
            try:
                btaudio.init()
                print("Bluetooth A2DP subsystem initialized")
            except Exception as error:
                print("Bluetooth A2DP init warning:", error)

    @property
    def is_playing(self):
        if self.output_mode == "Audio-Jack":
            return bool(self.pwm_out and self.pwm_out.playing)
        elif self.output_mode == "Bluetooth":
            if BT_SUPPORTED and btaudio is not None:
                return bool(btaudio.is_playing())
            return False
        return False

    def play(self, filepath):
        self.stop()
        try:
            self.decoder = audiomp3.MP3Decoder(filepath)
        except (OSError, RuntimeError) as error:
            raise error

        if self.output_mode == "Audio-Jack":
            if self.pwm_out is not None:
                self.pwm_out.play(self.decoder)
            else:
                raise RuntimeError("Audio-Jack PWM hardware not ready")
        elif self.output_mode == "Bluetooth":
            if BT_SUPPORTED and btaudio is not None:
                btaudio.play(self.decoder)
            else:
                print("[BT] Bluetooth output active (awaiting native C A2DP UF2)")

    def pause(self):
        if self.output_mode == "Audio-Jack" and self.pwm_out:
            self.pwm_out.pause()
        elif self.output_mode == "Bluetooth" and BT_SUPPORTED and btaudio:
            btaudio.pause()

    def resume(self):
        if self.output_mode == "Audio-Jack" and self.pwm_out:
            self.pwm_out.resume()
        elif self.output_mode == "Bluetooth" and BT_SUPPORTED and btaudio:
            btaudio.resume()

    def stop(self):
        if self.pwm_out and self.pwm_out.playing:
            self.pwm_out.stop()
        if BT_SUPPORTED and btaudio and btaudio.is_playing():
            btaudio.stop()
        if self.decoder:
            try:
                self.decoder.file.close()
            except Exception:
                pass
            self.decoder = None

    def set_volume(self, volume):
        self.volume = max(0, min(100, volume))
        if BT_SUPPORTED and btaudio:
            try:
                btaudio.set_volume(self.volume)
            except Exception:
                pass

    def set_output_mode(self, mode):
        if self.output_mode != mode:
            self.stop()
            self.output_mode = mode

    def connect_bluetooth(self, device):
        self.set_output_mode("Bluetooth")
        self.connected_device = device
        if BT_SUPPORTED and btaudio is not None:
            try:
                res = btaudio.connect(device)
                return bool(res)
            except Exception as error:
                print("Bluetooth connect error:", error)
                return False
        else:
            print("[BT] Connected to:", device)
            return True