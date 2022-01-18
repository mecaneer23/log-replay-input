import json
import time
from pynput import keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener, KeyCode, Key, Controller as KeyboardController
import threading

with open("config.json") as config:
    config = json.load(config)

class MyMouseController(threading.Thread):
    def __init__(self, instructions=[], mouse=MouseController, pressed=False):
        super(MyMouseController, self).__init__()
        self.instructions = instructions
        self.mouse = mouse()
        self.pressed = pressed

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def run(self):
        for i in self.instructions:
            self.mouse.position = (i["x"], i["y"])
            if i["pressed"] == True:
                self.mouse.press(eval(i["button"]))
                self.pressed = True
            if self.pressed == True and i["pressed"] == False and i["button"] is not None:
                self.mouse.release(eval(i["button"]))
                self.pressed = False

            time.sleep(i["time"])


class MyKeyboardController(threading.Thread):
    def __init__(self, instructions=[], keyboard=KeyboardController, pressed=False, special=False):
        super(MyKeyboardController, self).__init__()
        self.instructions = instructions
        self.keyboard = keyboard()
        self.pressed = pressed
        self.special = special

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def run(self):
        for i in self.instructions:
            if i["pressed"] == True:
                if i["special"] == True:
                    self.keyboard.press(eval(i["key"]))
                else:
                    self.keyboard.press(i["key"])
                self.pressed = True
            if self.pressed == True and i["pressed"] == False:
                if i["special"] == True:
                    self.keyboard.release(eval(i["key"]))
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

    mouse.run()
    keyboard.run()


replay(input("filename: ") or config["storage_file"])


# when done with entire project, add gamepad support using vgamepad
