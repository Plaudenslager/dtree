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


from Tkinter import *
class Application(Frame):

    def say_hi(self):
        print "Type change"

    def say_add(self):
        print "Add branch"

    def say_node(self):
        print "Add node"

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
        self.add_branch["command"] = self.say_add
        self.add_branch.pack({"side": "left"})

        self.add_node = Button(self)
        self.add_node["text"] = "Add Node"
        self.add_node["command"] = self.say_node
        self.add_node.pack({"side": "left"})

        self.w.create_line(0,0,600,600)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()