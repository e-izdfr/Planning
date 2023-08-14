class State_Forward:
    def __init__(self, parent, action, positive_literals, path_cost=0, heuristic_cost=0):
        self.parent = parent
        self.action = action
        self.positive_literals = positive_literals
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost

    def __str__(self):
        return ''.join(self.positive_literals + [self.parent.__str__(), self.action.__str__()])
    
    def __eq__(self, other):
        return set(self.positive_literals) == set(other.positive_literals)

    def __hash__(self):
        self.positive_literals.sort()
        #return hash(''.join(self.positive_literals))
        return hash(''.join(self.positive_literals + [self.parent.__str__(), self.action.__str__()]))