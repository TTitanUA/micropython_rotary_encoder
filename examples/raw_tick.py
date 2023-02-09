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


# Start the event loop
print(f"Connect you rotary encoder to the next GPIO pins: CLK {ENCODER_CLK_PIN}, DT {ENCODER_DT_PIN} and SW {ENCODER_SW_PIN}")
print("In this example, we use the manual tick execution.")
print("This method allows you to have full control over how events are handled. But it can also cause events to be skipped.")
print("Use this method only if you understand what you are doing.")

tick_count = 0
while True:
    tick_count += 1
    if tick_count > 2000:
        print(f"Counter: {some_counter}")
        tick_count = 0

    encoder.raw_tick()
    utime.sleep_ms(1)
