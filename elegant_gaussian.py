import numpy as np
import tensorflow as tf
import math
import SimpleITK as sitk


def elegant_gaussian(kernel_size=(3,5,5), sigma=(1,1,1), dims=3, ball=False):
    dims = min(len(kernel_size), len(sigma), dims)
    kernel_size = kernel_size[:dims]
    sigma = sigma[:dims]
    distance_arr = np.zeros(kernel_size+(dims,), dtype=np.float32)
    factor = 1.
    for i in range(dims):
        vector_shape = [1 for i in range(dims)]
        vector_shape[i] = kernel_size[i]
        vector = np.arange(-(kernel_size[i]//2), -(kernel_size[i]//2)+kernel_size[i]).reshape(vector_shape)
        copy_shape = list(kernel_size)
        copy_shape[i] = 1
        tmp = np.tile(vector, copy_shape)
        distance_arr[...,i] = tmp
        factor *= math.pow(math.pi, 1/2.) * sigma[i]
    filter = np.sum((distance_arr*distance_arr)/(2*np.array(sigma)*np.array(sigma)), axis=-1, dtype=np.float32)
    filter = np.exp(-filter) / factor
    if ball:
        radius = np.array([i//2 for i in kernel_size])
        filter[np.sum((distance_arr/radius)*(distance_arr/radius),axis=-1)>1.5] = np.min(filter)
    filter = (filter - np.min(filter)) / (np.max(filter) - np.min(filter))

    return filter


# # try to use meshgrid
# def elegant_gaussian1(kernel_size=(3,5,5), sigma=(1,1,1), dims=3):
#     dims = min(len(kernel_size), len(sigma), dims)
#     kernel_size = kernel_size[:dims]
#     sigma = sigma[:dims]
#     factor = 1.
#     coords = []
#     for i in range(dims):
#         coord = np.arange(-(kernel_size[i]//2), -(kernel_size[i]//2)+kernel_size[i])
#         coords.append(coord)
#         factor *= math.pow(math.pi, 1/2.) * sigma[i]
#     distance_arrs = [np.expand_dims(i, axis=-1) for i in np.meshgrid(*coords, indexing='ij')]
#     distance_arr = np.concatenate(distance_arrs, axis=3)
#     filter = np.sum((distance_arr*distance_arr)/(2*np.array(sigma)*np.array(sigma)), axis=-1, dtype=np.float32)
#     filter = np.exp(-filter) / factor
#     filter = (filter - np.min(filter)) / (np.max(filter) - np.min(filter))
#     return filter


if __name__ == '__main__':

    x = np.zeros((1,64,128,128,1),dtype=np.float32)
    x[0,32,64,64,0] = 1
    inpt = tf.constant(x)
    kernel_size = (15,15,15)
    sigma = (2,6,10)
    filter = elegant_gaussian(kernel_size, sigma, ball=True)
    filter = tf.constant(filter, shape=kernel_size+(1,1))
    y = tf.nn.conv3d(inpt, filter, strides=[1,1,1,1,1], padding='SAME')
    with tf.Session() as sess:
        result = y.eval()[0,:,:,:,0]
        image = sitk.GetImageFromArray((result*255).astype(np.uint8))
        sitk.WriteImage(image, "gaussian_ball.nii.gz")



