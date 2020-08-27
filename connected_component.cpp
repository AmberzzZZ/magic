#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <time.h>

using namespace std;

#define CLOCKS_PER_SEC ((clock_t)1000)

// recursive
void search_neighbor(int* src, std::vector<int> &components, int i, int j, int k, int width, int height, int depth)
{
    int index = k + j*width + i*height*width;
    if (src[index] != 0)
    {
        components.push_back(index);
        src[index] = 0;
        for (int ii = i - 1; ii <= i + 1; ii++)
            for (int jj = j - 1; jj <= j + 1; jj++)
                for (int kk = k - 1; kk <= k + 1; kk++)
                    if (ii >= 0 && ii < depth && jj >= 0 && jj < height && kk >= 0 && kk < width)
                        search_neighbor(src, components, ii, jj, kk, width, height, depth);
    }
}


// region growing
void search_neighbor2(int* src, std::vector<int> &components, int i, int j, int k, int width, int height, int depth)
{
    int index = k + j*width + i*height*width;
    std::vector<int> seeds = {index};
    while (seeds.size())
    {
        int index = seeds.back();
        seeds.pop_back();
        if (src[index])
        {
            int i = index / (height*width);
            int j = (index - i*height*width) / width;
            int k = index - i*height*width - j*width;
            components.push_back(index);
            src[index] = 0;
            for (int ii = i - 1; ii <= i + 1; ii++)
                for (int jj = j - 1; jj <= j + 1; jj++)
                    for (int kk = k - 1; kk <= k + 1; kk++)
                        if (ii >= 0 && ii < depth && jj >= 0 && jj < height && kk >= 0 && kk < width)
                        {
                            int neighbor_index = kk + jj*width + ii*height*width;
                            seeds.push_back(neighbor_index);
                        }
        }
    }
}



void connectedComponents3D(int* src, int* dst, int width, int height, int depth, int min_th=0)
{
    int i, j, k;
    int v = 11;
    for (i = 0; i < depth; i++)
        for (j = 0; j < height; j++)
            for (k = 0; k < width; k++)
            {
                int index = k + j*width + i*height*width;
                if (src[index] != 0)
                {
                    std::vector<int> components;
                    // search_neighbor(src, components, i, j, k, width, height, depth);
                    search_neighbor2(src, components, i, j, k, width, height, depth);
                    std::cout << "v: " << v << " components.size(): " << components.size() << std::endl;
                    if (components.size() > min_th)
                    {
                        for (auto it : components)
                            dst[it] = v;
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
    clock_t startTime = clock();
    connectedComponents3D(src, dst, width, height, depth);
    clock_t endTime = clock();
    double totalTime = (double)(endTime-startTime) / CLOCKS_PER_SEC;
    std::cout << "total time: " << totalTime << std::endl;

    for (int i=0; i<width*height*depth; i++)
        std::cout << dst[i] << " ";
}


// recursive method: total time: 0.254
// region growing: total time: 0.193
