import sys
import tree
from calls import call_table

def get_syscall_tuples(child):
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
        call_tuples.append((tup[1], tup[0]))

    call_tuples = sorted(call_tuples, key=lambda tup: tup[0], reverse=True)

    return call_tuples

filename = "test.out"
if len(sys.argv) > 1:
    filename = sys.argv[1]

buf_len = 3

if len(sys.argv) > 2:
    buf_len = int(sys.argv[2])

syscall_file = open(filename, "r")

instr_tree = tree.TreeNode("")

total_count = 0

correct_preds = 0
incorrect_preds = 0

predicted_instr = ""

for line in syscall_file:
    instrs = line.split("|")

    total_count += len(instrs)

    level = instr_tree

    if len(instrs) > buf_len:
        instrs = instrs[-buf_len:]


    if "(" not in instrs[-2]:
        print len(instrs), instrs[-2]
        print instrs[-1]
        exit(1)

    for instr in instrs[:-1]:
        if "(" in instr:
            instr_index = int(instr.split(" ")[1])

            instr = call_table[instr_index]


            if instr == predicted_instr:
                correct_preds += 1
            elif predicted_instr != "":
                incorrect_preds += 1
                print predicted_instr, instr

            predicted_instr = ""

        else:
            #instr = instr.split(" ")[0]
            pass
        child = level.getChild(instr)
        if child is not None:
            child.incrementWeight()

            tuples = get_syscall_tuples(child)

            if len(tuples) > 0 and tuples[0][0] > 0:

                total_weight = 0
                for tup in tuples:
                    total_weight += tup[0]

                print total_weight
                print tuples
                most_common = tuples[0]

                if float(most_common[0])/float(total_weight) >= .5:
                    predicted_instr = most_common[1]

        else:
            child = level.addChild(instr)

        level = child



#instr_tree.print_tree()

print total_count

print "correct predictions:", correct_preds
print "incorrect predictions:", incorrect_preds

for child in instr_tree.children:
    if len(child.children) > 0:
        call_tuples = get_syscall_tuples(child)
        if call_tuples[0][0] != 1:
            print child.instr, child.weight, len(call_tuples), call_tuples
