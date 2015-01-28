__author__ = 'peter'

from DTree import *

'''
Create a sample tree:

Should I get insurance on my phone?
If I do, it costs an extra $100, but covers all defects, and up to 2 accidents (which cost an extra $80 each)
If I don't, the replacement cost of the phone is 750.

'''

print "Create tree and root node"
tree = Tree()
tree.display()

print "\nSet root node to decision with 2 branches"
tree.set_node(node_ID=0,node_type='D', branches=2)
tree.display()

print "\nSet the description and cashflow for the branches"
# specify a node and branch by tree[node_ID][branch_number_starting_with_0]
tree[0][0]['description'] = 'get insurance'
tree[0][0]['cashflow'] = -100
tree[0][1]['description'] = 'skip insurance'
tree[0][1]['cashflow'] = 0
tree.display()

print "\nAdd child event to the get insurance branch, with 4 branches"
# use Parent_ID to combine node_ID and branch_number, so the new node knows where to go on the tree
parent = Parent_ID(node_ID=0, branch_number=0)
tree.add_node(parent_ID=parent, node_type='E', branches=4)

print "\nSet the description, cashflow, and probability for the branches"
# get the child node ID by walking down the branch from the root node
# note - if the probabilities don't sum to 1, the tree cannot be solved, so backsolve (bs) values will be None
nodeID = tree[0][0]['child']
tree[nodeID][0]['description'] = 'no problems'
tree[nodeID][0]['cashflow'] = 0
tree[nodeID][0]['probability'] = .25
tree[nodeID][1]['description'] = 'hardware defect'
tree[nodeID][1]['cashflow'] = 0
tree[nodeID][1]['probability'] = .25
tree[nodeID][2]['description'] = 'one accident'
tree[nodeID][2]['cashflow'] = -80
tree[nodeID][2]['probability'] = .25
tree[nodeID][3]['description'] = 'two accidents'
tree[nodeID][3]['cashflow'] = -160
tree[nodeID][3]['probability'] = .25
tree.display()

print "\nCalculate width and depth of tree"
print 'width: %d' % tree.width()
print 'depth: %d' % tree.depth()
