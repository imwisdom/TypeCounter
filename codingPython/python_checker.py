
import pythonparser
from pythonparser.ast import FunctionDef, Assign, Dict, List, Subscript, Index, Str, Num, Name, Attribute, If, Tuple, \
    Set, BinOp, While, DictComp, ListComp
from pythonparser.ast import For
from pythonparser.ast import Call
from pythonparser.parser import commalist

loop_count = 5
recv_count = 4

func_count_map = {}
func_node_map = {}

list_map = {}
dict_map = {}
tuple_map = {}
set_map = {}
map_map = {}

is_correct_map = True

def count_func_into_map(node):
    global func_count_map
    global func_node_map
    name = node.name

    if not name in func_count_map:
        func_count_map[name] = 1
        func_node_map[name] = node
    else:
        func_count_map[name] = func_count_map[name] + 1


def count_var_into_map(method_name, target, value):
    name = ''

    if hasattr(target, 'name'):
        name = target.name
    elif hasattr(target, 'id'):
        name = target.id
    elif hasattr(target, 'value') and hasattr(target, 'id'):
        name = target.value.id

    global dict_map
    global list_map
    global tuple_map
    global set_map
    global map_map


    if name == '' :
        return

    name = method_name+name

    if name in dict_map :
        dict_map[name] = dict_map[name] + 1

    elif name in list_map :
        list_map[name] = list_map[name] + 1

    elif name in tuple_map :
        tuple_map[name] = tuple_map[name] + 1

    elif name in set_map :
        set_map[name] = set_map[name] + 1

    elif isinstance(value, DictComp) or isinstance(value, Dict) or \
            (isinstance(value, Index) and (isinstance(value.value, Str))):
            dict_map[name] = 1

    elif isinstance(value, ListComp) or isinstance(value, List) or (isinstance(value, Index) and isinstance(value.value, Num)):
            list_map[name] = 1

    elif isinstance(value, Tuple) :
            tuple_map[name] = 1

    elif isinstance(value, Set) :
            set_map[name] = 1

    elif isinstance(value, Call) :
        value_func = value.func
        if isinstance(value_func, Name) :
            func_name = value_func.id
            if func_name == 'dict' or func_name == 'defaultdict' :
                dict_map[name] = 1
            elif func_name == 'map' :
                map_map[name] = 1
            elif func_name == 'list' :
                list_map[name] = 1
            elif func_name == 'set' :
                set_map[name] = 1
            elif func_name == 'tuple' :
                tuple_map[name] = 1

        elif isinstance(value_func, Attribute) and isinstance(value_func.value, Name) and value_func.value.id == 'collections' :
            if value_func.attr.find('dict') or value_func.attr.find('Dict') :
                dict_map[name] = 1
            elif value_func.attr.find('tuple') :
                tuple_map[name] = 1


def count_object_type_in_method(body_list, parent_func_name, parent_recv_num):
    global loop_count
    global recv_count

    if parent_recv_num >= recv_count :
        return

    for a_body in body_list:

        if isinstance(a_body, For):
            for i in range(0, loop_count):
                count_object_type_in_method([a_body.target], parent_func_name, parent_recv_num)
                count_object_type_in_method([a_body.iter], parent_func_name, parent_recv_num)
                count_object_type_in_method(a_body.body, parent_func_name, parent_recv_num)

        elif isinstance(a_body, While):

            for i in range(0, loop_count):
                count_object_type_in_method([a_body.test], parent_func_name, parent_recv_num)
                count_object_type_in_method(a_body.body, parent_func_name, parent_recv_num)

        elif isinstance(a_body, FunctionDef):
            count_func_into_map(a_body)

        elif isinstance(a_body, Call):

            if hasattr(a_body, 'args') :
                count_object_type_in_method(a_body.args, parent_func_name, parent_recv_num)

            if isinstance(a_body.func, Attribute):
                count_object_type_in_method([a_body.func], parent_func_name, parent_recv_num)
                continue

            if hasattr(a_body.func, 'value'):
                name = a_body.func.value.id
            elif hasattr(a_body.func, 'name'):
                name = a_body.func.name
            else:
                name = a_body.func.id

            if not name in func_node_map:
                count_object_type_in_method([a_body.func], parent_func_name, parent_recv_num)
                continue

            func_node = func_node_map[name]

            # if func_node != None:
            #     if not (cur_method != None and cur_method.id == name):  # is recursive method
            #         cur_method = a_body
            #         count_object_type_in_method(func_node.body)
            #         count_func_into_map(func_node)

            if func_node != None :
                if name != parent_func_name :
                    count_object_type_in_method(func_node.body, name, parent_recv_num)
                    count_func_into_map(func_node)
                else :
                    count_object_type_in_method(func_node.body, parent_func_name, parent_recv_num+1)
                    count_func_into_map(func_node)


        elif isinstance(a_body, Assign):
            var_target = a_body.targets
            var_value = a_body.value

            if isinstance(var_target[0], Subscript) :
                count_object_type_in_method(var_target, parent_func_name, parent_recv_num)
            elif isinstance(var_value, BinOp) and isinstance(var_value.left, List):
                count_var_into_map(parent_func_name, var_target[0], var_value.left)
            elif isinstance(var_value, BinOp) and isinstance(var_value.right, List):
                count_var_into_map(parent_func_name, var_target[0], var_value.right)
            else :
                count_var_into_map(parent_func_name, var_target[0], var_value)

            # count_object_type_in_method(var_target)
            count_object_type_in_method([var_value, None], parent_func_name, parent_recv_num)

        elif isinstance(a_body, Subscript):
            if a_body.slice is not None and isinstance(a_body.slice, Index):
                if isinstance(a_body.value, Subscript) or isinstance(a_body.value, Call):
                    count_object_type_in_method([a_body.value], parent_func_name, parent_recv_num)
                else:
                    count_var_into_map(parent_func_name, a_body.value, a_body.slice)

        elif isinstance(a_body, If):
            count_object_type_in_method(a_body.body, parent_func_name, parent_recv_num)

            if hasattr(a_body, 'orelse') :
                count_object_type_in_method(a_body.orelse, parent_func_name, parent_recv_num)

            if hasattr(a_body.test, 'comparators'):
                count_object_type_in_method(a_body.test.comparators, parent_func_name, parent_recv_num)
                count_object_type_in_method([a_body.test.left], parent_func_name, parent_recv_num)

            if hasattr(a_body.test, 'values'):
                count_object_type_in_method(a_body.test.values, parent_func_name, parent_recv_num)



        elif isinstance(a_body, Name):
            count_var_into_map(parent_func_name, a_body, None)

        elif isinstance(a_body, BinOp):
            count_object_type_in_method([a_body.left], parent_func_name, parent_recv_num)
            count_object_type_in_method([a_body.right], parent_func_name, parent_recv_num)

        elif isinstance(a_body, commalist) :
            count_object_type_in_method(a_body, parent_func_name, parent_recv_num)

        elif hasattr(a_body, 'elts'):
            count_object_type_in_method([a_body.elts], parent_func_name, parent_recv_num)

        elif hasattr(a_body, 'body'):
            count_object_type_in_method([a_body.body], parent_func_name, parent_recv_num)

        elif hasattr(a_body, 'value'):
            count_object_type_in_method([a_body.value], parent_func_name, parent_recv_num)


def count_object_type(body_list):
    global loop_count
    global recv_count
    global func_node_map

    for a_body in body_list:
        if isinstance(a_body, For):
            for i in range(0, loop_count):
                count_object_type([a_body.target])
                count_object_type([a_body.iter])
                count_object_type(a_body.body)

        elif isinstance(a_body, While):

            for i in range(0, loop_count):
                count_object_type([a_body.test])
                count_object_type(a_body.body)

        elif isinstance(a_body, FunctionDef):
            count_func_into_map(a_body)

        elif isinstance(a_body, Call):
            name = ""
            if hasattr(a_body, 'args') :
                count_object_type(a_body.args)

            if isinstance(a_body.func, Attribute) :
                count_object_type([a_body.func])
                continue

            if hasattr(a_body.func, 'value'):
                name = a_body.func.value.id
            elif hasattr(a_body.func, 'name'):
                name = a_body.func.name
            else:
                name = a_body.func.id

            if not name in func_node_map:
                count_object_type([a_body.func])
                continue

            func_node = func_node_map[name]

            if func_node is not None:
                # if cur_method is not None and cur_method.id == name:  # is recursive method
                #
                #     for i in range(0, recv_count):
                #         count_object_type_in_method(func_node.body)
                #         count_func_into_map(func_node)
                #
                # else:
                #     cur_method = a_body.func
                #     count_object_type(func_node.body)
                #     count_func_into_map(func_node)
                count_object_type_in_method(func_node.body, name, 0)
                count_func_into_map(func_node)


        elif isinstance(a_body, Assign):
            var_target = a_body.targets
            var_value = a_body.value

            if isinstance(var_target[0], Subscript) :
                count_object_type(var_target)
            elif isinstance(var_value, BinOp) and isinstance(var_value.left, List):
                count_var_into_map("", var_target[0], var_value.left)
            elif isinstance(var_value, BinOp) and isinstance(var_value.right, List):
                count_var_into_map("", var_target[0], var_value.right)
            else :
                count_var_into_map("", var_target[0], var_value)
            # count_object_type(var_target)
            count_object_type([var_value])

        elif isinstance(a_body, Subscript):
            if a_body.slice is not None and isinstance(a_body.slice, Index):
                if isinstance(a_body.value, Subscript) or isinstance(a_body.value, Call):
                    count_object_type([a_body.value])
                else:
                    count_var_into_map("", a_body.value, a_body.slice)

        elif isinstance(a_body, If):
            count_object_type(a_body.body)

            if hasattr(a_body, 'orelse') :
                count_object_type(a_body.orelse)
            if hasattr(a_body.test, 'comparators') :
                count_object_type(a_body.test.comparators)
                count_object_type([a_body.test.left])
            if hasattr(a_body.test, 'values') :
                count_object_type(a_body.test.values)

        elif isinstance(a_body, Name):
            count_var_into_map("", a_body, None)

        elif isinstance(a_body, BinOp):
            count_object_type([a_body.left])
            count_object_type([a_body.right])

        elif isinstance(a_body, commalist) :
            count_object_type(a_body)

        elif hasattr(a_body, 'elts'):
            count_object_type([a_body.elts])

        elif hasattr(a_body, 'body'):
            count_object_type([a_body.body])

        elif hasattr(a_body, 'value'):
            count_object_type([a_body.value])

        elif hasattr(a_body, 'values'):
            count_object_type(a_body.values)


def evaluate(training_src, test_src) :
    training_array = count_total_data(training_src)
    test_array = count_total_data(test_src)

    max = 0
    max_index = 0

    for i in range(0, 5) :
        if training_array[i] == 0 and test_array[i] > 0 :
            if i == 0 :
                return "List를 사용해 보세요"
            elif i == 1 :
                return "Dictionary를 사용해 보세요"
            elif i == 2 :
                return "Tuple을 사용해 보세요"
            elif i == 3 :
                return "Set을 사용해 보세요"
            else :
                return "Map을 사용해 보세요"

        else :
            if test_array[i] == 0 :
                continue
            cur = abs(test_array[i] - training_array[i])/test_array[i]
            if cur > max :
                max = cur
                max_index = i


    if max == 0 :
        return "사소한 값들이 잘못 설정되어있음"
    else :
        if max_index == 0 :
            return "List 사용 방식이 잘못됨"
        elif max_index == 1 :
            return "Dictionary 사용 방식이 잘못됨"
        elif max_index == 2 :
            return "Tuple 사용 방식이 잘못됨"
        elif max_index == 3 :
            return "Set 사용 방식이 잘못됨"
        elif max_index == 4 :
            return "Map 사용 방식이 잘못됨"
        return ""


def count_total_data(source_code) :
    global func_count_map
    global func_node_map
    global list_map
    global dict_map
    global tuple_map
    global set_map
    global map_map

    source_code = source_code.strip()
    new_src_code = ""
    for a_src in source_code.split("\n") :
        if a_src.find('class ') > -1 and a_src.find("()") > -1 :
            a_src = a_src.replace("()", "(self)")
        new_src_code = new_src_code + a_src + "\n"

    p = pythonparser.parse(new_src_code)
    count_object_type(p.body)

    total_array = [total_list_data(list_map), total_dict_data(dict_map), total_tuple_data(tuple_map),
                   total_set_data(set_map), total_map_data(map_map)]

    list_map = {}
    dict_map = {}
    tuple_map = {}
    set_map = {}
    map_map = {}
    func_count_map = {}
    func_node_map = {}

    return total_array


def total_list_data(list_map) :
    sum = 0

    for key in list_map:
        sum = sum + list_map[key]

    return sum


def total_dict_data(dict_map):
    sum = 0
    for key in dict_map:
        sum = sum + dict_map[key]
    return sum


def total_tuple_data(tuple_map):
    sum = 0
    for key in tuple_map:
        sum = sum + tuple_map[key]
    return sum


def total_set_data(set_map) :
    sum = 0

    for key in set_map:
        sum = sum + set_map[key]

    return sum


def total_map_data(map_map) :
    sum = 0

    for key in map_map:
        sum = sum + map_map[key]

    return sum


wrong_source_code = '''

import math
def reconstruct_path(cameFrom, current):
    total_path = list([current])
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return total_path

def A_star(graph, start, goal): #start : ex) (0,0)
    openset = list([start])
    cameFrom = dict()
    
    gScore = dict() #gscore[n] n 까지의 최소 길이
    for i in graph.keys():
        gScore[i] = float('inf')
    gScore[goal] = float('inf')
    gScore[start] = 0
    
    fScore = dict()
    for i in graph.keys():
        fScore[i] = float('inf')
    fScore[start] = heuristic(start,goal) # h(start) = goal 까지의길이
    while openset != []:
        current = openset[0]
        for i in openset:
            if fScore[i] < fScore[current]:
                current = i
        if current == goal:
            return reconstruct_path(cameFrom,current)
        openset.remove(current)

        for neighbor in graph.get(current).keys():
            tentative_gScore = gScore[current] + graph.get(current).get(neighbor)
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + heuristic(neighbor,goal)
                if neighbor not in openset:
                    openset.append(neighbor)
    

    return False
def heuristic(start, goal):
    return math.sqrt((start[0]-goal[0])**2 + (start[1]- goal[1])**2)

def mazeinput():
    a = input().split()
    n = int(a[0])  #미로의 세로로샛을때 갯수
    m = int(a[1])  #미로의 가로로셋을때 갯수
    finaldict = dict()

    for i in range(n):
        line = input()
        for j in range(m):
            finaldict.update({(j,i):line[j]})
            
    return finaldict

def drawgraph(maze): #edges 생성 함수
    graph = dict() #키 : 튜플(현 좌표) , 밸류 : {연결되는 좌표 : 길이}
    #현재 노드 의 상하좌우를 탐색해서 W가아니면 edge 생성
    for i in maze.keys():
        if maze[i] == 'W':
            continue
        if maze[i] == 'E':
            continue
        x = i[0]
        y = i[1]
        graph[i] = dict()
        graphUpdate(graph,x-1,y,maze,i)
        graphUpdate(graph,x+1,y,maze,i)
        graphUpdate(graph,x,y-1,maze,i)
        graphUpdate(graph,x,y+1,maze,i)
        
            
    return graph

def graphUpdate(graph,x,y,maze,i):
    if maze[(x,y)] == 'R':
        graph.get(i).update( { (x,y) : 1 } )
            
    elif maze[(x,y)] == 'B':
        graph.get(i).update( { (x,y) : 3 } )
            
    elif maze[(x,y)] == 'E':
        graph.get(i).update( { (x,y) : 1 } )
    
    return

def find_start_goal_list(maze):
    startandgoal = list()
    for i in maze.keys():
        if maze[i] == 'S':
            startandgoal.append(i)
    for i in maze.keys():
        if maze[i] == 'E':
            startandgoal.append(i)
    return startandgoal

def redraw_maze(maze, cameFrom):
    currline = 0
    RorB = ['R','B']
    if cameFrom == False:
        for i in maze.keys():
            if currline != i[1]:
                currline = i[1]
                print()
            print(maze[i], end='')
        return

    for i in maze.keys():
        if currline != i[1]:
            currline = i[1]
            print()
        if i in cameFrom:
            if maze[i] in RorB:
                print('P', end='')
                continue
        print(maze[i], end='')

        

a = mazeinput()
b=drawgraph(a)
st_go = find_start_goal_list(a)
astar = A_star(b,st_go[0],st_go[1])
redraw_maze(a, astar)

'''

correct_source_code = '''
import math
import collections
def reconstruct_path(cameFrom, current):
    total_path = list([current])
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return total_path

def A_star(graph, start, goal): #start : ex) (0,0)
    openset = list([start])
    cameFrom = collections.OrderedDict()
    
    gScore = collections.OrderedDict() #gscore[n] n 까지의 최소 길이
    for i in graph.keys():
        gScore[i] = float('inf')
    gScore[goal] = float('inf')
    gScore[start] = 0
    
    fScore = collections.OrderedDict()
    for i in graph.keys():
        fScore[i] = float('inf')
    fScore[start] = heuristic(start,goal) # h(start) = goal 까지의길이
    while openset != []:
        current = openset[0]
        for i in openset:
            if fScore[i] < fScore[current]:
                current = i
        if current == goal:
            return reconstruct_path(cameFrom,current)
        openset.remove(current)

        for neighbor in graph.get(current).keys():
            tentative_gScore = gScore[current] + graph.get(current).get(neighbor)
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + heuristic(neighbor,goal)
                if neighbor not in openset:
                    openset.append(neighbor)
    

    return False
def heuristic(start, goal):
    return math.sqrt((start[0]-goal[0])**2 + (start[1]- goal[1])**2)

def mazeinput():
    a = input().split()
    n = int(a[0])  #미로의 세로로샛을때 갯수
    m = int(a[1])  #미로의 가로로셋을때 갯수
    finaldict = collections.OrderedDict()

    for i in range(n):
        line = input()
        for j in range(m):
            finaldict.update({(j,i):line[j]})
            
    return finaldict

def drawgraph(maze): #edges 생성 함수
    graph = collections.OrderedDict() #키 : 튜플(현 좌표) , 밸류 : {연결되는 좌표 : 길이}
    #현재 노드 의 상하좌우를 탐색해서 W가아니면 edge 생성
    for i in maze.keys():
        if maze[i] == 'W':
            continue
        if maze[i] == 'E':
            continue
        x = i[0]
        y = i[1]
        graph[i] = collections.OrderedDict()
        graphUpdate(graph,x-1,y,maze,i)
        graphUpdate(graph,x+1,y,maze,i)
        graphUpdate(graph,x,y-1,maze,i)
        graphUpdate(graph,x,y+1,maze,i)
        
            
    return graph

def graphUpdate(graph,x,y,maze,i):
    if maze[(x,y)] == 'R':
        graph.get(i).update( { (x,y) : 1 } )
            
    elif maze[(x,y)] == 'B':
        graph.get(i).update( { (x,y) : 3 } )
            
    elif maze[(x,y)] == 'E':
        graph.get(i).update( { (x,y) : 1 } )
    
    return

def find_start_goal_list(maze):
    startandgoal = list()
    for i in maze.keys():
        if maze[i] == 'S':
            startandgoal.append(i)
    for i in maze.keys():
        if maze[i] == 'E':
            startandgoal.append(i)
    return startandgoal

def redraw_maze(maze, cameFrom):
    currline = 0
    RorB = ['R','B']
    if cameFrom == False:
        for i in maze.keys():
            if currline != i[1]:
                currline = i[1]
                print()
            print(maze[i], end='')
        return

    for i in maze.keys():
        if currline != i[1]:
            currline = i[1]
            print()
        if i in cameFrom:
            if maze[i] in RorB:
                print('P', end='')
                continue
        print(maze[i], end='')

        

a = mazeinput()
b=drawgraph(a)
st_go = find_start_goal_list(a)
astar = A_star(b,st_go[0],st_go[1])
redraw_maze(a, astar)


'''
#print(evaluate(wrong_source_code, correct_source_code))