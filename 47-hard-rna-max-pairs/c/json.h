// Minimal JSON reader for challenge input.
//
// json_parse() rewrites the buffer it is handed — strings are unescaped in
// place — so that buffer must outlive every JsonValue read from it.

#ifndef JSON_H
#define JSON_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { JSON_NULL, JSON_BOOL, JSON_NUM, JSON_STR, JSON_ARR, JSON_OBJ } JsonType;

typedef struct JsonValue JsonValue;

struct JsonValue {
	JsonType type;
	union {
		int boolean;
		struct {
			double d;
			long long i;
			int is_int;
		} num;
		const char *str;
		struct {
			JsonValue *item;
			size_t len;
		} arr;
		struct {
			const char **key;
			JsonValue *val;
			size_t len;
		} obj;
	} as;
};

typedef struct {
	char *p;
} JsonParser;

static inline _Noreturn void json_die(const char *msg) {
	fprintf(stderr, "json: %s\n", msg);
	exit(1);
}

static inline void *json_alloc(void *ptr, size_t bytes) {
	void *fresh = realloc(ptr, bytes);
	if (fresh == NULL) {
		json_die("out of memory");
	}
	return fresh;
}

static inline void json_ws(JsonParser *ps) {
	while (*ps->p == ' ' || *ps->p == '\t' || *ps->p == '\n' || *ps->p == '\r') {
		ps->p++;
	}
}

static inline void json_expect(JsonParser *ps, char c) {
	if (*ps->p != c) {
		json_die("unexpected character");
	}
	ps->p++;
}

static inline void json_utf8(char **w, unsigned cp) {
	if (cp < 0x80) {
		*(*w)++ = (char)cp;
	} else if (cp < 0x800) {
		*(*w)++ = (char)(0xC0 | (cp >> 6));
		*(*w)++ = (char)(0x80 | (cp & 0x3F));
	} else if (cp < 0x10000) {
		*(*w)++ = (char)(0xE0 | (cp >> 12));
		*(*w)++ = (char)(0x80 | ((cp >> 6) & 0x3F));
		*(*w)++ = (char)(0x80 | (cp & 0x3F));
	} else {
		*(*w)++ = (char)(0xF0 | (cp >> 18));
		*(*w)++ = (char)(0x80 | ((cp >> 12) & 0x3F));
		*(*w)++ = (char)(0x80 | ((cp >> 6) & 0x3F));
		*(*w)++ = (char)(0x80 | (cp & 0x3F));
	}
}

static inline unsigned json_hex4(JsonParser *ps) {
	unsigned v = 0;
	for (int k = 0; k < 4; k++) {
		char c = *ps->p++;
		if (c >= '0' && c <= '9') {
			v = v * 16 + (unsigned)(c - '0');
		} else if (c >= 'a' && c <= 'f') {
			v = v * 16 + (unsigned)(c - 'a' + 10);
		} else if (c >= 'A' && c <= 'F') {
			v = v * 16 + (unsigned)(c - 'A' + 10);
		} else {
			json_die("bad \\u escape");
		}
	}
	return v;
}

// Unescaping never grows the text, so decoded bytes are written back over the
// opening quote and the source they came from.
static inline const char *json_string(JsonParser *ps) {
	json_expect(ps, '"');
	char *w = ps->p - 1;
	const char *start = w;
	while (*ps->p != '"') {
		if (*ps->p == '\0') {
			json_die("unterminated string");
		}
		if (*ps->p != '\\') {
			*w++ = *ps->p++;
			continue;
		}
		ps->p++;
		switch (*ps->p++) {
		case '"':
			*w++ = '"';
			break;
		case '\\':
			*w++ = '\\';
			break;
		case '/':
			*w++ = '/';
			break;
		case 'b':
			*w++ = '\b';
			break;
		case 'f':
			*w++ = '\f';
			break;
		case 'n':
			*w++ = '\n';
			break;
		case 'r':
			*w++ = '\r';
			break;
		case 't':
			*w++ = '\t';
			break;
		case 'u': {
			unsigned cp = json_hex4(ps);
			if (cp >= 0xD800 && cp <= 0xDBFF && ps->p[0] == '\\' && ps->p[1] == 'u') {
				ps->p += 2;
				unsigned lo = json_hex4(ps);
				cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00);
			}
			json_utf8(&w, cp);
			break;
		}
		default:
			json_die("bad escape");
		}
	}
	ps->p++;
	*w = '\0';
	return start;
}

static inline void json_number(JsonParser *ps, JsonValue *v) {
	const char *start = ps->p;
	int is_int = 1;
	if (*ps->p == '-' || *ps->p == '+') {
		ps->p++;
	}
	while (*ps->p >= '0' && *ps->p <= '9') {
		ps->p++;
	}
	if (*ps->p == '.') {
		is_int = 0;
		ps->p++;
		while (*ps->p >= '0' && *ps->p <= '9') {
			ps->p++;
		}
	}
	if (*ps->p == 'e' || *ps->p == 'E') {
		is_int = 0;
		ps->p++;
		if (*ps->p == '-' || *ps->p == '+') {
			ps->p++;
		}
		while (*ps->p >= '0' && *ps->p <= '9') {
			ps->p++;
		}
	}
	if (ps->p == start) {
		json_die("bad number");
	}
	v->type = JSON_NUM;
	v->as.num.is_int = is_int;
	if (is_int) {
		v->as.num.i = strtoll(start, NULL, 10);
		v->as.num.d = (double)v->as.num.i;
	} else {
		v->as.num.d = strtod(start, NULL);
		v->as.num.i = (long long)v->as.num.d;
	}
}

static inline void json_value(JsonParser *ps, JsonValue *v);

static inline void json_array(JsonParser *ps, JsonValue *v) {
	json_expect(ps, '[');
	JsonValue *item = NULL;
	size_t cap = 0, len = 0;
	json_ws(ps);
	if (*ps->p == ']') {
		ps->p++;
	} else {
		for (;;) {
			if (len == cap) {
				cap = cap ? cap * 2 : 8;
				item = (JsonValue *)json_alloc(item, cap * sizeof *item);
			}
			json_value(ps, &item[len++]);
			json_ws(ps);
			if (*ps->p == ',') {
				ps->p++;
				continue;
			}
			json_expect(ps, ']');
			break;
		}
	}
	v->type = JSON_ARR;
	v->as.arr.item = item;
	v->as.arr.len = len;
}

static inline void json_object(JsonParser *ps, JsonValue *v) {
	json_expect(ps, '{');
	const char **key = NULL;
	JsonValue *val = NULL;
	size_t cap = 0, len = 0;
	json_ws(ps);
	if (*ps->p == '}') {
		ps->p++;
	} else {
		for (;;) {
			if (len == cap) {
				cap = cap ? cap * 2 : 8;
				key = (const char **)json_alloc(key, cap * sizeof *key);
				val = (JsonValue *)json_alloc(val, cap * sizeof *val);
			}
			json_ws(ps);
			key[len] = json_string(ps);
			json_ws(ps);
			json_expect(ps, ':');
			json_value(ps, &val[len]);
			len++;
			json_ws(ps);
			if (*ps->p == ',') {
				ps->p++;
				continue;
			}
			json_expect(ps, '}');
			break;
		}
	}
	v->type = JSON_OBJ;
	v->as.obj.key = key;
	v->as.obj.val = val;
	v->as.obj.len = len;
}

static inline void json_value(JsonParser *ps, JsonValue *v) {
	json_ws(ps);
	switch (*ps->p) {
	case '{':
		json_object(ps, v);
		break;
	case '[':
		json_array(ps, v);
		break;
	case '"':
		v->type = JSON_STR;
		v->as.str = json_string(ps);
		break;
	case 't':
		if (strncmp(ps->p, "true", 4) != 0) {
			json_die("bad literal");
		}
		ps->p += 4;
		v->type = JSON_BOOL;
		v->as.boolean = 1;
		break;
	case 'f':
		if (strncmp(ps->p, "false", 5) != 0) {
			json_die("bad literal");
		}
		ps->p += 5;
		v->type = JSON_BOOL;
		v->as.boolean = 0;
		break;
	case 'n':
		if (strncmp(ps->p, "null", 4) != 0) {
			json_die("bad literal");
		}
		ps->p += 4;
		v->type = JSON_NULL;
		break;
	default:
		json_number(ps, v);
		break;
	}
}

static inline void json_parse(char *src, JsonValue *root) {
	JsonParser ps = { src };
	json_value(&ps, root);
	json_ws(&ps);
	if (*ps.p != '\0') {
		json_die("trailing content after value");
	}
}

static inline void json_free(JsonValue *v) {
	if (v == NULL) {
		return;
	}
	if (v->type == JSON_ARR) {
		for (size_t i = 0; i < v->as.arr.len; i++) {
			json_free(&v->as.arr.item[i]);
		}
		free(v->as.arr.item);
	} else if (v->type == JSON_OBJ) {
		for (size_t i = 0; i < v->as.obj.len; i++) {
			json_free(&v->as.obj.val[i]);
		}
		free(v->as.obj.key);
		free(v->as.obj.val);
	}
}

// NULL when the key is absent, so optional fields read naturally.
static inline const JsonValue *json_get(const JsonValue *v, const char *key) {
	if (v == NULL || v->type != JSON_OBJ) {
		json_die("expected an object");
	}
	for (size_t i = 0; i < v->as.obj.len; i++) {
		if (strcmp(v->as.obj.key[i], key) == 0) {
			return &v->as.obj.val[i];
		}
	}
	return NULL;
}

static inline size_t json_len(const JsonValue *v) {
	if (v == NULL) {
		return 0;
	}
	if (v->type == JSON_ARR) {
		return v->as.arr.len;
	}
	if (v->type == JSON_OBJ) {
		return v->as.obj.len;
	}
	return 0;
}

static inline const JsonValue *json_at(const JsonValue *v, size_t i) {
	if (v == NULL || v->type != JSON_ARR || i >= v->as.arr.len) {
		json_die("array index out of range");
	}
	return &v->as.arr.item[i];
}

static inline int json_is_null(const JsonValue *v) {
	return v == NULL || v->type == JSON_NULL;
}

static inline long long json_int(const JsonValue *v) {
	if (v == NULL || v->type != JSON_NUM) {
		json_die("expected a number");
	}
	return v->as.num.i;
}

static inline double json_num(const JsonValue *v) {
	if (v == NULL || v->type != JSON_NUM) {
		json_die("expected a number");
	}
	return v->as.num.d;
}

static inline const char *json_str(const JsonValue *v) {
	if (v == NULL || v->type != JSON_STR) {
		json_die("expected a string");
	}
	return v->as.str;
}

static inline int json_bool(const JsonValue *v) {
	if (v == NULL || v->type != JSON_BOOL) {
		json_die("expected a boolean");
	}
	return v->as.boolean;
}

#endif
