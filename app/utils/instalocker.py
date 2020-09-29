import pyautogui
import time
from typing import List, Optional
from pyscreeze import Box


from app.utils import Configs


class Instalocker:
    """
    Class used to perform all steps to insta-lock chosen champion and print message on chat

    Attributes:
    -------------
    __json : dict
        json with configs about personal positions for user

    Methods:
    -------------
    lock(champion)
        picks specific champion

    print_on_chat(msg)
        print message on chat in lobby

    __print_msg(msg, location, with_enter)
        print msg in location (optionally with pressing enter)

    __locate_img(img, location, patience)
        wait for img to be found in location

    __pick_champion(img, location, patience)
        wait for img to be found in location and pick champion
    """

    def __init__(self, json):
        self.__json = json

    def lock(self, champion: str) -> None:
        """
        Perform locking of champion with following steps:
        1. Print champion name in entry
        2. Wait for image be able to lock
        3. Pick champion
        :param champion: name of champion
        :return: None
        """
        champion_img_path = Configs.BASE_PATH + fr'\img\champions\{champion.capitalize()}.png'
        self.__print_msg(champion, self.__json['CHAMP_ENTRY_LOC'])
        self.__pick_champion(champion_img_path, self.__json['CHAMP_IMG_LOC'], Configs.IMG_FIND_PATIENCE)

    def print_on_chat(self, msg: str) -> None:
        """
        Print message on chat
        :param msg: message to print
        :return:
        """
        self.__print_msg(msg, self.__json['CHAT_LOC'], with_enter=True)
        print('Printed: ', msg)

    def __print_msg(self, msg: str, location: List[int], with_enter: bool = False) -> None:
        """
        Print message using pyautogui
        :param msg: message to print :type str
        :param location: location of message :type List[int, int]
        :param with_enter: if press enter at the end of writing :type bool
        :return:
        """
        pyautogui.click(location)
        print(location)
        pyautogui.write(msg)
        if with_enter:
            pyautogui.press('enter')

    def __locate_img(self, img: str, location: List[int], patience: int) -> Optional[Box]:
        """
        Wait for image to appear in specific location, maximum time of waiting is specified by patience

        If time of locating is higher than patience, Exception is raised

        :param img: path to image
        :param location: location of image region with margin of error
        :param patience: maximum time of waiting
        :return: location of image
        """
        c = time.time()
        # adjust region
        location = (location[0] - 10, location[1] - 10, location[2] + 20, location[3] + 20)
        while True:
            box = pyautogui.locateOnScreen(img, region=location, confidence=Configs.CONFIDENCE)
            if box:
                return box
            elif time.time() - c >= patience:
                raise RuntimeError

    def __pick_champion(self, img: str, location: List[int], patience: int) -> None:
        """
        Wait for image to appear and pick champion (click on specific place)
        :param img: path to image
        :param location: location of image region with margin of error
        :param patience: maximum time of waiting
        :return:
        """
        location = self.__locate_img(img, location, patience)
        pyautogui.click(location)
