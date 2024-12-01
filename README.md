# PARCO-H1 Project
Student: Salvatore Andaloro (email: [salvatore.andaloro@studenti.unitn.it](mailto:salvatore.andaloro@studenti.unitn.it))

The repository contains the following files:
```
|- sequential.c       : sequential implementation
|- cache_optimized.c  : cache-optimized implementation
|- openmp.c           : OpenMP implementation
|- peak_bandwidth.c   : benchmark used to measure the peak bandwidth of the system
|- main.pbs           : PBS script that runs all the implementations
```
### Reproducibility instructions

The results presented in the report can be reproduced by submitting the `main.pbs` file to the cluster using the following command:
```bash
qsub -q short_cpuQ -v PATH_TO_DIRECTORY=/home/<username>/<path_to_project_directory> /home/<username>/<path_to_project_directory>/main.pbs
```
Where `<username>` has to be replaced with the actual username and `<path_to_project_directory>` has to be replaced with the complete path from the home directory to the project directory. The path to the project should not contain spaces or commas, otherwise the qsub may interpret it incorrectly.

To allow a quick completion of the script, each implementation will be run only once by default. The number of runs can be changed by setting the RUNS environment variable as follows:
```bash
qsub -q short_cpuQ -v PATH_TO_DIRECTORY=/home/<username>/<path_to_project_directory>,RUNS=<number_of_runs> /home/<username>/<path_to_project_directory>/main.pbs
```

Alternatively, the PBS file can be run as a regular bash script on any Linux machine with `gcc-9.1.0` installed and the openmp library and by specifying the `PATH_TO_DIRECTORY` environment variable using
```bash
export PATH_TO_DIRECTORY=/home/<username>/<path_to_project_directory>
```

### Expected output
The PBS job will reserve a node with 64 cores and 10GB of memory. Once started, it should take less than a minute to complete (if the number of runs was set to be one). When the job completes, the output of the bash script will be printed to the `stdout.o` file (located in the directory where the script is run from).

The script performs the following operations:
1. prints to the output file the original and transposed matrix for the sequential, cache-optimized and OpenMP code to verify their correctness;
2. prints the system bandwidth given by `peak_bandwidth.c`(the code is run using 64 cores);
3. runs the sequential and the cache-optimized one with the flag configurations that are presented in the report
4. runs the parallel implementation with 1, 2, 4, 8, 16, 32 and 64 cores.

The data given by the runs is saved to the `results.csv` file (located in the `results` directory inside the project's directory). The csv file will contain a line for each run. The columns of the csv file are:
```
name - name of the run, as printed in the output file
size - size of the matrix
threads - number of threads
sym_time - wall-clock time taken to perform the symmetry check in seconds
transp_time - wall-clock time taken to perform the matrix transpose operation in seconds
```