#!/bin/bash

# Lista de pares de entrada
declare -a input_pairs=(
    "512 1000"
    "1024 1000"
    "1024 2000"
    "1024 10000"
    "2048 1000"
    "2048 10000"
    "2028 15000"
)

# Lista de números de threads para OpenMP (modifique conforme necessário)
real_threads=$(nproc --all)
max_factor="2"
max_threads=$(awk "function ceil(x){return int(x)+(x>int(x))} BEGIN {print ceil($real_threads*$max_factor)}")
echo "Max threads: $max_threads - Real threads: $real_threads"
# Verifica se o número máximo de threads é maior que 0
if [ $max_threads -le 0 ]; then
    echo "Error: No available threads."
    exit 1
fi

# seq FIRST STEP LAST
declare -a num_threads_list=(
    #$(seq 2 4 $max_threads)
    $(awk "BEGIN { for (i = 2; i <= $max_threads; i*=2) print i }")
    $(expr $real_threads / 2 - 1)
    $(expr $real_threads / 2)
    $(expr $real_threads / 2 + 1)
    $(expr $real_threads - 1)
    $real_threads
    $(expr $real_threads + 1)
    $max_threads
)
declare -a num_threads_list=($(printf '%s\n' "${num_threads_list[@]}" | sort -nu)) # Remove duplicates and sort
echo "Num threads list: ${num_threads_list[@]}"

len_input_pairs=${#input_pairs[@]}
len_num_threads=${#num_threads_list[@]}
longest_time="6*60"
prob_max_time=$(awk "BEGIN { print $len_input_pairs * ($len_num_threads + 1) * $longest_time }")

echo "Maximum probable time for the test is: $prob_max_time seconds"

# Nome do arquivo de saída
output_file="execution_times.txt"

# Limpa o arquivo antes de escrever novos dados
echo "Input1 Input2 Execution_Time_Seq(s) Execution_Time_MP(s) Threads" > "$output_file"

export OMP_PROC_BIND=true

prog_stdin="./.prog_in"
if [ -p $prog_stdin ]; then
    rm $prog_stdin
fi

VTUNE_ACTIVE=1
vtune_type="hpc-performance"
vtune_out="./vtune_out/"
# Intel VTune Profiler CLI
# performance-snapshot, hotspots and/or hpc-performance
# vtune -collect performance-snapshot hotspots hpc-performance -r my_results -- ./laplace_seqa
# vtune -collect hotspots -r $vtune_output -- ./laplace_seq
# https://www.intel.com/content/www/us/en/docs/vtune-profiler/user-guide/2024-0/command-line-interface.html

out_dir="./out"
if [ ! -d "$out_dir" ]; then
    mkdir $out_dir
fi

# Executa os testes sequenciais e salva os resultados
for pair in "${input_pairs[@]}"; do
    echo "Running laplace_seq with input: $pair"
    out_file="$out_dir/laplace_seq_${pair// /_}.txt"
    # Executa o VTune em segundo plan
    start_time=$(date +%s.%N)
    if [ $VTUNE_ACTIVE -eq 1 ]; then
        # Executa o VTune em segundo plano
        vtune_output="$vtune_out/vtune_${pair// /_}_seq"
        # Launches the analysis tool with the process
        vtune -collect $vtune_type -r $vtune_output ./laplace_seq $pair &> $out_file
    else
        # Executa o programa em segundo plano
        ./laplace_seq $pair &> $out_file
    fi
    end_time=$(date +%s.%N)

    # Calcula o tempo de execução
    exec_time_seq=$(echo "$end_time - $start_time" | bc)
    echo "$pair $exec_time_seq"
    echo "$pair $exec_time_seq" >> "$output_file"
done

# Executa os testes paralelos (MP) com diferentes números de threads
for num_threads in "${num_threads_list[@]}"; do
    export OMP_NUM_THREADS=$num_threads  # Define o número de threads do OpenMP
    
    for pair in "${input_pairs[@]}"; do
        echo "Running laplace_mp with input: $pair and $num_threads threads"
        # Cria o pipe para a entrada padrão
        out_file="$out_dir/laplace_mp_${pair// /_}_$num_threads.txt"
        
        # Executa o VTune em segundo plan
        start_time=$(date +%s.%N)
        if [ $VTUNE_ACTIVE -eq 1 ]; then
            # Executa o VTune em segundo plano
            vtune_output="$vtune_out/vtune_${pair// /_}_mp_${num_threads}"
            # Launches the analysis tool with the process
            vtune -collect $vtune_type -r $vtune_output ./laplace_mp $pair &> $out_file
        else
            # Executa o programa em segundo plano
            ./laplace_mp $pair &> $out_file
        fi
        end_time=$(date +%s.%N)

        # Calcula o tempo de execução
        exec_time_mp=$(echo "$end_time - $start_time" | bc)
        echo "$pair $exec_time_mp"

        # Atualiza o arquivo com o tempo de execução paralelo
        # Procurando a linha correspondente ao par de entrada para adicionar o tempo MP
        sed -i "/^$pair/ s/$/ $exec_time_mp $num_threads/" "$output_file"
    done
done

echo "Results saved in $output_file"
