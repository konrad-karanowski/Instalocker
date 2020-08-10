import json
import pyautogui
import time


from app.utils import Configs
from app.utils import Instalocker


class Manager:
    """
    Class to control one process of insta-locking

    Attributes:
    -------------
    __locker : Instalocker
        locker to pick champion

    __json : dict
        json with configurations

    __is_running : bool
        is waiting for match running

    Methods:
    -------------
    """

    def __init__(self, messanger):
        self.__messanger = messanger

        json_path = Configs.BASE_PATH + r'\config.json'
        with open(json_path, 'r') as json_file:
            self.__json = json.load(json_file)

        self.__locker = Instalocker(self.__json)
        self.__is_running = False

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
        self.__is_running = True
        print('Waiting for match...')
        self.__messanger.print_message('Waiting for match...')
        lock = self.__wait_for_match()
        if lock:
            self.__pick_champion(champion, msg)
            self.__messanger.switch_button_text()
        else:
            print('Abandoned looking for match')
            return

    def __wait_for_match(self) -> bool:
        """
        Perform all actions before joining to lobby

        TODO
        -auto-accept

        :return: was program cancelled
        """
        self.__locate_pixel(self.__json['PIXEL_COLOR'], self.__json['PIXEL_LOC'])
        return self.__is_running

    def __locate_pixel(self, color, position) -> None:
        """
        Locate pixel that informs that match is started
        :param color: pixel color
        :param position: expected position on screen
        :return:
        """
        while True and self.__is_running:
            box = pyautogui.pixelMatchesColor(*position, expectedRGBColor=color)
            if box:
                return

    def __pick_champion(self, champion, msg) -> None:
        """
        Pick champion using Instalocker class

        :param champion: name of champion
        :param msg: message to print
        :return:
        """
        self.__messanger.print_message('Match found!')
        start = time.time()
        self.__locker.lock(champion)
        self.__locker.print_on_chat(msg)
        stop = time.time()
        self.__messanger.print_message(f'Executed in {round(stop - start, 4)} seconds')

    def stop_running(self) -> None:
        """
        Stops running of the manager, can be used only to cancel waiting for locking!

        :return:
        """
        self.__is_running = False
