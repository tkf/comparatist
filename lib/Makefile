all: $(patsubst %.c, %.so, $(wildcard *.c))

%.so: %.c
	gcc -Wall -shared -O3 -march=native -ffast-math -std=c11 -fPIC -lm $< -o $@
