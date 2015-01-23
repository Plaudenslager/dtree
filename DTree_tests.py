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

if __name__ == '__main__':
    unittest.main()