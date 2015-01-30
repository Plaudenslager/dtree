__author__ = 'peter'

from DTree import *

'''
Create a sample tree:

Should I get insurance on my phone?
From MFG, it costs an extra $100, but covers all defects, and up to 2 accidents (which cost an extra $80 each)
From carrier, it costs $7 / month (or $154 for 2 years), and covers all defects at $150 each
If I don't, repairs cost $100, and replacement cost is 750.

'''

print "Create tree and root node"
tree = Tree()
tree.display()

print "\nSet root node to decision with 3 branches"
tree.set_node(node_ID=0,node_type='D', branches=3)
tree.display()

print "\nSet the description and cashflow for the branches"
# specify a node and branch by tree[node_ID][branch_number_starting_with_0]
tree[0][0]['description'] = 'MFG insurance'
tree[0][0]['cashflow'] = -100
tree[0][1]['description'] = 'Carrier insurance'
tree[0][1]['cashflow'] = -154
tree[0][2]['description'] = 'skip insurance'
tree[0][2]['cashflow'] = 0
tree.display()

print "\nAdd child event to the MFG insurance branch, with 4 branches"
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

print "\nAdd child event to the Carrier insurance branch, with 4 branches"
# use Parent_ID to combine node_ID and branch_number, so the new node knows where to go on the tree
parent = Parent_ID(node_ID=0, branch_number=1)
tree.add_node(parent_ID=parent, node_type='E', branches=4)

print "\nSet the description, cashflow, and probability for the branches"
# same as before, but get a different nodeID by looking at the other branch
# note that we duplicate the event from above, because the same outcomes could occur whether we have insurance or not
# but we change the cashflows, because the insurance is different

nodeID = tree[0][1]['child']
tree[nodeID][0]['description'] = 'no problems'
tree[nodeID][0]['cashflow'] = 0
tree[nodeID][0]['probability'] = .25
tree[nodeID][1]['description'] = 'hardware defect'
tree[nodeID][1]['cashflow'] = -100
tree[nodeID][1]['probability'] = .25
tree[nodeID][2]['description'] = 'one accident'
tree[nodeID][2]['cashflow'] = -100
tree[nodeID][2]['probability'] = .25
tree[nodeID][3]['description'] = 'two accidents'
tree[nodeID][3]['cashflow'] = -200
tree[nodeID][3]['probability'] = .25
tree.display()

print "\nAdd child event to the skip insurance branch, with 4 branches"
# same as before, but different branch_number
parent = Parent_ID(node_ID=0, branch_number=2)
tree.add_node(parent_ID=parent, node_type='E', branches=4)

print "\nSet the description, cashflow, and probability for the branches"
# same as before, but get a different nodeID by looking at the other branch
# note that we duplicate the event from above, because the same outcomes could occur whether we have insurance or not
# but we change the cashflows, because the insurance is not there to cover the problems

nodeID = tree[0][2]['child']
tree[nodeID][0]['description'] = 'no problems'
tree[nodeID][0]['cashflow'] = 0
tree[nodeID][0]['probability'] = .25
tree[nodeID][1]['description'] = 'hardware defect'
tree[nodeID][1]['cashflow'] = -100
tree[nodeID][1]['probability'] = .25
tree[nodeID][2]['description'] = 'one accident'
tree[nodeID][2]['cashflow'] = -100
tree[nodeID][2]['probability'] = .25
tree[nodeID][3]['description'] = 'two accidents'
tree[nodeID][3]['cashflow'] = -200
tree[nodeID][3]['probability'] = .25
tree.display()

print "\nWithout insurance, only minor accidents can be fixed for $100"
print "Add events to one- and two- accident branches to consider odds of major or minor accidents"
# get the right starting node
nodeID = tree[0][2]['child']
parent = Parent_ID(node_ID=nodeID, branch_number=2)
new_node = tree.add_node(parent_ID=parent, node_type='E', branches=2)
# adding a node returns the new node ID, so easy to grab it now, rather than walking the tree

print "\nSet the description, cashflow, and probability for the branches"
# this time we will use the node ID we got when we created the node
# we might change the cashflow on the one-accident branch to 0, and set the minor & major accident cashflows here
# to make it slightly easier, we leave the minor accident cashflow already listed alone, and just add the difference
# for a major accident
nodeID = new_node
tree[nodeID][0]['description'] = 'minor accident'
tree[nodeID][0]['cashflow'] = 0
tree[nodeID][0]['probability'] = .70
tree[nodeID][1]['description'] = 'major accident'
tree[nodeID][1]['cashflow'] = -650
tree[nodeID][1]['probability'] = .30

print "Do it again for the two accident branch"
# everything is the same, except for the branch number where we create the new node
nodeID = tree[0][2]['child']
parent = Parent_ID(node_ID=nodeID, branch_number=3)
new_node = tree.add_node(parent_ID=parent, node_type='E', branches=2)

print "\nSet the description, cashflow, and probability for the branches"
# everything is the same as above, except for the node ID, which we got when it was created
# also note that having to replace the phone twice is pretty expensive
nodeID = new_node
tree[nodeID][0]['description'] = 'minor accident'
tree[nodeID][0]['cashflow'] = 0
tree[nodeID][0]['probability'] = .70
tree[nodeID][1]['description'] = 'major accident'
tree[nodeID][1]['cashflow'] = -1300
tree[nodeID][1]['probability'] = .30

print "\nThis should be our final tree"
tree.display()

print "\nHow to read the tree:"
print "* The backsolve (bs:) value on the root node (D:0 ) tells us the average amount we will spend on repairs & insurance ($160)"
print "* Our decision is to buy the insurance, because the backsolve for that is higher than for carrier or skip (-160 vs -254 or -246)"
print "* With insurance, the expected cost of accidents is -60, the sum of all the bs values across all the outcomes"
print "* So we add -60 to the cost of the insurance to find a total cost of -160"
print "*\n With carrier insurance, the expected cost of accidents is -254."
print "\n* Without insurance, the expected cost of accidents is -246; although the probabilities are the same, the costs are higher"
print "\n* Also notice the terminal values at the end of the arrows"
print "* They help indicate the worst-case scenarios, e.g. with MFG insurance, max expense is -260; without could be -1500."

print "\nCalculate width and depth of tree"
print 'width: %d' % tree.width()
print 'depth: %d' % tree.depth()
