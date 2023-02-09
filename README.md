This is an automatic translation, may be incorrect in some places. See sources and examples!
# Rotary Encoder
Library for Raspberry Pi Pico microcontroller encoder using MicroPython language.
Library features:
- Encoder: normal rotation, pressed rotation, fast rotation
- Button: anti-rattle, hold, click, multiple clicks
- Encoder button registration is optional
- Interrupts are used for registering events
- Events can be handled in several ways:
    - With asyncio task (recommended)
    - By interrupt timer
    - Independent function call

The following materials were used to develop the library:
- Library [Rotary Encoder](https://github.com/MikeTeachman/micropython-rotary) by Mike Teachman
- Library (Arduino) [EncButton](https://github.com/GyverLibs/EncButton), by AlexGyver
- Material [Rotary Encoder](https://www.coderdojotc.org/micropython/sensors/10-rotary-encoder/), by CoderDojoTC

### Compatibility
- MicroPython 1.19.1
- Raspberry Pi Pico
- Rotary Encoder EC11 (KY-040)

On the hardware above the library has been tested and works correctly.
But with small crutches, it can work on other equipment.

### ATTENTION
You use this module at your own risk. 
My experience in MicroPython programming is the whole 7 days. So there may be nuances that I haven't considered.
If you notice a bug or have suggestions for improvement, write to Issues.

## Contents
- [Install](https://github.com/TTitanUA/micropython_rotary_encoder#install)
- [Initialization](https://github.com/TTitanUA/micropython_rotary_encoder#init)
- [Documentation](https://github.com/TTitanUA/micropython_rotary_encoder#doc)
- [Examples](https://github.com/TTitanUA/micropython_rotary_encoder/tree/main/examples)
- [Bugs and feedback](https://github.com/TTitanUA/micropython_rotary_encoder#feedback)

<a id="install"></a>
## Installation
- Install the library via pip (Thonny -> Manage Packages) by name **micropython-rotary-encoder**
- Or manual installation:
   - [Download library from github](https://github.com/TTitanUA/micropython_rotary_encoder/)
   - take the **micropython_rotary_encoder** folder from the archive.
   - upload to the root of the microcontroller or to the **lib** folder.

If you want to play around with the logic of the library, then the 2nd installation option is preferable. :)

<a id="init"></a>
## Usage
### Initialization
```python
from machine import Pin
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent

# create pins for encoder and button
en_pin_clk = Pin(15, Pin.IN, Pin.PULL_UP)
en_pin_dt = Pin(9, Pin.IN, Pin.PULL_UP)
en_pin_sw = Pin(8, Pin.IN, Pin.PULL_UP)

# create an encoder object
encoder = RotaryEncoderRP2(en_pin_clk, en_pin_dt, en_pin_sw)
```
After initialization, the encoder automatically subscribes to encoder and button pin interrupts.
But encoder event processing must be started manually.

#### Using the uasyncio library
This is the best option for most projects.
```python
# at the beginning of the file add the import of the uasyncio library
import uasyncio as asyncio

# ----
# Encoder initialization code above ^
# ----

async def async_some_other_task():
    print("async_some_other_task")
    while True:
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(
        encoder.async_tick(1), # run encoder event handling every 1ms
        async_some_other_task(),
    )

asyncio.run(main())
```

#### With timer interrupts
You can read more about timers [here](https://docs.micropython.org/en/latest/library/machine.Timer.html)
For Raspberry Pi Pico [here](https://docs.micropython.org/en/latest/rp2/quickref.html#timers)
Be careful, although this is the easiest option, it is not optimal.
Since encoder events are handled in a timer interrupt, other interrupts will be delayed.
```python
# ----
# Encoder initialization code above ^
# ----

encoder.timer_tick(1) # запускаем обработку событий энкодера каждые 1 мс
```

#### By manual call
Everything is in your hands, but don't forget to call the `raw_tick()` method every 1 - 5 ms.
```python
import utime
# ----
# Encoder initialization code above ^
# ----

while True:
    encoder.raw_tick() # handle encoder events
    utime.sleep_ms(1) # delay
```

<a id="doc"></a>
## Documentation
### Constructor parameters

| Parameter    | Type | Default | Description                            |
|--------------|------|---------|----------------------------------------|
| pin_clk      | pin  | None    | Pin CLK encoder                        |
| pin_dt       | pin  | None    | Pin DT encoder                         |
| pin_sw       | pin  | None    | Pin buttons                            |
| debounce_ms  | int  | 50      | Contact bounce timeout                 |
| encoder_step | int  | 1       | Encoder step                           |
| hold_ms      | int  | 1000    | Button hold timeout                    |
| step_ms      | int  | 200     | Timeout between encoder events         |
| fast_ms      | int  | 50      | Timeout between encoder events on hold |
| click_ms     | int  | 400     | Timeout between button presses         |

- `pin_clk`, `pin_dt` - encoder pins, if one of them is not specified, then the library will work only in button mode.
- `pin_sw` - optional parameter, if not specified, the library will work only in encoder mode.
- `debounce_ms` - contact bounce timeout, protection against false positives of the button.
- `encoder_step` - encoder step, this is the number of encoder events before triggering.
For example, if the step is 1, then each encoder event will fire a trigger.
If the step is 2, then the trigger will fire on every second encoder event.
Useful for compensating for encoder chatter.
- `hold_ms` - button hold timeout, if the button is held longer than this time, the `HELD` event will fire.
- `step_ms` - timeout between multiple clicks, if click events occur faster than this time, the `MULTIPLE_CLICK` event will fire.
- `fast_ms` - timeout between encoder events for fast scrolling `TURN_LEFT_FAST | TURN_RIGHT_FAST`.
- `click_ms` - timeout between clicking and releasing the button for the `CLICK` event.

### События
Encoder/button events are passed to callbacks, which can be registered with the `on()` method.

| Event                | Parameters passed to callback | Trigger condition                                                   |
|----------------------|-------------------------------|---------------------------------------------------------------------|
| ANY                  | event_id: int, clicks: int    | Duplicate any event                                                 |
| CLICK                | None                          | The button was pressed and released in `click_ms`                   |
| MULTIPLE_CLICK       | clicks: int                   | The button was pressed, released and pressed again within `step_ms` |
| HELD                 | None                          | Button held longer `hold_ms`                                        |
| RELEASE              | None                          | The button was released after `HELD`                                |
| TURN_LEFT            | None                          | The encoder has been turned to the left                             |
| TURN_LEFT_FAST       | None                          | The encoder was turned faster than `fast_ms`                        |
| TURN_LEFT_HOLD       | None                          | The encoder was turned to the left and with the                     |
| TURN_LEFT_FAST_HOLD  | None                          | The encoder was turned faster than `fast_ms` and with the           |
| TURN_RIGHT           | None                          | The encoder has been turned to the right                            |
| TURN_RIGHT_FAST      | None                          | The encoder was turned faster than `fast_ms`                        |
| TURN_RIGHT_HOLD      | None                          | The encoder was turned to the right and with the pressed button     |
| TURN_RIGHT_FAST_HOLD | None                          | The encoder was turned faster than `fast_ms` and with the           |

### Register callbacks
To register callbacks, you need to use the `on(event, callback)` method, which takes two parameters.
- `event` - event, property of the `RotaryEncoderEvent` class.
- `callback` - a function that will be called when the event fires.
The number of arguments to the callback function depends on the event. See table above.

```python

# ----
# Encoder initialization code above ^
# ----

# subscribe to encoder events
def on_click():
    print("CLICK")
    
def on_multy_clicks(clicks: int):
    print(f"CLICK {clicks} times")

def on_any(event_id: int, clicks: int):
    print(f"ANY {event_id}, clicks {clicks}")

encoder.on(RotaryEncoderEvent.CLICK, on_click)
encoder.on(RotaryEncoderEvent.MULTIPLE_CLICK, on_multy_clicks)
encoder.on(RotaryEncoderEvent.ANY, on_any)
```

### Unsubscribing from events
To unsubscribe from events, you need to use the `off(event, callback)` method, which takes two parameters.
- `event` - event, property of the `RotaryEncoderEvent` class.
- `callback` - a link to a function that was registered earlier.
For one method call, only one callback from one event is unsubscribed.

```python
# ----
# Callback registration code above ^
# ----

# unsubscribe from the encoder event
encoder.off(RotaryEncoderEvent.CLICK, on_click)

# example with multiple subscription
encoder.on(RotaryEncoderEvent.CLICK, on_click) # subscribe first
encoder.on(RotaryEncoderEvent.CLICK, on_click) # subscribe second

encoder.off(RotaryEncoderEvent.CLICK, on_click) # unsubscribe first
```

### Unsubscribe from all events
To unsubscribe from all events, you need to use the `off_all()` method, which takes two parameters.
- `event` - event, property of the `RotaryEncoderEvent` class.
- `callback` - a reference to a function that was registered earlier, if it is not passed, then all listeners of this event will be unsubscribed.

```python
# ----
# Encoder initialization code above ^
# ----
def on_click():
    print("CLICK")

def on_click2():
    print("CLICK2")


encoder.on(RotaryEncoderEvent.CLICK, on_click) # subscribe first, with callback on_click
encoder.on(RotaryEncoderEvent.CLICK, on_click2) # subscribe second, with callback on_click2
encoder.on(RotaryEncoderEvent.CLICK, on_click) # subscribe third, with callback on_click

# unsubscribe from the RotaryEncoderEvent.CLICK event only listeners with the on_click callback function
encoder.off_all(RotaryEncoderEvent.CLICK, on_click) # unsubscribe all `on_click` listeners from event RotaryEncoderEvent.CLICK

# unsubscribe from the RotaryEncoderEvent.CLICK event of all listeners
encoder.off_all(RotaryEncoderEvent.CLICK) # unsubscribe all listeners from event RotaryEncoderEvent.CLICK
```

## Examples
Examples of using the encoder can be found in the [examples](https://github.com/TTitanUA/micropython_rotary_encoder/tree/main/examples) folder.

<a id="feedback"></a>
## Bugs and feedback
If you find bugs, create [issue](https://github.com/TTitanUA/micropython_rotary_encoder/issues).
The library is open for revision and your [pull requests](https://github.com/TTitanUA/micropython_rotary_encoder/pulls).
