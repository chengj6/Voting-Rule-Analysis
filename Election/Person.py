##Voters have a list of preferences over the issues
##Id represents their 'identifier' and voter is a boolean value
class Person:
    def __init__(self):
        self.pref = None
        self.id = None
        self.voter = None

    def __init__(self, pref, id, voter):
        self.voter = voter
        self.id = id
        self.pref = pref
