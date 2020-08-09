import tkinter as tk


from app.frames import MainFrame


frames = {
    'main': MainFrame
}


class Application(tk.Tk):
    """
    Main application created using tkinter module

        Attributes:
    -------------
    container : tk.Frame
        main container for windows

    frames : dict[str, tk.Frame]
        list of frames used in application

    Methods:
    -------------
    show_frame(key)
        show frame behind the key
    """

    def __init__(self, *args, **kwargs):
        """
        Basic configs of tkinter window
        """
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title("Instalocker")
        self.geometry('380x170')
        self.resizable(False, False)

        # main container
        self.container = tk.Frame(self)
        self.container.pack()

        self.frames = dict()
        for key, frame in frames.items():
            self.frames[key] = frame(self.container, controller=self)
            self.frames[key].grid(row=0, column=0, sticky='nsew')
        self.show_frame('main')

    def show_frame(self, key: str) -> None:
        """
        Raise frame specified by key

        :param key: key of frame in self.frames dict
        :return:
        """
        frame = self.frames[key]
        frame.tkraise()
