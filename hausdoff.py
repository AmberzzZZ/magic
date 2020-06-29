import numpy as np


def h(a,b):
    num = b.shape[0]
    dim = b.shape[-1]
    a = np.tile(a, (1,num))
    b = np.reshape(b, (-1))
    dis = np.sqrt(np.sum(np.reshape((a-b)**2, (a.shape[0],num, dim)), axis=-1))
    d0 = np.min(dis, axis=1)
    return np.max(d0)


if __name__ == '__main__':

    a = np.zeros((64,128,128), dtype=np.uint8)
    a[30:45,30:100,40:80] = 1
    coords = np.where(a>0)
    a = np.stack(coords).T
    #
    center_a = np.sum(a,axis=0,keepdims=True) / a.shape[0]
    dis = np.sum((a-center_a)**2, axis=-1)
    indices = np.argsort(dis)
    a = a[indices[-8000:]]
    print(a.shape)

    b = np.zeros((64,128,128), dtype=np.uint8)
    b[46:65,60:99,33:92] = 1
    coords = np.where(b>0)
    b = np.stack(coords).T
    #
    center_b = np.sum(b,axis=0,keepdims=True) / b.shape[0]
    dis = np.sum((b-center_b)**2, axis=-1)
    indices = np.argsort(dis)
    b = b[indices[-8000:]]
    print(b.shape)

    ha = h(a, b)
    hb = h(b, a)
    print(ha, hb)

