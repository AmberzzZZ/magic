## 用来更新一些tool scripts

1. elegant_gaussian.py: n维高斯核
    生成n维坐标可以直接用np.indices(dims)

2. trilinear.py: 三线性插值

3. border.py: 利用pooling获取border

4. dTrans.py: 距离场(Euclidean/City block/Chessboard distance) & Hausdorff distance

5. wc.py: wordcloud

6. hausdoff.py: Hausdoff distance计算，3D的配准时间复杂度较大，取距离质心最远的N个点做近似

7. connect_componet.cpp: 3d连通域