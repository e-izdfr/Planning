import itertools
from State_Forward import *
from State_Backward import *
from Action import *

def goal_test(node, goal_schema):
    if set(goal_schema[0]).issubset(node.positive_literals) and not any(element in node.positive_literals for element in
                                                                        goal_schema[1]):
        return True
    
    else:
        return False

def Filter_Actions(node, action):
    if set(action.positive_preconditions).issubset(node.positive_literals) and not any(element in node.positive_literals for element in
                                                                                      action.negative_preconditions):
        return True
    
    else:
        return False

def Applicable_Actions(node, actions):
    return list(filter(lambda x: Filter_Actions(node, x), actions))

def Forward_State_Space_Search(initial_state, goal_schema, actions):
    frontier = [initial_state]
    explored_set = set()
    
    while(True):
        if len(frontier) == 0:
            return 'failure'
        node = frontier.pop(0)
        explored_set.add(hash(node))
        if goal_test(node, goal_schema):
            solution = []
            g = node
            while(g is not None):
                solution.append(g)
                g = g.parent
            return [s.action.name for s in solution[::-1][1:]]
        
        for action in Applicable_Actions(node, actions):
            child = State_Forward(node, action, [n for n in list(set(node.positive_literals + action.add_list)) if n not in
                                                 action.delete_list])
            if hash(child) not in explored_set:
                frontier.append(child)

def goal_test2(node, initial_state):
    if set(node.positive_literals).issubset(initial_state.positive_literals) and not any(element in initial_state.positive_literals 
                                                                                         for element in node.negative_literals):
        return True
    
    else:
        return False

def Filter_Actions2(node, action):
    if not any(element in node.positive_literals for element in action.delete_list) and not any(element in node.negative_literals for
                                                                                                element in
                                                                                                action.add_list):
        return True
    
    else:
        return False

def Applicable_Actions2(node, actions):
    return list(filter(lambda x: Filter_Actions2(node, x), actions))

def Backward_State_Space_Search(initial_state, goal_schema, actions):
    goal = State_Backward(None, None, goal_schema[0], goal_schema[1])
    frontier = [goal]
    explored_set = set()
    while(True):
        if len(frontier) == 0:
            return 'failure'
        node = frontier.pop(0)
        explored_set.add(hash(node))
        if goal_test2(node, initial_state):
            solution = [initial_state]
            g = node
            while(g is not None):
                solution.append(g)
                g = g.child
            return [s.action.name for s in solution[1:len(solution) - 1]]
        
        for action in Applicable_Actions2(node, actions):
            parent = State_Backward(node, action, [n for n in list(set([ m for m in node.positive_literals if m not in action.add_list]
                                                                       + action.positive_preconditions))], action.negative_preconditions)
            if hash(parent) not in explored_set and parent not in frontier:
                frontier.append(parent)

def Ignore_Preconditions(initial_state, goal_schema, actions, node):
    if set(goal_schema[0]).issubset(initial_state.positive_literals) and not any(element in initial_state.positive_literals for element in
                                                                                goal_schema[1]):
        return 0
    k = 1
    while(True):
        combinations = list(itertools.combinations(actions, k))
        if any(list(filter(lambda tuple : set(goal_schema[0]).issubset(set.union(*map(set, [tuple[i].add_list for i in
                                                                                                 range(len(tuple))]))) and
                           not any(element in initial_state.positive_literals for element in goal_schema[1]), combinations))):
            return k
        k += 1

def Ignore_Delete_Lists(initial_state, goal_schema, actions, node):
    if set(goal_schema[0]).issubset(initial_state.positive_literals) and not any(element in initial_state.positive_literals for element in
                                                                                goal_schema[1]):
        return 0
    k = 1
    while(True):
        combinations = list(itertools.combinations(Applicable_Actions(node, actions), k))
        if any(list(filter(lambda tuple : set(goal_schema[0]).issubset(set(tuple[0].delete_list).union(set(tuple[1].delete_list))) and
                                                                   not any(element in initial_state.positive_literals for element in
                                                                      goal_schema[1]), combinations))):
            return k
        k += 1

def A_Star_Search(initial_state, goal_schema, actions):
    frontier = [initial_state]
    explored_set = set()
    if len(frontier) == 0:
        return 'failure'
    node = frontier.pop(0)
    while(True):
        if goal_test(node, goal_schema):
            solution = []
            g = node
            while(g != None):
                solution.append(g)
                g = g.parent
                return [s.action.name for s in solution]
        explored_set.add(hash(node))
        for action in Applicable_Actions(node, actions):
            child = State_Forward(node, action, [n for n in list(set(node.positive_literals + action.add_list)) if n not in
                                                action.delete_list], node.path_cost + 1)
            child.heuristic_cost = Ignore_Preconditions(initial_state, goal_schema, actions, child)
            if hash(child) not in explored_set and child not in frontier:
                frontier.append(child)
                frontier.sort(key=lambda x: x.path_cost + x.heuristic_cost)
                
            elif child in frontier and child.path_cost + child.heuristic_cost < frontier[frontier.index(child)].path_cost + \
                frontier[frontier.index(child)].heuristic_cost:
                    frontier[frontier.index(child)] = child
                    frontier.sort(key=lambda x: x.path_cost + x.heuristic_cost)

def main():
    initial_state_spare_tire_problem_positive_literals = ['atflataxle', 'atsparetrunk']
    state_spare_tire_problem_goal_schema = [['atspareaxle'], []]
    state_spare_tire_problem_actions = [Action('removetireflataxle', ['atflataxle'], [], ['atflatground'], ['atflataxle']),
                                                    Action('removetiresparetrunk', ['atsparetrunk'], [], ['atspareground'],
                                                           ['atsparetrunk']), Action('removetirespareaxle', ['atspareaxle'], [],
                                                                                     ['atspareground'], ['atspareaxle']),
                                                           Action('removetireflattrunk', ['atflattrunk'], [], ['atflatground'],
                                                                  ['atflattrunk']), Action('putonflataxle', ['atflatground'],
                                                                                           ['atflataxle'], ['atflatground'], []),
                                                                  Action('putonspareaxle', ['atspareground'], ['atflataxle'],
                                                                         ['atspareaxle'], ['atspareground']),
                                                                  Action('leaveovernight', [], [], [], ['atspareground', 'atspareaxle',
                                                                        'atsparetrunk', 'atflatground', 'atflataxle', 'atflattrunk'])]
    initial_state = State_Forward(None, None, initial_state_spare_tire_problem_positive_literals)
    print(Forward_State_Space_Search(initial_state, state_spare_tire_problem_goal_schema, state_spare_tire_problem_actions))
    #initial_state = State_Backward(None, None, initial_state_spare_tire_problem_positive_literals, [])
    #print(Backward_State_Space_Search(initial_state, state_spare_tire_problem_goal_schema, state_spare_tire_problem_actions))
    print(A_Star_Search(initial_state, state_spare_tire_problem_goal_schema, state_spare_tire_problem_actions))
main()