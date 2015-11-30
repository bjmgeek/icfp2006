CFLAGS=-Wall -pedantic -O3 -std=c99
MACHINE := $(shell uname -m)

ifeq ($(MACHINE), x86_64)
CFLAGS+= -m64
endif

codex.um: codex.out
	python fix_codex.py
codex.out: codex.umz um Makefile
	./um codex.umz < codex_pw > codex.out
um_dbg: um.c
	${CC} ${CFLAGS} -Ddebug_output um.c -o um_dbg
%: %.dump
	python hex2bin.py $<
clean:
	rm codex.um codex.out um
