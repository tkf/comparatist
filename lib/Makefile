all: $(patsubst %.c, %.so, $(wildcard *.c))

libcomparatist_oup.so: libcomparatist_oup.c
	gcc -Wall -shared -O3 -march=native -ffast-math -std=c11 -fPIC $< -lm -lgsl -lgslcblas -o $@

%.so: %.c
	gcc -Wall -shared -O3 -march=native -ffast-math -std=c11 -fPIC -lm $< -o $@
