CFLAGS=-Wall -pedantic -O3 -funroll-loops
codex.um: codex.out
	python fix_codex.py
codex.out: codex.umz um Makefile
	(echo '(\b.bb)(\v.vv)06FHPVboundvarHRAk';echo p) | ./um codex.umz > codex.out
