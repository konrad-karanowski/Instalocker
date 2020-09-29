import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import pyautogui
import os
import json


from app.utils import WindowConfig


PATH = os.path.abspath(os.curdir)


class UpdateWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title("")
        self.geometry(f'250x150')
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
        updated = WindowConfig.OPTIONS
        self.to_update = [champion for champion in json_['CHAMPIONS'] if champion not in updated]
        print(self.to_update)

        # get parameters
        self.entry_loc = json_['CHAMP_ENTRY_LOC']
        self.champ_loc = json_['CHAMP_IMG_LOC']

        # create widgets
        self.label = ttk.Label(self, text="Enter practise tool and click 'Update' when ready.")
        self.label.pack()

        self.button = ttk.Button(self, text='Update champions list')
        self.button['command'] = self.configure_champion
        self.button.pack()

    def configure_champion(self):
        img = self.get_dummy()
        c = time.time()
        for i, champion in enumerate(self.to_update):
            print(champion)
            self.configure_one(champion, img)
            z = time.time()
            if c - z >= 80:
                break
        messagebox.showinfo('Success!', f'Updated {i + 1} champions')
        self.controller.destroy()

    def open_json(self):
        json_path = PATH + r'\config.json'
        with open(json_path, 'r') as json_file:
            json_ = json.load(json_file)
        return json_

    def configure_one(self, champion, dummy):
        self.print_champion_name(champion)
        self.take_screen(champion, dummy)
        num_bs = len(champion)
        self.clear_champion(num_bs)

    def print_champion_name(self, champion):
        pyautogui.click(self.entry_loc)
        pyautogui.write(champion)

    def clear_champion(self, num_backspaces):
        pyautogui.click(self.entry_loc)
        pyautogui.click(self.entry_loc)
        pyautogui.press('backspace')

    def take_screen(self, champion, dummy):
        time.sleep(1)
        img = pyautogui.screenshot(region=self.champ_loc)
        if img != dummy:
            img.save(fr'{PATH}\img\champions\{champion}.png')
            print('Saved!')

    def get_dummy(self):
        self.print_champion_name('xxxxx')
        img = pyautogui.screenshot(region=self.champ_loc)
        return img

