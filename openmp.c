#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#define BLOCK_SIZE 64

void init_rand(float **m, int size) {
    #pragma omp parallel for simd
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            m[i][j] = (float)rand();
        }
    }
}

void print_mat(float **m, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            printf("%12.0f ", m[i][j]);
        }
        printf("\n");
    }
}

int check_sym(float **m, int size) {
    int is_sym = 1;
    #pragma omp parallel for simd reduction(&:is_sym)
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < i; j++) {
            if (m[i][j] != m[j][i]) {
                is_sym &= 0;
            }
        }
    }
    return is_sym;
}

void blocked_transpose(float **m, float **t, int i1, int i2, int j1, int j2, int size) {
    // Test for overflows
    i2 = (i2 < size) ? i2 : size;
    j2 = (j2 < size) ? j2 : size;
    // Perform matrix transposition on the block
    for (int i = i1; i < i2; i++) {
        #pragma omp simd
        for (int j = j1; j < j2; j++) {
            t[i][j] = m[j][i];
        }
    }
}

void divide_transpose(float **m, float **t, int size) {
    #pragma omp parallel for
    for (int i = 0; i < size; i += BLOCK_SIZE) {
        for (int j = 0; j < size; j += BLOCK_SIZE) {
            blocked_transpose(m, t, i, i + BLOCK_SIZE, j, j + BLOCK_SIZE, size);
        }
    }
}

int main(int argc, char **argv) {
    int size = 4096;
    if (argc > 1) {
        size = strtol(argv[1], NULL, 10);
    }

    float **m = (float **)malloc(size * sizeof(float *));
    float **t = (float **)malloc(size * sizeof(float *));
    for (int i = 0; i < size; i++) {
        m[i] = (float *)malloc(size * sizeof(float));
        t[i] = (float *)malloc(size * sizeof(float));
    }
    
    init_rand(m, size);
    double start, end;
    int is_sym = 0;
    // Check if the matrix is symmetric
    start = omp_get_wtime();
    is_sym = check_sym(m, size);
    end = omp_get_wtime();
    printf("%.9f,", end-start);
    // Print some output to stderr to avoid the compiler optimizing the check away
    fprintf(stderr, "%d", is_sym);

    start = omp_get_wtime();
    // Compute blocked transpose
    divide_transpose(m, t, size);
    end = omp_get_wtime();

    printf("%.9f\n", end-start);
    // Print some output to stderr to avoid the compiler optimizing the transpose away
    fprintf(stderr, "%d", t[size-1][size-1]);

    return 0;
}
