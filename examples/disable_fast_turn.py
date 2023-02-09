from machine import Pin
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent
import utime

# constants
ENCODER_CLK_PIN = 15
ENCODER_DT_PIN = 9
ENCODER_SW_PIN = 8


# Define the pins for the rotary encoder and the button
encoder_pin_clk = Pin(ENCODER_CLK_PIN, Pin.IN, Pin.PULL_UP)
encoder_pin_dt = Pin(ENCODER_DT_PIN, Pin.IN, Pin.PULL_UP)
encoder_pin_sw = Pin(ENCODER_SW_PIN, Pin.IN, Pin.PULL_UP)

# Create the rotary encoder object
encoder = RotaryEncoderRP2(
    pin_clk=encoder_pin_clk,
    pin_dt=encoder_pin_dt,
    pin_sw=encoder_pin_sw,
    fast_ms=0,  # disable fast turn events
)

some_counter = 0


# Listeners
def turn_left_listener():
    global some_counter
    some_counter -= 1
    print(f"Turn left")


def turn_right_listener():
    global some_counter
    some_counter += 1
    print(f"Turn right")


# subscribe to events
encoder.on(RotaryEncoderEvent.TURN_LEFT, turn_left_listener)
encoder.on(RotaryEncoderEvent.TURN_RIGHT, turn_right_listener)

# Subscribe to system timer irq
encoder.timer_tick()


# Start the event loop
print(f"Connect you rotary encoder to the next GPIO pins: CLK {ENCODER_CLK_PIN}, DT {ENCODER_DT_PIN} and SW {ENCODER_SW_PIN}")
print("In this example, we disable a fast turn events.")
print("TURN_LEFT_FAST, TURN_RIGHT_FAST, TURN_LEFT_FAST_HOLD, TURN_RIGHT_FAST_HOLD events are not fired.")

while True:
    print(f"Counter: {some_counter}")
    utime.sleep(2)
