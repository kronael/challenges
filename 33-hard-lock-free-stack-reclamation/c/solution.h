#ifndef SOLUTION_H
#define SOLUTION_H

#include <stdatomic.h>
#include <stdbool.h>
#include <stdint.h>

typedef struct Node Node;

struct Node {
	uint64_t value;
	_Atomic(Node *) next;
};

typedef struct {
	_Atomic(Node *) head;
} Stack;

void stack_init(Stack *s);

// Release everything the stack still owns. No thread may touch s afterwards.
void stack_destroy(Stack *s);

void stack_push(Stack *s, uint64_t value);

// Returns false when the stack is empty.
bool stack_pop(Stack *s, uint64_t *out);

// Nodes must be obtained and released only through these two — the stress test
// balances the counts to catch leaks and double frees.
Node *node_alloc(uint64_t value);
void node_free(Node *n);
uint64_t node_allocs(void);
uint64_t node_frees(void);

#endif
