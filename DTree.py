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

class Node:
    def __init__(self, node_type='D', ID=None):
        if node_type not in ['D','E']: return

        if ID == None:
            self.ID = str(uuid.uuid1())
        else:
            self.ID = str(ID).strip().lower().replace(" ","")

        self.branches = []
        self.__parent = None
        self.node_type = node_type

    def add_branch(self, name=None, cashflow=0, probability=0):
        if name==None:
            name = self.node_type+str(len(self.branches))
        branch = dict(name=name, cashflow=cashflow, backsolve=0, probability=probability, child=None)
        self.branches.append(branch)

    def del_branch(self, branch_number):
        del self.branches[branch_number]

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, parent_node_ID, branch_number):
        self.__parent = (parent_node_ID, branch_number)

    @property
    def width(self):
        total_width = len(self.branches)
        for current_branch in self.branches:
            if current_branch['child'] is not None:
                branch_width = self.width(current_branch)
                current_branch = current_branch - 1 + branch_width
        return total_width

    @property
    def backsolve(self, branch_number):
        return self.branches[branch_number]['backsolve']

    @backsolve.setter
    def backsolve(self, branch_number, value):
        self.branches[branch_number]['backsolve'] = value

    def get_branch_number(self, branch_name):
        if branch_name in self.branches:
            return self.branches.index(branch_name)
        else:
            return None


class Tree(object):
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