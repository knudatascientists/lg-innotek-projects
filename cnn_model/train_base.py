#%%
import os
import sys

import cv2
import ft_model
import silence_tensorflow
import tensorflow as tf

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import settings

# setting tensorflow
silence_tensorflow.silence_tensorflow()
tf.random.set_seed(42)

# gpu setting
gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices("GPU")
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

# load model class
model = ft_model.Model(settings.IMG_SHAPE, top_trainable=False)
date = "20221129-194816"
epoch = 200
weight_path = f"./weight/top_weight/{date}/{epoch}"
model.load_weights(weight_path)

# load dataset
train_set, val_set = model.get_dataset(settings.IMG_PATH, settings.IMG_SHAPE, 32)

# load compiler and callbacks
optimizer, loss, metrics = model.get_compiler(0.00005)
callbacks = model.get_callbacks(settings.BASE_WEIGHT, settings.BASE_LOGS)

#%%
# model compile and fit
model.compile(optimizer, loss, metrics)
model.fit(train_set, epochs=50, validation_data=val_set, callbacks=callbacks)

# %%
