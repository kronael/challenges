.PHONY: all test clean
CC ?= gcc
all: test
test: main
	./main
main: main.c
	$(CC) -std=c11 -O2 -pthread -Wall -Wextra -o main main.c
clean:
	rm -f main
