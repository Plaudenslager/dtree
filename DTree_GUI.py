__author__ = 'peter'

import pickle
from GUI import Application, ScrollableView, Document, Window, Cursor, rgb
from GUI.Geometry import pt_in_rect, offset_rect, rects_intersect
from GUI.StdColors import black, red
from GUI.Files import FileType

from DTree import *

class DTreeApp(Application):
    """Edit DTRee Documents."""

    def __init__(self):
        Application.__init__(self)

        # Define file_type for use with Open and Save commands
        self.file_type = FileType(name = "Decision Tree Document", suffix = "dtree")

    def open_app(self):
        # Create a new, empty document when opening the application
        self.new_cmd()

    def make_document(self, fileref):
        # Used by the built-in new_cmd function, which is attached to the File:New menu
        # and may be also be called programmatically

        return DTreeDoc()

    def make_window(self, document):
        # Define the window for a document; receives a document object

        # Create the top-level window object, and associate it with the document
        # When the window is closed, the document will have a chance to ask about saving changes
        win = Window(size = (400, 400), document = document)

        # Define the view that will contain the data
        view = DTreeView(model = document,
                        extent = (1000, 1000),
                        scrolling = 'hv')

        # Position the view on the window
        # These options make the view cover the whole window, and the former resizes with the latter
        win.place(view,
                  left = 0,
                  top = 0,
                  right = 0,
                  bottom = 0,
                  sticky = 'nsew')

        # Show the window, including the view
        win.show()

class DTreeDoc(Document):
    # Define the main data structure for the document
    tree = Tree()

    def new_contents(self):
        # Gets run on a File:New command (or method call)

        # Set root node to decision with 3 branches
        # TODO: (P2) Make default starting node type and number of branches a setting in preferences
        self.tree.set_node(node_id=0, node_type='D', branches=3)

    def read_contents(self, file):
        # Gets run on a File:Open command (or method call)
        self.tree = pickle.load(file)


    def write_contents(self, file):
        # Gets run on a File:Save or File:SaveAs command (or method call)
        pickle.dump(self.tree, file)

    def walk_tree(self, node_id=0, level=0, depth=0):
        # Walk the tree (depth first) and return node details
        if node_id == 0:
            # Root node - update calculations, print root node details,
            self.solve()
            print "%s:%s bs: $%s" % (self[node_id].node_type, node_id, self[node_id].node_value)
            depth = self.depth(0)

    # TODO: (P0) Add DTree editing functions here, like Edit Node

class BlobView(ScrollableView):
    # Defines the view; this one handles two functions:
    # Drawing and user input
    # It also inherits the capabilities of the built-in ScrollableView

    def draw(self, canvas, update_rect):
        # Define how to redraw everything within update_rect

        canvas.fillcolor = red
        canvas.pencolor = black
        # Walk the tree (depth first) and print node details in tree format
        for node in self.model.tree:

class NodeImage:

    def __init__(self, x, y):
        self.size = 40
        self.rect = (x - self.size/2, y - self.size/2, x + self.size/2, y + self.size/2)

    def contains(self, x, y):
        return pt_in_rect((x, y), self.rect)

    def intersects(self, rect):
        return rects_intersect(rect, self.rect)

    def move(self, dx, dy):
        self.rect = offset_rect(self.rect, (dx, dy))

    def draw(self, canvas):
        l, t, r, b = self.rect
        canvas.newpath()
        canvas.moveto(l, t)
        canvas.lineto(r, t)
        canvas.lineto(r, b)
        canvas.lineto(l, b)
        canvas.closepath()
        canvas.fill_stroke()