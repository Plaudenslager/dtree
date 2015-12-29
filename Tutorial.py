__author__ = 'peter'
"""
Tutorial for PyGUI
From http://www.cosc.canterbury.ac.nz/greg.ewing/python_gui/version/Doc/Tutorial.html
"""

import pickle
from GUI import Application, ScrollableView, Document, Window, Cursor, rgb
from GUI.Geometry import pt_in_rect, offset_rect, rects_intersect
from GUI.StdColors import black, red
from GUI.Files import FileType


class BlobApp(Application):
    """BlobEdit edits Blob Documents. Blob Documents are documents containing Blobs. Blobs are red squares that you place by clicking and move around by dragging."""

    def __init__(self):
        Application.__init__(self)

        # Define file_type for use with Open and Save commands
        self.file_type = FileType(name = "Blob Document", suffix = "blob")

        # Define our cursor; image file is located in same directory as this .py file
        self.blob_cursor = Cursor("blob.tiff")

    def open_app(self):
        # Create a new, empty document when opening the application
        self.new_cmd()

    def make_document(self, fileref):
        # Used by the built-in new_cmd function, which is attached to the File:New menu
        # and may be also be called programmatically

        return BlobDoc()

    def make_window(self, document):
        # Define the window for a document; receives a document object

        # Create the top-level window object, and associate it with the document
        # When the window is closed, the document will have a chance to ask about saving changes
        win = Window(size = (400, 400), document = document)

        # Define the view that will contain the data
        view = BlobView(model = document,
                        extent = (1000, 1000),
                        scrolling = 'hv',
                        cursor = self.blob_cursor)

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


class BlobDoc(Document):
    # Defines the main functions and interactions for a document
    # Including standard functions like New, Open, Save
    # As well as application-specific functions

    # Define the main data structure for the document
    blobs = None

    def new_contents(self):
        # Gets run on a File:New command (or method call)
        self.blobs = []

    def read_contents(self, file):
        # Gets run on a File:Open command (or method call)
        self.blobs = pickle.load(file)

    def write_contents(self, file):
        # Gets run on a File:Save or File:SaveAs command (or method call)
        pickle.dump(self.blobs, file)

    def add_blob(self, blob):

        self.blobs.append(blob)

        # Mark document as needing to be saved
        self.changed()

        # Notify view to redraw screen
        self.notify_views()

    def move_blob(self, blob, dx, dy):
        blob.move(dx, dy)
        self.changed()
        self.notify_views()

    def delete_blob(self, blob):
        self.blobs.remove(blob)
        self.changed()
        self.notify_views()

    def find_blob(self, x, y):
        for blob in self.blobs:
            if blob.contains(x, y):
                return blob
        return None


class BlobView(ScrollableView):
    # Defines the view; this one handles two functions:
    # Drawing and user input
    # It also inherits the capabilities of the built-in ScrollableView

    def draw(self, canvas, update_rect):
        # Define how to redraw everything within update_rect
        canvas.fillcolor = red
        canvas.pencolor = black
        for blob in self.model.blobs:
            if blob.intersects(update_rect):
                # This test is not strictly necessary, because drawing is only done within update_rect,
                # but could same time if expensive calculations must be made before drawing
                blob.draw(canvas)

    def mouse_down(self, event):
        # Handles mouse clicks
        x, y = event.position
        blob = self.model.find_blob(x, y)
        if blob:
            if not event.shift:
                self.drag_blob(blob, x, y)
            else:
                self.model.delete_blob(blob)
        else:
            self.model.add_blob(Blob(x, y))

    def drag_blob(self, blob, x0, y0):
        for event in self.track_mouse():
              x, y = event.position
              self.model.move_blob(blob, x - x0, y - y0)
              x0 = x
              y0 = y


class Blob:

    def __init__(self, x, y):
        self.rect = (x - 20, y - 20, x + 20, y + 20)

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

BlobApp().run()