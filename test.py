import sys


filename = "test.out"
if len(sys.argv) > 1:
    filename = sys.argv[1]


syscall_file = open(filename, "r")


for line in syscall_file:
    instrs = line.split("|")
    print instrs[-2]
