// Shared fixture runner: runs every small case through solve() and compares what
// answer_print() writes against the matching .out file.

#include "harness.h"
#include "json.h"
#include "solution.h"

#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CASES_DIR "../cases"
#define SHOWN 160

static int small_case(const struct dirent *e) {
	size_t len = strlen(e->d_name);
	if (len < 4 || strcmp(e->d_name + len - 3, ".in") != 0) {
		return 0;
	}
	return strstr(e->d_name, "_large_") == NULL;
}

static size_t trim(char *s) {
	size_t len = strlen(s);
	while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r' || s[len - 1] == ' ' ||
	                   s[len - 1] == '\t')) {
		len--;
	}
	s[len] = '\0';
	return len;
}

static void show(const char *label, const char *text, size_t len) {
	if (len > SHOWN) {
		printf("       %s: %.*s... (%zu bytes)\n", label, SHOWN, text, len);
	} else {
		printf("       %s: %s\n", label, text);
	}
}

int main(void) {
	struct dirent **ents;
	int n = scandir(CASES_DIR, &ents, small_case, alphasort);
	if (n < 0) {
		perror(CASES_DIR);
		return 1;
	}
	if (n == 0) {
		fprintf(stderr, "no small cases found in %s\n", CASES_DIR);
		return 1;
	}

	int failed = 0;
	for (int k = 0; k < n; k++) {
		char in_path[512], out_path[512];
		int plen = snprintf(in_path, sizeof in_path, "%s/%s", CASES_DIR, ents[k]->d_name);
		if (plen < 0 || (size_t)plen >= sizeof in_path) {
			fprintf(stderr, "case path too long: %s\n", ents[k]->d_name);
			return 1;
		}
		memcpy(out_path, in_path, (size_t)plen - 2);
		memcpy(out_path + plen - 2, "out", 4);

		char *src = read_path(in_path);
		JsonValue root;
		json_parse(src, &root);

		Input in;
		input_parse(&root, &in);
		Answer ans = solve(&in);

		char *got = NULL;
		size_t got_len = 0;
		FILE *mem = open_memstream(&got, &got_len);
		if (mem == NULL) {
			perror("open_memstream");
			return 1;
		}
		answer_print(mem, &ans);
		fclose(mem);

		char *want = read_path(out_path);
		size_t want_len = strlen(want);

		// Byte-exact, matching `make bench`'s `cmp -s`; trailing whitespace is a
		// real difference. `trim` is only for readable diagnostics on a mismatch.
		if (got_len == want_len && memcmp(got, want, got_len) == 0) {
			printf("PASS  %s\n", ents[k]->d_name);
		} else {
			printf("FAIL  %s\n", ents[k]->d_name);
			show("want", want, trim(want));
			show("got ", got, trim(got));
			failed++;
		}

		free(want);
		free(got);
		answer_free(&ans);
		input_free(&in);
		json_free(&root);
		free(src);
		free(ents[k]);
	}
	free(ents);

	if (failed > 0) {
		printf("%d of %d cases FAILED\n", failed, n);
		return 1;
	}
	printf("%d cases passed\n", n);
	return 0;
}
