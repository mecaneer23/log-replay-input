from pynput import mouse, keyboard
import json
import time

with open("config.json") as config:
    config = json.load(config)
output = {"keyboard": [], "mouse": [], "keyboard_times": [], "mouse_times": []}


def add_mousepress(location, pressed=False, scroll_direction=0, button=None):
    global output
    output["mouse"].append(
        {
            "x": location[0],
            "y": location[1],
            "pressed": pressed,
            "button": button,
            "scroll_direction": scroll_direction,
            "time": 0,
        }
    )
    output["mouse_times"].append(time.time())


def on_move_mouse(x, y):
    add_mousepress((x, y))


def on_click_mouse(x, y, button, pressed):
    add_mousepress((x, y), pressed, button=str(button))


def on_scroll_mouse(x, y, dx, dy):
    add_mousepress((x, y), scroll_direction=dy)


def add_keypress(key, pressed, special):
    global output
    output["keyboard"].append(
        {
            "key": key,
            "pressed": pressed,
            "special": special,
            "time": None
        }
    )
    output["keyboard_times"].append(time.time())


def on_press_key(key):
    try:
        add_keypress(key.char, True, False)
    except AttributeError:
        add_keypress(str(key), True, True)


def on_release_key(key):
    try:
        add_keypress(key.char, False, False)
    except AttributeError:
        add_keypress(str(key), False, True)


def start_logging():
    output["keyboard_times"].append(time.time())
    output["mouse_times"].append(time.time())
    mouse.Listener(
        on_move=on_move_mouse, on_click=on_click_mouse, on_scroll=on_scroll_mouse
    ).start()
    keyboard.Listener(on_press=on_press_key, on_release=on_release_key).start()
    finish_logging(input("output file: ") or config["storage_file"])

def finish_logging(file):
    for i, _ in enumerate(output["keyboard"]):
        output["keyboard"][i]["time"] = abs(output["keyboard_times"][i] - output["keyboard_times"][i-1])
    for i, _ in enumerate(output["mouse"]):
        output["mouse"][i]["time"] = abs(output["mouse_times"][i] - output["mouse_times"][i - 1])
    output.pop("keyboard_times")
    output.pop("mouse_times")
    with open(file, "w") as output_file:
        json.dump(output, output_file)

# input("Press enter to start logging")
# time.sleep(3)
start_logging()
