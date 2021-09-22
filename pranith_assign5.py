#!/usr/bin/env python
# coding: utf-8

# In[8]:


import sys
from copy import deepcopy, copy
from collections import deque
import math
import random
from queue import PriorityQueue


# valid moves of a given ghost at a given position
def valid_moves(gameboard, ghost):
    
    pos = gameboard.cur_pos[ghost]
    
    valid_moves = []
    
    if gameboard.working_maze[pos[0] - 1][pos[1]] != '#':
        valid_moves.append('U')
    if gameboard.working_maze[pos[0] + 1][pos[1]] != '#':
        valid_moves.append('D')
    if gameboard.working_maze[pos[0]][pos[1] + 1] != '#':
        valid_moves.append('R')
    if gameboard.working_maze[pos[0]][pos[1] - 1] != '#':
        valid_moves.append('L')
    
    return valid_moves

# number of valid moves determines how each ghost moves
def common_moves(gameboard, ghost):
    
    moves = valid_moves(gameboard, ghost)
    count = len(moves)
    
    if count == 1:
        next_move(gameboard, moves[0], ghost)

    if count == 2:
        opp_dir = opp_drn[gameboard.cur_drn[ghost]]

        if gameboard.cur_drn[ghost] in moves:
            next_move(gameboard, gameboard.cur_drn[ghost], ghost)
        elif opp_dir == moves[0]:
            next_move(gameboard, moves[1], ghost)
        else:
            next_move(gameboard, moves[0], ghost)

    if count == 3 or count == 4:
        if ghost == 'P':
            punky_move(gameboard)
        if ghost == 'B':
            bunky_move(gameboard)
        if ghost == 'D':
            dunky_move(gameboard)
        if ghost == 'R':
            runky_move(gameboard)

# moving a player using the next_move
def next_move(gameboard, next_move, player):
    global game_over_bool
    
    pos = gameboard.cur_pos[player]
    
    if next_move == 'L':
        gameboard.working_maze[pos[0]][pos[1] - 1] = player
        gameboard.cur_pos[player] = [pos[0], pos[1] - 1]
        
    
        
    if next_move == 'D':
        gameboard.working_maze[pos[0] + 1][pos[1]] = player
        gameboard.cur_pos[player] = [pos[0] + 1, pos[1]]
        
    if next_move == 'R':
        gameboard.working_maze[pos[0]][pos[1] + 1] = player
        gameboard.cur_pos[player] = [pos[0], pos[1] + 1]
        
    if next_move == 'U':
        gameboard.working_maze[pos[0] - 1][pos[1]] = player
        gameboard.cur_pos[player] = [pos[0] - 1, pos[1]]
  
    gameboard.cur_drn[player] = next_move
 
    game_over_pos = gameboard.cur_pos[player]
    
    # this if-else when Actman meets ghost at the same cell 
    
    if player != 'A' and game_over_pos == gameboard.cur_pos['A']:
#         print("*******************Ghost killed Actman**************")
        
        game_over_bool = True
        gameboard.actman_score = gameboard.actman_score - 1
        gameboard.working_maze[game_over_pos[0]][game_over_pos[1]] = 'X'
    
    elif gameboard.cur_pos['A'] == gameboard.cur_pos['P'] or gameboard.cur_pos['A'] ==             gameboard.cur_pos['B'] or gameboard.cur_pos['A'] == gameboard.cur_pos['D'] or             gameboard.cur_pos['A'] == gameboard.cur_pos['R']:
#         print("*******************Actman killed Ghost**************")
        game_over_bool = True
        gameboard.actman_score = gameboard.actman_score - 1
        gameboard.working_maze[game_over_pos[0]][game_over_pos[1]] = 'X'

    replace_cell(gameboard, pos, player)

# Ghost Punky's special move defined
def punky_move(gameboard):

    ghost = 'P'
    my_moves = valid_moves(gameboard, ghost)
    my_pos = gameboard.cur_pos[ghost]
    moves_dict = euclidean2(gameboard, my_pos)

    new_moves_dict = {}

    for move in my_moves:
        new_moves_dict[move] = moves_dict[move]

    min_dist_move(gameboard, new_moves_dict, ghost)


# Ghost Bunky's special moves defined
def bunky_move(gameboard):
    ghost = 'B'

    my_pos = gameboard.cur_pos[ghost]
    target_loc = bunky_target_location(gameboard)
    moves_dict = euclidean_distance(my_pos, target_loc)

    my_moves = valid_moves(gameboard, ghost)

    new_moves_dict = {}

    for move in my_moves:
        new_moves_dict[move] = moves_dict[move]

    min_dist_move(gameboard, new_moves_dict, ghost)


# Ghost Dunky's special moves defined
def dunky_move(gameboard):
    ghost = 'D'

    if gameboard.dunky_index == len(dunky_list_locations):
        gameboard.dunky_index = 0

    while gameboard.cur_pos[ghost] == list(dunky_list_locations[gameboard.dunky_index]):
        gameboard.dunky_index += 1

        if gameboard.dunky_index == len(dunky_list_locations):
            gameboard.dunky_index = 0

    target_location = dunky_list_locations[gameboard.dunky_index]
    my_pos = gameboard.cur_pos[ghost]
    my_moves = valid_moves(gameboard, ghost)

    new_moves_dict = {}

    moves_dict = euclidean_distance(my_pos, target_location)

    for move in my_moves:
        new_moves_dict[move] = moves_dict[move]

    min_dist_move(gameboard, new_moves_dict, ghost)

#     gameboard.dunky_index = gameboard.dunky_index


# Ghost Runky's special move defined
def runky_move(gameboard):
    ghost = 'R'

    if gameboard.runky_index == len(runky_list_moves):
        gameboard.runky_index = 0

    while runky_list_moves[gameboard.runky_index] not in valid_moves(gameboard, ghost):
        gameboard.runky_index += 1

        if gameboard.runky_index == len(runky_list_moves):
            gameboard.runky_index = 0

    next_move(gameboard, runky_list_moves[gameboard.runky_index], ghost)
    gameboard.runky_index = gameboard.runky_index + 1


#substitute of distance2target
def euclidean_distance(my_pos, target_loc):
    dist = {}
    dist['U'] = math.sqrt((my_pos[0] - 1 - target_loc[0]) ** 2 + (my_pos[1] - target_loc[1]) ** 2)
    dist['R'] = math.sqrt((my_pos[0] - target_loc[0]) ** 2 + (my_pos[1] + 1 - target_loc[1]) ** 2)
    dist['D'] = math.sqrt((my_pos[0] + 1 - target_loc[0]) ** 2 + (my_pos[1] - target_loc[1]) ** 2)
    dist['L'] = math.sqrt((my_pos[0] - target_loc[0]) ** 2 + (my_pos[1] - 1 - target_loc[1]) ** 2)
    return dist

#substitute of distance2
def euclidean2(gameboard, my_pos):
    act_pos = gameboard.cur_pos['A']
    dist = {}
    
    dist['U'] = math.sqrt((my_pos[0] - 1 - act_pos[0]) ** 2 + (my_pos[1] - act_pos[1]) ** 2)
    dist['R'] = math.sqrt((my_pos[0] - act_pos[0]) ** 2 + (my_pos[1] + 1 - act_pos[1]) ** 2)
    dist['D'] = math.sqrt((my_pos[0] + 1 - act_pos[0]) ** 2 + (my_pos[1] - act_pos[1]) ** 2)
    dist['L'] = math.sqrt((my_pos[0] - act_pos[0]) ** 2 + (my_pos[1] - 1 - act_pos[1]) ** 2)

    return dist

# distance of given cell to a target cell 
def distance2target(my_pos, target_loc):
    dist = {}
    dist['U'] = abs(my_pos[0] - 1 - target_loc[0]) + abs(my_pos[1] - target_loc[1])
    dist['R'] = abs(my_pos[0] - target_loc[0]) + abs(my_pos[1] + 1 - target_loc[1])
    dist['D'] = abs(my_pos[0] + 1 - target_loc[0]) + abs(my_pos[1] - target_loc[1])
    dist['L'] = abs(my_pos[0] - target_loc[0]) + abs(my_pos[1] - 1 - target_loc[1])
    
    return dist

# distance of a given cell to Actman's cell
def distance2(gameboard, my_pos):
    act_pos = gameboard.cur_pos['A']
    dist = {}

    dist['U'] = abs(my_pos[0] - 1 - act_pos[0]) + abs(my_pos[1] - act_pos[1])
    dist['R'] = abs(my_pos[0] - act_pos[0]) + abs(my_pos[1] + 1 - act_pos[1])
    dist['D'] = abs(my_pos[0] + 1 - act_pos[0]) + abs(my_pos[1] - act_pos[1])
    dist['L'] = abs(my_pos[0] - act_pos[0]) + abs(my_pos[1] - 1 - act_pos[1])

    return dist


# minimum distance of the available moves
def min_dist_move(gameboard, moves_dict, ghost):

    min_dist = min(moves_dict.values())
    min_dist_moves = [key for key in moves_dict if moves_dict[key] == min_dist]

    if len(min_dist_moves) == 1:
        next_move(gameboard, min_dist_moves[0], ghost)
    else:
        min_dis_dict = {}

        for move in min_dist_moves:
            min_dis_dict[move] = move_pref[move]

        final_min_dist = min(min_dis_dict.values())
        final_move = [key for key in min_dis_dict if min_dis_dict[key] == final_min_dist]
        next_move(gameboard, final_move[0], ghost)

# bunky's target can be beyond the boundaries
def bunky_target_location(gameboard):
    player = 'A'
    pos = gameboard.cur_pos[player]
    new_pos = deepcopy(pos)
    drn = gameboard.cur_drn['A']
    
    if drn == 'U':
        new_pos[0] = new_pos[0] - 5
    if drn == 'R':
        new_pos[1] = new_pos[1] + 5
    if drn == 'D':
        new_pos[0] = new_pos[0] + 5
    if drn == 'L':
        new_pos[1] = new_pos[1] - 5

    return new_pos


def cell_limit_check(gameboard):

    player = 'A'
    pos = gameboard.cur_pos[player]
    new_pos = copy(pos)
    drn = gameboard.cur_drn['A']

    if drn == 'U':
        if new_pos[0] - 4 <= 0:
            new_pos[0] = 0
        else:
            new_pos[0] = new_pos[0] - 4

    if drn == 'R':
        if new_pos[1] + 4 > columns:
            new_pos[1] = columns - 1
        else:
            new_pos[1] = new_pos[1] + 4

    if drn == 'D':
        if new_pos[0] + 4 > rows:
            new_pos[0] = rows - 1
        else:
            new_pos[0] = new_pos[0] + 4

    if drn == 'L':
        if new_pos[1] - 4 <= 0:
            new_pos[1] = 0
        else:
            new_pos[1] = new_pos[1] - 4
    
    return new_pos

 
def valid_moves_for_act(gameboard, actman):
    avoid_em_all = ['#', 'P', 'B', 'D', 'R']

    pos = gameboard.cur_pos[actman]
    valid_moves = []

    if gameboard.working_maze[pos[0]][pos[1] - 1] not in avoid_em_all:
        valid_moves.append('L')
    if gameboard.working_maze[pos[0] + 1][pos[1]] not in avoid_em_all:
        valid_moves.append('D')
    if gameboard.working_maze[pos[0]][pos[1] + 1] not in avoid_em_all:
        valid_moves.append('R')
        
    if gameboard.working_maze[pos[0] - 1][pos[1]] not in avoid_em_all:
        valid_moves.append('U')
    
    return valid_moves


def replace_cell(gameboard, pos, player):

    if player == 'A':
        gameboard.given_maze[pos[0]][pos[1]] = ' '
        gameboard.working_maze[pos[0]][pos[1]] = ' '

    else:
        if gameboard.given_maze[pos[0]][pos[1]] in ['P', 'B', 'D', 'R', 'A']:
            gameboard.working_maze[pos[0]][pos[1]] = ' '

        elif gameboard.given_maze[pos[0]][pos[1]] == '$':
            gameboard.working_maze[pos[0]][pos[1]] = '$'

        elif gameboard.given_maze[pos[0]][pos[1]] == '*':
            gameboard.working_maze[pos[0]][pos[1]] = '*'

        elif gameboard.given_maze[pos[0]][pos[1]] == '.':
            gameboard.working_maze[pos[0]][pos[1]] = '.'

        elif gameboard.given_maze[pos[0]][pos[1]] == ' ':
            gameboard.working_maze[pos[0]][pos[1]] = ' '


def game_win(gameboard):
    global game_win_bool

    if total_score == gameboard.actman_score:
        game_win_bool = True


def calculate_score(gameboard1, move):

    my_pos = gameboard1.cur_pos['A']

    if move == 'L':
        if gameboard1.working_maze[my_pos[0]][my_pos[1] - 1] in treasure_value:
            gameboard1.actman_score = gameboard1.actman_score + treasure_value[gameboard1.working_maze[my_pos[0]][my_pos[1] - 1]]

    if move == 'R':
        if gameboard1.working_maze[my_pos[0]][my_pos[1] + 1] in treasure_value:
            gameboard1.actman_score = gameboard1.actman_score + treasure_value[gameboard1.working_maze[my_pos[0]][my_pos[1] + 1]]

    if move == 'U':
        if gameboard1.working_maze[my_pos[0] - 1][my_pos[1]] in treasure_value:
            gameboard1.actman_score = gameboard1.actman_score + treasure_value[gameboard1.working_maze[my_pos[0] - 1][my_pos[1]]]

    if move == 'D':
        if gameboard1.working_maze[my_pos[0] + 1][my_pos[1]] in treasure_value:
            gameboard1.actman_score = gameboard1.actman_score + treasure_value[gameboard1.working_maze[my_pos[0] + 1][my_pos[1]]]

    return gameboard1.actman_score

 
def transitionFunction(gameboard1, plan):

    for m in plan:
        
        calculate_score(gameboard1, m)
        next_move(gameboard1, m, 'A')
        common_moves(gameboard1, 'P')
        common_moves(gameboard1, 'B')
        common_moves(gameboard1, 'D')
        common_moves(gameboard1, 'R')
        
#     gbPrint(gameboard1)

    
class GameBoard:

    def __init__(self, working_maze, given_maze, actman_score, cur_pos, cur_drn, dunky_index, runky_index):

        self.working_maze = working_maze
        self.given_maze = given_maze
        self.actman_score = actman_score
        self.cur_pos = cur_pos
        self.cur_drn = cur_drn
        self.dunky_index = dunky_index
        self.runky_index = runky_index

def gbPrint( gameboard ) :

    #print(gb.working_maze)

#     print("gameboard: ")
    for l in gameboard.working_maze :
        print("".join(l))
        
    print("inside gbPrint: ", gameboard.actman_score)
    
    return gameboard.actman_score
#     print(gameboard.cur_pos)
#     print(gameboard.cur_drn)
#    print(gameboard.dunky_index)
#    print(gameboard.runky_index)
#     print('--')

def actman_bfs(gameboard):
    # frontier contains sequence of moves
    frontier = deque()
    frontier.append("")

    z = 0

    while len(frontier) > 0:
        plan = frontier.popleft()

        if len(plan) > z :
            z = len(plan)
#             print(z)

        # gameboard1 is the GameBoard snapshot after executing plan on gameboard
        gameboard1 = deepcopy(gameboard)

        transitionFunction(gameboard1, plan)

        #print('===')
#         print(plan)
#         gbPrint(gameboard1)

        if gameboard1.actman_score >= 16:
            print(plan)
            print("==================after winning==================")
            gbPrint(gameboard1)
            
            return plan
#             return plan, gameboard1.actman_score, gameboard1.working_maze

        my_moves = valid_moves_for_act(gameboard1, 'A')

        for move in my_moves:
            frontier.append(plan + move)
            
            
def heuristic_function(actman_score):
    global total_score
    return total_score - actman_score    

def goal(gameboard):
    is_goal = False
    
    if gameboard.actman_score >= 20:
        is_goal = True

# Iterative Deepening DFS
def actman_iterativeDeep_dfs(gameboard):
    
    depth = 0
    result = False
     
    res = []
    
    while result is False:
        
        res = actman_bounded_dfs(gameboard, depth)
        
        if isinstance(res, tuple):
            result = True
            break
        
        depth = depth + 1
    return res

# Bounded DFS
def actman_bounded_dfs(gameboard, depth):
    
#     is_limit_reached = False
    
    frontier = deque()
    frontier.append("")
    
    while len(frontier) > 0:
        
        plan = frontier.pop()
        gameboard1 = deepcopy(gameboard)
        
        transitionFunction(gameboard1, plan)
        
        if len(plan) > depth:
            continue
        
        if len(plan) == depth:
                    
            if gameboard1.actman_score >= 20:
                return plan, gameboard1.actman_score, gameboard1.working_maze
    
        
        my_moves = valid_moves_for_act(gameboard1, 'A')

        for move in my_moves:
            frontier.append(plan + move)

def actman_Astar_search(gameboard):
    global total_score
    visited = []
    
    frontier = PriorityQueue()
    frontier.put((2000, ""))
    
    while not frontier.empty():
        
        plan = frontier.get(0)[1]
        gameboard1 = deepcopy(gameboard)
        transitionFunction(gameboard1, plan)
        
        
        if gameboard1.actman_score == total_score:
            return plan, gameboard1.actman_score, gameboard1.working_maze
#             return plan
        
        my_moves = valid_moves_for_act(gameboard1, 'A')
        for move in my_moves:
            planX = plan + move

            gameboard2 = deepcopy(gameboard)            
            transitionFunction(gameboard2, planX)
            if is_not_visited(gameboard2, visited) and not game_over(gameboard2):
                
                a_function = len(planX) + heuristic_function(gameboard2.actman_score)
#                 print("function: ", a_function)

                frontier.put((a_function, planX))
                visited.append(gameboard2)
    
    
    
def actman_greedy_bfs(gameboard):
    
    visited = []

    frontier = PriorityQueue()
    frontier.put((1999, ""))
    
    while not frontier.empty():
        
        plan = frontier.get(0)[1]
        gameboard1 = deepcopy(gameboard)
        transitionFunction(gameboard1, plan)
        
#         if is_not_visited(gameboard1, visited) and not game_over(gameboard1):
        if gameboard1.actman_score >= 24:
#             gbPrint(gameboard1)
#             return plan
            return plan, gameboard1.actman_score, gameboard1.working_maze
        

        my_moves = valid_moves_for_act(gameboard1, 'A')
        for move in my_moves:
            planX = plan + move

            gameboard2 = deepcopy(gameboard)            
            transitionFunction(gameboard2, planX)
            if is_not_visited(gameboard2, visited) and not game_over(gameboard2):

                frontier.put((heuristic_function(gameboard2.actman_score), planX))
                visited.append(gameboard2)

# if a gameboard already visited or not                
def is_not_visited(board, visited_boards):
    for v in visited_boards:
        if v.actman_score == board.actman_score and v.cur_pos['A'] == board.cur_pos['A'] and v.cur_pos['P'] == board.cur_pos['P'] and v.cur_pos['B'] == board.cur_pos['B'] and v.cur_pos['D'] == board.cur_pos['D'] and v.cur_pos['R'] == board.cur_pos['R']:
            return False
    return True

def game_over(gameboard):
    
    if gameboard.cur_pos['A'] == gameboard.cur_pos['P'] or gameboard.cur_pos['A'] == gameboard.cur_pos['B'] or gameboard.cur_pos['A'] == gameboard.cur_pos['D'] or gameboard.cur_pos['A'] == gameboard.cur_pos['R']:
        return True
    return False
        

# read from input file from command-line

inFile = open(sys.argv[1], "r")
outFile = open(sys.argv[2], "w")

# read input file
# inFile = open("dungeon_51.txt", "r")
# outFile = open("output2.txt", "w")

 
# making a 2D list
Lines = inFile.readlines()
input_pblm = []

for line in Lines:
    list1 = []
    for char in line.strip():
        list1.append(char)
    input_pblm.append(list1)


rows = int(input_pblm[0][0])

col = input_pblm[0][2:]

columns = ''
for i in col:
    columns = columns + i
columns = int(columns)

given_maze = input_pblm[1:rows + 1]

working_maze = deepcopy(given_maze)


#position of a player in the maze
def position(player):

    for i in range(len(working_maze)):
        for j in range(len(working_maze[i])):
            if working_maze[i][j] == player:
                return [i, j]


move_pref = {'U': 1, 'R': 2, 'D': 3, 'L': 4}


cur_pos = {'P': position('P'), 'B': position('B'), 'D': position('D'), 'R': position('R'),
                           'A': position('A')}

cur_drn = {'P': input_pblm[rows + 1][0], 'B': input_pblm[rows + 1][1], 'D': input_pblm[rows + 1][2],
           'R': input_pblm[rows + 1][3], 'A': ''}

opp_drn = {'L': 'R', 'R': 'L', 'U': 'D', 'D': 'U'}
 
runky_list_moves = input_pblm[rows + 3]

dunky_locations = input_pblm[rows + 2][2:]

for i in dunky_locations:
    if i == ' ':
        dunky_locations.remove(i)

dunky_locations = [int(i) for i in dunky_locations]
it = iter(dunky_locations)

dunky_list_locations = list(zip(it, it))

total_score = 0

treasure_value = {'.': 1, '$': 5, '*': 10}

for i in range(len(working_maze)):
        for j in range(len(working_maze[i])):
            if working_maze[i][j] in treasure_value.keys():
                total_score = total_score + treasure_value[working_maze[i][j]]
                
# print(total_score)

game_win_bool = False
game_over_bool = False


gameboard = GameBoard(working_maze, given_maze, 0, cur_pos, cur_drn, 0, 0)

# actman_bfs(gameboard)
# # result = actman_bfs(gameboard)
# result1 = actman_iterativeDeep_dfs(gameboard)
result1 = actman_Astar_search(gameboard)
# print(result1)

# result1 = actman_greedy_bfs(gameboard)

with outFile as filename:
    if isinstance(result1, bool):
        print(result1, file=filename)
    else:
        print(result1[0], file=filename)
        print(result1[1], file=filename)
        for l in result1[2] :
            print("".join(l), file=filename)
    
outFile.close()

# Test for dungeons

# transitionFunction(gameboard, 'DDLLLLUUUDDDRRRRRRRR')
# transitionFunction(gameboard, 'DRRUUL')
# transitionFunction(gameboard, 'UUURRRDDUULLLLLLDDDRRRRR')

# gbPrint( gameboard )

#print(valid_moves_for_act(gameboard, 'A'))

