#!/bin/bash

# Lista de pares de entrada
declare -a input_pairs=("512 1000" "1024 1000" "1024 2000" "1024 10000" "2028 15000")

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

prog_stdin="./.prog_in"
if [ -p $prog_stdin ]; then
    rm $prog_stdin
fi

VTUNE_ACTIVE=0
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
    # Creates the stdin pipe
    mkfifo $prog_stdin
    out_file="$out_dir/laplace_seq_${pair// /_}.txt"
    # Executa o programa em segundo plano
    ./laplace_seq < $prog_stdin > $out_file 2>&1 &
    # Captura o PID do processo em segundo plano
    ppid=$!

    # Executa o VTune em segundo plan
    if [ $VTUNE_ACTIVE -eq 1 ]; then
        # Executa o VTune em segundo plano
        vtune_output="$vtune_out/vtune_${pair// /_}_seq"
        vtune_output_hpc="${vtune_output}_hpc"
        vtune_output_hs="${vtune_output}_hs"
        vtune_output_ps="${vtune_output}_ps"
        # Launches the analysis tool with the process ID
        vtune -collect hotspots -r $vtune_output_hs -target-pid $ppid &
        hspid=$!
        vtune -collect hpc-performance -r $vtune_output_hpc -target-pid $ppid &
        hpcpid=$!
        vtune -collect performance-snapshot -r $vtune_output_ps -target-pid $ppid &
        pspid=$!
    fi

    # Aguarda o processo em segundo plano ser iniciado
    start_time=$(date +%s.%N)
    echo "$pair" > $prog_stdin
    wait $ppid
    end_time=$(date +%s.%N)
    # Aguarda o VTune terminar
    if [ $VTUNE_ACTIVE -eq 1 ]; then
        wait $hspid
        wait $hpcpid
        wait $pspid
    fi

    # Remove o pipe
    rm $prog_stdin
    # Calcula o tempo de execução
    exec_time_seq=$(echo "$end_time - $start_time" | bc)
    echo "$ppid: $pair $exec_time_seq"
    echo "$pair $exec_time_seq" >> "$output_file"
done

# Executa os testes paralelos (MP) com diferentes números de threads
for num_threads in "${num_threads_list[@]}"; do
    export OMP_NUM_THREADS=$num_threads  # Define o número de threads do OpenMP
    
    for pair in "${input_pairs[@]}"; do
        echo "Running laplace_mp with input: $pair and $num_threads threads"
        # Cria o pipe para a entrada padrão
        mkfifo $prog_stdin
        out_file="$out_dir/laplace_mp_${pair// /_}_$num_threads.txt"

        # Executa o programa em segundo plano
        ./laplace_mp < $prog_stdin > $out_file 2>&1 &
        # Captura o PID do processo em segundo plano
        ppid=$!

        # Executa o VTune em segundo plano
        if [ $VTUNE_ACTIVE -eq 1 ]; then
            # Executa o VTune em segundo plano
            vtune_output="$vtune_out/vtune_${pair// /_}_mp_${num_threads}"
            vtune_output_hpc="${vtune_output}_hpc"
            vtune_output_hs="${vtune_output}_hs"
            vtune_output_ps="${vtune_output}_ps"
            # Launches the analysis tool with the process ID
            vtune -collect hotspots -r $vtune_output_hs -target-pid $ppid &
            hspid=$!
            vtune -collect hpc-performance -r $vtune_output_hpc -target-pid $ppid &
            hpcpid=$!
            vtune -collect performance-snapshot -r $vtune_output_ps -target-pid $ppid &
            pspid=$!
        fi

        # Aguarda o processo em segundo plano ser iniciado
        start_time=$(date +%s.%N)
        echo "$pair" > $prog_stdin
        wait $ppid
        end_time=$(date +%s.%N)
        # Aguarda o VTune terminar
        if [ $VTUNE_ACTIVE -eq 1 ]; then
            wait $hspid
            wait $hpcpid
            wait $pspid
        fi

        # Remove o pipe
        rm $prog_stdin
        # Calcula o tempo de execução
        exec_time_mp=$(echo "$end_time - $start_time" | bc)
        echo "$ppid: $pair $exec_time_mp"

        # Atualiza o arquivo com o tempo de execução paralelo
        # Procurando a linha correspondente ao par de entrada para adicionar o tempo MP
        sed -i "/^$pair/ s/$/ $exec_time_mp $num_threads/" "$output_file"
    done
done

echo "Results saved in $output_file"
