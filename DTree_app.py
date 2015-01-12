__author__ = 'peter'

from DTree import Node

# Create root node
root = Node('D')

# Add some branches
for i in range(0,6):
    root.add_branch()

# Calculate width of tree
print 'width: %d' % root.width

# Print branch numbers and names
print
print 'branch','name','child'
for branch in root.branches:
    b_name = branch['description']
    number = root.branch_number(b_name)
    c = branch['child']
    print (number, b_name, c)

print '='*20

# Delete a branch
root.del_branch(3)

# Print branch numbers and names
print
print 'branch','name','child'
for branch in root.branches:
    b_name = branch['description']
    number = root.branch_number(b_name)
    c = branch['child']
    print (number, b_name, c)

# Calculate width of tree
print 'width: %d' % root.width

# Create a child node, and add it to a branch
child = Node('E')
root.set_child(1,child)
print child.ID
print root.branches[1]['child'].ID

print '='*20

# Print branch numbers and names
print
print 'branch','name','child'
for branch in root.branches:
    b_name = branch['description']
    number = root.branch_number(b_name)
    c = branch['child']
    print (number, b_name, c)

# Calculate width of tree
print 'width: %d' % root.width

# Create a child node, and add it to a branch
child = Node('E')
c = root.get_child(1)
c.add_branch()
c.add_branch()
c.set_child(1,child)
print child.ID
print c.branches[1]['child'].ID

print '='*20

# Print branch numbers and names
print
print 'branch','name','child'
for branch in root.branches:
    b_name = branch['description']
    number = root.branch_number(b_name)
    c = branch['child']
    print (number, b_name, c)

# Calculate width of tree
print 'width: %d' % root.width