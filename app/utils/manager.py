from pynput.keyboard import Listener
import json
import pyautogui
import time
from pynput.keyboard import Key


from app.utils import Configs
from app.utils import Instalocker


class Manager:
    """
    Class to control one process of insta-locking

    Attributes:
    -------------
    __locker : Instalocker
        locker to pick champion

    __champion : str
        name of champion to pick

    __msg : str
        message to print

    Methods:
    -------------
    listen()
        wait for keyboard using pynput.keyboard.Listener

    __on_press(key)
        function to execute while listening

    wait()
        wait for game start using pixelMatch
    """

    def __init__(self):
        """
        """
        self.__locker = Instalocker()

    def listen(self, champion: str, msg: str) -> None:
        """
        Wait for key to click using pynput.keyboard.Listener

        :param champion: name of champion
        :param msg: message to print
        :return:
        """
        print('Ready to pick')
        print(f'Champion: {champion}')
        print(f'Msg: {msg}')
        print("Press 'space' to insta-lock!")
        with Listener(on_press=lambda key: self.__on_press(key, champion, msg)) as listener:
            listener.join()

    def __on_press(self, key: Key, champion: str, msg: str):
        """
        If user click START_KEY starts locking
        If user click EXIT_KEY exit lobby process

        Keys settings are available to customize in configs.py

        :param champion: name of champion
        :param msg: message to print
        :param key: key from keyboard to use
        :return:
        """
        if key == Configs.START_KEY:
            self.__locker.lock(champion)
            self.__locker.print_on_chat(msg)
            print('Success!')
            return False
        elif key == Configs.EXIT_KEY:
            return False

    def wait(self, champion: str, msg: str):
        """
        Waits for match starts and perform picking and printing on chat

        TODO
        -auto accepting
        -canceling waiting

        :param champion: name of champion to pick
        :param msg: message to print on chat
        :return:
        """
        json_path = Configs.BASE_PATH + r'\config.json'
        with open(json_path, 'r') as json_file:
            json_ = json.load(json_file)
        print('Waiting for match...')
        self.__locate_pixel(json_['PIXEL_COLOR'], json_['PIXEL_LOC'])
        print('Match found!')
        start = time.time()
        self.__locker.lock(champion)
        self.__locker.print_on_chat(msg)
        stop = time.time()
        print(f'Executed in {round(stop - start, 4)} seconds')

    def __locate_pixel(self, color, position) -> None:
        """
        Locate pixel that informs that match is started
        :param color: pixel color
        :param position: expected position on screen
        :return:
        """
        while True:
            box = pyautogui.pixelMatchesColor(*position, expectedRGBColor=color)
            if box:
                return
