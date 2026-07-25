// Checked allocation, and slurping stdin or a fixture file whole.

#ifndef HARNESS_H
#define HARNESS_H

#include <stdio.h>
#include <stdlib.h>

// Zero-sized requests still return a distinct pointer, so `free` is always safe
// and an empty array never aliases another one.
static inline void *xmalloc(size_t bytes) {
	void *p = malloc(bytes != 0 ? bytes : 1);
	if (p == NULL) {
		fprintf(stderr, "out of memory\n");
		exit(1);
	}
	return p;
}

static inline void *xcalloc(size_t count, size_t size) {
	void *p = calloc(count != 0 ? count : 1, size);
	if (p == NULL) {
		fprintf(stderr, "out of memory\n");
		exit(1);
	}
	return p;
}

static inline void *xrealloc(void *ptr, size_t bytes) {
	void *p = realloc(ptr, bytes != 0 ? bytes : 1);
	if (p == NULL) {
		fprintf(stderr, "out of memory\n");
		exit(1);
	}
	return p;
}

static inline char *read_stream(FILE *f) {
	size_t cap = 1 << 16, len = 0;
	char *buf = (char *)malloc(cap);
	if (buf == NULL) {
		fprintf(stderr, "out of memory\n");
		exit(1);
	}
	for (;;) {
		if (len + 1 >= cap) {
			cap *= 2;
			char *grown = (char *)realloc(buf, cap);
			if (grown == NULL) {
				free(buf);
				fprintf(stderr, "out of memory\n");
				exit(1);
			}
			buf = grown;
		}
		size_t got = fread(buf + len, 1, cap - len - 1, f);
		if (got == 0) {
			break;
		}
		len += got;
	}
	buf[len] = '\0';
	return buf;
}

static inline char *read_path(const char *path) {
	FILE *f = fopen(path, "rb");
	if (f == NULL) {
		perror(path);
		exit(1);
	}
	char *buf = read_stream(f);
	fclose(f);
	return buf;
}

#endif
