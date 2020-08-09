from pynput.keyboard import Key
import os


class Configs:

    # path
    BASE_PATH = os.path.abspath(os.curdir)

    # key config
    START_KEY = Key.space
    EXIT_KEY = Key.esc

    # base configs
    CLICK_DURATION = 0.001
    IMG_FIND_PATIENCE = 5


class WindowConfig:

    OPTIONS = [
        'Ahri',
        'Yone'
    ]
