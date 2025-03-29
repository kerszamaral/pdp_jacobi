CC=gcc
FLAGS=-O3 
EXEC=laplace_seq

all: $(EXEC)

$(EXEC):
	$(CC) $(FLAGS) $(EXEC).c   -c -o $(EXEC).o
	$(CC) $(FLAGS) $(EXEC).o -o $(EXEC)

check: $(EXEC)
	time ./$(EXEC) | ./plot_heatmap.py

run: $(EXEC)
	./get_results.sh

plot: $(EXEC)
	python3 ./plot_results.py

clean:
	rm -f laplace_seq *.o *.png *.txt
