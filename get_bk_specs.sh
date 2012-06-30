for model in 000 010 020 030 040 050 100 200 300 400 500; do (echo bbarker;echo plinko;echo bk_specs; echo 500)|./umix |fgrep -e '->' |grep -v '*' > 500.spec ; done
