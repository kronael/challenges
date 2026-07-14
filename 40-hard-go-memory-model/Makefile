GO ?= go
GOFMT ?= gofmt
QUIZ ?= 02_channel_ordering.go
BENCH ?= ./quizzes/10_false_sharing_bench_test.go
RACY := 01_unsynchronised_write.go
RACE_OK := 02_channel_ordering.go 03_waitgroup_fence.go 05_goroutine_start.go 06_once_init.go 07_mutex_interleave.go 08_close_channel.go 09_select_ordering.go
ALL_QUIZZES := $(RACY) $(RACE_OK) 04_atomic_vs_plain.go 10_false_sharing_bench_test.go

.PHONY: all test compile run race bench fmt help

all: test

test:
	@for quiz in $(ALL_QUIZZES); do \
		echo "compile $$quiz"; \
		$(GO) test ./quizzes/$$quiz >/dev/null || exit $$?; \
	done
	@for quiz in $(RACE_OK); do \
		echo "race $$quiz"; \
		$(GO) run -race ./quizzes/$$quiz >/dev/null || exit $$?; \
	done
	@for quiz in $(RACY); do \
		echo "expected race $$quiz"; \
		if $(GO) run -race ./quizzes/$$quiz >/tmp/go-memory-model-race.log 2>&1; then \
			echo "expected race detector failure for $$quiz"; \
			exit 1; \
		fi; \
		grep -q "DATA RACE" /tmp/go-memory-model-race.log || exit $$?; \
	done
	@$(MAKE) bench >/dev/null

compile:
	$(GO) test ./quizzes/$(QUIZ)

run:
	$(GO) run ./quizzes/$(QUIZ)

race:
	$(GO) run -race ./quizzes/$(QUIZ)

bench:
	$(GO) test -bench=. -benchmem -cpu=2,4,8 $(BENCH)

fmt:
	$(GOFMT) -w quizzes/*.go

help:
	@echo "make test                  compile all quizzes, race-run runnable quizzes, run quiz 10 bench"
	@echo "make compile QUIZ=name.go  compile one quiz file"
	@echo "make run QUIZ=name.go      run one quiz file"
	@echo "make race QUIZ=name.go     run one quiz file with the race detector"
	@echo "make bench                 run quiz 10 benchmark"
