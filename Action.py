from audioop import add
from numpy import negative, positive
from requests import delete


class Action:
    def __init__(self, name, positive_preconditions, negative_preconditions , add_list, delete_list):
        self.name = name
        self.positive_preconditions = positive_preconditions
        self.negative_preconditions = negative_preconditions
        self.add_list = add_list
        self.delete_list = delete_list
    
    def __str__(self):
        self.positive_preconditions.sort()
        self.negative_preconditions.sort()
        self.add_list.sort()
        self.delete_list.sort()
        return ''.join(self.positive_preconditions + self.negative_preconditions + self.add_list + self.delete_list) + self.name