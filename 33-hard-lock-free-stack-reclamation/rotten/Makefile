.PHONY: all test stress clean
CC ?= gcc
all: test
test: main
	./main
stress: main
	./main stress
main: main.c
	$(CC) -std=c11 -O2 -pthread -Wall -Wextra -o main main.c
clean:
	rm -f main
