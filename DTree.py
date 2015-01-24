__author__ = 'peter'

import uuid

class Parent_ID:
    def __init__(self, node_ID, branch_number):
        self.node_ID = node_ID
        self.branch_number = branch_number

class Node:
    def __init__(self, node_type='D', ID=None):
        node_type = node_type.upper()
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

    def change_node(self):
        if self.node_type == 'E':
            self.node_type = 'D'
        else:
            self.node_type = 'E'

    @property
    def best_node(self):
        a = self.node_value()
        return self._best_node

    @property
    def node_value(self):
        if self.node_type == 'E':
            self.best_node = None
            p = [b['probability'] for b in self.branches]
            if None in p or sum(p) <> 1:
                return None
            else:
                a = [b['backsolve'] for b in self.branches]
                if None in a:
                    return None
                else:
                    return round(sum(a),2)

        else:
            a = [b['backsolve'] for b in self.branches]
            if None in a:
                return None
            else:
                max_value = max(a)
                for index, value in enumerate(a):
                    if value == max_value:
                        self._best_node = index
                        return round(max_value,2)

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
        self.nodes[0].parent = Parent_ID(0,0)

    def set_node(self, node_ID, node_type, branches, warn=True):
        if node_ID not in self.nodes:
            return
        self.clear_node(node_ID)
        node = self[node_ID]
        if node.node_type <> node_type:
            node.change_node()
        p = 1.0/branches
        while branches > 0:
            self.add_branch(node_ID,probability=p)
            branches -= 1

    def clear_node(self, node_ID):
        while self[node_ID].width >0:
            self.del_branch(node_ID)

    def add_node(self, parent_ID, node_type='D', ID=None, branches=2):
        if self[parent_ID.node_ID][parent_ID.branch_number]['child'] is not None:
            print "***** WTF tried to add a node where one already exists ******"
            return
        branches = max(2,branches)
        node = Node(node_type,ID)
        node.parent = parent_ID
        self.nodes[node.ID] = node
        self.__update_parent(node.ID)
        for b in range(0, branches):
            p = 1.0 / branches
            node.add_branch(description=None, cashflow=0, probability=p)
        self.__forward_solve()
        return node.ID

    def del_node(self, node_ID):
        self.clear_node(node_ID)
        self.__update_parent(node_ID, clear=True)
        del self.nodes[node_ID]
        self.__forward_solve()

    def add_branch(self, node_ID, description=None, cashflow=0, probability=0.0):
        node = self[node_ID]
        node.add_branch(description=description, cashflow=cashflow, probability=probability)
        self.__forward_solve()

    def del_branch(self, node_ID):
        #Can only delete last branch
        branch_number = self[node_ID].width-1
        if branch_number <0:
            return
        branch = self[node_ID].branches[branch_number]
        if branch['child'] is not None:
            self.del_node(branch['child'])
            if branch['child'] is not None:
                print "********* WTF deleted child node, but is still listed in parent branch *********"

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
            self.__forward_solve()
            print "%s:%s bs: $%d" %(self[node_ID].node_type,node_ID, self[node_ID].node_value)
            depth = self.depth(0)
        if self[node_ID].width > 0:
            level += 1
            for branch in self[node_ID].branches:
                #print "\t"*level, branch
                if branch['child'] == None:
                    spacer_string = "-"*(8*depth-4*level)+">"
                    print "\t"*level,"%s cf: $%d, p: %.1f%%, bs: $%d %s %d" % (branch['description'], branch['cashflow'],
                                                                   branch['probability']*100, branch['backsolve'],
                                                                   spacer_string, branch['t_value'])
                else:
                    print "\t"*level,"%s cf: $%d, p: %.1f%%, bs: $%d\t%s:%s" %(branch['description'],branch['cashflow'],
                                                                         branch['probability']*100, branch['backsolve'],
                                                                         self[branch['child']].node_type, branch['child'])
                    self.display(branch['child'],level+1,depth)

    def depth(self,node_ID=0):
        max_depth = 1
        if self[node_ID].width > 0:
            for branch in self[node_ID].branches:
                if branch['child'] is not None:
                    branch_depth = self.depth(branch['child']) + 1
                    max_depth = max(max_depth, branch_depth)
        return max_depth

    def solve(self):
        self.__forward_solve(0,0)

    def __forward_solve(self, node_ID=0, cashflow=0):
        if self[node_ID].width > 0:
            for index, branch in enumerate(self[node_ID].branches):
                cf = cashflow + branch['cashflow']
                if branch['child'] is not None:
                    downstream_investments = self.__forward_solve(branch['child'], cf)
                    if downstream_investments is None:
                        backsolve = None
                    else:
                        backsolve = branch['cashflow'] + downstream_investments
                else:
                    branch['t_value'] = cf
                    backsolve = branch['cashflow']

                self[node_ID].update_backsolve(index, backsolve)

            return self[node_ID].node_value

    def __update_parent(self, child_node_ID, clear=False):
        parent_ID = self[child_node_ID].parent
        if clear:
            self[parent_ID.node_ID].branches[parent_ID.branch_number]['child'] = None
        else:
            self[parent_ID.node_ID].branches[parent_ID.branch_number]['child'] = child_node_ID

    def __getitem__(self, item):
        if item not in self.nodes:
            print "***** WTF tried to get a non-existent node ID: %s", item
        return self.nodes[item]

def InteractiveTreeMain():
    # provide interactive command line for interacting with a tree
    pass

def CommandLoop():
    cmd = None
    while cmd not in ['D','E']:
        cmd_string = raw_input('Enter D# or E# to create a new Decision or Event with # branches >')
        cmd = cmd_string[0].upper()
        branches = int(cmd_string[1:])
    tree = Tree()
    tree.set_node(0,cmd,branches)
    tree.display()

    node_ID = 0
    while cmd_string not in ['q','Q']:
        branch = None
        while branch not in range(0,tree[node_ID].width):
            #TODO: fix function to go up to parent node - currently breaks the branch selection loop
            cmd_string = raw_input('Enter branch number to edit, or U to move up to parent node >')
            if cmd_string[0].upper() == 'U':
                print '(now operating on node: %s)' %node_ID
                node_ID = tree[node_ID][branch].parent.node_ID
                continue
            else:
                branch = int(cmd_string)

        cmd_string = raw_input('Enter cf#, p#, D#, or E# to set cashflow, probability, D or E; C to enter child node>')
        if cmd_string[0] == 'C':
            c_ID = tree[node_ID][branch]['child']
            if c_ID is not None:
                node_ID = tree[node_ID][branch]['child']
                print '(now operating on node: %s)' %node_ID

        if cmd_string[0:2] == 'cf':
            tree[node_ID][branch]['cashflow'] = int(cmd_string[2:])
            print '(set node %s branch %d cashflow to $%d)' %(node_ID, branch, int(cmd_string[2:]))
        if cmd_string[0] == 'p':
            tree[node_ID][branch]['probability'] = float(cmd_string[1:])
            print '(set node %s branch %d probability to %f%%)' %(node_ID, branch, float(cmd_string[1:]))
        if cmd_string[0].upper() in ['D','E']:
            cmd = cmd_string[0].upper()
            branches = int(cmd_string[1:])
            parent=Parent_ID(node_ID,branch)
            tree.add_node(parent, cmd, branches=branches)
            print '(add %s node with %d branches to branch %d )' %(cmd, int(cmd_string[1:]), branch)


        tree.display()


if __name__ == '__main__':
    CommandLoop()

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