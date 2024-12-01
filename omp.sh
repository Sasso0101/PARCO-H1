# Run OpenMP codes
results_dir=${1:-results}

declare -A runs
sizes=(40000)
runs=(["40000"]=1)
mkdir -p $results_dir/plots
echo "name,size,threads,sym_time,transp_time" > $results_dir/times.csv

declare -A omp
omp=(["strong_scaling"]="-O3 -march=native -fopenmp openmp.c")
threads=(1 2 4 8 16 32 64)

for code in "${!omp[@]}"
do
  printf 'Running %s\n' "$code"
  # Compile code
  gcc-9.1.0 ${omp[$code]} -o bin/$code
  for size in "${sizes[@]}"
  do
    printf '%s... ' "$size"

    for t in "${threads[@]}"
    do
      export OMP_NUM_THREADS=$t
      for (( j=0; j<${runs[$size]}; j++ ))
      do
        # Run code and save results in new line
        echo "$code,$size,$t,$(./bin/"$code" "$size")"
      done
    done >> $results_dir/times.csv 2> /dev/null
  done
  printf '\n'
done

omp=(["weak_scaling"]="-O3 -march=native -fopenmp openmp.c")
threads=(1 2 4 8 16 32 64)
declare -A dimensions
dimensions=(["1"]=1000 ["2"]=1414 ["4"]=2000 ["8"]=2828 ["16"]=4000 ["32"]=5657 ["64"]=8000)

for code in "${!omp[@]}"
do
  printf 'Running %s\n' "$code"
  # Compile code
  gcc-9.1.0 ${omp[$code]} -o bin/$code
  for threads in "${threads[@]}"
  do
    printf '%s... ' "${dimensions[$threads]}"

    export OMP_NUM_THREADS=$threads
    echo "$code,${dimensions[$threads]},$threads,$(./bin/"$code" "${dimensions[$threads]}")" >> $results_dir/times.csv 2> /dev/null
  done
  printf '\n'
done

python3 omp.py $results_dir