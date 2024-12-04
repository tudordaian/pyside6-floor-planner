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





#TODO da uncomment si la editor_widget la acel TODO pt eraser
#TODO trebuie sa repari undo si redo ca sa mearga si cu eraser mode
# class ObjectCommand(QUndoCommand):
#     def __init__(self, scene, placeable_object, remove=False):
#         super().__init__()
#         self.scene = scene
#         self.placeable_object = placeable_object
#         self.remove = remove
#         self.added = not remove
#
#     def undo(self):
#         if self.added:
#             self.scene.removeItem(self.placeable_object)
#             self.added = False
#         else:
#             self.scene.addItem(self.placeable_object)
#             self.added = True
#
#     def redo(self):
#         if not self.added:
#             self.scene.addItem(self.placeable_object)
#             self.added = True
#         else:
#             self.scene.removeItem(self.placeable_object)
#             self.added = False
#