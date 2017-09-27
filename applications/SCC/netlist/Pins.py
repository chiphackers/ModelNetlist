from .nlNode import nlNode

class Pin(nlNode):
    """
    Generic Pin Class
    """
    def __init__(self, name, parent):
        super().__init__('PIN', name, parent)

