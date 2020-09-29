import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import pyautogui
import os
import json


PATH = os.path.abspath(os.curdir)


class UpdateWindow(tk.Tk):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title("")
        self.geometry(f'400x320')
        self.resizable(False, False)
        self.lift()

        container = tk.Frame(self)
        container.pack(expand=True)

        self.frame = UpdateFrame(container, self)
        self.frame.pack(expand=True)


class UpdateFrame(tk.Frame):

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)
        self.controller = controller

        # create list of champions
        json_ = self.open_json()

        # get parameters
        self.entry_loc = json_['CHAMP_ENTRY_LOC']
        self.champ_loc = json_['CHAMP_IMG_LOC']

        # create widgets
        self.label = ttk.Label(self, text="""
    Print champions names (separated by ','), 
    enter practise tool and click 'Update' when ready."""
                               )
        self.label.pack()

        self.text = tk.Text(self, height=10, width=35)
        self.text.pack()

        self.button = ttk.Button(self, text='Update')
        self.button['command'] = self.configure_champion
        self.button.pack()

    def configure_champion(self):
        to_update = self.parse_text()
        updated = list()
        c = time.time()
        for i, champion in enumerate(to_update):
            self.configure_one(champion)
            updated.append(updated)
            z = time.time()
            if c - z >= 80:
                break
        self.save_json(updated)
        self.controller.parent.setup_options()
        messagebox.showinfo('Success!', f'Updated {i + 1} champions')
        self.controller.destroy()

    def open_json(self):
        json_path = PATH + r'\config.json'
        with open(json_path, 'r') as json_file:
            json_ = json.load(json_file)
        return json_

    def save_json(self, champions):
        json_path = PATH + r'\config.json'
        with open(json_path, 'r') as json_file:
            json_ = json.load(json_file)
        json_['CHAMPIONS'] = champions

    def configure_one(self, champion):
        self.print_champion_name(champion)
        self.take_screen(champion)
        self.clear_champion()

    def print_champion_name(self, champion):
        pyautogui.click(self.entry_loc)
        pyautogui.write(champion)

    def clear_champion(self):
        pyautogui.click(self.entry_loc)
        pyautogui.click(self.entry_loc)
        pyautogui.press('backspace')

    def take_screen(self, champion):
        time.sleep(1)
        img = pyautogui.screenshot(region=self.champ_loc)
        img.save(fr'{PATH}\img\champions\{champion}.png')

    def parse_text(self):
        text = self.text.get(0.0, tk.END)
        split = text.split(',')
        return [element.strip('\n').replace(' ', '') for element in split]
