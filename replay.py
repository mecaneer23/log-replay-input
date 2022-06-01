import json
import time
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import threading

with open("config.json") as config:
    config = json.load(config)


class MyMouseController:

    def __init__(self, instructions=[], mouse=MouseController, pressed=False):
        self.instructions = instructions
        self.mouse = mouse()
        self.pressed = pressed

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def run(self):
        for i, v in enumerate(self.instructions):
            self.mouse.position = (v["x"], v["y"])
            try:
                if v["pressed"]:
                    self.mouse.press(eval(f"mouse.{v['button']}"))
                    self.pressed = True
                if (self.pressed and
                    not v["pressed"] and
                    v["button"] is not None):
                    self.mouse.release(eval(f"mouse.{v['button']}"))
                    self.pressed = False
            except NameError as e:
                print(v, e)
                exit(1)
            time.sleep(v["time"])


class MyKeyboardController:

    def __init__(self,
                instructions=[],
                keyboard=KeyboardController,
                pressed=False,
                special=False):
        self.instructions = instructions
        self.keyboard = keyboard()
        self.pressed = pressed
        self.special = special

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def run(self):
        for i in self.instructions:
            if i["pressed"]:
                if i["special"]:
                    self.keyboard.press(eval(f"keyboard.{i['key']}"))
                else:
                    self.keyboard.press(i["key"])
                    print(i["key"])
                self.pressed = True
            if self.pressed and not i["pressed"]:
                if i["special"]:
                    self.keyboard.release(eval(f"keyboard.{i['key']}"))
                else:
                    self.keyboard.release(i["key"])
                self.pressed = False

            time.sleep(i["time"])


def replay(file):
    with open(file) as input_file:
        instructions = json.load(input_file)

    mouse = MyMouseController()
    keyboard = MyKeyboardController()

    for instruction in instructions["mouse"]:
        mouse.add_instruction(instruction)

    for instruction in instructions["keyboard"]:
        keyboard.add_instruction(instruction)

    threading.Thread(target=mouse.run).start()
    threading.Thread(target=keyboard.run).start()


replay(input("filename: ") or config["storage_file"])

# when done with entire project, add gamepad support using vgamepad
