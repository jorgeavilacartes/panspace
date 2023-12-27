"CAE with Batch Normalization"
import tensorflow as tf

def CNNAutoencoderCAEBN(latent_dim: int = 100):

  # Encoder 
  input_enc = tf.keras.layers.Input(shape=(64,64,1), name="input_encoder")
  x = tf.keras.layers.Conv2D(filters=16, kernel_size=(3,3), strides=1, padding="same", activation="relu")(input_enc) # output (62,62,16)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), strides=1, padding="same", activation="relu")(x) # output (60,60,32)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), strides=2, padding="same", activation="relu")(x) # output (29,29,64)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), strides=1, padding="same", activation="relu")(x) # output (27,27,128)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Flatten()(x)
  x = tf.keras.layers.Dense(latent_dim, activation="relu",)(x)
  x = tf.math.l2_normalize(x, axis=1,)   # Embedding: L2 normalization layer
  emb = tf.keras.layers.Identity(False, name="output_encoder")(x)
  # Decoder
  x = tf.keras.layers.Dense(27 * 27 * 128 , activation="relu", name="input_decoder")(emb)
  x = tf.keras.layers.Reshape((27, 27, 128))(x) # output (27,27,128)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Conv2DTranspose(filters=64, kernel_size=(3,3), strides=1, activation="relu")(x) # output (29,29,64)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Conv2DTranspose(filters=32, kernel_size=(3,3), strides=2, activation="relu")(x) # output (59,59,32)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Conv2DTranspose(filters=16, kernel_size=(3,3), strides=1, activation="relu")(x) # output (61,61,16)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  out_dec = tf.keras.layers.Conv2DTranspose(filters=1, kernel_size=(4,4), strides=1, activation="sigmoid", name="output_decoder")(x) # output (64,64,1) 

  autoencoder = tf.keras.models.Model(inputs=input_enc, outputs=out_dec)

  return autoencoder