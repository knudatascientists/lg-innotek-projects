#%%
import cv2
import fc_model
import numpy as np
import setting
import silence_tensorflow
import tensorflow as tf

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

# load model
model = fc_model.get_my_model(setting.IMG_SIZE)

# load datasets
train_set, val_set = fc_model.get_dataset(setting.IMG_PATH, 1)

#%%
# load compiler, callbacks
optimizer, loss, metrics = fc_model.get_compiler(0.001)
callbacks = fc_model.get_callbacks(setting.FC_WEIGHT, setting.FC_LOGS)

# model compile and fit
model.compile(optimizer, loss, metrics)
model.fit(train_set, epochs=30, validation_data=val_set, callbacks=callbacks)

# %%
