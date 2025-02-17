import tensorflow as tf
from keras import callbacks 
from tensorflow import keras
from keras import callbacks
from keras import EarlyStopping, ModelCheckpoint, LearningRateScheduler
from model.preprocess import load_and_preprocess_data
from model.vit_model import VisionTransformer
import math

X_train, X_test, y_train, y_test = load_and_preprocess_data()

vit = VisionTransformer()

initial_lr = 0.001
def lr_scheduler(epoch):
    return initial_lr * 0.5 * (1 + math.cos(math.pi * epoch / 50))

vit.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=initial_lr),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

callbacks = [
    EarlyStopping(patience=5, restore_best_weights=True),
    ModelCheckpoint("model/saved_model/brain_tumor_vit", save_best_only=True),
    LearningRateScheduler(lr_scheduler)
]

history = vit.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=50,
    batch_size=16,
    callbacks=callbacks
)

vit.save("model/saved_model/brain_tumor_vit")





