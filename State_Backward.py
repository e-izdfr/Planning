class State_Backward:
    def __init__(self, child, action, positive_literals, negative_literals):
        self.child = child
        self.action = action
        self.positive_literals = positive_literals
        self.negative_literals = negative_literals

    def __eq__(self, other):
        return set(self.positive_literals) == set(other.positive_literals) and set(self.negative_literals) == \
            set(other.negative_literals)

    def __hash__(self):
        self.positive_literals.sort()
        self.negative_literals.sort()
        #return hash(''.join(self.positive_literals) + '_' + ''.join(self.negative_literals))
        return hash(''.join(self.positive_literals +  self.negative_literals + [self.child.__str__(), self.action.__str__()]))