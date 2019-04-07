##Currently unused, since a list would be the same
##Preferences are randomly generated over uniform distribution from 0 to 1
class Preferences:

    def __init__(self, issues, p):
        assert(issues == len(p))
        self.issues = issues
        self.p = p
