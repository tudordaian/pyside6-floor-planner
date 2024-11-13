from PySide6.QtGui import QUndoCommand

class PlaceableObjectCommand(QUndoCommand):
    def __init__(self, scene, placeable_object):
        super().__init__()
        self.scene = scene
        self.placeable_object = placeable_object
        self.added = False

    def undo(self):
        if self.added:
            self.scene.removeItem(self.placeable_object)
            self.added = False

    def redo(self):
        if not self.added:
            self.scene.addItem(self.placeable_object)
            self.added = True