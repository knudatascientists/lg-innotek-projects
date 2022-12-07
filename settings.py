import datetime

# default folder path
FOLDER_PATH = "./image/module/overkill/"
UP_FOLER_PATH = "./image/module/"

# sampe folder path
test_ok_path = "./image/module/true_ok/GSY827AN7A4002_AAO03151K_PKT04_CM1EQSUA0011_20220712220034_DirectLight_OK.jpg"

# sample NG images
test_np_path1 = "./image/module/true_ng/GSY827AN7B0918_AAO05408K_PKT07_CM1EQSUA0012_20220712000659_DirectLight_NG.jpg"
test_np_path2 = "./image/module/true_ng/GSY827AN7C4411_AAO31565K_PKT08_CM1EQSUA0011_20220713080822_DirectLight_NG.jpg"
test_np_path3 = "./image/module/true_ng/GSY827AN7B0519_AAO12705K_PKT08_CM1EQSUA0011_20220711213213_DirectLight_NG.jpg"

# test requierments
TEMPLATE_PATH = "./image/template/"
DEBUG_PATH = "./"
SAVE_FOLDER_PATH = "./"

# test 3 requierments
T3_THRESHOLD = 0.01

# debug image text
GUI_IMG_SIZE = 600
TEXT_LOC = (100, 100)
DEBUG_THICKNESS = 7
DEBUG_TEXT_SIZE = 3

# GUI shape
LOGO_IMG_SIZE = 800
WIDTH = 400
HEIGHT = 600
MENU_WIDTH = WIDTH // 4
MENU_HEIGHT = HEIGHT // 30


# GUI colors
FRAME_COLOR = "#f2f2f2"
MENU_COLOR = "#beb7b1"
ITEM_COLOR = "#dfd8c7"
LEBEL_COLOR = "#fff"

# TEXT
FONT = "Consolas"
FONT_SIZE = 8

# CNN setting
IMG_SIZE = (600, 400)
IMG_SHAPE = IMG_SIZE[::-1]
IMG_PATH = "../image/train/train_pre"

BASE_WEIGHT = "./weight/base_weight/base_weight"
TOP_WEIGHT = "./weight/top_weight/top_weight"

sub_dir_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

BASE_LOGS = "./logs/base_logs/" + sub_dir_name
TOP_LOGS = "./logs/top_logs/" + sub_dir_name


# pyinstaller setting
def resource_path(relative_path):
    import os
    import sys

    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
