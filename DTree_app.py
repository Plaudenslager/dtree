__author__ = 'peter'

from DTree import Node

root = Node('D')
print root.width
root.add_branch()
print root.width
root.add_branch()
print root.width