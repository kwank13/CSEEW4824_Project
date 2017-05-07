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
prev_syscall = ""

patterns = {}

for line in syscall_file:
    instrs = line.split("|")

    total_count += len(instrs)

    level = instr_tree


    #if len(instrs) > buf_len:
        #instrs = instrs[-buf_len:]


    if "(" not in instrs[-2]:
        print len(instrs), instrs[-2]
        print instrs[-1]
        exit(1)

    syscall_predicted = False

    n = 0

    child = None
    for instr in instrs[:-1]:
        is_syscall = False
        if "(" in instr:
            instr_index = int(instr.split(" ")[1])

            instr = call_table[instr_index]

            is_syscall = True

            #if prev_syscall in patterns:
            #    if patterns[prev_syscall][-1] == instr:
            #        correct_preds += 1
            #    else:
            #        incorrect_preds += 1
            if instr == predicted_instr:
                correct_preds += 1
            elif predicted_instr != "":
                incorrect_preds += 1

            if predicted_instr != "":
                #print predicted_instr, instr
                pass

            #predicted_instr = instr

            if prev_syscall in patterns:
                patterns[prev_syscall].append(instr)
            else:
                patterns[prev_syscall] = [instr]
            prev_syscall = instr

        else:
            #instr = instr.split(" ")[0]
            pass
        if n >= len(instrs) - buf_len:
            child = level.getChild(instr)

        tuples = []
        if child is not None:
            child.incrementWeight()
            if is_syscall:
                child.set_prev_syscall(prev_syscall)
        else:
            if n >= len(instrs) - buf_len:
                child = level.addChild(instr)

        if not is_syscall:
            instr_cont = instr_tree.get_instr(instr)

            pred_tree = ""
            if instr_cont is not None:
                tuples = get_syscall_tuples(instr_cont)

                if len(tuples) > 0 and tuples[0][0] > 0:

                    total_weight = 0
                    for tup in tuples:
                        total_weight += tup[0]

                   # print total_weight
                   # print tuples
                    most_common = tuples[0]

                    pred_tree = most_common[1]

            pred_pat = ""
            count_tups = []
            if prev_syscall in patterns:
                count = {}
                total = 0
                for call in patterns[prev_syscall]:
                    if call in count:
                        count[call] += 1
                    else:
                        count[call] = 1
                    total += 1

                count_tups = count.items()

                count_tups = sorted(count_tups, key=lambda tup: tup[1], reverse=True)
                if float(count_tups[0][1])/float(total) >= .5:
                    pred_pat = count_tups[0][0]





            if pred_pat == pred_tree:
                predicted_instr = pred_pat
            elif pred_tree != "":
                predicted_instr = pred_pat
            else:
                predicted_instr = ""

            #found = False
            #for call in count_tups:
            #    for tup in tuples:
            #        if tup[1] == call[0]:
            #            predicted_instr = call[0]
            #            found = True
            #            break

            #    if found:
            #        break



        #if not is_syscall:
        #    if prev_syscall in patterns:
        #        predicted_instr = patterns[prev_syscall][-1]
        #        syscall_predicted = True
        #    else:
        #        predicted_instr = ""
        if n >= len(instrs) - buf_len:
            level = child
        n+=1


#instr_tree.print_tree()

print total_count

print "correct predictions:", correct_preds
print "incorrect predictions:", incorrect_preds

exit(0)
for child in instr_tree.children:
    if len(child.children) > 0:
        call_tuples = get_syscall_tuples(child)
        if call_tuples[0][0] != 1:
            print child.instr, child.weight, len(call_tuples), call_tuples
