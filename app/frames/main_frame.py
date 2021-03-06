import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json


from app.utils import WindowConfig, Configs
from app.utils.setup_config import setup_configure
from app.frames.running_window import RunningWindow


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
        self.options = WindowConfig.OPTIONS
        self.champion = tk.StringVar()

        # create widgets
        self.combobox = ttk.Combobox(self, textvariable=self.champion, value=self.options, width=38)
        self.combobox.pack(pady=12)

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
        result = setup_configure()
        if result:
            messagebox.showinfo('Success!', 'Configured successfully. Now do not change position of your LoL client.')
        else:
            messagebox.showerror('Error!', 'Could not configure. Try again.')

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
