CFLAGS=-Wall -pedantic -O3
codex.um: codex.out
	python fix_codex.py
codex.out: codex.umz um Makefile
	(echo '(\b.bb)(\v.vv)06FHPVboundvarHRAk';echo p) | ./um codex.umz > codex.out
um_dbg: um.c
	${CC} ${CFLAGS} -Ddebug_output um.c -o um_dbg
