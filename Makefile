CC=gcc
FLAGS=-O3 -Wall -Wextra -Wpedantic
EXEC=laplace_seq laplace_mp

all: $(EXEC)

gprof: FLAGS += -pg
gprof: $(EXEC)

laplace_seq: laplace_seq.c
	$(CC) $(FLAGS) laplace_seq.c -o laplace_seq

laplace_mp: FLAGS += -fopenmp
laplace_mp: laplace_mp.c
	$(CC) $(FLAGS) laplace_mp.c -o laplace_mp

check: $(EXEC)
	time ./$(EXEC) | ./plot_heatmap.py

run: $(EXEC)
	./get_results.sh

plot: $(EXEC)
	python3 ./plot_results.py

clean:
	rm -f laplace_seq *.o *.png laplace_mp *.txt
