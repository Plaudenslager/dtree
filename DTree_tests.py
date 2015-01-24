__author__ = 'peter'

from DTree import Tree, Node, Parent_ID
import unittest


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
        # Verify that a wide tree can be created
        root_width = 10
        self.assertEqual(self.tree.width(), 1)

        self.tree.set_node(0,'D',root_width)
        self.assertEqual(self.tree.width(), root_width)

        for branch in range(0,root_width):
            parent = Parent_ID(0, branch)
            self.tree.add_node(parent,'E', branches=10)
            self.assertEqual(self.tree.width(),(branch+1)*9+10)

        self.assertEqual(self.tree.width(), 100)
        self.assertEqual(self.tree.depth(),2)

    def test_deep(self):
        # Verify that a deep tree can be created
        depth = 10
        self.tree.set_node(0,'D', 3)
        node_ID = 0
        for level in range(1, depth):
            parent = Parent_ID(node_ID, 1)
            node_ID = self.tree.add_node(parent,'E', branches=3)

        self.assertEqual(self.tree.width(), 21)
        self.assertEqual(self.tree.depth(), 10)




if __name__ == '__main__':
    unittest.main()