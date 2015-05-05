"""
The "travel from home to the park" example from my lectures.
Author: Dana Nau <nau@cs.umd.edu>, May 31, 2013
This file should work correctly in both Python 2.7 and Python 3.2.
"""

import pyhop_SeRPE

def taxi_rate(dist):
    return (8 + 0.5 * dist)

def walk(state, a, x, y):
    state.cash[a] = state.cash[a] - 1
    if state.loc[a] == x:
        state.loc[a] = y
        return state
    else: return False

def get_cash(state, a):
    state.cash[a] = state.cash[a] + 1
    return state

def call_taxi(state, a, x):
    state.loc['taxi'] = x
    return state
    
def ride_taxi(state, a, x, y):
    if state.loc['taxi'] == x and state.loc[a] == x:
        state.loc['taxi'] = y
        state.loc[a] = y
        state.owe[a] = taxi_rate(state.dist[x][y])
        return state
    else: return False

def pay_driver(state, a):
    if state.cash[a] >= state.owe[a]:
        state.cash[a] = state.cash[a] - state.owe[a]
        state.owe[a] = 0
        return state
    else: return False

pyhop_SeRPE.declare_operators(walk, call_taxi, ride_taxi, pay_driver, get_cash)
print('')
pyhop_SeRPE.print_operators()



def travel_by_foot(state, a, x, y):
    if state.dist[x][y] <= 2:
        result = pyhop_SeRPE.execute_action('walk(state, a, x, y)', state)
        subtasks = [('walk', a, x, y)]
        return {'state':result, 'subtasks':subtasks}
        # return [('walk', a, x, y)] # use eval
    return {'state':False, 'subtasks':False}

def travel_by_taxi(state, a, x, y):
    import copy
    if state.cash[a] >= taxi_rate(state.dist[x][y]):
        result = copy.deepcopy(state)
        result = pyhop_SeRPE.execute_action('call_taxi', result, state, (a, x))
        result = pyhop_SeRPE.execute_action('ride_taxi', result, state, (a, x, y))
        result = pyhop_SeRPE.execute_action('pay_driver', result, state, (a))
        subtasks = [('call_taxi', a, x), ('ride_taxi', a, x, y), ('pay_driver', a)] if result != False else False
        return {'state':result, 'subtasks':subtasks}
        # return [('call_taxi', a, x), ('ride_taxi', a, x, y), ('pay_driver', a)]
    else:
        return go_to_bank(state, a, x, y)
    
def go_to_bank(state, a, x, y):
        import copy
        result = copy.deepcopy(state)
        result = pyhop_SeRPE.execute_action('get_cash', result, state, (a))
        result = pyhop_SeRPE.execute_action('travel', result, state, (a, x, y))
        subtasks = [('get_cash', a), ('travel', a, x, y)]  if result != False else False
        return {'state':result, 'subtasks':subtasks}
#         return False # [('go_to_bank', a), ('travel', a, x, y)]

pyhop_SeRPE.declare_methods('travel', travel_by_foot, travel_by_taxi)
print('')
pyhop_SeRPE.print_methods()

state1 = pyhop_SeRPE.State('state1')
state1.loc = {'me':'home'}
state1.cash = {'me':10}
state1.owe = {'me':0}
state1.dist = {'home':{'park':8}, 'park':{'home':8}}

print("""
********************************************************************************
Call pyhop_SeRPE.pyhop_SeRPE(state1,[('travel','me','home','park')]) with different verbosity levels
********************************************************************************
""")

# print("- If verbose=0 (the default), pyhop_SeRPE returns the solution but prints nothing.\n")
# pyhop_SeRPE.pyhop_SeRPE(state1, [('travel', 'me', 'home', 'park')])
# 
# print('- If verbose=1, pyhop_SeRPE prints the problem and solution, and returns the solution:')
# pyhop_SeRPE.pyhop_SeRPE(state1, [('travel', 'me', 'home', 'park')], verbose=1)
# 
# print('- If verbose=2, pyhop_SeRPE also prints a note at each recursive call:')
# pyhop_SeRPE.pyhop_SeRPE(state1, [('travel', 'me', 'home', 'park')], verbose=2)

print('- If verbose=3, pyhop_SeRPE also prints the intermediate states:')
pyhop_SeRPE.pyhop_SeRPE(state1, [('travel', 'me', 'home', 'park')], verbose=3)

