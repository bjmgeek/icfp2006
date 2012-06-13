#!/bin/sh
socat exec:"./um_dbg codex.um",pty exec:"./adv.py -"
