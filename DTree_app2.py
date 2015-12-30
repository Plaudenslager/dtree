__author__ = 'peter'

from DTree import *

'''
Create a sample tree:

Should I repair or replace my car?
Repairing my car costs $2,600 today, and has cost about $9000 over last 4 years.
    This averages to $2,250 per year, but usually comes in big lumps at random times.
Replacing my car will cost $5,000 today, and $428 per month for 66 months
 - OR-
Replacing my car will cost $10,000 today, and $350 per month for 66 months

'''

print "Create tree and root node"
tree = Tree()
tree.display()

print "\nSet root node to decision with 3 branches"
tree.set_node(node_id=0, node_type='D', branches=3)
tree.display()

print "\nSet the description and cashflow for the branches"
# specify a node and branch by tree[node_id][branch_number_starting_with_0]
tree[0][0]['description'] = 'Repair'
tree[0][0]['cashflow'] = -2600
tree[0][1]['description'] = 'Replace Low Down'
tree[0][1]['cashflow'] = -5000
tree[0][2]['description'] = 'Replace High Down'
tree[0][2]['cashflow'] = -10000
tree.display()


print "\nAdd child event to the Repair branch, with 3 branches"
# use Parent_ID to combine node_id and branch_number, so the new node knows where to go on the tree
parent = ParentID(node_id=0, branch_number=0)
tree.add_node(parent_id=parent, node_type='E', branches=4)

print "\nSet the description, cashflow, and probability for the branches"
# get the child node ID by walking down the branch from the root node
# note - if the probabilities don't sum to 1, the tree cannot be solved, so backsolve (bs) values will be None
nodeID = tree[0][0]['child']
tree[nodeID][0]['description'] = 'no problems'
tree[nodeID][0]['cashflow'] = 0
tree[nodeID][0]['probability'] = .25
tree[nodeID][1]['description'] = 'Small problem'
tree[nodeID][1]['cashflow'] = -1000
tree[nodeID][1]['probability'] = .25
tree[nodeID][2]['description'] = 'Medium problem'
tree[nodeID][2]['cashflow'] = -2000
tree[nodeID][2]['probability'] = .25
tree[nodeID][3]['description'] = 'Large problem'
tree[nodeID][3]['cashflow'] = -6000
tree[nodeID][3]['probability'] = .25
tree.display()