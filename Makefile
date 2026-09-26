# Repo-wide checks; `make help` lists them. golden/ is the fast reference and
# passes every level. rotten/ is the naive control: correct on the small cases,
# but it fails the next level.
SHELL := /bin/bash

# io and api goldens with a python suite, plus the golden beside each io
# rotten, which is C when the challenge has the vec level. sys (29-34) golden
# and rotten are C with no cases.
ROTTEN := $(sort $(dir $(wildcard [0-9][0-9]-*/rotten/test_solution.py)))
GOLDEN := $(sort $(dir $(wildcard [0-9][0-9]-*/golden/test_solution.py)) \
	$(ROTTEN:rotten/=golden/))
SYS    := $(sort $(dir $(wildcard [0-9][0-9]-*/golden/main.c)))
SYS_ROTTEN := $(sort $(dir $(wildcard [0-9][0-9]-*/rotten/main.c)))
# vec level: every golden must grade vectorized, and 66-68's rotten scalar.
VEC    := $(sort $(dir $(shell grep -l 'shared/vec.mk' \
	[0-9][0-9]-*/golden/Makefile [0-9][0-9]-*/rotten/Makefile 2>/dev/null)))
VEC_CCS := cc $(if $(shell command -v clang 2>/dev/null),clang)
CLEAN := $(sort \
	$(dir $(wildcard [0-9][0-9]-*/c/Makefile)) \
	$(dir $(wildcard [0-9][0-9]-*/go/Makefile)) \
	$(dir $(wildcard [0-9][0-9]-*/rust/Makefile)) \
	$(SYS) $(SYS_ROTTEN) $(VEC) \
	template/c/ template/go/ template/rust/)

GOLDEN_TIMEOUT ?= 15   # generous: golden must finish well within this
ROTTEN_TIMEOUT ?= 5    # short: the naive trap must blow past this

.PHONY: all test cases golden rotten sys sys-rotten vec clean help

all: test

cases:
	python3 scripts/large_cases.py --check

test:
	cd scripts && python3 -X dev -W error -m unittest discover -p 'test_*.py'
	@fail=0; \
	for d in $(sort $(GOLDEN) $(ROTTEN) $(VEC)); do \
	  printf "test  %-34s " "$$d"; \
	  if out=$$(cd $$d && make test 2>&1); then echo "ok"; \
	  else echo "FAIL"; echo "$$out" | tail -3 | sed 's/^/    /'; fail=1; fi; \
	done; \
	[ $$fail -eq 0 ] && echo "all golden+rotten case suites pass" || { echo "FAILURES above"; exit 1; }

golden: cases
	@fail=0; \
	for d in $(GOLDEN); do \
	  printf "golden %-33s " "$$d"; \
	  if ! (cd $$d && make test) >/dev/null 2>&1; then echo "TEST FAIL"; fail=1; \
	  elif ! $(MAKE) -n -C $$d bench >/dev/null 2>&1; then echo "ok (test; no bench)"; \
	  elif out=$$(cd $$d && make bench TIMEOUT=$(GOLDEN_TIMEOUT) 2>&1); then echo "ok (test + bench)"; \
	  elif grep -q 'TIMEOUT (' <<<"$$out"; then echo "BENCH TIMEOUT — golden too slow!"; fail=1; \
	  else echo "BENCH FAIL"; echo "$$out" | tail -3 | sed 's/^/    /'; fail=1; fi; \
	done; \
	[ $$fail -eq 0 ] && echo "all golden pass test and bench" || { echo "FAILURES above"; exit 1; }

rotten: cases
	@fail=0; \
	for d in $(ROTTEN); do \
	  printf "rotten %-33s " "$$d"; \
	  if ! out=$$(cd $$d && make test 2>&1); then \
	    echo "TEST FAIL — rotten must pass small cases"; echo "$$out" | tail -3 | sed 's/^/    /'; fail=1; continue; \
	  fi; \
	  echo "small ok"; \
	  out=$$(python3 scripts/bench.py --workdir "$$d" --timeout "$(ROTTEN_TIMEOUT)" \
	      --expect-timeout -- uv run python main.py 2>&1) || fail=1; \
	  echo "$$out" | sed 's/^/       /'; \
	done; \
	[ $$fail -eq 0 ] && echo "all rotten pass small tests and every large case times out" || { echo "FAILURES above"; exit 1; }

sys:
	@fail=0; \
	for d in $(SYS); do \
	  printf "sys    %-33s " "$$d"; \
	  if out=$$(cd $$d && make test 2>&1); then echo "ok (stress passes)"; \
	  else echo "FAIL"; echo "$$out" | tail -3 | sed 's/^/    /'; fail=1; fi; \
	done; \
	[ $$fail -eq 0 ] && echo "all sys golden stress tests pass" || { echo "FAILURES above"; exit 1; }

sys-rotten:
	@fail=0; \
	for d in $(SYS_ROTTEN); do \
	  printf "sysbad %-33s " "$$d"; \
	  if ! out=$$(cd $$d && make test 2>&1); then \
	    echo "SANITY FAIL"; echo "$$out" | tail -3 | sed 's/^/    /'; fail=1; continue; \
	  fi; \
	  out=$$(cd $$d && timeout -k 2 5 ./main stress 2>&1); code=$$?; \
	  if [ $$code -eq 1 ]; then echo "ok (sanity passes; stress detects the defect)"; \
	  elif [ $$code -eq 0 ]; then echo "STRESS PASSED — defect not exposed"; fail=1; \
	  elif [ $$code -eq 124 ]; then echo "STRESS HUNG"; fail=1; \
	  else echo "STRESS CRASHED (exit $$code) — not a controlled detection"; echo "$$out" | tail -3 | sed 's/^/    /'; fail=1; fi; \
	done; \
	[ $$fail -eq 0 ] && echo "all sys rotten controls expose their defect" || { echo "FAILURES above"; exit 1; }

vec:
	@fail=0; \
	for cc in $(VEC_CCS); do \
	  for d in $(VEC); do \
	    printf "vec    %-6s %-40s " "$$cc" "$$d"; \
	    if out=$$(cd $$d && $(MAKE) -s --no-print-directory clean && \
	        $(MAKE) -s --no-print-directory vec CC=$$cc 2>&1); then echo "ok"; \
	    else echo "FAIL"; fail=1; fi; \
	    echo "$$out" | sed 's/^/    /'; \
	  done; \
	done; \
	for d in $(VEC); do $(MAKE) -s --no-print-directory -C $$d clean; done; \
	[ $$fail -eq 0 ] && echo "every vec golden vectorizes and every vec rotten stays scalar" || { echo "FAILURES above"; exit 1; }

clean:
	@for d in $(CLEAN); do \
	  $(MAKE) --no-print-directory -C "$$d" clean || exit $$?; \
	done

help:
	@echo "test    — script tests; every golden + rotten passes its case suite"
	@echo "cases   — verify every seeded large-case recipe is reproducible"
	@echo "golden  — every io golden passes test AND generated bench cases"
	@echo "rotten  — every io rotten passes small tests and generated cases time out"
	@echo "sys     — every sys (29-34) golden C stress test passes"
	@echo "sys-rotten — every sys rotten passes sanity and fails controlled stress"
	@echo "vec     — every vec golden vectorizes and 66-68's rotten stays scalar, under cc, then clang if on PATH"
	@echo "clean   — remove compiled artifacts from every challenge"
	@echo "Override GOLDEN_TIMEOUT (def 15s) / ROTTEN_TIMEOUT (def 5s)."
