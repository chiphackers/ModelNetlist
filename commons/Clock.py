class Clock:
    def __init__(self,name):
        self.name = name
        self.outputs = []

    def set_outputs(self,pin):
        self.outputs.append(pin)

