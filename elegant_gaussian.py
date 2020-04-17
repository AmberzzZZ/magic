import numpy as np
import tensorflow as tf
import math
import SimpleITK as sitk


def elegant_gaussian(kernel_size=(3,5,5), sigma=(1,1,1), dims=3):
    dims = min(len(kernel_size), len(sigma), dims)
    kernel_size = kernel_size[:dims]
    sigma = sigma[:dims]
    distance_arr = np.zeros(kernel_size+(dims,), dtype=np.float32)
    for i in range(dims):
        vector_shape = [1 for i in range(dims)]
        vector_shape[i] = kernel_size[i]
        vector = np.arange(-(kernel_size[i]//2), -(kernel_size[i]//2)+kernel_size[i]).reshape(vector_shape)
        copy_shape = list(kernel_size)
        copy_shape[i] = 1
        tmp = np.tile(vector, copy_shape)
        distance_arr[...,i] = tmp
    filter = np.sum((distance_arr*distance_arr)/(2*np.array(sigma)*np.array(sigma)), axis=-1, dtype=np.float32)
    filter = np.exp(-filter)
    for i in range(dims):
        filter /= math.pow(math.pi, 1/2.) * sigma[i]
    filter = (filter - np.min(filter)) / (np.max(filter) - np.min(filter))
    return filter


if __name__ == '__main__':


    x = np.zeros((1,64,64,64,1),dtype=np.float32)
    x[0,32,32,32,0] = 1
    inpt = tf.constant(x)
    kernel_size = (13,17,21)
    sigma = (2,6,10)
    filter = elegant_gaussian(kernel_size, sigma)
    filter = tf.constant(filter, shape=kernel_size+(1,1))
    y = tf.nn.conv3d(inpt, filter, strides=[1,1,1,1,1], padding='SAME')
    with tf.Session() as sess:
        result = y.eval()[0,:,:,:,0]
        image = sitk.GetImageFromArray((result*255).astype(np.uint8))
        sitk.WriteImage(image, "gaussian_tube.nii.gz")



