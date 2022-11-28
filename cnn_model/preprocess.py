import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import img_preprocess
import settings

raw_ng_path = "../image/train/train_raw/true_ng"
raw_ok_path = "../image/train/train_raw/true_ok"

pre_ng_path = "../image/train/train_pre/true_ng"
pre_ok_path = "../image/train/train_pre/true_ok"


img_preprocess.cvt_train_img_path(raw_ng_path, pre_ng_path, settings.IMG_SIZE)
img_preprocess.cvt_train_img_path(raw_ok_path, pre_ok_path, settings.IMG_SIZE)
