#!/usr/bin/env python3
import matplotlib.pyplot as plt
from math import ceil

def read_data_from_txt(filename) -> dict[tuple[int, int], list[tuple[float, int]]]:
    data: dict[tuple[int, int], list[tuple[float, int]]] = {}
    with open(filename, 'r') as file:
        next(file)  # Pular cabeçalho
        for line in file:
            parts = line.split()
            input1, input2, exec_time = int(parts[0]), int(parts[1]), float(parts[2])
            rest = parts[3:]
            first_exec = exec_time
            exec_threads = [(first_exec/exec_time, 1)]
            jmp = 2
            offset = 0
            if input2 == 10000:
                jmp = 4
                offset = 2
            print(f"input1: {input1}, input2: {input2}, exec_time: {exec_time}")
            for exec, threads in zip(rest[offset::jmp], rest[offset+1::jmp]):
                exec_threads.append((first_exec/float(exec), int(threads)))
            data[(input1, input2)] = exec_threads
    return data

def plot_execution_time(data, output_filename="execution_time_plot.png"):
    for d in data:
        print(d)

    #plt.figure(figsize=(8, 6))
    # plt.plot([f"{d[0]}x{d[1]}" for d in data], [d[2] for d in data], marker='o', linestyle='-', color='b')
    #plt.xlabel("Input Size (NxM)")
    #plt.ylabel("Execution Time (s)")
    #plt.title("Execution Time vs. Input Size")
    #plt.grid()
    #plt.savefig(output_filename, dpi=300)
    #plt.show()

#plotar por thread (1,2,4,...)
def plot_threads(data: dict[tuple[int, int], list[tuple[float, int]]], output_filename="threads.png", depth_name="Depth") -> None:
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))
    
    resolutions = []
    for resolution in data.keys():
        resolutions.append(resolution[0])
    resolutions = list(set(resolutions))
    resolutions.sort()
    
    ticks_per_resolution = {}
    for idx, resolution in enumerate(resolutions):
        all_ticks = []
        ax = axs.flat[idx]
        for lbls, dat in data.items():
            if lbls[0] != resolution:
                continue
            input_size = f"{depth_name} {lbls[1]}x{lbls[1]}"
            exec_times = [et[0] for et in dat]
            threads = [str(et[1]) for et in dat]
            all_ticks.extend(exec_times)
            ax.plot(threads, exec_times, marker='o', linestyle='-', label=input_size)
        ideals = [str(et[1]) for et in data[list(data.keys())[0]]]
        all_ticks.extend([float(ideal) for ideal in ideals])
        all_ticks = list(set(all_ticks))
        all_ticks.sort()
        ticks_per_resolution[resolution] = all_ticks
        ax.plot(ideals, [float(ideal) for ideal in ideals], marker='o', linestyle='-', label="Ideal", color='black', visible=True)

    thread_nums = [str(thread) for _, thread in list(data.values())[0]]
    max_speedup = max(max([max([et[0] for et in dat]) for dat in data.values()]), float(max([str(et[1]) for et in data[list(data.keys())[0]]])))
    for ax, resolution in zip(axs.flat, resolutions):
        ax.set_xticks(range(len(thread_nums)))
        ax.set_xticklabels(thread_nums)
        ax.set_xlabel("Number of Threads")
        ax.set_ylabel("Speedup")
        ax.set_title(f"Resolution: {resolution}")
        ax.legend(loc='upper left')
        # ax.set_ylim(0, ceil(max_speedup))
        ax.set_xlim(-1, len(thread_nums))
        ax.set_yscale('log', base=10)
        # ax.grid(which="minor")
        
    fig.tight_layout()
    plt.suptitle("Speedup vs. Number of Threads", fontsize=16)
    plt.subplots_adjust(top=0.93)  # Ajuste para o título
    plt.savefig(output_filename, dpi=300)
    plt.show()

#plotar por resolução ((512,1000),(512,2000),...)
def plot_resolution(data: dict[tuple[int, int], list[tuple[float, int]]], output_filename="resolution.png") -> None:
    plt.figure(figsize=(8, 6))
    
    thread_nums = [(i, thread) for i, (_, thread) in enumerate(list(data.values())[0])]
    
    for i, thread in thread_nums:
        exec_times = [d[i][0] for d in data.values()]
        plt.plot([f"{d[0]}x{d[1]}" for d in data.keys()], exec_times, marker='o', linestyle='-', label=f"Threads: {thread}")
    
    # plt.yscale('log')
    plt.xticks(rotation=60) 
    plt.xlabel("Resolution")
    plt.ylabel("Speedup")
    plt.title("Speedup vs. Resolution")
    plt.legend()
    plt.grid()
    plt.savefig(output_filename, dpi=300)
    plt.show()

if __name__ == "__main__":
    filename = "execution_times.txt"  # Nome do arquivo de entrada
    data = read_data_from_txt(filename)
    data
    # plot_execution_time(data)
    plot_threads(data)
    plot_resolution(data)
