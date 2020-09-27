"""
https://gist.github.com/RomanSteinberg/c4a47470ab1c06b0c45fa92d07afe2e3
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from tensorflow.keras import layers
import tensorflow as tf

tf.keras.backend.clear_session()  # For easy reset of notebook state.


class Sampling(layers.Layer):
    """Uses (z_mean, z_log_var) to sample z, the vector encoding a digit."""

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon


class Encoder(layers.Layer):
    """Maps MNIST digits to a triplet (z_mean, z_log_var, z)."""

    def __init__(self,
               latent_dim=32,
               intermediate_dim=64,
               name='encoder',
               **kwargs):
        super(Encoder, self).__init__(name=name, **kwargs)
        self.dense_proj = layers.Dense(intermediate_dim,
                                       activation='relu',
                                       # force all weights to be positive to reflect that
                                       # higher input should result in higher intermediate values
                                       # tf.keras.constraints.NonNeg()
                                       kernel_constraint=tf.keras.constraints.MinMaxNorm(min_value=0.001))
        self.dense_mean = layers.Dense(latent_dim, use_bias=False)
        self.dense_log_var = layers.Dense(latent_dim, use_bias=False)
        self.sampling = Sampling()

    def call(self, inputs):
        x = self.dense_proj(inputs)
        z_mean = self.dense_mean(x)
        z_log_var = self.dense_log_var(x)
        z = self.sampling((z_mean, z_log_var))
        return z_mean, z_log_var, z


class Decoder(layers.Layer):
    """Converts z, the encoded digit vector, back into a readable digit."""

    def __init__(self,
               original_dim,
               intermediate_dim=64,
               name='decoder',
               **kwargs):
        super(Decoder, self).__init__(name=name, **kwargs)
        self.dense_proj = layers.Dense(intermediate_dim, activation='relu', use_bias=False)
        self.dense_output = layers.Dense(original_dim, activation='linear', use_bias=False)

    def call(self, inputs):
        x = self.dense_proj(inputs)
        return self.dense_output(x)


class VariationalAutoEncoder(tf.keras.Model):
    """Combines the encoder and decoder into an end-to-end model for training."""

    def __init__(self,
               original_dim,
               intermediate_dim=64,
               latent_dim=32,
               name='autoencoder',
               **kwargs):
        super(VariationalAutoEncoder, self).__init__(name=name, **kwargs)
        self.original_dim = original_dim
        self.encoder = Encoder(latent_dim=latent_dim,
                               intermediate_dim=intermediate_dim)
        self.decoder = Decoder(original_dim, intermediate_dim=intermediate_dim)

    def call(self, inputs):
        # self._set_inputs(inputs)
        z_mean, z_log_var, z = self.encoder(inputs)
        reconstructed = self.decoder(z)
        # Add KL divergence regularization loss.
        kl_loss = -0.5 * tf.reduce_mean(
            z_log_var - tf.square(z_mean) - tf.exp(z_log_var) + 1)
        self.add_loss(kl_loss)
        return reconstructed

    def fit(self, X, y=None):
        # this to be compatible with sklearn Pipeline
        return self

    def transform(self, X, y=None):
        # this to be compatible with sklearn Pipeline
        return self.encoder.call(X)[0].numpy()


def train():

    # keep intermediate dim to 1
    # this ensures that model is linear and simple
    # we want it to be as simple as possible
    # and not to model any outliers / funny data-points
    original_dim = 4
    intermediate_dim = 1
    latent_dim = 1
    vae = VariationalAutoEncoder(original_dim, intermediate_dim, latent_dim)

    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
    mse_loss_fn = tf.keras.losses.MeanSquaredError()

    loss_metric = tf.keras.metrics.Mean()

    # TODO: fix data loading mess
    # load the following from make_score.py
    # x_train = model_pipe.transform(train_data)
    x_train = None

    train_dataset = tf.data.Dataset.from_tensor_slices(x_train)
    train_dataset = train_dataset.shuffle(buffer_size=1000).batch(1000)

    # Iterate over epochs.
    for epoch in range(1000):

        # Iterate over the batches of the dataset.
        for step, x_batch_train in enumerate(train_dataset):
            with tf.GradientTape() as tape:
                reconstructed = vae(x_batch_train)
                # Compute reconstruction loss
                loss = mse_loss_fn(x_batch_train, reconstructed)
                # loss += sum(vae.losses) * 0 # Add KLD regularization loss

            grads = tape.gradient(loss, vae.trainable_weights)
            optimizer.apply_gradients(zip(grads, vae.trainable_weights))

            loss_metric(loss)

            if step % 100 == 0:
                print('step %s: mean loss = %s' % (step, loss_metric.result()))

    # vae.transform(np.array([[-0.45,  1.  , -1.  , -1]]))


def save(vae):
    # convert to tf lite and save
    #
    # cannot convert to tflite due to the following error:
    # Ops that can be supported by the flex runtime
    # (enabled via setting the -emit-select-tf-ops flag): RandomStandardNormal.
    #
    # can set converter.allow_custom_ops = True
    # but then during the loading the following happens:
    # RuntimeError: Encountered unresolved custom op: RandomStandardNormal.
    # Node number 0 (RandomStandardNormal) failed to prepare.
    #
    # converter = tf.lite.TFLiteConverter.from_keras_model(vae)
    # converter.allow_custom_ops = True
    # tflite_model = converter.convert()
    #
    # tflite_model_file_path = 'web_score/scorers/vae_model.tflite'
    # with open(tflite_model_file_path, 'wb') as f:
    #   f.write(tflite_model)

    # will use full tensorflow takes ~130 mb in prod
    model_file_path = 'web_score/scorers/vae_model'
    vae.save_weights(model_file_path)


def load():

    original_dim = 4
    intermediate_dim = 1
    latent_dim = 1
    vae = VariationalAutoEncoder(original_dim, intermediate_dim, latent_dim)

    model_file_path = 'web_score/scorers/vae_model'
    vae.load_weights(model_file_path)

    return vae


def inspect(vae):

    import numpy as np
    import pylab as plt

    grids = np.meshgrid(*[np.linspace(-1, 1, 10) for _ in range(2)])
    x = np.column_stack((grid.ravel() for grid in grids))
    pred = vae.transform(np.concatenate([x, np.zeros_like(x)], axis=1))
    pred = pred.reshape(grids[0].shape)

    fig, ax = plt.subplots()
    ax.contourf(grids[0], grids[1], pred, cmap=plt.cm.Blues_r)
