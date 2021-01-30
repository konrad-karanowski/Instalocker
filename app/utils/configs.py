import os


class Configs:

    # path
    BASE_PATH = os.path.abspath(os.curdir)

    # base configs
    CLICK_DURATION = 0.001
    IMG_FIND_PATIENCE = 5

    # config patience
    CONF_CHAMP_PATIENCE = 10
    CONF_ENTRY_PATIENCE = 10
    CONF_CHAT_PATIENCE = 10
    CONF_PIXEL_PATIENCE = 10

    # confidence of image
    CONFIDENCE = 0.95
