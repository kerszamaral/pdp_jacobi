#!/usr/bin/env python3

import subprocess
import time
import csv
import matplotlib.pyplot as plt

# Definir os pares de entrada
# linear -> resolução
input_pairs = [(512, 1000), (1024, 1000), (1024, 2000), (1024, 10000)]

# Nome do arquivo CSV
csv_filename = "execution_times.csv"

# Abrir arquivo CSV para escrita
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Input1", "Input2", "Execution Time (s)"])
    
    for pair in input_pairs:
        print(f"Running with input: {pair[0]} {pair[1]}")
        
        process = subprocess.Popen("./laplace_seq", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        start_time = time.time()
        process.communicate(input=f"{pair[0]} {pair[1]}\n")
        end_time = time.time()
        
        exec_time = end_time - start_time
        print(f"Execution time: {exec_time:.4f} seconds")
        
        writer.writerow([pair[0], pair[1], exec_time])

# Ler dados do CSV para plotagem
data = []
with open(csv_filename, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Pular cabeçalho
    for row in reader:
        data.append((int(row[0]), int(row[1]), float(row[2])))

# Criar gráfico
plt.figure(figsize=(8, 6))
plt.plot([f"{d[0]}x{d[1]}" for d in data], [d[2] for d in data], marker='o', linestyle='-', color='b')
plt.xlabel("Input Size (NxM)")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs. Input Size")
plt.grid()
plt.savefig("execution_time_plot.png", dpi=300)
plt.show()
