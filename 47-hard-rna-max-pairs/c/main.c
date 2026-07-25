#include "harness.h"
#include "json.h"
#include "solution.h"

#include <stdio.h>
#include <stdlib.h>

int main(void) {
	char *src = read_stream(stdin);
	JsonValue root;
	json_parse(src, &root);

	Input in;
	input_parse(&root, &in);
	Answer ans = solve(&in);
	answer_print(stdout, &ans);

	answer_free(&ans);
	input_free(&in);
	json_free(&root);
	free(src);
	return 0;
}
