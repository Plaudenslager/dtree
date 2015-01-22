__author__ = 'peter'

from DTree import *
import random

def print_tree():
    print'Nodes in tree'
    print'ID:\tType\tbranches'
    for k,v in tree.nodes.iteritems():
        print '%d:\t%s' %(k,v.node_type,)
    print 80*'=','\n'

print "Create tree and root node"
tree = Tree()
tree.display()

print "\nAdd some branches"
for i in range(0,6):
    tree.add_branch(0, cashflow=i*100, probability=1.0/6)
tree.display()

print "\nCalculate width of tree"
print 'width: %d' % tree.width()

print "\nDelete a branch"
tree.del_branch(0)
tree.display()
print 'width: %d' % tree.width()

print "\nCreate a child node, and add it to a branch"
tree.add_node(Parent_ID(0,0),'E')
tree.display()
print 'width: %d' % tree.width()

print "\n list nodes"
for item in tree.nodes.keys():
    print item

print "\nCreate many more child nodes, add branches"
for i in range(0,10):
    node = random.choice(tree.nodes.keys())
    if len(tree[node].branches) < 3:
        tree.add_branch(node,cashflow=random.randint(-5000,5000))
        print '-created branch on node %s' %node
    else:
        branch = random.choice(range(len(tree[node].branches)))
        new_node = tree.add_node(Parent_ID(node,branch),random.choice(['E','D']))
        print '+created new node %s on branch %d of node %s' %(new_node,branch,node)

tree.display()
print 'width: %d' % tree.width()
print 'depth: %d' % tree.depth()

print "\nDelete everything under the root node"
while tree[0].width > 0:
    print tree[0].width
    tree.del_branch(0)

tree.display()
print 'width: %d' % tree.width()
print 'depth: %d' % tree.depth()

print "\nBuild a new tree deliberately"