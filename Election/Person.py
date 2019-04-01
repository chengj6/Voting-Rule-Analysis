##Voters have a list of preferences over the issues
class Person:
    def __init__(self):
        self.pref = None
        self.id = None

    def __init__(self, pref, id):
        self.id = id
        self.pref = pref
