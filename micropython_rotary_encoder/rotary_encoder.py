import utime
from machine import Pin


class RotaryEncoderEvent:
    ANY = 1
    CLICK = 2
    MULTIPLE_CLICK = 3
    HELD = 4
    RELEASED = 5
    TURN_LEFT = 6
    TURN_LEFT_FAST = 7
    TURN_LEFT_HOLD = 8
    TURN_LEFT_FAST_HOLD = 9
    TURN_RIGHT = 10
    TURN_RIGHT_FAST = 11
    TURN_RIGHT_HOLD = 12
    TURN_RIGHT_FAST_HOLD = 13


class RotaryEncoder:
    """Base class for encoder button"""

    pin_clk: Pin
    "attribute EncoderButton.pin_clk is the pin for the encoder clk"

    pin_dt: Pin
    "attribute EncoderButton.pin_dt is the pin for the encoder dt"

    pin_sw: Pin
    "attribute EncoderButton.pin_sw is the pin for the encoder sw"

    sw_debounce_ms: int = 50
    "attribute EncoderButton.sw_debounce_ms is used to filter out pin jitter"

    enc_step: int = 1
    "attribute EncoderButton.enc_step is used to filter out pin jitter"

    sw_hold_ms: int = 1000
    "attribute EncoderButton.sw_hold_ms is used to detect a long press"

    sw_step_ms: int = 200
    "attribute EncoderButton.sw_step_ms is used to detect a multiple press"

    sw_click_ms: int = 400
    "attribute EncoderButton.sw_click_ms is used to detect a single click"

    enc_fast_ms: int = 50
    "attribute EncoderButton.enc_fast_ms is used to detect a fast encoder turn"

    _enc_last_event_ms: int = 0

    _enc_last_dir: int = 0

    _enc_last_status: int = 0

    _flag_last_event: int = 0

    _sw_last_event_ms: int = 0

    _sw_prev_event_ms: int = 0

    _sw_prev_state: bool = False

    _sw_last_state: bool = False

    _sw_held_with_encoder: bool = False

    _sw_held: bool = False

    _sw_clicks: int = 0

    _listeners: dict = {}

    def __init__(
            self,
            pin_clk: Pin = None,
            pin_dt: Pin = None,
            pin_sw: Pin = None,
            debounce_ms: int = 50,
            encoder_step: int = 1,
            hold_ms: int = 1000,
            step_ms: int = 200,
            fast_ms: int = 50,
            click_ms: int = 400,
    ):
        self.pin_clk = pin_clk
        self.pin_dt = pin_dt
        self.pin_sw = pin_sw
        self.sw_debounce_ms = debounce_ms
        self.enc_step = encoder_step
        self.sw_hold_ms = hold_ms
        self.sw_step_ms = step_ms
        self.enc_fast_ms = fast_ms
        self.sw_click_ms = click_ms

    def on(self, event: int, callback: callable):
        if event not in self._listeners:
            self._listeners[event] = []

        self._listeners[event].append(callback)

    def off(self, event: int, callback: callable):
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def off_all(self, event: int, callback: callable = None):
        if event in self._listeners:
            if callback is None:
                self._listeners[event] = []
            else:
                while callback in self._listeners[event]:
                    self._listeners[event].remove(callback)

    def _sw_irq_handler(self, pin):
        timestamp = utime.ticks_ms()
        c_s = pin.value() == 0

        if self._sw_last_state == c_s or utime.ticks_diff(timestamp, self._sw_last_event_ms) < self.sw_debounce_ms:
            return

        self._sw_prev_state = self._sw_last_state
        self._sw_last_state = c_s
        self._sw_last_event_ms = timestamp

    def _sw_tick_process_event(self):
        # local cache
        __sw_l_s = self._sw_last_state
        __sw_h_w_e = self._sw_held_with_encoder
        __sw_s_ms = self.sw_step_ms
        __sw_l_e_ms = self._sw_last_event_ms
        __sw_p_e_ms = self._sw_prev_event_ms

        # button event already processed
        if __sw_l_s == self._sw_prev_state:
            return

        # process encoder event with held button
        if __sw_h_w_e and __sw_l_s:
            return

        elif __sw_h_w_e and not __sw_l_s:
            self._sw_held_with_encoder = False
            self._sw_last_event_ms = 0
            return

        timestamp = utime.ticks_ms()

        # button pressed
        if __sw_l_s:
            # button held
            if utime.ticks_diff(utime.ticks_ms(), __sw_l_e_ms) > self.sw_hold_ms and not self._sw_held:
                self._sw_held = True
                self._flag_last_event = RotaryEncoderEvent.HELD
            # it's a multiple click
            elif utime.ticks_diff(__sw_l_e_ms, self._sw_prev_event_ms) < __sw_s_ms:
                self._sw_prev_event_ms = 1
        else:
            # button release
            if self._sw_held:
                self._sw_held = False
                self._flag_last_event = RotaryEncoderEvent.RELEASED
                self._sw_prev_state = __sw_l_s
            # maybe a multiple click, need wait for the next event
            elif utime.ticks_diff(timestamp, __sw_l_e_ms) < __sw_s_ms:
                if __sw_p_e_ms == 1:
                    if self._sw_clicks == 0:
                        self._sw_clicks = 1
                    self._sw_clicks += 1
                self._sw_prev_event_ms = timestamp
            # maybe a single click
            elif utime.ticks_diff(timestamp, __sw_l_e_ms) < self.sw_click_ms:
                # it's a single click
                if self._sw_clicks == 0:
                    self._flag_last_event = RotaryEncoderEvent.CLICK
                else:
                    self._flag_last_event = RotaryEncoderEvent.MULTIPLE_CLICK
                self._sw_prev_state = __sw_l_s
            # some old event, skip it
            else:
                self._sw_prev_state = __sw_l_s

    def _enc_irq_handler(self, pin):
        new_status = (self.pin_dt.value() << 1) | self.pin_clk.value()
        if new_status == self._enc_last_status:
            return

        transition = (self._enc_last_status << 2) | new_status

        if self._sw_last_state:
            self._sw_held_with_encoder = True

        direction = 0
        if transition == 0b1110:
            direction = 1
        elif transition == 0b1101:
            direction = -1

        if direction != 0:
            self._enc_process_event(direction)

        self._enc_last_status = new_status

    def _enc_process_event(self, direction: int):
        self._enc_last_dir += direction
        self._enc_last_event_ms = utime.ticks_ms()

    def _enc_tick_process_turn_event(self):
        # local cache
        __e_l_d = self._enc_last_dir

        # @FIXME: It is a crunch, but it works for now
        # 15ms it's a time for one step
        if self.enc_fast_ms == 0:
            fast_turn_count = 1000
        else:
            fast_turn_count = (self.enc_fast_ms // 15)

        if __e_l_d > 0:
            if __e_l_d > fast_turn_count:
                if self._sw_held_with_encoder:
                    self._flag_last_event = RotaryEncoderEvent.TURN_RIGHT_FAST_HOLD
                else:
                    self._flag_last_event = RotaryEncoderEvent.TURN_RIGHT_FAST
            else:
                if self._sw_held_with_encoder:
                    self._flag_last_event = RotaryEncoderEvent.TURN_RIGHT_HOLD
                else:
                    self._flag_last_event = RotaryEncoderEvent.TURN_RIGHT
        else:
            if __e_l_d < -fast_turn_count:
                if self._sw_held_with_encoder:
                    self._flag_last_event = RotaryEncoderEvent.TURN_LEFT_FAST_HOLD
                else:
                    self._flag_last_event = RotaryEncoderEvent.TURN_LEFT_FAST
            else:
                if self._sw_held_with_encoder:
                    self._flag_last_event = RotaryEncoderEvent.TURN_LEFT_HOLD
                else:
                    self._flag_last_event = RotaryEncoderEvent.TURN_LEFT

        self._enc_last_dir = 0

    def __encoder_has_event(self):
        return self._enc_last_dir >= self.enc_step or self._enc_last_dir <= -self.enc_step

    def __tick(self):
        self._sw_tick_process_event()

        if self.__encoder_has_event() and utime.ticks_diff(utime.ticks_ms(),
                                                           self._enc_last_event_ms) > self.enc_fast_ms:

            self._enc_tick_process_turn_event()
        if self._flag_last_event != 0:
            try:
                self.__call_listeners()
            except Exception as e:
                print(f"RotaryEncoder call listeners error: {e}")

            if self._flag_last_event == RotaryEncoderEvent.MULTIPLE_CLICK:
                self._sw_clicks = 0

            self._flag_last_event = 0

    def __call_listeners(self):
        # local cache
        __l_e = self._flag_last_event

        if __l_e != 0:
            # local cache
            __sw_c = self._sw_clicks
            __e_e = RotaryEncoderEvent.ANY
            __m_c_e = RotaryEncoderEvent.MULTIPLE_CLICK
            __list = self._listeners

            if __l_e in __list:
                for __l in __list[__l_e]:
                    try:
                        if __l_e == __m_c_e:
                            __l(__sw_c)
                        else:
                            __l()
                    except Exception as e:
                        print(f"RotaryEncoder callback error. Event: {__l_e}, Listener: {__l}, Error: {e}")
            if __e_e in __list:
                for __l in __list[__e_e]:
                    try:
                        if __l_e == __m_c_e:
                            __l(__l_e, __sw_c)
                        else:
                            __l(__l_e, 0)
                    except Exception as e:
                        print(f"RotaryEncoder callback error. Event: {__e_e}, Listener: {__l}, Error: {e}")
