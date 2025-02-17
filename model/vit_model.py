import tensorflow as tf
from keras import layers, Model
import numpy as np

class VisionTransformer(Model):
    def __init__(self, img_size=64, patch_size=8, in_channels=4, num_classes=2, d_model=256, num_heads=8, mlp_dim=512, num_layers=6, dropout=0.2):
        super(VisionTransformer, self).__init__()
        self.num_patches = (img_size // patch_size) ** 2
        self.patch_size = patch_size
        self.patch_embed = layers.Conv2D(d_model, kernel_size=patch_size, strides=patch_size, padding='valid')
        self.cls_token = self.add_weight("cls_token", shape=(1, 1, d_model), initializer="random_normal")
        self.pos_embedding = self.add_weight("pos_embedding", shape=(1, self.num_patches + 1, d_model), initializer="random_normal")
        
        self.encoder_blocks = []
        for _ in range(num_layers):
            block = tf.keras.Sequential([
                layers.LayerNormalization(epsilon=1e-6),
                layers.MultiHeadAttention(num_heads=num_heads, key_dim=d_model//num_heads, dropout=dropout),
                layers.Add(),
                layers.LayerNormalization(epsilon=1e-6),
                layers.Dense(mlp_dim, activation='gelu'),
                layers.Dropout(dropout),
                layers.Dense(d_model),
                layers.Dropout(dropout),
                layers.Add()
            ])
            self.encoder_blocks.append(block)

        self.layer_norm = layers.LayerNormalization(epsilon=1e-6)
        self.mlp_head = tf.keras.Sequential([
            layers.Dense(mlp_dim, activation='gelu'),
            layers.Dropout(dropout),
            layers.Dense(num_classes, activation='softmax')
        ])

    def call(self, x, training=False):
        x = self.patch_embed(x)
        x = tf.reshape(x, (tf.shape(x)[0], -1, tf.shape(x)[-1]))
        cls_tokens = tf.repeat(self.cls_token, tf.shape(x)[0], axis=0)
        x = tf.concat([cls_tokens, x], axis=1)
        x = x + self.pos_embedding

        for block in self.encoder_blocks:
            x = block(x, training=training)
        
        x = self.layer_norm(x[:, 0])
        return self.mlp_head(x)