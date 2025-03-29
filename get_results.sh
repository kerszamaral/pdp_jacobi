#!/bin/bash

# Lista de pares de entrada
declare -a input_pairs=("512 1000" "1024 1000" "1024 2000" "1024 10000")

# Lista de números de threads para OpenMP (modifique conforme necessário)
real_threads=$(nproc --all)
max_threads=$(awk "function ceil(x){return int(x)+(x>int(x))} BEGIN {print ceil($real_threads*1.5)}")
echo "Max threads: $max_threads - Real threads: $real_threads"
# Verifica se o número máximo de threads é maior que 0
if [ $max_threads -le 0 ]; then
    echo "Error: No available threads."
    exit 1
fi

# seq FIRST STEP LAST
declare -a num_threads_list=(
    $(seq 2 4 $max_threads)
    $real_threads
    $(expr $real_threads / 2)
    $(expr $real_threads - 1)
    $(expr $real_threads + 1)
    $(expr $real_threads / 2 + 1)
    $(expr $real_threads / 2 - 1)
)
declare -a num_threads_list=($(printf '%s\n' "${num_threads_list[@]}" | sort -nu)) # Remove duplicates and sort
echo "Num threads list: ${num_threads_list[@]}"

# Nome do arquivo de saída
output_file="execution_times.txt"

# Limpa o arquivo antes de escrever novos dados
echo "Input1 Input2 Execution_Time_Seq(s) Execution_Time_MP(s) Threads" > "$output_file"

export OMP_PROC_BIND=true

# Executa os testes sequenciais e salva os resultados
for pair in "${input_pairs[@]}"; do
    echo "Running laplace_seq with input: $pair"
    start_time=$(date +%s.%N)
    echo "$pair" | ./laplace_seq > /dev/null 2>&1
    end_time=$(date +%s.%N)
    exec_time_seq=$(echo "$end_time - $start_time" | bc)
    
    echo "$pair $exec_time_seq" >> "$output_file"
done

# Executa os testes paralelos (MP) com diferentes números de threads
for num_threads in "${num_threads_list[@]}"; do
    export OMP_NUM_THREADS=$num_threads  # Define o número de threads do OpenMP
    
    for pair in "${input_pairs[@]}"; do
        echo "Running laplace_mp with input: $pair and $num_threads threads"
        start_time=$(date +%s.%N)
        echo "$pair" | ./laplace_mp > /dev/null 2>&1
        end_time=$(date +%s.%N)
        exec_time_mp=$(echo "$end_time - $start_time" | bc)
        
        # Atualiza o arquivo com o tempo de execução paralelo
        # Procurando a linha correspondente ao par de entrada para adicionar o tempo MP
        sed -i "/^$pair/ s/$/ $exec_time_mp $num_threads/" "$output_file"
    done
done

echo "Results saved in $output_file"
