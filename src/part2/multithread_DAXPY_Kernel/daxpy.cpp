#include <iostream>
#include <vector>
#include <thread>

// Function to compute a segment of the DAXPY operation
void daxpy_segment(std::vector<double>& x, std::vector<double>& y, double a, size_t start, size_t end) {
    for (size_t i = start; i < end; ++i) {
        y[i] = a * x[i] + y[i];
    }
}

int main() {
    const size_t N = 1000000;  // Vector size
    const double a = 2.5;      // Scalar multiplier
    const int num_threads = 4; // Number of threads

    // Initialize vectors
    std::vector<double> x(N, 1.0);
    std::vector<double> y(N, 2.0);

    // Divide work among threads
    size_t segment_size = N / num_threads;
    std::vector<std::thread> threads;

    for (int t = 0; t < num_threads; ++t) {
        size_t start = t * segment_size;
        size_t end = (t == num_threads - 1) ? N : start + segment_size;

        threads.emplace_back(daxpy_segment, std::ref(x), std::ref(y), a, start, end);
    }

    // Join threads
    for (auto& thread : threads) {
        thread.join();
    }

    // Output results for verification
    std::cout << "DAXPY completed. y[0] = " << y[0] << ", y[N-1] = " << y[N-1] << std::endl;
    return 0;
}
