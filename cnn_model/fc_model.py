import tensorflow as tf


def get_augmenter():
    data_augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomBrightness(0.05, value_range=[-1.0, 1.0]),
            tf.keras.layers.RandomRotation(0.01, fill_mode="nearest"),
            tf.keras.layers.RandomContrast(0.03),
            tf.keras.layers.RandomFlip(),
            tf.keras.layers.RandomTranslation(0.03, 0.03),
        ],
        name="data_augmentation",
    )

    return data_augmentation


def get_preprocessor(image_size):
    IMAGE_SIZE = image_size

    resize_and_rescale = tf.keras.Sequential(
        [
            tf.keras.layers.Resizing(IMAGE_SIZE[0], IMAGE_SIZE[1], interpolation="bicubic"),
            tf.keras.layers.Rescaling(1.0 / 255),
        ],
        name="resize_and_rescale",
    )

    return resize_and_rescale


def get_my_model(image_size):
    input_shape = image_size + (3,)

    my_model = tf.keras.Sequential(
        [
            get_augmenter(),
            get_preprocessor(image_size),
            tf.keras.layers.Conv2D(
                32,
                kernel_size=3,
                padding="same",
                kernel_regularizer=tf.keras.regularizers.L2(l2=0.001),
                input_shape=input_shape,
            ),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.ReLU(),
            tf.keras.layers.Dropout(0.4),
            tf.keras.layers.MaxPool2D(),
            tf.keras.layers.Conv2D(
                64,
                kernel_size=3,
                padding="same",
                kernel_regularizer=tf.keras.regularizers.L2(l2=0.001),
            ),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.ReLU(),
            tf.keras.layers.Dropout(0.4),
            tf.keras.layers.MaxPool2D(),
            tf.keras.layers.Conv2D(
                128,
                kernel_size=3,
                padding="same",
                kernel_regularizer=tf.keras.regularizers.L2(l2=0.001),
            ),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.ReLU(),
            tf.keras.layers.Dropout(0.4),
            tf.keras.layers.MaxPool2D(),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(128, activation="relu", kernel_regularizer=tf.keras.regularizers.L2(l2=0.001)),
            tf.keras.layers.Dropout(0.4),
            tf.keras.layers.Dense(32, activation="relu", kernel_regularizer=tf.keras.regularizers.L2(l2=0.001)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(1, activation="sigmoid", kernel_regularizer=tf.keras.regularizers.L2(l2=0.001)),
        ],
        name="my_model",
    )

    return my_model


def get_dataset(path, batch_size):
    train_ds = tf.keras.utils.image_dataset_from_directory(
        path,
        label_mode="binary",
        color_mode="grayscale",
        validation_split=0.2,
        subset="training",
        seed=42,
        batch_size=batch_size,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        path,
        label_mode="binary",
        color_mode="grayscale",
        validation_split=0.2,
        subset="validation",
        seed=42,
        batch_size=batch_size,
    )

    return train_ds, val_ds


def get_compiler(learning_rate: int):
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    loss = tf.keras.losses.BinaryFocalCrossentropy(gamma=2.0, from_logits=False)
    metrics = [
        tf.keras.metrics.BinaryAccuracy(name="accuracy"),
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall"),
        tf.keras.metrics.RecallAtPrecision(1, name="recall_at_perfect_precision"),
    ]

    return optimizer, loss, metrics


def get_callbacks(weight_path, board_path):
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="accuracy", patience=3),
        tf.keras.callbacks.ModelCheckpoint(weight_path, save_weights_only=True, save_best_only=True),
        tf.keras.callbacks.TensorBoard(log_dir=board_path, histogram_freq=1),
    ]

    return callbacks
