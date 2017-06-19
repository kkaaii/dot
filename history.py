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
HEAD_SAVE_X = "  %s [label=\"%s\", fontsize=10]\n"
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
    def __init__(self, text, prev = None):
        self.text = text
        self.prev = prev

class BranchManager:
    def __init__(self):
        self.branches = {}

    def insert(self, name, text, prev = None):
        if self.branches.has_key(name):
            print("ERROR: Branch '%s' existed" % name)
            return None
        branch = Branch(text, prev)
        self.branches[name] = branch
        return branch

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
        node = Node(date)
        self.nodes[name] = node
        return node

    def remove(self, name):
        if self.nodes.has_key(name):
            self.nodes.pop(name)

    def get(self, name):
        return self.nodes.has_key(name) and self.nodes.get(name) or None

    def keys(self):
        return sorted(self.nodes.keys(), cmp=lambda x,y:cmp(x[-4:], y[-4:]), reverse=True)

class Edge:
    def __init__(self, prev, text = None, back = None):
        self.prev = prev
        self.text = text
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

class History:
    def __init__(self):
        self.dotLoad = DEFAULT_DOT_FILE
        self.dotSave = DEFAULT_DOT_FILE
        self.command = None

        self.dateMgr = DateManager()
        self.branchMgr = BranchManager()
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

    def loadRanks(self, dot):
        print("Loading Ranks...")
        if cmp(dot.readline(), RANK_LOAD_1):
            return False
        regex = re.compile(RANK_LOAD_X)
        while True:
            line = dot.readline()
            if not cmp(line, RANK_LOAD_0):
                break;
            match = regex.search(line)
            if not match:
                return False
            date = match.group(1)
            name = match.group(2)
            self.dateMgr.insert(date)
            if not self.nodeMgr.insert(name, date):
                return False
        return True

    def saveRanks(self, dot):
        dot.write(RANK_SAVE_1)
        for name in self.nodeMgr.keys():
            node = self.nodeMgr.get(name)
            dot.write(RANK_SAVE_X % (node.date, name))
        dot.write(RANK_SAVE_0)

    def loadHeads(self, dot):
        print("Loading Heads...")
        if cmp(dot.readline(), HEAD_LOAD_1):
            return False
        regex = re.compile(HEAD_LOAD_X)
        while True:
            line = dot.readline()
            if not cmp(line, HEAD_LOAD_0):
                break
            match = regex.search(line)
            if not match:
                return False
            name = match.group(1)
            text = match.group(2)
            self.branchMgr.insert(name, text)
        return True

    def saveHeads(self, dot):
        dot.write(HEAD_SAVE_1)
        for name in self.branchMgr.keys():
            branch = self.branchMgr.get(name)
            dot.write(HEAD_SAVE_X % (name, branch.text))
        dot.write(HEAD_SAVE_0)

    def loadNodes(self, dot):
        print("Loading Nodes...")
        if cmp(dot.readline(), NODE_LOAD_1):
            return False
        if cmp(dot.readline(), NODE_LOAD_2):
            return False
        regex = re.compile(NODE_LOAD_X)
        while True:
            line = dot.readline()
            if not cmp(line, NODE_LOAD_0):
                break
            match = regex.search(line)
            if not match:
                return False
            branch = self.branchMgr.get(match.group(1))
            branch.prev = match.group(2)
        return True

    def saveNodes(self, dot):
        dot.write(NODE_SAVE_1)
        dot.write(NODE_SAVE_2)
        for name in self.branchMgr.keys():
            branch = self.branchMgr.get(name)
            if branch.prev:
                dot.write(NODE_SAVE_X % (name, branch.prev))
        dot.write(NODE_SAVE_0)

    def loadEdges(self, dot):
        print("Loading Edges...")
        while True:
            line = dot.readline()
            if not cmp(line, EDGE_LOAD_0):
                break
            name, prev = line.strip().split(" -> ")
            node = self.nodeMgr.get(name)
            node.edge = Edge(prev)
        return True

    def saveEdges(self, dot):
        for name in self.nodeMgr.keys():
            edge = self.nodeMgr.get(name).edge
            if not edge:
                continue
            dot.write("  %s -> %s" % (name, edge.prev))
            if edge.back:
                if edge.text:
                    dot.write("[dir=back, color=red, style=bold, label=\"%s\"]\n" % edge.text)
                else:
                    dot.write("[dir=back, color=red, style=bold]\n")
            else:
                if edge.text:
                    dot.write("[label=\"%s\"]\n" % edge.text)
                else:
                    dot.write("\n")
        dot.write(EDGE_SAVE_0)

    def loadFile(self):
        try:
            dot = open(self.dotLoad, 'r')
        except IOError:
            return False

        if cmp(dot.readline(), FILE_LOAD_1):
            return False
        if not self.loadDates(dot):
            return False
        if not self.loadRanks(dot):
            return False
        if not self.loadHeads(dot):
            return False
        if not self.loadNodes(dot):
            return False
        if not self.loadEdges(dot):
            return False
        if cmp(dot.readline(), FILE_LOAD_0):
            return False
        dot.close()
        return True

    def saveFile(self):
        dot = open(self.dotSave, 'w')
        dot.write(FILE_SAVE_1)
        self.saveDates(dot)
        self.saveRanks(dot)
        self.saveHeads(dot)
        self.saveNodes(dot)
        self.saveEdges(dot)
        dot.write(FILE_SAVE_0)
        dot.close()

    def parseArguments(self):
        print("Parsing Arguments...")
        optDict = {}
        for option in sys.argv[1:]:
            if '=' in option:
                key, value = str(option).split('=')
                optDict[key] = value
            else:
                optDict[str(option)] = None
        self.dotLoad = optDict.get('-if', DEFAULT_DOT_FILE)
        self.dotSave = optDict.get('-of', DEFAULT_DOT_FILE)
        self.command = optDict.get('-c', None)

    def branchCreate(self, name, text, prev):
        self.branchMgr.insert(name, text, prev)

    def branchDelete(self, name):
        self.branchMgr.remove(name)

    def branchUpdate(self, name, text, prev):
        branch = self.branchMgr.get(name)
        if text:
            branch.text = text
        if prev:
            branch.prev = prev

    def nodeCreate(self, name, date, prev = None):
        self.dateMgr.insert(date)
        node = self.nodeMgr.insert(name, date)
        if self.nodeMgr.nodes.has_key(prev):
            node.edge = Edge(prev)

    def nodeDelete(self, name):
        node = self.nodeMgr.get(name)
        if node:
            prev = node.edge and node.edge.prev or None
            for k in self.branchMgr.keys():
                branch = self.branchMgr.get(k)
                if not cmp(branch.prev, name):
                    branch.prev = prev
            for k in self.nodeMgr.keys():
                edge = self.nodeMgr.get(k).edge
                if edge and not cmp(edge.prev, name):
                    edge.prev = prev
            self.dateMgr.remove(node.date)
            self.nodeMgr.remove(name)

    def processCommand(self):
        if not self.command:
            return False
        args = self.command.split(' ')
        if not cmp(args[0], 'branch'):
            name = args[2]
            if not cmp(args[1], '-c'):
                text = len(args) > 3 and args[3] or None
                prev = len(args) > 4 and args[4] or None
                self.branchCreate(name, text, prev)
            elif not cmp(args[1], '-d'):
                self.branchDelete(name)
            elif not cmp(args[1], '-u'):
                text = len(args) > 3 and args[3] or None
                prev = len(args) > 4 and args[4] or None
                if '*' in text:
                    text = None
                self.branchUpdate(name, text, prev)
        if not cmp(args[0], 'node'):
            name = args[2]
            if not cmp(args[1], '-c'):
                date = args[3]
                prev = len(args) > 4 and args[4] or None
                self.nodeCreate(name, date, prev)
            elif not cmp(args[1], '-d'):
                self.nodeDelete(name)
            elif not cmp(args[1], '-u'):
                self.nodeUpdate(name)
        return True

    def run(self):
        self.parseArguments()
        self.loadFile()
        self.processCommand()
        self.saveFile()
        pass

def main():
    History().run()

if __name__ == "__main__":
    main()
