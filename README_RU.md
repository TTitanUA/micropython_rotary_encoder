# Rotary Encoder
Библиотека для работы с энкодером на микроконтроллере Raspberry Pi Pico на языке MicroPython.
Возможности библиотеки:
- Энкодер: обычный поворот, нажатый поворот, быстрый поворот
- Кнопка: антидребезг, удержание, клик, несколько кликов
- Регистрация кнопки энкодера не обязательна
- Для регистрации событий используется прерывания
- Обработка событий может быть выполнена несколькими способами:
    - С помощью задачи asyncio (рекомендуется)
    - Таймером прерывания
    - Самостоятельным вызовом функции

При разработке библиотеки использовались следующие материалы:
- Библиотека [Rotary Encoder](https://github.com/MikeTeachman/micropython-rotary), автор Mike Teachman
- Библиотека (Arduino) [EncButton](https://github.com/GyverLibs/EncButton), автор AlexGyver
- Материал [Rotary Encoder](https://www.coderdojotc.org/micropython/sensors/10-rotary-encoder/), автор CoderDojoTC

### Совместимость
- MicroPython 1.19.1
- Raspberry Pi Pico
- Rotary Encoder EC11 (KY-040)

На представленном выше оборудовании библиотека была протестирована и работает корректно.
Но с не большими костылями она может работать и на другом оборудовании.

### ВНИМАНИЕ
Вы используете данный модуль на свой страх и риск. 
Мой опыт в программировании на MicroPython равняется целым 7 дням. Так что могут быть нюансы, которые я не учел.
Если вы заметили ошибку или у вас есть предложения по улучшению, то пишите в Issues.

## Содержание
- [Установка](#install)
- [Инициализация](#init)
- [Документация](#doc)
- [Примеры](https://github.com/TTitanUA/micropython_rotary_encoder/tree/main/examples)
- [Баги и обратная связь](#feedback)

<a id="install"></a>
## Установка
- Библиотеку установить через pip (Thonny -> Manage Packages) по названию **micropython-rotary-encoder** 
- Или ручная установка:
  - [Скачать библиотеку с github](https://github.com/TTitanUA/micropython_rotary_encoder/) 
  - забрать папку **micropython_rotary_encoder** из архива.
  - загрузить в корень микроконтроллера или в папку **lib**.

Если хотите поиграться с логикой библиотеки, то 2й вариант установки предпочтительнее. :)

<a id="init"></a>
## Использование
### Инициализация
```python
from machine import Pin
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent

# создаем пины для энкодера и кнопки
en_pin_clk = Pin(15, Pin.IN, Pin.PULL_UP)
en_pin_dt = Pin(9, Pin.IN, Pin.PULL_UP)
en_pin_sw = Pin(8, Pin.IN, Pin.PULL_UP)

# создаем объект энкодера
encoder = RotaryEncoderRP2(en_pin_clk, en_pin_dt, en_pin_sw)
```
После инициализации энкодер автоматически подписывается на прерывания пинов энкодера и кнопки.
Но обработку событий энкодера необходимо запускать вручную.

#### С помощью библиотеки uasyncio
Это оптимальный вариант для большинства проектов.
```python
# в начало файла добавляем импорт библиотеки uasyncio
import uasyncio as asyncio

# ----
# Код инициализации энкодера выше ^
# ----

async def async_some_other_task():
    print("async_some_other_task")
    while True:
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(
        encoder.async_tick(1), # запускаем обработку событий энкодера каждые 1 мс
        async_some_other_task(),
    )

asyncio.run(main())
```

#### С помощью прерываний по таймеру
Подробнее про таймеры можно почитать [здесь](https://docs.micropython.org/en/latest/library/machine.Timer.html)
Для Raspberry Pi Pico [здесь](https://docs.micropython.org/en/latest/rp2/quickref.html#timers)
Будьте внимательны, хоть это и самый простой вариант, но он не оптимален.
Так как обработка событий энкодера происходит в прерывании по таймеру, другие прерывания будут отложены.
```python
# ----
# Код инициализации энкодера выше ^
# ----

encoder.timer_tick(1) # запускаем обработку событий энкодера каждые 1 мс
```

#### С помощью ручного вызова
Все в ваших руках, но не забывайте вызывать метод `raw_tick()` каждые 1 - 5 мс.
```python
import utime
# ----
# Код инициализации энкодера выше ^
# ----

while True:
    encoder.raw_tick() # обрабатываем события энкодера
    utime.sleep_ms(1) # задержка
```

<a id="doc"></a>
## Документация
### Параметры конструктора

| Параметр          | Тип  | По умолчанию | Описание                                        |
|-------------------|------|--------------|-------------------------------------------------|
| pin_clk           | Pin  | None         | Пин CLK энкодера                                |
| pin_dt            | Pin  | None         | Пин DT энкодера                                 |
| pin_sw            | Pin  | None         | Пин кнопки                                      |
| debounce_ms       | int  | 50           | Таймаут дребезга контактов                      |
| encoder_step      | int  | 1            | Шаг энкодера                                    |
| hold_ms           | int  | 1000         | Таймаут удержания кнопки                        |
| step_ms           | int  | 200          | Таймаут между событиями энкодера                |
| fast_ms           | int  | 50           | Таймаут между событиями энкодера при удержании  |
| click_ms          | int  | 400          | Таймаут между нажатиями кнопки                  |

- `pin_clk`, `pin_dt` - пины энкодера, если одтин из них не указан, то библиотека будет работать только в режиме кнопки.
- `pin_sw` - необязательный параметр, если не указан, то библиотека будет работать только в режиме энкодера.
- `debounce_ms` - таймаут дребезга контактов, защита от ложных срабатываний кнопки.
- `encoder_step` - шаг энкодера, это количество событий энкодера до срабатывания тригера. 
Например, если шаг 1, то при каждом событии энкодера будет срабатывать тригер. 
В случае, если шаг 2, то тригер будет срабатывать при каждом втором событии энкодера.
Полезно для компенсации дребезга энкодера.
- `hold_ms` - таймаут удержания кнопки, если кнопка удерживается дольше этого времени, то будет срабатывать событие `HELD`.
- `step_ms` - таймаут между множественными кликами, если события клика происходят быстрее этого времени, то будет срабатывать событие `MULTIPLE_CLICK`.
- `fast_ms` - таймаут между событиями энкодера для быстрого пролистывания `TURN_LEFT_FAST | TURN_RIGHT_FAST`.
- `click_ms` - таймаут между нажатием и отпусканием кнопки для события `CLICK`.

### События
События энкодера/кнопки передаются в коллбэки, которые можно зарегистрировать с помощью метода `on()`.


| Событие              | Параметры передаваемые в callback | Условие срабатывания                                       |
|----------------------|-----------------------------------|------------------------------------------------------------|
| ANY                  | event_id: int, clicks: int        | Дублирует любое событие                                    |
| CLICK                | None                              | Кнопка была нажата и отпущена за `click_ms`                |
| MULTIPLE_CLICK       | clicks: int                       | Кнопка была нажата, отпущена и снова нажата за `step_ms`   |
| HELD                 | None                              | Кнопка удерживается дольше `hold_ms`                       |
| RELEASE              | None                              | Кнопка была отпущена после `HELD`                          |
| TURN_LEFT            | None                              | Энкодер был повёрнут влево                                 |
| TURN_LEFT_FAST       | None                              | Энкодер был повёрнут быстрее `fast_ms`                     |
| TURN_LEFT_HOLD       | None                              | Энкодер был повёрнут влево и с нажатой кнопкой             |
| TURN_LEFT_FAST_HOLD  | None                              | Энкодер был повёрнут быстрее `fast_ms` и с нажатой кнопкой |
| TURN_RIGHT           | None                              | Энкодер был повёрнут вправо                                |
| TURN_RIGHT_FAST      | None                              | Энкодер был повёрнут быстрее `fast_ms`                     |
| TURN_RIGHT_HOLD      | None                              | Энкодер был повёрнут вправо и с нажатой кнопкой            |
| TURN_RIGHT_FAST_HOLD | None                              | Энкодер был повёрнут быстрее `fast_ms` и с нажатой кнопкой |

### Регистрация коллбэков
Для регистрации коллбэков нужно использовать метод `on(event, callback)`, которая принимает два парамера. 
 - `event` - событие, свойство класса `RotaryEncoderEvent`.
 - `callback` - функция, которая будет вызвана при срабатывании события.
Количество аргументов функции коллбэка зависит от события. Смотрите таблицу выше.

```python

# ----
# Код инициализации энкодера выше ^
# ----

# подписываемся на события энкодера
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

### Отписка от событий
Для отписки от событий нужно использовать метод `off(event, callback)`, который принимает два парамера. 
 - `event` - событие, свойство класса `RotaryEncoderEvent`.
 - `callback` - ссылка на функцию, которая была зарегистрирована ранее.
За один вызов метода, происходит отписка только одного коллбека от одного события.

```python
# ----
# Код регистрации коллбэков выше ^
# ----

# отписываемся от события энкодера
encoder.off(RotaryEncoderEvent.CLICK, on_click)

# пример с множественной подпиской
encoder.on(RotaryEncoderEvent.CLICK, on_click) # subscribe one
encoder.on(RotaryEncoderEvent.CLICK, on_click) # subscribe two

encoder.off(RotaryEncoderEvent.CLICK, on_click) # unsubscribe one
```

### Отписка от всех событий
Для отписки от всех событий нужно использовать метод `off_all()`, который принимает два парамера. 
  - `event` - событие, свойство класса `RotaryEncoderEvent`.
  - `callback` - ссылка на функцию, которая была зарегистрирована ранее, если она не передана, то будут отписаны все слушатели данного события.

```python
# ----
# Код инициализации энкодера выше ^
# ----
def on_click():
    print("CLICK")

def on_click2():
    print("CLICK2")


encoder.on(RotaryEncoderEvent.CLICK, on_click) # subscribe one, with callback on_click
encoder.on(RotaryEncoderEvent.CLICK, on_click2) # subscribe two, with callback on_click2
encoder.on(RotaryEncoderEvent.CLICK, on_click) # subscribe three, with callback on_click

# отписываем от события RotaryEncoderEvent.CLICK только слушателей с коллбэк функцией on_click
encoder.off_all(RotaryEncoderEvent.CLICK, on_click) # unsubscribe all `on_click` listeners from event RotaryEncoderEvent.CLICK

# отписываем от события RotaryEncoderEvent.CLICK всех слушателей
encoder.off_all(RotaryEncoderEvent.CLICK) # unsubscribe all listeners from event RotaryEncoderEvent.CLICK
```

## Примеры
Примеры использования энкодера можно найти в папке [examples](https://github.com/TTitanUA/micropython_rotary_encoder/tree/main/examples).

<a id="feedback"></a>
## Баги и обратная связь
При нахождении багов создавайте [issue](https://github.com/TTitanUA/micropython_rotary_encoder/issues)
Библиотека открыта для доработки и ваших [pull запросов](https://github.com/TTitanUA/micropython_rotary_encoder/pulls)!


