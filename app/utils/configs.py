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

    # config patience
    CONF_CHAMP_PATIENCE = 10
    CONF_ENTRY_PATIENCE = 10
    CONF_CHAT_PATIENCE = 10
    CONF_PIXEL_PATIENCE = 10


class WindowConfig:

    OPTIONS = [
        'Ahri',
        'Yone'
    ]
