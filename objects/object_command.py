from PySide6.QtGui import QUndoCommand

class ObjectCommand(QUndoCommand):
    def __init__(self, scene, placeable_object, remove=False):
        super().__init__()
        self.scene = scene
        self.placeable_object = placeable_object
        self.remove = remove

    def undo(self):
        if self.remove:
            self.scene.addItem(self.placeable_object)
        else:
            self.scene.removeItem(self.placeable_object)

    def redo(self):
        if self.remove:
            self.scene.removeItem(self.placeable_object)
        else:
            self.scene.addItem(self.placeable_object)