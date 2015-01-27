# dtree
decision tree calculator

Decision Trees are used to make decisions where each choice has different immediate consequences of income and cost (cashflow).  Decisions are choices you make, and Events are outcomes which are out of your control.  In addition to a cashflow, each outcome of the event has a probability (all the probabilities must sum to 1).

Conceptual usage:
* Decide if the initial node is an event or a decision.  Lable the cashflows (and if an event, probabilities) for each option.
* If desired, add additional decision or event nodes to the ends of the branches of the previous nodes.
* Follow each branch, adding up the cashflows (positive for income, negative for outflow), and write the total at the end of the final branch.
* Starting with a final branch, work backwards.  For events, add up all the downstream (i.e. after that event occurs) cashflows, and multiply by the probability of that event (ignoring any preceeding events).  This is the expected value for this branch.  For decisions, identify the highest value branch - this is the expected value for this branch.
* Continue to work backwards, adding the expected value of downstream branchs to the current cashflow for the branch you are working on, until you get to the root of the tree (i.e. the first decision or event).  When adding events, add up all the branch expected values - this is the expected value for the whole event.  For decisions, take only the highest value option.
* At this point, you know the average / expected value for each event, and the best choice to make at each decision.  You also know the average value of the whole chain of events (e.g. if you made dozens of decisions according to this tree, on average, you would gain or lose the identified cashflow).

Code useage:
* Create a new tree object, specifying whether it is an event or a decision.  The first node ID is always 0, and begins with no branches.
* Use tree.add_branch to add a branch, with a cashflow and (if desired) a probability.
* Use tree.display to print the tree with all the final values
* Use tree.solve to do all the forward and backward calculations
* Use tree.width and tree.depth to calculate and display those values
* Use tree.add_node to add a new node to a branch.  You will need to create a new parent_ID to hold the parent node ID and branch number.  For the first node, the node ID is 0.  New nodes will generate their own ID, and will place it in the 'child' property of the parent node.  You can retrieve this value later by starting with node 0, and getting the child node ID from the branch.  If necessary, work your way down the tree to get to the node you want.
* Deleting a node will delete all child branches and nodes
* del_branch will delete the last (highest numbered) branch for the node, and all child nodes and branches

Get all nodes with tree.nodes()
Get a particular node with tree[node_ID]
Get a particular branch with tree[node_ID][branch_no] (branches are numbered starting with 0)
Get or set a node property with tree[node_ID][branch_no][property] (properties are: cashflow, probability, child)
Best practice for setting the child property is to use add_node

Read the value of a node (highest value of decision branches, expected value of event node) with tree[node_ID].node_value.
Get the branch number of the best choice in a decision node with tree[node_ID].best_branch.

There are a few tests, but not complete code coverage.
There is also some broken GUI that doesn't really work, and was designed before the full tree API was done.

Pull requests are welcome!
