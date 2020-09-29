import tkinter as tk
from tkinter import messagebox
import pyautogui
from PIL import ImageTk
import time


from app.utils.setup_config import setup_configure


class ConfigWindow(tk.Tk):
    """
    Window handling effects while waiting for match and locking phase
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        time.sleep(1)
        screen = pyautogui.screenshot()
        self.title("")
        self.geometry(f'{screen.width}x{screen.height}+0+0')
        self.resizable(True, True)
        self.lift()

        container = tk.Frame(self)
        container.pack(expand=True)

        self.frame = ConfigFrame(container, self, screen)
        self.frame.pack(expand=True)

    def destroy(self):
        messagebox.showinfo('Success!', 'Configured successfully. Now do not change position of your LoL client.')
        super().destroy()


class ConfigFrame(tk.Frame):

    SWITCHER = [
        'champion',
        'champion entry',
        'chat entry',
        'runes'
    ]

    COLORS = [
        'red',
        'blue',
        'yellow',
        'green'
    ]

    def __init__(self, container, controller, screen, **kwargs):
        super().__init__(container, **kwargs)
        self.controller = controller
        self.screen = screen

        # configs
        self.configs = list()
        self.switcher_counter = 0

        # create canvas
        self.canvas = tk.Canvas(self, height=screen.height, width=screen.width)
        self.canvas.pack()
        self.canvas.image = ImageTk.PhotoImage(self.screen, master=self.canvas)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        self.canvas.bind('<Button-1>', self.draw_rectangle)
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None

        # reset click counter
        self.counter = 0

    def popup_info_window(self):
        messagebox.showinfo(f'Locate {self.SWITCHER[self.switcher_counter]}',
                            'Create box on screen using two clicks: top-left corner and bottom-right corner')

    def ask_cancel(self):
        answer = messagebox.askyesno('Are you sure?', f'Save location for {self.SWITCHER[self.switcher_counter]}')
        return answer

    def draw_rectangle(self, event):
        """
        Draw rectangle and end process
        :param event:
        :return:
        """
        if self.counter == 0:
            self.x1 = event.x
            self.y1 = event.y
            self.counter += 1
        else:
            self.x2 = event.x
            self.y2 = event.y
            prev = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                                width=0.5, fill=self.COLORS[self.switcher_counter])
            self.counter = 0
            if self.ask_cancel():
                self.add_element()
                if self.switcher_counter >= 4:
                    setup_configure(self.configs, self.screen)
                    self.controller.destroy()
            else:
                self.canvas.delete(prev)

    def add_element(self):
        """
        Add box to box list and increment switcher counter
        :return:
        """
        self.switcher_counter += 1
        box = [self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1]
        self.configs.append(box)
