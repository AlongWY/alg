#include <random>
#include <vector>
#include <algorithm>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

int rand_partition(std::vector<int> &array, int p, int r) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(p, r);
    auto i = dis(gen);

    std::swap(array[r], array[i]);
    int x = array[r];
    i = p - 1;
    for (auto j = p; j < r; j++) {
        if (array[j] < x) {
            i = i + 1;
            std::swap(array[i], array[j]);
        }
    }
    std::swap(array[i + 1], array[r]);
    return i + 1;
}

void quicksort_(std::vector<int> &array, int p, int r) {
    if (p < r) {
        auto q = rand_partition(array, p, r);
        quicksort_(array, p, q - 1);
        quicksort_(array, q + 1, r);
    }
}

std::vector<int> quicksort(std::vector<int> array) {
   quicksort_(array,0,array.size()-1);
   return array;
}

std::vector<int> cppsort(std::vector<int> array) {
   std::sort(array.begin(), array.end());
   return array;
}

PYBIND11_MODULE(quicksort, m) {
    m.doc() = "quick sort"; // optional module docstring
    m.def("cppsort", &cppsort, "C++ sort");
    m.def("quicksort", &quicksort, "A quick sort c++ extension");
}