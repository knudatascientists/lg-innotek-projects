import datetime

# default folder path
FOLDER_PATH = "./image/module/true_ok/"
UP_FOLER_PATH = "./image/module/"

# sampe folder path
test_ok_path = "./image/module/true_ok/GSY827AN7A4002_AAO03151K_PKT04_CM1EQSUA0011_20220712220034_DirectLight_OK.jpg"

# sample NG images
test_np_path1 = "./image/module/true_ng/GSY827AN7B0918_AAO05408K_PKT07_CM1EQSUA0012_20220712000659_DirectLight_NG.jpg"
test_np_path2 = "./image/module/true_ng/GSY827AN7C4411_AAO31565K_PKT08_CM1EQSUA0011_20220713080822_DirectLight_NG.jpg"
test_np_path3 = "./image/module/true_ng/GSY827AN7B0519_AAO12705K_PKT08_CM1EQSUA0011_20220711213213_DirectLight_NG.jpg"

# test requierments
TEMPLATE_PATH = "./image/template/"
DEBUG_PATH = "./image/debug_images/"

# test 3 requierments
T3_THRESHOLD = 0.01

# GUI shape
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
FC_WEIGHT = "./weight/fc_weight/fc_weight"

sub_dir_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

BASE_LOGS = "./logs/base_logs/" + sub_dir_name
TOP_LOGS = "./logs/top_logs/" + sub_dir_name
FC_LOGS = "./logs/fc_logs/" + sub_dir_name
