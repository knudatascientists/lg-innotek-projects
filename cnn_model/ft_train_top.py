#%%
import cv2
import ft_model
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

# load model class
model = ft_model.Model(setting.IMG_SIZE, base_trainable=False)
# model.load_weights(setting.TOP_WEIGHT)

# load dataset
train_set, val_set = model.get_dataset(setting.IMG_PATH, 8)

# load compiler and callbacks
optimizer, loss, metrics = model.get_compiler(0.0005)
callbacks = model.get_callbacks(setting.TOP_WEIGHT, setting.TOP_LOGS)

#%%
# model compile and fit
model.compile(optimizer, loss, metrics)
model.fit(train_set, epochs=50, validation_data=val_set, callbacks=callbacks)

# %%
