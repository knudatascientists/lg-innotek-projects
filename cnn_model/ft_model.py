import tensorflow as tf


class Model(tf.keras.Model):
    def __init__(self, height, width, base_trainable=True, top_trainable=True):
        super().__init__(self)
        self.height = height
        self.width = width
        self.base_trainable = base_trainable
        self.top_trainable = top_trainable
        self.augmenter = self.get_augmenter()
        self.preprocessor = self.get_preprocessor()
        self.base_model = self.get_base_model(self.height, self.width, self.base_trainable)
        self.top_model = self.get_top_model(self.top_trainable)

    def get_augmenter(self):
        data_augmentation = tf.keras.Sequential(
            [
                # tf.keras.layers.RandomBrightness(0.05, value_range=[-1.0, 1.0]),
                # tf.keras.layers.RandomContrast(0.05),
                tf.keras.layers.RandomFlip(),
                tf.keras.layers.RandomTranslation(0.03, 0.03),
            ],
            name="data_augmentation",
        )

        return data_augmentation

    def get_preprocessor(self):

        resize_and_rescale = tf.keras.Sequential(
            [
                tf.keras.layers.Rescaling(1.0 / 255),
            ],
            name="resize_and_rescale",
        )

        return resize_and_rescale

    def get_base_model(self, height, width, trainable=True):
        IMAGE_SIZE = (height, width)
        IMAGE_SHAPE = IMAGE_SIZE + (3,)

        base_model = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(
            include_top=False, weights="imagenet", input_shape=IMAGE_SHAPE, include_preprocessing=False
        )

        base_model.trainable = trainable

        return base_model

    def get_top_model(self, trainable=True):
        top_model = tf.keras.Sequential(
            [
                tf.keras.layers.GlobalAveragePooling2D(),
                tf.keras.layers.BatchNormalization(),
                tf.keras.layers.Dropout(0.5),
                tf.keras.layers.Dense(128, activation="relu"),
                tf.keras.layers.Dropout(0.4),
                tf.keras.layers.Dense(32, activation="relu"),
                tf.keras.layers.Dropout(0.3),
                tf.keras.layers.Dense(1, activation="sigmoid"),
            ],
            name="top_model",
        )

        top_model.trainalbe = trainable

        return top_model

    def call(self, inputs):
        x = self.augmenter(inputs)
        x = self.preprocessor(x)
        x = self.base_model(x)
        return self.top_model(x)

    @property
    def export_model(self):
        return tf.keras.Sequential([self.preprocessor, self.base_model, self.top_model])

    @classmethod
    def get_dataset(cls, path, height, width, batch_size):
        train_ds = tf.keras.utils.image_dataset_from_directory(
            path,
            label_mode="binary",
            color_mode="rgb",
            validation_split=0.2,
            subset="training",
            seed=42,
            batch_size=batch_size,
            image_size=(height, width),
        )

        val_ds = tf.keras.utils.image_dataset_from_directory(
            path,
            label_mode="binary",
            color_mode="rgb",
            validation_split=0.2,
            subset="validation",
            seed=42,
            batch_size=batch_size,
            image_size=(height, width),
        )

        return train_ds, val_ds

    @classmethod
    def get_compiler(cls, learning_rate: int):
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        loss = tf.keras.losses.BinaryFocalCrossentropy(gamma=2.0, from_logits=False)
        metrics = [
            tf.keras.metrics.BinaryAccuracy(name="accuracy"),
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
            tf.keras.metrics.RecallAtPrecision(1, name="recall_at_perfect_precision"),
        ]

        return optimizer, loss, metrics

    @classmethod
    def get_callbacks(cls, weight_path, board_path):
        callbacks = [
            # tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True, monitor="loss"),
            tf.keras.callbacks.ModelCheckpoint(
                weight_path, save_weights_only=True, save_best_only=True, monitor="accuracy"
            ),
            tf.keras.callbacks.TensorBoard(log_dir=board_path, histogram_freq=1),
        ]

        return callbacks
