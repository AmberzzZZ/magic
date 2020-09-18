import numpy as np
import cv2
import math


def curve_fit(points, k):
    # k: polynomial params: a0->ak
    # return: mat_a: a0->ak
    N = len(points)
    mat_x = np.zeros((k+1,k+1))
    mat_y = np.zeros((k+1))
    for i in range(k+1):
        for j in range(k+1):
            for m in range(N):
                mat_x[i][j] += math.pow(points[m][1], i+j)

        for m in range(N):
            mat_y[i] += math.pow(points[m][1], i) * points[m][0]

    mat_a = np.linalg.solve(mat_x, mat_y)
    return mat_a


if __name__ == '__main__':

    coords = [[221,37], [210,58], [203,81], [201,105], [193,128], [191,152], [189,178], [185,202], [180,229], [182,249], [193, 272]]

    # draw points
    canvas = np.zeros((512,512))
    for coord_xy in coords:
        cv2.circle(canvas, tuple(coord_xy), 5, 255, 2)

    # fit
    k = 2
    mat_a = curve_fit(coords, k)
    print(mat_a)

    # draw curve
    for i in range(512):
        curve_y = 0
        for j in range(k+1):
            curve_y += int(mat_a[j]*math.pow(i,j))
        if curve_y>=512 or curve_y<0:
            continue
        cv2.circle(canvas, (curve_y, i), 1, 255, -1)

    cv2.imshow("tmp", canvas)
    cv2.waitKey(0)



