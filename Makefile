# Project-wide checks across every NN-slug challenge.
#
#   make test     every golden AND rotten passes its case suite (make test in each)
#   make golden   every golden passes test AND bench (fast — must NOT time out)
#   make rotten   every rotten passes test BUT times out on bench (the trap)
#   make all      test
#
# golden/ is the optimised reference; rotten/ is the naive trap that is correct on
# the small cases but too slow on the large ones. These targets assert exactly that
# contract holds across the whole repo.
SHELL := /bin/bash

# io challenges only: golden/rotten that ship a python case-suite. sys challenges
# (02-07) have C golden/rotten with no cases — their rotten is *meant* to fail its
# stress test, so they are verified separately via `make sys`, never in `test`.
GOLDEN := $(sort $(dir $(wildcard [0-9][0-9]-*/golden/test_solution.py)))
ROTTEN := $(sort $(dir $(wildcard [0-9][0-9]-*/rotten/test_solution.py)))
SYS    := $(sort $(dir $(wildcard [0-9][0-9]-*/golden/main.c)))

GOLDEN_TIMEOUT ?= 15   # generous: golden must finish well within this
ROTTEN_TIMEOUT ?= 5    # short: the naive trap must blow past this

.PHONY: all test golden rotten sys help

all: test

test:
	@fail=0; \
	for d in $(GOLDEN) $(ROTTEN); do \
	  printf "test  %-34s " "$$d"; \
	  if (cd $$d && make test) >/tmp/ptest.log 2>&1; then echo "ok"; \
	  else echo "FAIL"; sed 's/^/    /' /tmp/ptest.log | tail -3; fail=1; fi; \
	done; \
	[ $$fail -eq 0 ] && echo "all golden+rotten case suites pass" || { echo "FAILURES above"; exit 1; }

golden:
	@fail=0; \
	for d in $(GOLDEN); do \
	  printf "golden %-33s " "$$d"; \
	  if ! (cd $$d && make test) >/tmp/pgold.log 2>&1; then echo "TEST FAIL"; fail=1; continue; fi; \
	  if grep -q '^bench:' $$d/Makefile; then \
	    if (cd $$d && make bench TIMEOUT=$(GOLDEN_TIMEOUT)) >/tmp/pgold-bench.log 2>&1; then \
	      if grep -q TIMEOUT /tmp/pgold-bench.log; then \
	        echo "BENCH TIMEOUT — golden too slow!"; fail=1; \
	      else echo "ok (test + bench)"; fi; \
	    else \
	      if grep -q TIMEOUT /tmp/pgold-bench.log; then echo "BENCH TIMEOUT — golden too slow!"; \
	      else echo "BENCH FAIL"; sed 's/^/    /' /tmp/pgold-bench.log | tail -3; fi; \
	      fail=1; \
	    fi; \
	  else echo "ok (test; no bench)"; fi; \
	done; \
	[ $$fail -eq 0 ] && echo "all golden pass test and bench" || { echo "FAILURES above"; exit 1; }

rotten:
	@fail=0; \
	for d in $(ROTTEN); do \
	  printf "rotten %-33s " "$$d"; \
	  if ! (cd $$d && make test) >/tmp/prot.log 2>&1; then \
	    echo "TEST FAIL — rotten must pass small cases"; sed 's/^/    /' /tmp/prot.log | tail -3; fail=1; continue; \
	  fi; \
	  if (cd $$d && make bench TIMEOUT=$(ROTTEN_TIMEOUT)) 2>/dev/null | grep -q TIMEOUT; then \
	    echo "ok (passes test, times out on bench)"; \
	  else echo "NO TIMEOUT — rotten is not slow enough to be a trap"; fail=1; fi; \
	done; \
	[ $$fail -eq 0 ] && echo "all rotten pass test and time out on bench" || { echo "FAILURES above"; exit 1; }

sys:
	@fail=0; \
	for d in $(SYS); do \
	  printf "sys    %-33s " "$$d"; \
	  if (cd $$d && make test) >/tmp/psys.log 2>&1; then echo "ok (stress passes)"; \
	  else echo "FAIL"; sed 's/^/    /' /tmp/psys.log | tail -3; fail=1; fi; \
	done; \
	[ $$fail -eq 0 ] && echo "all sys golden stress tests pass" || { echo "FAILURES above"; exit 1; }

help:
	@echo "test    — every io golden + rotten passes its case suite"
	@echo "golden  — every io golden passes test AND bench (must not time out)"
	@echo "rotten  — every io rotten passes test BUT times out on bench (the trap)"
	@echo "sys     — every sys (02-07) golden C stress test passes"
	@echo "Override GOLDEN_TIMEOUT (def 15s) / ROTTEN_TIMEOUT (def 5s)."
