## 用来更新一些tool scripts

1. elegant_gaussian.py: n维高斯核
    生成n维坐标可以直接用np.indices(dims)

2. trilinear.py: 三线性插值

3. border.py: 利用pooling获取border

4. dTrans.py: 距离场(Euclidean/City block/Chessboard distance) & Hausdorff distance

5. wc.py: wordcloud

6. hausdoff.py: Hausdoff distance计算，3D的配准时间复杂度较大，取距离质心最远的N个点做近似

7. connect_componet.cpp: 
    递归版3d连通域，实际跑起来容易超出递归深度导致栈溢出，
    region growing版不会报错，时间竟然更少，可能跟具体测试数据也有一定关系
7.1. connect_componet.py: 
    递归版3d连通域，python版同样有递归深度限制问题，但是可以通过sys调整，
    region growing版本，用循环替换递归，效率变差


8. curve_fit.py: 最小二乘法曲线拟合