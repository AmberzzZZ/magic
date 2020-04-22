import cv2
import numpy as np
import tensorflow as tf


def resize_trilinear(arr, factors=(1,1,1), output_size=None):
    z, y, x = arr.shape
    if output_size is None:
        output_z, output_y, output_x = [int(s*f) for s,f in zip(arr.shape, factors)]
    else:
        output_z, output_y, output_x = output_size

    # resize yx
    arr = resize2d(arr, output_y, output_x)
    arr = np.transpose(arr, (2,1,0))
    # resize yz
    arr = resize2d(arr, output_y, output_z)
    arr = np.transpose(arr, (2,1,0))

    return arr


def resize2d(arr, h, w):
    new_arr = []
    for i in range(arr.shape[0]):
        slice = arr[i]
        slice = cv2.resize(slice, (w,h))
        new_arr.append(slice)
    return np.array(new_arr)


if __name__ == '__main__':

    x = np.ones((5,3,2))
    y = resize_trilinear(x, factors=(2,2,2), output_size=None)
    print(y.shape)


