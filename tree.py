import sys

class TreeNode(object):
    def __init__(self, instr, initWeight=1):
        self.children = []
        self.weight = initWeight
        self.instr = instr
        self.prev_syscall = ""

    def addChild(self, instr, weight=1):
        child = TreeNode(instr, weight)
        self.children.append(child)
        return child

    def getChild(self, instr):
        for child in self.children:
            if child.instr == instr:
                return child
        return None

    def getWeight(self):
        return self.weight

    def incrementWeight(self):
        self.weight += 1

    def set_prev_syscall(self, prev):
        self.prev_syscall = prev

    def get_instr(self, instr):
        if self.instr == instr:
            return self

        for child in self.children:
            new_instr = child
            if new_instr.instr == instr:
                return new_instr

        return None

    def print_tree(self, depth=0, max_depth=-1):
        for x in range(0, depth):
            sys.stdout.write(" ")

        print "\\", self.weight, ":", self.instr

        if depth <= max_depth or max_depth==-1:
            self.children = sorted(self.children, key = lambda child: child.weight,
                    reverse=True)

            for child in self.children:
                child.print_tree(depth + 1, max_depth)

    def get_syscalls(self):
        if len(self.children) == 0:
            return [self.instr]
        else:
            ret = []
            for child in self.children:
                ret += child.get_syscalls()
            return ret
