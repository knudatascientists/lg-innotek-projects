import os
import sys

import cv2
import ft_model
import matplotlib.pyplot as plt
import pandas as pd
import silence_tensorflow
import tensorflow as tf
import tqdm

sys.path.append("../")
import img_preprocess
import settings

# setting tensorflow
silence_tensorflow.silence_tensorflow()
tf.random.set_seed(42)


def model_iu(img, model, only_proba=True, threshold=0.5):
    img = img_preprocess.cnn_preprocess_img(img, settings.IMG_SIZE, predict=True)
    proba = float(model.predict(img)[0][0])

    if only_proba is False:
        if proba >= threshold:
            return proba, "OK"
        else:
            return proba, "NG"

    return proba


def predict_dir(dir_path, model):
    probas = []

    img_names = os.listdir(dir_path)

    for img_name in img_names:
        img_path = os.path.join(dir_path, img_name)
        img = cv2.imread(img_path)

        proba = model_iu(img, model)
        probas.append(proba)

        print(proba)

    return probas


def low_score(dir_path, model):
    low_score = []

    img_names = os.listdir(dir_path)

    for img_name in img_names:
        img_path = os.path.join(dir_path, img_name)
        img = cv2.imread(img_path)

        score = model_iu(img, model)

        if score < 0.5:
            low_score.append(img_name)

        print(score)

    return low_score


model = ft_model.Model(settings.IMG_SHAPE, False, False)
model.load_weights("../cnn_model/weight/base_weight/20221129-221745/50")

ng_scores = predict_dir("../image/module/true_ng", model)

plt.figure(figsize=(10, 7))
plt.hist(ng_scores)
plt.show()


ovk_low = low_score("../image/module/overkill", model)
ovk_df = pd.DataFrame(ovk_low)

ovk_df.to_csv("overkill_low.csv")
