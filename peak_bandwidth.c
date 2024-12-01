#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char **argv) {
  int size = 4096;
  if (argc > 1) {
      size = strtol(argv[1], NULL, 10);
  }

  float *a;
  double start, end;
  int i;

  // Allocate memory for array
  a = (float *)malloc(size * sizeof(float));

  // Write some values to the array
  start = omp_get_wtime();
  #pragma omp parallel for simd
  for (i = 0; i < ARRAY_SIZE; i++) {
    a[i] = 42.0;
  }
  end_time = omp_get_wtime();

  // Calculate and print the bandwidth
  double bandwidth = (size * sizeof(float)) / (end - start) / 1e9;
  // Calculate and print the bandwidth using only one array
  printf("%f\n", bandwidth);

  return 0;
}