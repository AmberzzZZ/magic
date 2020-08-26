#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;


// 八连通
// 执行完，该连通区域对应的src全部为0，对应的dst为v；
void search_neighbor(int* src, std::vector<int> &ps, int i, int j, int k, int width, int height, int depth)
{
    int index = k + j*width + i*height*width;
    if (src[index] != 0)
    {
        ps.push_back(index);
        src[index] = 0;
        for (int ii = i - 1; ii <= i + 1; ii++)
            for (int jj = j - 1; jj <= j + 1; jj++)
                for (int kk = k - 1; kk <= k + 1; kk++)
                    if (ii >= 0 && ii < depth &&
                        jj >= 0 && jj < height &&
                        kk >= 0 && kk < width)
                        search_neighbor(src, ps, ii, jj, kk, width, height, depth);
    }
}


void connectedComponents3D(int* src, int* dst, int width, int height, int depth, int min_th=0)
{
    int i, j, k;
    int v = 11;
    std::vector<int> ps;
    for (i = 0; i < depth; i++)
        for (j = 0; j < height; j++)
            for (k = 0; k < width; k++)
            {
                int index = k + j*width + i*height*width;
                if (src[index] != 0)
                {
                    ps.clear();
                    search_neighbor(src, ps, i, j, k, width, height, depth);
                    // std::cout << "v: " << v << " ps.size(): " << ps.size() << std::endl;
                    if (ps.size() > min_th)
                    {
                        for (auto it : ps)
                        {
                            // std::cout << "it: " << it << std::endl;
                            dst[it] = v;
                        }
                        v++;    
                    }
                }
            }
    return;
}


int main()
{
    int width(4), height(4), depth(4);
    int *src = (int*)calloc(width*height*depth, sizeof(int));
    int *dst = (int*)calloc(width*height*depth, sizeof(int));
    src[0] = 1;
    src[1] = 1;
    src[30] = 1;
    src[31] = 1;
    src[56] = 1;
    connectedComponents3D(src, dst, width, height, depth);
    for (int i=0; i<width*height*depth; i++)
        std::cout << dst[i] << " ";



}
