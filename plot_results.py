#!/usr/bin/env python3

import matplotlib.pyplot as plt

def read_data_from_txt(filename):
    data = []
    with open(filename, 'r') as file:
        next(file)  # Pular cabeçalho
        for line in file:
            parts = line.split()
            if len(parts) == 3:
                input1, input2, exec_time = int(parts[0]), int(parts[1]), float(parts[2])
                data.append((input1, input2, exec_time))
    return data

def plot_execution_time(data, output_filename="execution_time_plot.png"):
    plt.figure(figsize=(8, 6))
    plt.plot([f"{d[0]}x{d[1]}" for d in data], [d[2] for d in data], marker='o', linestyle='-', color='b')
    plt.xlabel("Input Size (NxM)")
    plt.ylabel("Execution Time (s)")
    plt.title("Execution Time vs. Input Size")
    plt.grid()
    plt.savefig(output_filename, dpi=300)
    plt.show()

if __name__ == "__main__":
    filename = "execution_times.txt"  # Nome do arquivo de entrada
    data = read_data_from_txt(filename)
    plot_execution_time(data)
