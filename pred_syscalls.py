import sys
import tree


filename = "test.out"
if len(sys.argv) > 1:
    filename = sys.argv[1]


syscall_file = open(filename, "r")

instr_tree = tree.TreeNode("")

for line in syscall_file:
    instrs = line.split("|")

    level = instr_tree

    for instr in instrs[:-1]:
        if "(" in instr:
            instr = instr.split(" ")[1]
        child = level.getChild(instr)
        if child is not None:
            child.incrementWeight()
            level = child
        else:
            child = level.addChild(instr)



instr_tree.print_tree()
