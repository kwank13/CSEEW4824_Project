import sys
import tree
from calls import call_table


filename = "test.out"
if len(sys.argv) > 1:
    filename = sys.argv[1]

buf_len = 3

if len(sys.argv) > 2:
    buf_len = int(sys.argv[2])

syscall_file = open(filename, "r")

instr_tree = tree.TreeNode("")

for line in syscall_file:
    instrs = line.split("|")

    level = instr_tree

    if len(instrs) > buf_len:
        instrs = instrs[-buf_len:]

    # print len(instrs), instrs[-2]

    for instr in instrs[:-1]:
        if "(" in instr:
            instr = instr.split(" ")[1]
        else:
            #instr = instr.split(" ")[0]
            pass
        child = level.getChild(instr)
        if child is not None:
            child.incrementWeight()
        else:
            child = level.addChild(instr)

        level = child



#instr_tree.print_tree()


for child in instr_tree.children:
    if len(child.children) > 0:
        num_calls = {}
        calls = child.get_syscalls()
        for call in calls:
            if call in num_calls:
                num_calls[call] += 1
            else:
                num_calls[call] = 1

        orig_call_tuples = num_calls.items()
        call_tuples = []

        for tup in orig_call_tuples:
            call_tuples.append((tup[1], call_table[int(tup[0])]))

        call_tuples = sorted(call_tuples, key=lambda tup: tup[0], reverse=True)
        if call_tuples[0][0] != 1:
            print child.instr, child.weight, len(call_tuples), call_tuples
