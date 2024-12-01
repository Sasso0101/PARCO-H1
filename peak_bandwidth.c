#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char **argv) {
  unsigned long long size = 4096;
  int verbose = 0;
  if (argc > 1) {
    size = strtol(argv[1], NULL, 10);
  }
  if (argc > 2) {
    verbose = 1;
  }
  size = size * size;

  float *a;
  double start, end;

  // Allocate memory for array
  a = (float *)malloc(size * sizeof(float));

  // Write some values to the array
  start = omp_get_wtime();
  #pragma omp parallel for simd
  for (unsigned long long i = 0; i < size; i++) {
    a[i] = 42.0;
  }
  end = omp_get_wtime();
  if (verbose) {
    printf("%f\n", (double)size*4/(end-start)/1e9);
  } else {
    // Calculate and print wall time
    printf("1,%f\n", end - start);

    // Print some output to stderr to avoid the compiler optimizing the assignment away
    fprintf(stderr, "%d", a[size-1]);
  }
  return 0;
}