#!/usr/bin/env python3
import matplotlib.pyplot as plt

def read_data_from_txt(filename) -> dict[tuple[int, int], list[tuple[float, int]]]:
    data: dict[tuple[int, int], list[tuple[float, int]]] = {}
    with open(filename, 'r') as file:
        next(file)  # Pular cabeçalho
        for line in file:
            parts = line.split()
            input1, input2, per_usage = int(parts[0]), int(parts[1]), float(parts[2])
            rest = parts[3:]
            usage_threads = [(per_usage, 1)]
            jmp = 2
            offset = 0
            print(f"input1: {input1}, input2: {input2}, exec_time: {per_usage}")
            for usage, threads in zip(rest[offset::jmp], rest[offset+1::jmp]):
                usage_threads.append((float(usage), int(threads)))
            data[(input1, input2)] = usage_threads
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
    
    for idx, resolution in enumerate(resolutions):
        ax = axs.flat[idx]
        for lbls, dat in data.items():
            if lbls[0] != resolution:
                continue
            input_size = f"{depth_name} {lbls[1]}"
            exec_times = [et[0] for et in dat]
            threads = [str(et[1]) for et in dat]
            ax.plot(threads, exec_times, marker='o', linestyle='-', label=input_size)
    
    thread_nums = [str(thread) for _, thread in list(data.values())[0]]
    
    # max_y = max([max([et[0] for et in dat]) for dat in data.values()])
    # max_y = 100
    max_y = 1
    for ax, resolution in zip(axs.flat, resolutions):
        ax.set_xticks(range(len(thread_nums)))
        ax.set_xticklabels(thread_nums)
        ax.set_xlabel("Number of Threads")
        ax.set_ylabel("Effective Logical Core Utilization (%)")
        ax.set_title(f"Resolution: {resolution}")
        ax.legend(loc='upper right')
        ax.set_ylim(0, max_y)
        ax.set_xlim(-1, len(thread_nums))
        ax.grid()
        
    fig.tight_layout()
    plt.suptitle("Effective Logical Core Utilization vs. Number of Threads", fontsize=16)
    plt.subplots_adjust(top=0.93)  # Ajuste para o título
    # plt.yscale('log')
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
    plt.ylabel("Effective Logical Core Utilization (%)")
    plt.title("Effective Logical Core Utilization vs. Resolution")
    plt.legend()
    plt.grid()
    plt.savefig(output_filename, dpi=300)
    plt.show()

if __name__ == "__main__":
    filename = "efficiency.txt"  # Nome do arquivo de entrada
    data = read_data_from_txt(filename)
    # plot_execution_time(data)
    plot_threads(data, output_filename="threads_eff.png")
    plot_resolution(data, output_filename="resolution_eff.png")
