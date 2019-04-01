class Preference:
    def __init__(self):
        self.issues = 0
        self.p = []

    def __init__(self, issues, p):
        assert(issues == len(p))
        self.issues = issues
        self.p = p
