#!/bin/bash

python pred_syscalls.py $1 5
python pred_syscalls.py $1 10
python pred_syscalls.py $1 20
python pred_syscalls.py $1 50
python pred_syscalls.py $1 100
python pred_syscalls.py $1 200
python pred_syscalls.py $1 999
