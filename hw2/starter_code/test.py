from random import randint

class Node:

    left_child = None
    right_child = None

    def __init__(self, value = -1):
        self.value = value

    def isLeaf(self):
        return not (self.left_child and self.right_child)

class Tree:

    root = None

    def __init__(self, depth = 0):
        self.root = self.genTree(depth, 0)

    def genTree(self, depth, currentDepth):
        if currentDepth == depth:
            n = Node(randint(1, 101))
            print n.value
            return n
        result = Node()
        result.left_child = self.genTree(depth, currentDepth + 1)
        result.right_child = self.genTree(depth, currentDepth + 1)
        print result.value
        return result

    def printTree(self):
        buffer = []
        self.printTreeHelp(self.root, buffer, 0)
        # print buffer
        for l in buffer:
            print l

    def printTreeHelp(self, node, buffer, depth):
        # print "in helper"
        if node:
            # print "node here"
            # print "depth: " + str(depth) + ", size: " + str(len(buffer))
            if depth >= len(buffer):
                buffer.append([node.value])
                # print buffer
            else:
                buffer[depth].append(node.value)
            self.printTreeHelp(node.left_child, buffer, depth + 1)
            self.printTreeHelp(node.right_child, buffer, depth + 1)

def main():
    t = Tree(3)
    # print t.root.value
    t.printTree()

if __name__ == '__main__':
    main()
