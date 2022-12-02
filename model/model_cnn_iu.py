import os
import sys

import silence_tensorflow
import tensorflow as tf

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import cnn_model.ft_model as ft_model
import img_preprocess
import settings

# setting tensorflow
silence_tensorflow.silence_tensorflow()
tf.random.set_seed(42)

model = ft_model.Model(settings.IMG_SHAPE, False, False)
model.load_weights("./model/weight/50")


def model_iu(img, only_proba=True, threshold=0.5):
    """cnn predict model

    Args:
        img (np.array): opencv read image (bgr)
        only_proba (bool, optional): if False, return OK or NG. Defaults to True.
        threshold (float, optional): sigmoid threshold. Defaults to 0.5.

    Returns:
        proba: predict proba
        proba, value: return proba and OK or NG to tuple
    """
    img = img_preprocess.cnn_preprocess_img(img, settings.IMG_SIZE, predict=True)
    proba = float(model.predict(img)[0][0])

    if only_proba is False:
        if proba >= threshold:
            return proba, "OK"
        else:
            return proba, "NG"

    return proba
