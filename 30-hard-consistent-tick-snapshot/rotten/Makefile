.PHONY: all test stress clean
all: test
test: main
	./main
stress: main
	./main stress
main: main.c
	cc -std=c11 -O2 -pthread -Wall -Wextra -o main main.c
clean:
	rm -f main
