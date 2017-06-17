import sys
import re

DEFAULT_DOT_FILE = "dot.txt"

FILE_LOAD_1 = "digraph G {\n"
FILE_LOAD_0 = "}\n"

FILE_SAVE_1 = "digraph G {\n"
FILE_SAVE_0 = "}\n"

DATE_LOAD_1 = "  {\n"
DATE_LOAD_2 = "    node [shape=plaintext]\n"
DATE_LOAD_3 = "    edge [dir=none]\n"
DATE_LOAD_0 = "  }\n"

DATE_SAVE_1 = "  {\n"
DATE_SAVE_2 = "    node [shape=plaintext]\n"
DATE_SAVE_3 = "    edge [dir=none]\n"
DATE_SAVE_0 = "  }\n"

RANK_LOAD_1 = "\n"
RANK_LOAD_X = r'\s+{\s+rank=same;\s+\"(\S*)\";\s+(\w*)\s+};'
RANK_LOAD_0 = "\n"

RANK_SAVE_1 = "\n"
RANK_SAVE_X = "  { rank=same; \"%s\"; %s };\n"
RANK_SAVE_0 = "\n"

HEAD_LOAD_1 = "  node [shape=box, style=filled]\n"
HEAD_LOAD_X = r'\s+(\w*)\s+\[label=\"(\S*)\", fontsize=10\]'
HEAD_LOAD_0 = "\n"

HEAD_SAVE_1 = "  node [shape=box, style=filled]\n"
HEAD_SAVE_X = "  %s [label=\"%s\", fontsize=10]"
HEAD_SAVE_0 = "\n"

NODE_LOAD_1 = "  node [style=rounded]\n"
NODE_LOAD_2 = "  edge [dir=both]\n"
NODE_LOAD_X = r'\s+(\w*)\s+->\s+(\w*)\s+\[dir=none, style=dotted\]'
NODE_LOAD_0 = "\n"

NODE_SAVE_1 = "  node [style=rounded]\n"
NODE_SAVE_2 = "  edge [dir=both]\n"
NODE_SAVE_X = "  %s -> %s [dir=none, style=dotted]\n"
NODE_SAVE_0 = "\n"

EDGE_LOAD_0 = "\n"

EDGE_SAVE_0 = "\n"

class Branch:
    def __init__(self, label, prev = None):
        self.label = label
        self.prev = prev

class BranchManager:
    def __init__(self):
        self.branches = {}

    def insert(self, name, label, prev = None):
        if self.branches.has_key(name):
            print("ERROR: Branch '%s' existed" % name)
            return None
        return self.branches[name] = Branch(label, prev)

    def remove(self, name):
        if self.branches.has_key(name):
            self.branches.pop(name)

    def get(self, name):
        return self.branches.has_key(name) and self.branches.get(name) or None

    def keys(self):
        return sorted(self.branches.keys(), reverse=True)

class Node:
    def __init__(self, date, edge = None):
        self.date = date
        self.edge = edge

class NodeManager:
    def __init__(self):
        self.nodes = {}

    def insert(self, name, date):
        if self.nodes.has_key(name):
            print("ERROR: Node '%s' existed" % name)
            return None
        return self.nodes[name] = Node(date)

    def remove(self, name):
        if self.nodes.has_key(name):
            self.nodes.pop(name)

    def get(self, name):
        return self.nodes.has_key(name) and self.nodes.get(name) or None

    def keys(self):
        return sorted(self.node.keys(), cmp=lambda x,y:cmp(x[-4:], y[-4:]), reverse=True)

class Edge:
    def __init__(self, prev, label = None, Back = None):
        self.prev = prev
        self.label = label
        self.back = back

class DateManager:
    def __init__(self):
        self.dates = {}

    def insert(self, date):
        ref = 1
        if self.dates.has_key(date):
            ref = self.dates.get(date) + 1
        self.dates[date] = ref

    def remove(self, date):
        if not self.dates.has_key(date):
            print("ERROR: Date '%s' not existed" % date)
        else:
            ref = self.dates.get(date) - 1
            self.dates[date] = ref
            if not cmp(0, ref):
                self.dates.pop(date)

    def keys(self):
        return sorted(self.dates.keys(), reverse=True)

class Dot:
    def __init__(self):
        self.dotLoad = DEFAULT_DOT_FILE
        self.dotSave = DEFAULT_DOT_FILE
        self.command = None

        self.dateMgr = DateManager()
        self.brancgMgr = BranchManager()
        self.nodeMgr = NodeManager()

    def loadDates(self, dot):
        print("Loading Dates...")
        if cmp(dot.readline(), DATE_LOAD_1):
            print("ERROR: expect '%s'" % DATE_LOAD_1)
            return False
        if cmp(dot.readline(), DATE_LOAD_2):
            print("ERROR: expect '%s'" % DATE_LOAD_2)
            return False
        if cmp(dot.readline(), DATE_LOAD_3):
            print("ERROR: expect '%s'" % DATE_LOAD_3)
            return False
        while cmp(dot.readline(), DATE_LOAD_0):
            False
        return True

    def saveDates(self, dot):
        dot.write(DATE_SAVE_1)
        dot.write(DATE_SAVE_2)
        dot.write(DATE_SAVE_3)

        link = "    "
        prev = None
        for date in self.dateMgr.keys():
            if prev and cmp(date[5:7], prev[5:7]):
                dot.write("\n")
            dot.write("%s\"%s\"" % (link, date))
            link = " -> "
            prev = date
        dot.write(";\n")
        dot.write(DATE_SAVE_0)
