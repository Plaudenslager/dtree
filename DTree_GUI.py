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