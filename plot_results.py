#!/usr/bin/env python3
import matplotlib.pyplot as plt

def read_data_from_txt(filename):
    data = []
    with open(filename, 'r') as file:
        next(file)  # Pular cabeçalho
        for line in file:
            parts = line.split()
            input1, input2, exec_time = int(parts[0]), int(parts[1]), float(parts[2])
            rest = parts[3:]
            exec_threads = [(exec_time, 1)]
            jmp = 2
            if input2 == 10000:
                jmp = 4
            for exec, threads in zip(rest[::jmp], rest[1::jmp]):
                exec_threads.append((float(exec), int(threads)))
            data.append((input1, input2, exec_threads))
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
def plot_threads(data: list[tuple[int, int, list[tuple[float, int]]]], output_filename="threads.png") -> None:
    plt.figure(figsize=(8, 6))
    for d in data:
        input_size = f"{d[0]}x{d[1]}"
        exec_times = [et[0] for et in d[2]]
        threads = [str(et[1]) for et in d[2]]
        plt.plot(threads, exec_times, marker='o', linestyle='-', label=input_size)
    
    thread_nums = [thread for _, thread in data[0][2]]
    # plt.yscale('log')
    plt.xticks(range(len(thread_nums)), thread_nums)
    plt.xlabel("Number of Threads")
    plt.ylabel("Execution Time (s)")
    plt.title("Execution Time vs. Number of Threads")
    plt.legend()
    plt.grid()
    plt.savefig(output_filename, dpi=300)
    plt.show()

#plotar por resolução ((512,1000),(512,2000),...)
def plot_resolution(data: list[tuple[int, int, list[tuple[float, int]]]], output_filename="resolution.png") -> None:
    plt.figure(figsize=(8, 6))
    
    thread_nums = [(i, thread) for i, (_, thread) in enumerate(data[0][2])]
    
    for i, thread in thread_nums:
        exec_times = [d[2][i][0] for d in data]
        plt.plot([f"{d[0]}x{d[1]}" for d in data], exec_times, marker='o', linestyle='-', label=f"Threads: {thread}")
    
    plt.yscale('log')
    plt.xticks(rotation=60) 
    plt.xlabel("Resolution")
    plt.ylabel("Execution Time (s)")
    plt.title("Execution Time vs. Resolution")
    plt.legend()
    plt.grid()
    plt.savefig(output_filename, dpi=300)
    plt.show()

if __name__ == "__main__":
    filename = "execution_times.txt"  # Nome do arquivo de entrada
    data = read_data_from_txt(filename)
    # plot_execution_time(data)
    plot_threads(data)
    plot_resolution(data)
