import tensorflow as tf
import numpy as np
import SimpleITK as sitk


if __name__ == '__main__':

    y_true = np.ones((64,64,64))
    y_true[25:38,25:38,25:38] = 2
    sitk.WriteImage(sitk.GetImageFromArray(y_true), 'y.nii.gz')
    y_true = np.reshape(y_true, (1,64,64,64,1), order='C')

    negative = tf.constant(3 - y_true, np.float32)
    positive = tf.constant(y_true, np.float32)
    positive = tf.keras.backend.pool3d(positive, pool_size=(5,5,5), padding="same")
    negative = tf.keras.backend.pool3d(negative, pool_size=(5,5,5), padding="same")
    border = positive * negative

    with tf.Session() as sess:
        y3 = border.eval()[0,:,:,:,0]
        sitk.WriteImage(sitk.GetImageFromArray(y3), 'y3.nii.gz')


