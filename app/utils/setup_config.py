import pyautogui
import os
import json
import copy
import time


from app.utils import Configs


path = os.path.abspath(os.curdir)
images = [
    r'\champ.bmp',
    r'\chat.bmp',
    r'\entry.bmp',
    r'\pixel_rec.bmp'
]
paths = [path + r'\img\configs' + img for img in images]


def locate(path_: str, text: str, patience: int):
    """
    Locate image on screen

    :param patience: time in seconds to wait for result of location
    :param path_: path to img
    :param text: text to print
    :return:
    """
    print(f'Locating: {text}')
    c = time.time()
    while True:
        box = pyautogui.locateOnScreen(path_)
        if box:
            print(box)
            print('Located!')
            return list(box)
        if time.time() - c >= patience:
            raise RuntimeWarning(f'Run out of time for locating {text}')


def process_img_position(box):
    """
    Process location of expected champion location adding margin of error

    :param box: box for location
    :return: processed box
    """
    for i in range(2):
        box[i] -= 10
    for i in range(2, 4):
        box[i] += 15
    return box


def locate_pixel(path_: str, text: str, patience: int):
    """
    Locate image on screen and return color to track and expected position

    :param patience: time in seconds to wait for result of location
    :param path_: path to image
    :param text: text to print
    :return: position and color of pixel
    """
    print(f'Locating: {text}')
    c = time.time()
    while True:
        box = pyautogui.locateOnScreen(path_, confidence=Configs.CONFIDENCE)
        if box:
            print(box)
            break
        if time.time() - c >= patience:
            raise RuntimeWarning(f'Run out of time for locating {text}')

    position = pyautogui.center(box)
    color = pyautogui.pixel(*position)
    print('Located!')
    return [list(position), color]


def setup_configure() -> bool:
    """
    Setup configs locating positions used by bot:
    -champion entry position
    -expected champion position
    -chat position
    -pixel to track while waiting for match
    Then saves it in config.json

    :return: if configuration was successful
    """
    # locate elements
    try:
        champion_box = locate(paths[0], 'champ', Configs.CONF_CHAMP_PATIENCE)
        chat_box = locate(paths[1], 'chat', Configs.CONF_CHAT_PATIENCE)
        entry_box = locate(paths[2], 'entry', Configs.CONF_ENTRY_PATIENCE)
        pixel_loc, pixel_color = locate_pixel(paths[3], 'pixel', Configs.CONF_PIXEL_PATIENCE)
    except RuntimeWarning as exception:
        print(exception)
        return False

    # preprocess elements
    champion_box = process_img_position(champion_box)
    entry_full_box = copy.deepcopy(entry_box)
    chat_box = chat_box[:2]
    entry_box = entry_box[:2]

    # open json and write it
    json_path = path + r'\config.json'
    with open(json_path, 'r') as json_file:
        json_ = json.load(json_file)

    json_['CHAMP_IMG_LOC'] = champion_box
    json_['CHAT_LOC'] = chat_box
    json_['CHAMP_ENTRY_LOC'] = entry_box
    json_['PIXEL_LOC'] = pixel_loc
    json_['PIXEL_COLOR'] = pixel_color

    # save new configs
    with open(json_path, 'w') as json_file:
        json.dump(json_, json_file)

    return True
