import pyautogui
import os
import json
import copy


path = os.path.abspath(os.curdir)
images = [
    r'\champ.bmp',
    r'\chat.bmp',
    r'\entry.bmp',
    r'\pixel_rec.bmp'
]
paths = [path + r'\img\configs' + img for img in images]


def locate(path_, text):
    """
    Locate image on screen

    :param path_: path to img
    :param text: text to print
    :return:
    """
    print(f'Locating: {text}')
    while True:
        box = pyautogui.locateOnScreen(path_)
        if box:
            print(box)
            print('Located!')
            return list(box)


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


def locate_pixel(path_, text):
    """
    Locate image on screen and return color to track and expected position

    :param path_: path to image
    :param text: text to print
    :return: position and color of pixel
    """
    print(f'Locating: {text}')
    while True:
        box = pyautogui.locateOnScreen(path_)
        if box:
            print(box)
            break
    position = pyautogui.center(box)
    color = pyautogui.pixel(*position)
    print('Located!')
    return [list(position), color]


def setup_configure():
    """
    Setup configs locating positions used by bot:
    -champion entry position
    -expected champion position
    -chat position
    -pixel to track while waiting for match
    Then saves it in config.json

    :return:
    """
    # locate elements
    champion_box = locate(paths[0], 'champ')
    chat_box = locate(paths[1], 'chat')
    entry_box = locate(paths[2], 'entry')
    pixel_loc, pixel_color = locate_pixel(paths[3], 'pixel')

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
