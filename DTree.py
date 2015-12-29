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

import uuid


class ParentID:
    def __init__(self, node_id, branch_number):
        self.node_id = node_id
        self.branch_number = branch_number


class Node:
    def __init__(self, node_type='D', guid=None):
        node_type = node_type.upper()
        if node_type not in ['D', 'E']:
            raise ReferenceError('Illegal node type: {}'.format(node_type))

        if guid is None:
            self.ID = str(uuid.uuid1())
        else:
            self.ID = str(guid).strip().lower().replace(" ", "")

        self.branches = []
        self.node_type = node_type
        self.__parent_ID = None
        self._best_branch = None

    def add_branch(self, description=None, cashflow=0, probability=0.0):
        if description is None:
            description = self.node_type + str(len(self.branches))
        branch = dict(description=description, cashflow=cashflow, backsolve=0, probability=probability, child=None,
                      t_value=0, t_probability=0)
        self.branches.append(branch)

    def del_branch(self, branch_number):
        del self.branches[branch_number]

    def change_node(self):
        if self.node_type == 'E':
            self.node_type = 'D'
        else:
            self.node_type = 'E'

    def sensitivity(self):
        # run through the nodes,
        # figure out the required change to each cashflow to change decision
        # then run through the backsloves for the same reason

        # get the number to beat
        best_node_cashflow = self.branches[self.best_branch]['cashflow']
        for branch in self.branches:
            branch['cf_delta'] = best_node_cashflow - branch['cashflow']
        # this will give the current best node a sensitivity of 0,
        # but it should be the difference between its own cashflow and the next best cashflow
        # TODO: calculate the correct sensitivity for the current best node
        # TODO: calculate the sensitivity for event nodes

    @property
    def best_branch(self):
        # getting the node_value calculates and sets the private value for _best_branch
        self.node_value
        return self._best_branch

    @property
    def node_value(self):
        if self.width == 0:
            return 0
        if self.node_type == 'E':
            self._best_branch = None
            p = [b['probability'] for b in self.branches]
            if None in p or sum(p) != 1:
                return None
            else:
                a = [b['backsolve'] for b in self.branches]
                if None in a:
                    return None
                else:
                    return round(sum(a), 2)

        else:
            a = [b['backsolve'] for b in self.branches]
            if None in a:
                return None
            else:
                max_value = max(a)
                for index, value in enumerate(a):
                    if value == max_value:
                        self._best_branch = index
                        return round(max_value, 2)

    # @property
    # def t_value(self,branch_number):
    # return self.branches[branch_number]['t_value']

    # @t_value.setter
    # def t_value(self,branch_number,value):
    # self.branches[branch_number]['t_value'] = value

    # @property
    # def child(self, branch_number):
    # return self.branches[branch_number]['child']

    # @child.setter
    # def child(self, branch_number, value):
    #     self.branches[branch_number]['child'] = value

    @property
    def parent(self):
        return self.__parent_ID

    @parent.setter
    def parent(self, parent_id):
        self.__parent_ID = parent_id

    @property
    def width(self):
        return len(self.branches)

    def update_backsolve(self, branch_number, value):
        if value is not None and self.node_type == 'E':
            self.branches[branch_number]['backsolve'] = value * self.branches[branch_number]['probability']
        else:
            self.branches[branch_number]['backsolve'] = value

    # def branch_number(self, branch_name):
    #     a = [item['description'] for item in self.branches]
    #     return a.index(branch_name)

    def __getitem__(self, item):
        return self.branches[item]


class Tree():
    def __init__(self):
        # K,V in nodes dictionary is ID, node object
        self.nodes = dict()

        # Create root node
        root = Node(guid=0)
        self.nodes[0] = root
        self.nodes[0].parent = ParentID(0, 0)
        self.__max_description_length = 0

    @property
    def max_description_length(self):
        # used to format displays with aligned text
        return self.__max_description_length

    def set_node(self, node_id, node_type, branches):
        """ Change the type and number of branches on an existing node.
            Destroys any existing child branches.
            Typically used to configure a newly created node.

        :param node_id: Required existing node_id; if the ID doesn't exist, do nothing and return.
        :param node_type: Required single character; 'D' for decision, or 'E' for event
        :param branches: Required number of branches exiting the node (i.e. possible choices or event outcomes)
        :return: Nothing; data in Tree object is updated directly
        """
        # Make sure node exists - if not, do nothing
        if node_id not in self.nodes:
            return

        # Clear any child branches
        self.clear_node(node_id)
        node = self[node_id]

        # Ensure type is correct, change if necessary
        if node.node_type != node_type:
            node.change_node()

        # Calculate default probability for each branch (uniform across branches)
        p = 1.0 / branches

        # Add specified number of branches
        while branches > 0:
            self.add_branch(node_id, probability=p)
            branches -= 1

    def clear_node(self, node_id):
        # Deletes any child branches
        while self[node_id].width > 0:
            self.del_branch(node_id)

    def add_node(self, parent_id, node_type='D', guid=None, branches=2):
        """ Add a new node as a child of parent_id.  Raises ReferenceError if a node already exists on that branch.
        :param parent_id: Required object that contains a node_id and a branch number.
        :param node_type: Optional single character; 'D' for decision (default), or 'E' for event
        :param guid: Optional node_id.  Will be auto-generated by default.
        :param branches: Optional number of branches.  Defaults to 2.
        :return: node_id for the newly created node.
        """
        if self[parent_id.node_id][parent_id.branch_number]['child'] is not None:
            raise ReferenceError(
                'Tried to add a child node to branch {} of node {} that already has a child node {}'.format(
                    parent_id.node_id, parent_id.branch_number,
                    self[parent_id.node_id][parent_id.branch_number]['child']))

        branches = max(2, branches)
        if guid is None:
            guid = len(self.nodes)
        node = Node(node_type, guid)
        if node.ID in self.nodes:
            raise ReferenceError('Duplicate node ID: {}'.format(node.ID))

        node.parent = parent_id
        self.nodes[node.ID] = node
        self.__update_parent(node.ID)
        for b in range(0, branches):
            p = 1.0 / branches
            node.add_branch(description=None, cashflow=0, probability=p)
        self.solve()
        return node.ID

    def del_node(self, node_id):
        self.clear_node(node_id)
        self.__update_parent(node_id, clear=True)
        del self.nodes[node_id]
        self.solve()

    def add_branch(self, node_id, description=None, cashflow=0, probability=0.0):
        node = self[node_id]
        node.add_branch(description=description, cashflow=cashflow, probability=probability)
        self.solve()

    def del_branch(self, node_id):
        # Can only delete last branch
        branch_number = self[node_id].width - 1
        if branch_number < 0:
            raise ReferenceError('Illegal branch number {}'.format(branch_number))

        branch = self[node_id].branches[branch_number]
        if branch['child'] is not None:
            self.del_node(branch['child'])
            if branch['child'] is not None:
                raise ReferenceError('failed to delete child node')

        self[node_id].del_branch(branch_number)
        self.__forward_solve()

    def width(self, node_id=0):
        total_width = self[node_id].width
        if total_width > 0:
            for branch in self[node_id].branches:
                if branch['child'] is not None:
                    child_width = self.width(branch['child'])
                    if child_width > 0:
                        total_width += child_width - 1
        return max(total_width, 1)

    def display(self, node_id=0, level=0, depth=0):
        # Walk the tree (depth first) and print node details in tree format
        if node_id == 0:
            # Root node - update calculations, print root node details,
            self.solve()
            print "%s:%s bs: $%s" % (self[node_id].node_type, node_id, self[node_id].node_value)
            depth = self.depth(0)
        if self[node_id].width > 0:
            level += 1
            for branch in self[node_id].branches:
                if branch['child'] is None:
                    # Print the terminal value for this path through the tree
                    text_len = self.max_description_length - branch['text_len']
                    spacer_string = "-" * (8 * depth - 4 * level + text_len) + ">"
                    print "\t" * level, "%s cf: $%d, p: %.1f%%, bs: $%d %s %d (%.1f%%)" % (
                        branch['description'], branch['cashflow'],
                        branch['probability'] * 100, branch['backsolve'],
                        spacer_string, branch['t_value'], branch['t_probability'] * 100)
                else:
                    # Print node details for this node, and call the display function again for this node
                    print "\t" * level, "%s cf: $%d, p: %.1f%%, bs: $%s\t%s:%s" % (
                        branch['description'], branch['cashflow'],
                        branch['probability'] * 100, branch['backsolve'],
                        self[branch['child']].node_type, branch['child'])
                    self.display(branch['child'], level + 1, depth)

    def depth(self, node_id=0):
        max_depth = 1
        if self[node_id].width > 0:
            for branch in self[node_id].branches:
                if branch['child'] is not None:
                    branch_depth = self.depth(branch['child']) + 1
                    max_depth = max(max_depth, branch_depth)
        return max_depth

    def describe_tree(self):
        # TODO: Build function to describe recommendations from tree
        pass

    # Todo: Factor out depth-first, width-first searches for use with other functions, like solve & describe


    def sensitivity_analysis(self, node_id=0, data=0):
        '''
        For a node, calculate the change to each cashflow to shift the decision
        For events, calculate the change to each probability to shift the upstream decision
        calculate how much each backsolve must change to shift the upstream decision
        '''

        if self[node_id].width < 1:
            return
        self[node_id].sensitivity()

    def solve(self):
        self.__forward_solve(0, 0)
        self.__solve_probability(0, 1)

    def __solve_probability(self, node_id=0, probability=1):
        if self[node_id].width < 1:
            return

        if node_id == 0:
            self.__max_description_length = 0

        for index, branch in enumerate(self[node_id].branches):
            branch['text_len'] = 0
            for item in ['description', 'cashflow', 'probability', 'backsolve', 't_value']:
                branch['text_len'] += len(str(branch[item]))
            self.__max_description_length = max(branch['text_len'], self.__max_description_length)

            best_branch = self[node_id].best_branch
            # probability is product of all previous probabilities
            if self[node_id].node_type == 'D':
                if index == best_branch:
                    p = probability
                else:
                    p = 0
            else:
                p = probability * branch['probability']

            if branch['child'] is not None:
                self.__solve_probability(node_id=branch['child'], probability=p)
            else:
                branch['t_probability'] = p

    def __forward_solve(self, node_id=0, cashflow=0):
        """

        :param node_id: the node to be calculated
        :param cashflow: cashflows accumulated from parent node
        :return: backsolve value

        forward solve adds up all the cashflows along a particular path from root to end leaf
        back solve adds up all the downstream costs of a particular branch,
        using expected values for downstream events, and best choice values for downstream decisions

        This function typically starts with the root node and 0 cashflow,
        then walks down all the paths passing the cashflows forward until it reaches the last branch.
        Terminal value is calculated and updated, backsolve value is calculated, updated, and returned
        to the caller (usually the previous instance of this function)
        """
        if self[node_id].width > 0:
            for index, branch in enumerate(self[node_id].branches):
                # forward solve is the sum of all previous cashflows plus this cashflow
                cf = cashflow + branch['cashflow']
                if branch['child'] is not None:
                    downstream_investments = self.__forward_solve(branch['child'], cf)
                    if downstream_investments is None:
                        backsolve = None
                    else:
                        backsolve = branch['cashflow'] + downstream_investments
                else:
                    # Calculation for a leaf node
                    # forward solve is the sum of all previous cashflows
                    branch['t_value'] = cf
                    backsolve = branch['cashflow']

                self[node_id].update_backsolve(index, backsolve)

            # Need to return the backsolve value
            return self[node_id].node_value

    def __update_parent(self, child_node_id, clear=False):
        assert child_node_id in self.nodes
        parent_id = self[child_node_id].parent
        assert parent_id.branch_number < len(self[parent_id.node_id].branches)
        if clear:
            self[parent_id.node_id].branches[parent_id.branch_number]['child'] = None
        else:
            self[parent_id.node_id].branches[parent_id.branch_number]['child'] = child_node_id

    def __getitem__(self, item):
        if item not in self.nodes:
            print "***** WTF tried to get a non-existent node ID: %s", item
        return self.nodes[item]

def command_loop():
    cmd = None
    while cmd not in ['D', 'E']:
        cmd_string = raw_input('Enter D# or E# to create a new Decision or Event with # branches >')
        cmd = cmd_string[0].upper()
        branches = int(cmd_string[1:])
    tree = Tree()
    tree.set_node(0, cmd, branches)  # TODO: code analysis says this could be referenced before assignment
    tree.display()

    node_id = 0
    while cmd_string not in ['q', 'Q']:  # TODO: code analysis says this could be referenced before assignment
        branch = None
        while branch not in range(0, tree[node_id].width):
            # TODO: fix function to go up to parent node - currently breaks the branch selection loop
            cmd_string = raw_input('Enter branch number to edit, or U to move up to parent node >')
            if cmd_string[0].upper() == 'U':
                print '(now operating on node: %s)' % node_id
                node_id = tree[node_id][branch].parent.node_id
                continue
            else:
                branch = int(cmd_string)

        cmd_string = raw_input('Enter cf#, p#, D#, or E# to set cashflow, probability, D or E; C to enter child node>')
        if cmd_string[0] == 'C':
            c_id = tree[node_id][branch]['child']
            if c_id is not None:
                node_id = tree[node_id][branch]['child']
                print '(now operating on node: %s)' % node_id

        if cmd_string[0:2] == 'cf':
            tree[node_id][branch]['cashflow'] = int(cmd_string[2:])
            print '(set node %s branch %d cashflow to $%d)' % (node_id, branch, int(cmd_string[2:]))
        if cmd_string[0] == 'p':
            tree[node_id][branch]['probability'] = float(cmd_string[1:])
            print '(set node %s branch %d probability to %f%%)' % (node_id, branch, float(cmd_string[1:]))
        if cmd_string[0].upper() in ['D', 'E']:
            cmd = cmd_string[0].upper()
            branches = int(cmd_string[1:])
            parent = ParentID(node_id, branch)
            tree.add_node(parent, cmd, branches=branches)
            print '(add %s node with %d branches to branch %d )' % (cmd, int(cmd_string[1:]), branch)

        tree.display()


if __name__ == '__main__':
    command_loop()

