import sys
from time import time

# time1 = time()
# sleep(3)
# time2 = time()
# print(time2-time1)

# Assigning basic values
args = sys.argv
initial = args[1]
goal = args[2]
greedy_found = True
Astar_found = True


connection_to_final = []
with open("straightline.csv") as straightline_file:
    for row in straightline_file:
        row = row.split(",")
        if row[0] == goal:
            connection_to_final = [int(dist) for dist in row[1:]]
states_dict = {}
with open("driving.csv") as distance_file:
    row_num = 0
    for row in distance_file:
        row = row[:-1]
        row = row.split(",")
        if row_num == 0:
            row.pop(0)
            states = row
        else:
            states_dict[row[0]] = {}
            for i in range(1, len(row)):
                if row[i] != "-1":
                    states_dict[row[0]][states[i-1]] = int(row[i])
        row_num += 1


# Checking arguments
if len(args) != 3:
    raise ValueError("ERROR: Not enough or too many input arguments")


# Checking state abbrev. is used
if len(initial) != 2 or len(goal) != 2:
    raise ValueError("That is not the proper abbreviation of a state")

# Greedy Search
state_path1 = [initial]
total_cost1 = 0
connected_states1 = list(states_dict[initial].keys())
connected_states1.remove(initial)

time1 = time()
while goal not in state_path1:
    if len(connected_states1) == 0:
        greedy_found = False
        break
    total_distance = float('inf')
    destination_state = ""
    for state in connected_states1:
        idx = states.index(state)
        if connection_to_final[idx] < total_distance:
            destination_state = state
            total_distance = connection_to_final[idx]
    total_cost1 += states_dict[state_path1[len(state_path1) - 1]][destination_state]
    state_path1.append(destination_state)
    connected_states1.remove(state_path1[len(state_path1) - 1])
    for state in list(states_dict[state_path1[len(state_path1) - 1]].keys()):
        if state not in state_path1:
            connected_states1.append(state)
time2 = time()
greedy_time = time2-time1

# A* search
state_path2 = [initial]
expanded = 0
total_cost2 = 0
connected_states2 = list(states_dict[initial].keys())
connected_states2.remove(initial)
connected_dict = {}
for state in connected_states2:
    connected_dict[state] = (initial, states_dict[initial][state])

time1 = time()
while goal not in state_path2:
    if len(connected_states2) == 0:
        Astar_found = False
        break
    total_distance = float('inf')
    destination_state = ""
    for state in connected_states2:
        idx = states.index(state)
        connected_dist = connected_dict[state][1]
        if connected_dist + connection_to_final[idx] < total_distance:
            destination_state = state
            total_distance = connected_dist + connection_to_final[idx]
    total_cost2 = connected_dict[destination_state][1]
    state_path2.append(destination_state)
    connected_states2.remove(state_path2[len(state_path2) - 1])
    expanded += 1
    for state in list(states_dict[destination_state].keys()):
        total_dist = total_cost2 + states_dict[destination_state][state]
        if state != initial:
            if state not in connected_dict.keys():
                connected_states2.append(state)
                connected_dict[state] = (destination_state, total_cost2 + states_dict[destination_state][state])
            elif total_dist < connected_dict[state][1]:
                connected_dict[state] = (destination_state, total_cost2 + states_dict[destination_state][state])
if Astar_found:
    final = goal
    test_path = [final]
    while final != initial:
        prev_state = connected_dict[final][0]
        test_path.append(prev_state)
        final = prev_state
    state_path2 = list(reversed(test_path))
time2 = time()
Astar_time = time2-time1

# Formatting for submission
print("Bode, Jacob A20489414 solution:\n"
      "Initial State: {initial} \n"
      "Goal State: {goal}\n"
      .format(initial=initial, goal=goal))
if greedy_found:
    print("Greedy Best First Search:\n"
          "Solution path: {path}\n"
          "Number of states on a path: {states}\n"
          "Number of expanded nodes: {nodes}\n"
          "Path cost: {cost}\n"
          "Execution time:{time}\n"
          .format(path=state_path1, states=len(state_path1), nodes=len(state_path1)-1, cost=total_cost1,
                  time=greedy_time))
else:
    print("Greedy Best First Search:\n"
          "Solution path: FAILURE: NO PATH FOUND\n"
          "Number of states on a path: 0\n"
          "Number of expanded nodes: 0\n"
          "Path cost: 0\n"
          "Execution time:{time}\n"
          .format(time=greedy_time))
if greedy_found:
    print("A* Search:\n"
          "Solution path: {path}\n"
          "Number of states on a path: {states}\n"
          "Number of expanded nodes: {nodes}\n"
          "Path cost: {cost}\n"
          "Execution time:{time}\n"
          .format(path=state_path2, states=len(state_path2), nodes=expanded, cost=total_cost2, time=Astar_time))
else:
    print("A* Search:\n"
          "Solution path: FAILURE: NO PATH FOUND\n"
          "Number of states on a path: 0\n"
          "Number of expanded nodes: 0\n"
          "Path cost: 0\n"
          "Execution time:{time}\n"
          .format(time=Astar_time))
