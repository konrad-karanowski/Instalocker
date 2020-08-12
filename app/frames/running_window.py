import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime


from app.utils import Manager


class RunningWindow(tk.Tk):
    """
    Window handling effects while waiting for match and locking phase
    """

    def __init__(self, champion, msg, json_, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title("")
        self.geometry('500x220')
        self.resizable(False, False)
        self.lift()

        container = tk.Frame(self)
        container.pack(expand=True)

        self.frame = RunningWindowFrame(container, self, champion, msg, json_)
        self.frame.pack(expand=True)

    def destroy(self):
        self.frame.kill_thread()
        super().destroy()


class RunningWindowFrame(tk.Frame):
    """
    Main frame of locking phase

    Widgets:
    -------------
    yscrollbar : tk.Scrollbar
        scrollbar for scrolling logs

    text : tk.Text
        text entry to inform about progress

    abandon : ttk.Button
        button for abandon and exit waiting progress

    Attributes:
    -------------
    __manager : Manager
        manager to control locking

    __lock_thread : Thread
        main thread of locking

    Methods:
    -------------
    __abandon
        abandon match

    __start_locking
        start locking phase

    kill_thread :
        kill locking thread

    print_message :
        print message in text entry

    switch_button_text :
        switches button text from 'abandon' to 'done'

    """

    def __init__(self, container, controller, champion, msg, json_, **kwargs):
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

        self.__manager = Manager(self, json_)
        self.__lock_thread = threading.Thread(target=self.__start_locking, args=[champion, msg])
        self.__lock_thread.start()

    def __abandon(self):
        """
        Abandon match
        :return:
        """
        self.controller.destroy()

    def __start_locking(self, champion: str, msg: str):
        """
        Begin locking using manager class

        :param champion: name of champion
        :param msg: message to print in lobby
        :return:
        """
        self.__manager.wait(champion, msg)

    def kill_thread(self):
        """
        Kills locking thread

        :return:
        """
        self.__manager.stop_running()

    def print_message(self, msg: str):
        """
        Print message in frame in proper format

        :param msg: message to print
        :return:
        """
        time = datetime.now()
        message = f'[{time.hour}:{time.minute}]{msg}\n'
        self.text.insert(tk.END, message)

    def switch_button_text(self):
        """
        Switch text on button from 'abandon' to 'done

        :return:
        """
        self.abandon['text'] = 'Done!'
