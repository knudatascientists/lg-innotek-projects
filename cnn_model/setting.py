import datetime

# setting
IMG_PATH = "../image/module"
IMG_SIZE = (400, 600)
BASE_WEIGHT = "./weight/base_weight/base_weight"
TOP_WEIGHT = "./weight/top_weight/top_weight"
FC_WEIGHT = "./weight/fc_weight/fc_weight"

sub_dir_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

BASE_LOGS = "./logs/base_logs/" + sub_dir_name
TOP_LOGS = "./logs/top_logs/" + sub_dir_name
FC_LOGS = "./logs/fc_logs/" + sub_dir_name
