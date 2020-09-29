import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import glob


from app.utils import Configs
from app.frames.running_window import RunningWindow
from app.frames.config_window import ConfigWindow
from app.frames.update_window import UpdateWindow


PATH = os.path.abspath(os.curdir)


class MainFrame(tk.Frame):
    """
    Main frame of application

    Widgets:
    -------------
    combobox : ttk.Combobox
        combobox to choose champion

    text : tk.Text
        text entry to print message to print on chat in lobby

    start : ttk.Button
        button to start picking

    configs : ttk.Button
        button to configure program

    Attributes:
    -------------
    controller : Application extends tk.Tk
        main controller of application

    options : list[str]
        list of available champions in application

    champion : tk.StringVar
        name of champion to pick

    Methods:
    -------------
    start_()
        check if values are correct and start waiting, else raise messagebox.showerror

    configure_()
        configure positions using setup_config function

    lock_champion(champion, msg)
        activate waiting function in manager
    """

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)
        self.controller = controller

        # create variables
        self.champion = tk.StringVar()

        # create widgets
        self.label_champion = ttk.Label(self, text='Choose your champion: ')
        self.label_champion.pack()
        self.combobox = ttk.Combobox(self, textvariable=self.champion, width=38)
        self.combobox.pack(pady=12)
        self.setup_options()

        self.msg_label = ttk.Label(self, text='Enter message to be written on chat: ')
        self.msg_label.pack()
        self.text = tk.Text(self, width=33, height=3)
        self.text.pack()

        buttons_container = tk.Frame(self)
        buttons_container.pack(expand=True, pady=8)

        self.start = ttk.Button(buttons_container, text='Start')
        self.start['command'] = self.start_
        self.start.grid(row=0, column=0, padx=10)

        self.configs = ttk.Button(buttons_container, text='Config')
        self.configs['command'] = self.configure_
        self.configs.grid(row=0, column=1, padx=10)

        self.hard_config = ttk.Button(buttons_container, text='Update')
        self.hard_config['command'] = self.champion_configure_
        self.hard_config.grid(row=0, column=2, padx=10)

    def start_(self) -> None:
        """
        Check if champion is chosen and start picking

        :return:
        """
        champion = self.champion.get()
        msg = self.text.get('1.0', tk.END)
        if champion:
            self.lock_champion(champion, msg)
        else:
            messagebox.showerror('Error!', 'You must choose champion')

    def configure_(self) -> None:
        """
        Perform configuration using setup_configure function

        :return:
        """
        messagebox.showinfo('Configuration', 'Enter practise tool and click "Ok", when ready!')
        window = ConfigWindow()
        window.mainloop()

    def champion_configure_(self):
        window = UpdateWindow(self)
        window.mainloop()

    def lock_champion(self, champion, msg) -> None:
        """
        Lock champion using manager class

        :param champion: champion name
        :param msg: message to print
        
        :return:
        """
        json_ = self.open_json()
        if self.validate_configs(json_):
            window = RunningWindow(champion, msg, json_)
            window.mainloop()
        else:
            messagebox.showerror('Error!', 'Seems you did not make configure yet.')

    def validate_configs(self, json_):
        if json_:
            for value in json_.values():
                if not value:
                    return False
            return True
        else:
            return False

    def open_json(self):
        json_path = Configs.BASE_PATH + r'\config.json'
        with open(json_path, 'r') as json_file:
            json_ = json.load(json_file)
        return json_

    def setup_options(self):
        champions = glob.glob(fr'{PATH}\img\champions\*.png')
        self.combobox['value'] = [os.path.basename(champion)[:-4] for champion in champions]
