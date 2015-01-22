__author__ = 'peter'

'''
Structure
    EdgeDict1(Name, Cashflow, Backsolve, Probability, Child_node)
    Node(Type, EdgeDict1, EdgeDict2, EdgeDict3)
    Tree(Node1, Node2, Node3)

Operations
    Change node type
    Add branch
    Delete branch

Background tasks
    Calculate back solve
    Calculate terminal
    Identify best option
'''
import uuid

class Parent_ID:
    def __init__(self, node_ID, branch_number):
        self.node_ID = node_ID
        self.branch_number = branch_number

class Node:
    def __init__(self, node_type='D', ID=None):
        if node_type not in ['D','E']: return

        if ID == None:
            self.ID = str(uuid.uuid1()).split("-")[3]
        else:
            self.ID = str(ID).strip().lower().replace(" ","")

        self.branches = []
        self.__parent_ID = None
        self.node_type = node_type

    def add_branch(self, description=None, cashflow=0, probability=0.0):
        if description==None:
            description = self.node_type+str(len(self.branches))
        branch = dict(description=description, cashflow=cashflow, backsolve=0, probability=probability, child=None, t_value=0)
        self.branches.append(branch)

    def del_branch(self, branch_number):
        del self.branches[branch_number]

    @property
    def best_node(self):
        a = self.node_value()
        return self._best_node

    @property
    def node_value(self):
        if self.node_type == 'E':
            self.best_node = None
            p = [b['probability'] for b in self.branches]
            if sum(p) <> 1:
                return None
            else:
                a = [b['backsolve'] for b in self.branches]
                return sum(a)
        else:
            a = [b['backsolve'] for b in self.branches]
            max_value = max(a)
            for index, value in enumerate(a):
                if value == max_value:
                    self._best_node = index
                    return max_value

    @property
    def t_value(self,branch_number):
        return self.branches[branch_number]['t_value']

    @t_value.setter
    def t_value(self,branch_number,value):
        self.branches[branch_number]['t_value'] = value

    @property
    def child(self, branch_number):
        return self.branches[branch_number]['child']

    @child.setter
    def child(self, branch_number, value):
        self.branches[branch_number]['child'] = value

    @property
    def parent(self):
        return self.__parent_ID

    @parent.setter
    def parent(self, parent_node_ID, branch_number):
        self.__parent_ID = Parent_ID(parent_node_ID, branch_number)

    @property
    def width(self):
        return len(self.branches)

    def update_backsolve(self, branch_number, value):
        if value is not None and self.node_type == 'E':
            self.branches[branch_number]['backsolve'] = value * self.branches[branch_number]['probability']
        else:
            self.branches[branch_number]['backsolve'] = value

    def branch_number(self, branch_name):
        a = [item['description'] for item in self.branches]
        return a.index(branch_name)

    def __getitem__(self, item):
        return self.branches[item]


class Tree():
    def __init__(self):
        # K,V in nodes dictionary is ID, node object
        self.nodes = dict()

        # Create root node
        root = Node(ID=0)
        self.nodes[0] = root

    def add_node(self, parent_ID, node_type='D', ID=None, branches=2):
        branches = max(2,branches)
        node = Node(node_type,ID)
        node.parent = parent_ID
        self.__update_parent(parent_ID,node.ID)
        self.nodes[node.ID] = node
        for b in range(0, branches):
            p = 1.0 / branches
            node.add_branch(description=None, cashflow=0, probability=p)
        self.__forward_solve()
        return node.ID

    def del_node(self, node_ID):
        if self[node_ID].width > 0:
            for branch_number in range(0,self[node_ID].width):
                self.del_branch(node_ID,branch_number)
        parent = self[node_ID].parent
        self[parent.node_ID].branches[parent.branch_number]['child'] = None
        self[node_ID].delete()
        self.__forward_solve()

    def add_branch(self, node_ID, description=None, cashflow=0, probability=0.0):
        node = self[node_ID]
        node.add_branch(description=description, cashflow=cashflow, probability=probability)
        self.__forward_solve()

    def del_branch(self, node_ID, branch_number):
        if branch_number > self[node_ID].width+1:
            return
        else:
            branch = self[node_ID].branches[branch_number]
            if branch['child'] is not None:
                self.del_node(branch['child'])
            self[node_ID].del_branch(branch_number)
            self.__forward_solve()

    def width(self, node_ID=0):
        total_width = self[node_ID].width
        if total_width > 0:
            for branch in self[node_ID].branches:
                if branch['child'] is not None:
                    child_width = self.width(branch['child'])
                    if child_width > 0:
                        total_width += child_width -1
        return max(total_width,1)

    def display(self,node_ID=0,level=0, depth=0):
        if node_ID == 0:
            print "%s:%s" %(self[node_ID].node_type,node_ID)
            depth = self.depth(0)
        if self[node_ID].width > 0:
            level += 1
            for branch in self[node_ID].branches:
                #print "\t"*level, branch
                if branch['child'] == None:
                    spacer_string = "-"*(8*depth-4*level)+">"
                    print "\t"*level,"%s cf: %d, p: %d, bs: %d %s %d" % (branch['description'], branch['cashflow'],
                                                                   branch['probability']*100, branch['backsolve'],
                                                                   spacer_string, branch['t_value'])
                else:
                    print "\t"*level,"%s\t%s:%s" %(branch['description'],self[branch['child']].node_type, branch['child'])
                    self.display(branch['child'],level+1,depth)

    def depth(self,node_ID=0):
        max_depth = 1
        if self[node_ID].width > 0:
            for branch in self[node_ID].branches:
                if branch['child'] is not None:
                    branch_depth = self.depth(branch['child']) + 1
                    max_depth = max(max_depth, branch_depth)
        return max_depth

    def __forward_solve(self, node_ID=0, cashflow=0):
        if self[node_ID].width > 0:
            for index, branch in enumerate(self[node_ID].branches):
                cashflow += branch['cashflow']
                if branch['child'] is not None:
                    backsolve = self.__forward_solve(branch['child'], cashflow)
                else:
                    branch['t_value'] = cashflow
                    backsolve = branch['t_value']

                self[node_ID].update_backsolve(index, backsolve)

            return self[node_ID].node_value

    def __update_parent(self, parent_ID, child_node_ID):
        self[parent_ID.node_ID].branches[parent_ID.branch_number]['child'] = child_node_ID

    def __getitem__(self, item):
        return self.nodes[item]








class Old_Tree(object):
    def __init__(self, node_type='D'):
        # Types are: Decision, Event (first initial only)
        # Data structure:
            # Decision: name, cashflow, backsolve, child_node
            # Event: name, cashflow, backsolve, probability, child_node
        self.data = {'type':node_type}
        self.add()
        self.add()

    def add(self):
        next_branch = len(self.data)
        if self.data['type'] == 'D':
            d_name = 'Decision %d' % next_branch
            self.data[next_branch] = dict(name=d_name, cashflow=0, backsolve=0)

        if self.data['type'] == 'E':
            d_name = 'Event %d' % next_branch
            self.data[next_branch] = dict(name=d_name, cashflow=0, backsolve=0, probability=0)

    def change(self,desired_type):
        node_type = self.data['type']

        # check for illegal options
        if node_type == desired_type:
            # Cannot change a node to the same type
            return('error')

        # legal options
        if desired_type == 'D':
            self.data['type'] = 'D'
            del self.data['probability']

        if desired_type == 'T':
            selected_node['type'] = 'T'
            selected_node['probability'] = 0
            return()

    def extend(self, branch, node_type):
        if branch not in self.data:
            return('error')
        if 'child' not in self.data[branch]:
            self.data[branch]['child'] = Tree(node_type)
        else:
            return('error')

    def width(self):
        # depth first search
        # how many leafs on this node?
        current_width = len(self.data)
        current_branch = 1
        while len(self.data) > current_branch:
            if 'child' in self.data[current_branch]:
                child_width = self.width

class Edge():
    '''
    Treat the edges of the decision tree as the nodes.
    Decision and Event nodes contain data, plus the node type for the child node
    Root node is special type that contains only backsolve and child node type
    '''

    def __init__(self, parent_ID, node_type, description, cashflow, probability=None):
        self.parent_ID = parent_ID
        self.node_type = node_type
        self.description = description
        self.cashflow = cashflow
        self.probability = probability
        self.child_ID = None
        self.backsolve = 0
        self.solve = 0




from Tkinter import *
class Application(Frame):

    def say_hi(self):
        print "Type change"

    def do_branch(self):
        print "Add branch"
        self.draw_edge(2,self.column-1,1,1)


    def do_node(self):
        print "Add node"
        row=2
        self.draw_node('D',row,self.column)
        self.column += 1

    def createWidgets(self):
        self.w = Canvas(self, width=600, height=600)
        self.w.pack()

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit
        self.QUIT.pack({"side": "left"})

        self.change = Button(self)
        self.change["text"] = "Change Type"
        self.change["command"] = self.say_hi
        self.change.pack({"side": "left"})

        self.add_branch = Button(self)
        self.add_branch["text"] = "Add Branch"
        self.add_branch["command"] = self.do_branch
        self.add_branch.pack({"side": "left"})

        self.add_node = Button(self)
        self.add_node["text"] = "Add Node"
        self.add_node["command"] = self.do_node
        self.add_node.pack({"side": "left"})

    def draw_node(self,node_type,row,column):
        start_x = column*self.column_width
        start_y = row*self.node_size
        end_x = start_x+self.node_size
        end_y = start_y+self.node_size

        if node_type == 'D':
            print "drawing decision node at row: %d, column: %d" %(row,column)
            self.w.create_rectangle(start_x,start_y,end_x,end_y)
        if node_type == 'E':
            print "drawing event node at row: %d, column: %d" %(row,column)
            self.w.create_oval(start_x,start_y,end_x,end_y)

    def draw_edge(self, row, column, edge_count, edge_no):
        start_x = column*self.column_width+self.node_size
        start_y = row*self.node_size+int(self.node_size*edge_no/(edge_count+1))
        end_x = start_x+self.node_size*2
        end_y = (row+(edge_no/edge_count+1))*self.node_size
        self.w.create_line(start_x,start_y,end_x,end_y)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.column = 1
        self.node_size = 20
        self.column_width = 5*self.node_size


# root = Tk()
# app = Application(master=root)
# app.mainloop()
# root.destroy()