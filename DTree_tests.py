__author__ = 'peter'

'''
Copyright 2014 Peter Laudenslager

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   '''

from DTree import Tree, Node, Parent_ID
import unittest

class TestNodeFunctions(unittest.TestCase):

    def test_new_node(self):
        # Defaults to node type D, creates a node ID, and creates an empty list for the branches
        node = Node()
        self.assertEqual(node.node_type, 'D')
        self.assertIsNotNone(node.ID)
        self.assertEqual(node.branches, [])

        # Accepts legal node types; converts to upper case
        for ntype in ['d','D','e','E']:
            node = Node(node_type=ntype)
            self.assertEqual(node.node_type, ntype.upper())

        # Rejects illegal node types
        self.assertRaises(ReferenceError, Node, node_type='junk')

        # Works with the root node ID
        node = Node(ID=0)
        self.assertEqual(node.ID, '0')

        # Works with a custom node ID; strips out spaces; converts to lower
        node = Node(ID=' My Custom Node Name ')
        self.assertEqual(node.ID, 'mycustomnodename')

    # TODO Add test for add_branch

    # TODO Add test for del_branch

    # TODO Add test for change_node


class TestTreeFunctions(unittest.TestCase):

    def setUp(self):
        # create a tree
        self.tree = Tree()

    def test_solution(self):
        # verify that the math all works properly for a moderately complex tree
        self.tree.set_node(0,'D',2)
        self.tree[0][0]['cashflow'] = 100
        self.tree[0][1]['cashflow'] = -100
        self.tree.solve()

        self.assertEqual(self.tree[0].node_value, 100)
        self.assertEqual(self.tree[0].best_branch,0)

        parent = Parent_ID(0,0)
        node_ID = self.tree.add_node(parent,'E',branches=2)
        self.tree[node_ID][0]['cashflow'] = -300
        self.tree[node_ID][0]['probability'] = .60
        self.tree[node_ID][1]['cashflow'] = 400
        self.tree[node_ID][1]['probability'] = .40
        # This node is worth -20
        self.tree.solve()

        self.assertEqual(self.tree[node_ID].node_value,-20)
        self.assertEqual(self.tree[0].node_value, 80)
        self.assertEqual(self.tree[0].best_branch,0)

        parent = Parent_ID(0,1)
        node_ID = self.tree.add_node(parent,'E',branches=4)
        self.tree[node_ID][0]['cashflow'] = -500
        self.tree[node_ID][0]['probability'] = .20
        self.tree[node_ID][1]['cashflow'] = 1000
        self.tree[node_ID][1]['probability'] = .25
        self.tree[node_ID][2]['cashflow'] = -3000
        self.tree[node_ID][2]['probability'] = .05
        self.tree[node_ID][3]['cashflow'] = 400
        self.tree[node_ID][3]['probability'] = .50
        # This node is worth 200
        self.tree.solve()

        self.assertEqual(self.tree[node_ID].node_value, 200)
        self.assertEqual(self.tree[0].node_value, 100)
        self.assertEqual(self.tree[0].best_branch,1)

    def test_wide(self):
        # Verify that a very wide tree can be created
        root_width = 300
        child_width = 300

        self.assertEqual(self.tree.width(), 1)

        self.tree.set_node(0,'D',root_width)
        self.assertEqual(self.tree.width(), root_width)

        for branch in range(0,root_width):
            parent = Parent_ID(0, branch)
            self.tree.add_node(parent,'E', branches=child_width)
            self.assertEqual(self.tree.width(),(branch+1)*(child_width-1)+root_width)

        self.assertEqual(self.tree.width(), child_width*root_width)
        self.assertEqual(self.tree.depth(),2)

    def test_deep(self):
        # Verify that a very deep tree can be created
        depth = 973
        # over 973 will generate a recursion depth error on the forward_solve
        # this seems to be very sensitive to minor code changes; earlier version could do 974,
        # so we need to avoid very deep trees, but several hundred seems like plenty.

        self.tree.set_node(0,'D', 3)
        node_ID = 0
        for level in range(1, depth):
            parent = Parent_ID(node_ID, 1)
            node_ID = self.tree.add_node(parent,'E', branches=3)

            self.assertEqual(self.tree.depth(), level+1)
            self.assertEqual(self.tree.width(), 2*level+3)

        self.assertEqual(self.tree.width(), 2*depth+1)
        self.assertEqual(self.tree.depth(), depth)




if __name__ == '__main__':
    unittest.main()