import numpy as np


def h(a,b):
    a = np.expand_dims(a, axis=1)
    num = b.shape[0]
    a = np.tile(a, (1,num,1))      # [Na,Nb,dim]
    dis = np.sqrt(np.sum((a-b)**2, axis=-1))    # [Na,Nb]
    d0 = np.min(dis, axis=1)
    # debug
    # if np.max(d0) > 10:
    #     debug_idx_a = np.argmax(d0)
    #     debug_idx_b = np.argmin(dis[debug_idx_a])
    #     print("pa: ", a[debug_idx_a,0,:], "pb: ", b[debug_idx_b,:], "dis: ", np.max(d0))
    return np.max(d0)


def cal_hd_approx(y_true, y_pred):
    coords = np.where(y_true>0)
    yt = np.stack(coords).T
    center = np.sum(yt, axis=0, keepdims=True) / yt.shape[0]
    n_points = min(24000, len(coords[0]))

    dis = np.sum((yt-center)**2, axis=-1)
    indices = np.argsort(dis)
    yt = yt[indices[-n_points::4]]

    coords = np.where(y_pred>0)
    n_points = min(24000, len(coords[0]))
    yp = np.stack(coords).T
    dis = np.sum((yp-center)**2, axis=-1)
    indices = np.argsort(dis)
    yp = yp[indices[-n_points::4]]

    return max(h(yt,yp), h(yp,yt))


def cal_hd_slower(y_true, y_pred):
    coords = np.where(y_true>0)
    yt = np.stack(coords).T
    yt = yt[::8,:]

    coords = np.where(y_pred>0)
    yp = np.stack(coords).T
    yp = yp[::8,:]

    return max(h(yt,yp), h(yp,yt))


if __name__ == '__main__':

    a = np.zeros((64,128,128), dtype=np.uint8)
    a[30:45,30:100,40:80] = 1
    b = np.zeros((64,128,128), dtype=np.uint8)
    b[46:65,60:99,33:92] = 1

    #
    print(cal_hd_approx(a, b))

    #
    coords = np.where(a>0)
    a = np.stack(coords).T
    center_a = np.sum(a,axis=0,keepdims=True) / a.shape[0]
    dis = np.sum((a-center_a)**2, axis=-1)
    indices = np.argsort(dis)
    a = a[indices[-8000:]]
    print(a.shape)

    coords = np.where(b>0)
    b = np.stack(coords).T
    center_b = np.sum(b,axis=0,keepdims=True) / b.shape[0]
    dis = np.sum((b-center_b)**2, axis=-1)
    indices = np.argsort(dis)
    b = b[indices[-8000:]]
    print(b.shape)

    ha = h(a, b)
    hb = h(b, a)
    print(ha, hb)





