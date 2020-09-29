import pyautogui
import os
import numpy as np
import json


path = os.path.abspath(os.curdir)


def preprocess_pixel(position, screen):
    screen = np.array(screen, dtype=np.ndarray)
    position = center_box(position)
    rgb_color = screen[position[1], position[0], :]
    return position, (int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))


def save_image(position, screen):
    screen = screen.crop((position[0], position[1], position[0] + position[2], position[1] + position[3]))
    print(screen)
    screen.save(path + r'\img\config\match.png')
    return position


def process_img_position(box):
    """
    Process location of expected champion location adding margin of error

    :param box: box for location
    :return: processed box
    """
    #box[0] -= 8
    #box[1] += 10
    #box[2] -= 8
    #box[3] += 10
    return box


def center_box(box):
    return [box[0] + int(box[2] / 2), box[1] + int(box[3] / 2)]


def setup_configure(elements, screen) -> bool:
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
    champion_box = elements[0]
    entry_box = elements[1]
    chat_box = elements[2]
    #pixel_loc, pixel_color = preprocess_pixel(elements[3], screen)
    accept_loc = save_image(elements[3], screen)

    # preprocess elements
    champion_box = process_img_position(champion_box)
    chat_box = [int(i) for i in list(pyautogui.center(chat_box))]
    entry_box = center_box(entry_box)

    # open json and write it
    json_path = path + r'\config.json'
    with open(json_path, 'r') as json_file:
        json_ = json.load(json_file)
    if not json_:
        return False

    json_['CHAMP_IMG_LOC'] = champion_box
    json_['CHAT_LOC'] = chat_box
    json_['CHAMP_ENTRY_LOC'] = entry_box
    json_['PIXEL_LOC'] = accept_loc
    #json_['PIXEL_COLOR'] = pixel_color

    # save new configs
    with open(json_path, 'w') as json_file:
        json.dump(json_, json_file)

    return True
