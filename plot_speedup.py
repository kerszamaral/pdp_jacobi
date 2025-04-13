import matplotlib.pyplot as plt
import os
import csv

def plot_speedup():
    output_dir = 'graficos_speedup'
    os.makedirs(output_dir, exist_ok=True)

    csv_dados = []

    with open('execution_times.txt', 'r') as f:
        lines = f.readlines()

        for i, line in enumerate(lines[1:]):  # Ignora o cabeçalho
            line_split = line.strip().split()
            entrada = f"{line_split[0]}_{line_split[1]}"
            tempo_sequencial = float(line_split[2])
            dados = line_split[3:]

            tempos = list(map(float, dados[::2]))
            threads = list(map(int, dados[1::2]))

            threads = [1] + threads
            tempos = [tempo_sequencial] + tempos

            speedups = []
            for t, th in zip(tempos, threads):
                speedup = tempo_sequencial / t
                speedups.append(speedup)
                csv_dados.append((entrada, th, t, speedup))

            zipped = sorted(zip(threads, speedups))
            threads_ord, speedups_ord = zip(*zipped)

            plt.figure()
            plt.plot(threads_ord, speedups_ord, marker='o', label='Speedup real')
            plt.title(f"Speedup para entrada {entrada}")
            plt.xlabel("Número de Threads")
            plt.ylabel("Speedup")
            plt.legend()
            plt.grid(True)

            plt.savefig(os.path.join(output_dir, f"speedup_{entrada}.png"))
            plt.close()

    with open(f'{output_dir}/speedup_dados.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['entrada', 'threads', 'tempo', 'speedup'])
        writer.writerows(csv_dados)

plot_speedup()
