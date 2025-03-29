#!/bin/bash

# Lista de pares de entrada
declare -a input_pairs=("512 1000" "1024 1000" "1024 2000" "1024 10000")

# Lista de números de threads para OpenMP (modifique conforme necessário)
declare -a num_threads_list=(1 2 4 8)

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
