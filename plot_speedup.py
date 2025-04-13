import matplotlib.pyplot as plt
import numpy as np
import os
from collections import defaultdict

def plot_speedup_agrupado():
    output_dir = 'graficos_speedup_agrupados'
    os.makedirs(output_dir, exist_ok=True)

    grupos = defaultdict(list)

    with open('execution_times.txt', 'r') as f:
        lines = f.readlines()

        for line in lines[1:]:  # Ignora o cabeçalho
            line_split = line.strip().split()
            parte1 = line_split[0]  # ex: 500
            parte2 = line_split[1]  # ex: 1000
            entrada_nome = f"{parte1}x{parte2}"
            tempo_sequencial = float(line_split[2])
            dados = line_split[3:]

            tempos = list(map(float, dados[::2]))
            threads = list(map(int, dados[1::2]))

            # Adiciona o caso sequencial (1 thread)
            threads = [1] + threads
            tempos = [tempo_sequencial] + tempos

            grupos[parte1].append((entrada_nome, tempo_sequencial, list(zip(threads, tempos))))

    for grupo, entradas in grupos.items():
        plt.figure(figsize=(10, 6))
        
        for entrada_nome, tempo_seq, pares in entradas:
            threads = [t for t, _ in pares]
            tempos = [tp for _, tp in pares]
            speedups = [tempo_seq / tp for tp in tempos]

            zipped = sorted(zip(threads, speedups))
            threads_ord, speedups_ord = zip(*zipped)

            plt.plot(threads_ord, speedups_ord, marker='o', label=f'{entrada_nome}')

        plt.title(f"Speedup agrupado por dimensão {grupo}xN")
        plt.xlabel("Número de Threads")
        plt.ylabel("Speedup")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(os.path.join(output_dir, f"speedup_grupo_{grupo}x.png"))
        plt.close()

    print(f"Gráficos agrupados salvos em: {output_dir}/")

plot_speedup_agrupado()
