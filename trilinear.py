import cv2
import numpy as np
import SimpleITK as sitk


def resize_trilinear(arr, factors=(1,1,1), output_size=None, interpolation=cv2.INTER_LINEAR):
    z, y, x = arr.shape
    if output_size is None:
        output_z, output_y, output_x = [int(s*f) for s,f in zip(arr.shape, factors)]
    else:
        output_z, output_y, output_x = output_size

    # resize yx
    arr = resize2d(arr, output_y, output_x, interpolation=interpolation)
    arr = np.transpose(arr, (2,1,0))
    # resize yz
    arr = resize2d(arr, output_y, output_z, interpolation=interpolation)
    arr = np.transpose(arr, (2,1,0))

    return arr


def resize2d(arr, h, w, interpolation=cv2.INTER_LINEAR):
    new_arr = []
    for i in range(arr.shape[0]):
        slice = arr[i]
        slice = cv2.resize(slice, (w,h), interpolation=interpolation)
        new_arr.append(slice)
    return np.array(new_arr)


if __name__ == '__main__':

    x = sitk.ReadImage("gaussian_tube.nii.gz")
    x = sitk.GetArrayFromImage(x)
    y = resize_trilinear(x, factors=(2,2,2), output_size=None)

    sitk.WriteImage(sitk.GetImageFromArray(y), 'y.nii.gz')



