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

from DTree import Tree, Node, ParentID
import unittest


class TestNodeFunctions(unittest.TestCase):
    def test_new_node(self):
        # Defaults to node type D, creates a node ID, and creates an empty list for the branches
        node = Node()
        self.assertEqual(node.node_type, 'D')
        self.assertIsNotNone(node.ID)
        self.assertEqual(node.branches, [])

        # Accepts legal node types; converts to upper case
        for ntype in ['d', 'D', 'e', 'E']:
            node = Node(node_type=ntype)
            self.assertEqual(node.node_type, ntype.upper())

        # Rejects illegal node types
        self.assertRaises(ReferenceError, Node, node_type='junk')

        # Works with the root node guid
        node = Node(guid=0)
        self.assertEqual(node.ID, '0')

        # Works with a custom node ID; strips out spaces; converts to lower
        node = Node(guid=' My Custom Node Name ')
        self.assertEqual(node.ID, 'mycustomnodename')

    def test_sensitivity(self):
        # test for decision nodes & branches
        node = Node(node_type='D')

        # Create branches with all positive values
        node.add_branch(cashflow = 0)
        node.add_branch(cashflow = 1)
        node.add_branch(cashflow = 2)
        node.add_branch(cashflow = 3)
        node.add_branch(cashflow = 4)

        node.update_sensitivity()

        self.assertEqual(node.node_value, 4)
        self.assertEqual(node[0]['cf_delta'], 4)
        self.assertEqual(node[1]['cf_delta'], 3)
        self.assertEqual(node[2]['cf_delta'], 2)
        self.assertEqual(node[3]['cf_delta'], 1)
        self.assertEqual(node[4]['cf_delta'], -1)

        # Reset for next test
        node = Node(node_type='D')

        # Create branches with all negative values
        node.add_branch(cashflow = -10)
        node.add_branch(cashflow = -11)
        node.add_branch(cashflow = -12)
        node.add_branch(cashflow = -13)
        node.add_branch(cashflow = -14)

        node.update_sensitivity()

        self.assertEqual(node.node_value, -10)
        self.assertEqual(node[0]['cf_delta'], -1)
        self.assertEqual(node[1]['cf_delta'], 1)
        self.assertEqual(node[2]['cf_delta'], 2)
        self.assertEqual(node[3]['cf_delta'], 3)
        self.assertEqual(node[4]['cf_delta'], 4)

        # Test with event nodes / branches
        node = Node(node_type='E')

        # Create branches with all positive values
        node.add_branch(cashflow = 0, probability=.1)
        node.add_branch(cashflow = 1, probability=.2)
        node.add_branch(cashflow = 2, probability=.3)
        node.add_branch(cashflow = 3, probability=.3)
        node.add_branch(cashflow = 4, probability=.1)
        # expected value: 0+.2+.6+.9+.4=2.1

        node.update_sensitivity(parent_delta=2.2)

        self.assertEqual(node.node_value, 2.1)
        self.assertEqual(node[0]['cf_delta'], 1)
        self.assertEqual(node[1]['cf_delta'], .5)
        self.assertEqual(node[2]['cf_delta'], .333)
        self.assertEqual(node[3]['cf_delta'], .333)
        self.assertEqual(node[4]['cf_delta'], 1)

        # Reset for next test
        node = Node(node_type='E')

        # Create branches with all negative values
        node.add_branch(cashflow = -10, probability=.2)
        node.add_branch(cashflow = -11, probability=.1)
        node.add_branch(cashflow = -12, probability=.3)
        node.add_branch(cashflow = -13, probability=.3)
        node.add_branch(cashflow = -14, probability=.1)
        # expected value: -2-1.1-3.6-3.9-1.4= -12

        node.update_sensitivity(parent_delta= -4)

        self.assertEqual(node.node_value, -12)
        self.assertEqual(node[0]['cf_delta'], 40)
        self.assertEqual(node[1]['cf_delta'], 80)
        self.assertEqual(node[2]['cf_delta'], round(8/.3,3))
        self.assertEqual(node[3]['cf_delta'], round(8/.3,3))
        self.assertEqual(node[4]['cf_delta'], 80)

        # TODO Add test for add_branch

        # TODO Add test for del_branch

        # TODO Add test for change_node


class TestTreeFunctions(unittest.TestCase):
    def setUp(self):
        # create a tree
        self.tree = Tree()

    def test_t_probability(self):
        # verify the __solve_probability function
        self.tree.set_node(0, 'D', 2)
        self.tree[0][0]['cashflow'] = 300
        self.tree[0][1]['cashflow'] = -300
        self.tree.solve()

        self.assertEqual(self.tree[0][0]['t_probability'], 1)
        self.assertEqual(self.tree[0][1]['t_probability'], 0)

    def test_description_length(self):
        # verify that the calculation for __max_description_length works
        # calculated on lengths of ['description', 'cashflow', 'probability', 'backsolve', 't_value']
        # with defaults (with 4 branches), should be [2, 1, 4, 1, 1]
        # each change should be length of the description + 7
        self.assertEqual(self.tree.max_description_length, 0)

        self.tree.set_node(0, 'D', 4)
        self.tree.solve()
        self.assertEqual(self.tree.max_description_length, 9)

        self.tree[0][0]['description'] = 'short'
        self.tree.solve()
        self.assertEqual(self.tree.max_description_length, 12)

        self.tree[0][1]['description'] = 'medium-length description'
        self.tree.solve()
        self.assertEqual(self.tree.max_description_length, 32)

        self.tree[0][2]['description'] = 'a relatively long description that takes a lot of space'
        self.tree.solve()
        self.assertEqual(self.tree.max_description_length, 62)

        self.tree[0][3]['description'] = 'an incredibly, and possibly unreasonably long description that will likely cause any print function to wrap the line'
        self.tree.solve()
        self.assertEqual(self.tree.max_description_length, 123)

    def test_solution(self):
        # verify that the math all works properly for a moderately complex tree
        self.tree.set_node(0, 'D', 2)
        self.tree[0][0]['cashflow'] = 100
        self.tree[0][1]['cashflow'] = -100
        self.tree.solve()

        self.assertEqual(self.tree[0].node_value, 100)
        self.assertEqual(self.tree[0].best_branch, 0)
        self.assertEqual(self.tree[0][0]['t_probability'], 1)
        self.assertEqual(self.tree[0][1]['t_probability'], 0)

        parent = ParentID(0, 0)
        node_id = self.tree.add_node(parent, 'E', branches=2)
        self.tree[node_id][0]['cashflow'] = -300
        self.tree[node_id][0]['probability'] = .60
        self.tree[node_id][1]['cashflow'] = 400
        self.tree[node_id][1]['probability'] = .40
        # This node is worth -20
        self.tree.solve()

        self.assertEqual(self.tree[node_id].node_value, -20)
        self.assertEqual(self.tree[0].node_value, 80)
        self.assertEqual(self.tree[0].best_branch, 0)
        self.assertEqual(self.tree[node_id][0]['t_probability'], .6)
        self.assertEqual(self.tree[node_id][1]['t_probability'], .4)
        self.assertEqual(self.tree[0][1]['t_probability'], 0)

        parent = ParentID(0, 1)
        node_id = self.tree.add_node(parent, 'E', branches=4)
        self.tree[node_id][0]['cashflow'] = -500
        self.tree[node_id][0]['probability'] = .20
        self.tree[node_id][1]['cashflow'] = 1000
        self.tree[node_id][1]['probability'] = .25
        self.tree[node_id][2]['cashflow'] = -3000
        self.tree[node_id][2]['probability'] = .05
        self.tree[node_id][3]['cashflow'] = 400
        self.tree[node_id][3]['probability'] = .50
        # This node is worth 200
        self.tree.solve()

        self.assertEqual(self.tree[node_id].node_value, 200)
        self.assertEqual(self.tree[0].node_value, 100)
        self.assertEqual(self.tree[0].best_branch, 1)
        self.assertEqual(self.tree[node_id][0]['t_probability'], .2)
        self.assertEqual(self.tree[node_id][1]['t_probability'], .25)
        self.assertEqual(self.tree[node_id][2]['t_probability'], .05)
        self.assertEqual(self.tree[node_id][3]['t_probability'], .5)

    def test_wide(self):
        # Verify that a very wide tree can be created
        root_width = 15
        child_width = 15

        self.assertEqual(self.tree.width(), 1)

        self.tree.set_node(0, 'D', root_width)
        self.assertEqual(self.tree.width(), root_width)

        for branch in range(0, root_width):
            parent = ParentID(0, branch)
            self.tree.add_node(parent, 'E', branches=child_width)
            self.assertEqual(self.tree.width(), (branch + 1) * (child_width - 1) + root_width)

        self.assertEqual(self.tree.width(), child_width * root_width)
        self.assertEqual(self.tree.depth(), 2)

    def test_deep(self):
        # Verify that a very deep tree can be created
        depth = 100
        # over 973 will generate a recursion depth error on the forward_solve
        # this seems to be very sensitive to minor code changes; earlier version could do 974,
        # so we need to avoid very deep trees, but several hundred seems like plenty.

        self.tree.set_node(0, 'D', 3)
        node_id = 0
        for level in range(1, depth):
            parent = ParentID(node_id, 1)
            node_id = self.tree.add_node(parent, 'E', branches=3)

            self.assertEqual(self.tree.depth(), level + 1)
            self.assertEqual(self.tree.width(), 2 * level + 3)

        self.assertEqual(self.tree.width(), 2 * depth + 1)
        self.assertEqual(self.tree.depth(), depth)


if __name__ == '__main__':
    unittest.main()