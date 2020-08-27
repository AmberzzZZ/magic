import numpy as np
import time
import sys
sys.setrecursionlimit(9000000)


# recursive
def search_neighor(src_arr, ps, i, j, k):
    depth, height, width = src_arr.shape
    if src_arr[i,j,k]:
        ps.append((i,j,k))
        src_arr[i,j,k] = 0
        for ii in range(i-1, i+2):
            for jj in range(j-1, j+2):
                for kk in range(k-1, k+2):
                    if 0<=ii<depth and 0<=jj<height and 0<=kk<width:
                        search_neighor(src_arr, ps, ii, jj, kk)
    return ps, src_arr


# region growing
def search_neighbor2(src_arr, i, j, k):
    depth, height, width = src_arr.shape
    seeds = [[i,j,k]]
    component = []
    while seeds:
        i,j,k = seeds[0]
        seeds = seeds[1:]
        if src_arr[i,j,k]:
            src_arr[i,j,k] = 0
            component.append([i,j,k])
            for ii in range(i-1, i+2):
                for jj in range(j-1, j+2):
                    for kk in range(k-1, k+2):
                        if 0<=ii<depth and 0<=jj<height and 0<=kk<width:
                            seeds.append([ii,jj,kk])
    return component, src_arr


def connected_component(src_arr, min_th=1000):
    depth, height, width = src_arr.shape
    dst_arr = np.zeros_like(src_arr)
    start_idx = 11
    for i in range(depth):
        for j in range(height):
            for k in range(width):
                if src_arr[i,j,k]:
                    ps = []
                    coords, src_arr = search_neighor(src_arr, ps, i, j, k)
                    # coords, src_arr = search_neighbor2(src_arr, i, j, k)
                    if len(coords) > min_th:
                        for coord_zyx in coords:
                            z,y,x = coord_zyx
                            dst_arr[z,y,x] = start_idx
                        start_idx += 1
    return dst_arr


if __name__ == '__main__':

    a = np.zeros((64,64,64))
    a[10:20,35:45, 35:45] = 1
    a[60:62,10:20,33:55] = 1
    start = time.time()
    b = connected_component(a, min_th=0)
    end = time.time()
    print("总共用时{}秒".format((end - start))) 
    print(np.unique(b))


# recursive: 总共用时0.0824127197265625秒
# region growing: 总共用时0.8527581691741943秒
