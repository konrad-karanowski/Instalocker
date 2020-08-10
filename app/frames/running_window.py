import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime


from app.utils import Manager


class RunningWindow(tk.Tk):

    def __init__(self, champion, msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title("")
        self.geometry('500x220')

        container = tk.Frame(self)
        container.pack(expand=True)

        self.frame = RunningWindowFrame(container, self, champion, msg)
        self.frame.pack(expand=True)

    def destroy(self):
        self.frame.kill_thread()
        super().destroy()


class RunningWindowFrame(tk.Frame):

    def __init__(self, container, controller, champion, msg, **kwargs):
        super().__init__(container, **kwargs)
        self.controller = controller

        # widgets
        self.yscrollbar = tk.Scrollbar(self)
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text = tk.Text(self, wrap=tk.NONE, yscrollcommand=self.yscrollbar.set, height=8)
        self.text.pack(side=tk.TOP)

        self.yscrollbar.config(command=self.text.yview)

        self.abandon = ttk.Button(self, text='Abandon')
        self.abandon['command'] = self.__abandon
        self.abandon.pack(pady=10)

        self.__manager = Manager(self)
        self.__lock_thread = threading.Thread(target=self.__start_locking, args=[champion, msg])
        self.__lock_thread.start()

    def __abandon(self):
        self.controller.destroy()

    def __start_locking(self, champion, msg):
        self.__manager.wait(champion, msg)

    def kill_thread(self):
        self.__manager.stop_running()

    def print_message(self, msg):
        time = datetime.now()
        message = f'[{time.hour}:{time.minute}]{msg}\n'
        self.text.insert(tk.END, message)

    def switch_button_text(self):
        self.abandon['text'] = 'Done!'
