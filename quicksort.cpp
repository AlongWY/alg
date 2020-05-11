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

void insert_sort(std::vector<int> &array, int l, int r) {
    for (int j = l; j <= r; j++) {
        int key = array[j];
        int i = j - 1;
        for (; i >= 0 && key < array[i]; i--) {
            array[i + 1] = array[i];
        }
        array[i + 1] = key;
    }
}

std::pair<int, int> rand_partition_opt(std::vector<int> &array, int l, int r) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(l, r);
    auto i = dis(gen);

    // a[l] ? ? ? ? ? a[i] ? ? ? ? ? ? a[r] ->
    // a[l] ? ? ? ? ? a[r] ? ? ? ? ? ? a[i]
    std::swap(array[r], array[i]);

    int x = array[r];
    i = r - 1;
    auto ml = l;
    auto mr = r;

    while (i >= ml) {
        if (array[i] > x) {
            std::swap(array[i--], array[mr--]);
        } else if (array[i] < x) {
            std::swap(array[i], array[ml++]);
        } else
            i--;
    }

    return std::make_pair(ml, mr);
}

void quicksort_opt_(std::vector<int> &array, int l, int r) {
    if (r - l <= 16) {
        insert_sort(array, l, r);
    } else if (l < r) {
        auto m = rand_partition_opt(array, l, r);
        quicksort_opt_(array, l, m.first - 1);
        quicksort_opt_(array, m.second + 1, r);
    }
}

std::vector<int> quicksort_opt(std::vector<int> array) {
    quicksort_opt_(array, 0, array.size() - 1);
    return array;
}

std::vector<int> cppsort(std::vector<int> array) {
   std::sort(array.begin(), array.end());
   return array;
}

int compare(const void *a, const void *b) {
    return (*(int *) a - *(int *) b);
}

std::vector<int> csort(std::vector<int> array) {
    std::qsort(array.data(), array.size(), sizeof(int), compare);
    return array;
}

PYBIND11_MODULE(quicksort, m) {
    m.doc() = "quick sort"; // optional module docstring
    m.def("csort", &csort, "C qsort");
    m.def("cppsort", &cppsort, "C++ sort");
    m.def("quicksort", &quicksort, "A quick sort c++ extension");
    m.def("quicksort_opt", &quicksort_opt, "A optimizerd quick sort c++ extension");
}