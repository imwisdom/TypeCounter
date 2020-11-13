import pythonparser
from pythonparser.ast import FunctionDef, Assign, Dict, List, Subscript, Index, Str, Num, Name, Attribute, If, Tuple, \
    Set, BinOp, While, DictComp, ListComp, Expr, ClassDef
from pythonparser.ast import For
from pythonparser.ast import Call
from pythonparser.parser import commalist
import math

loop_count = 8
recv_count = 4

func_count_map = {}
func_node_map = {}

class_count_map = {}
class_node_map = {}

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


def count_class_into_map(node):
    global class_count_map
    global class_node_map
    name = ""

    if hasattr(node, 'name'):
        name = node.name
    elif hasattr(node, 'id'):
        name = node.id

    if name == "" :
        return

    if not name in class_count_map:
        class_count_map[name] = 1
        class_node_map[name] = node
        count_object_type(node.body)
    else:
        class_count_map[name] = class_count_map[name] + 1
        class_node = class_node_map[name]

        if isinstance(class_node.body[0], FunctionDef) and class_node.body[0].name == "__init__" :
            count_object_type(class_node.body[0].body)


def count_var_into_map(target, value):
    name = ''

    if hasattr(target, 'name'):
        name = target.name
    elif hasattr(target, 'id'):
        name = target.id
    elif hasattr(target, 'value') and hasattr(target.value, 'id'):
        name = target.value.id

    global dict_map
    global list_map
    global tuple_map
    global set_map
    global map_map
    global class_count_map

    if name == '':
        return

    if name in dict_map:
        dict_map[name] = dict_map[name] + 1

    elif name in list_map:
        list_map[name] = list_map[name] + 1

    elif name in tuple_map:
        tuple_map[name] = tuple_map[name] + 1

    elif name in set_map:
        set_map[name] = set_map[name] + 1

    elif isinstance(value, DictComp) or isinstance(value, Dict) or \
            (isinstance(value, Index) and (isinstance(value.value, Str))):
        dict_map[name] = 1

    elif isinstance(value, ListComp) or isinstance(value, List) or (
            isinstance(value, Index) and isinstance(value.value, Num)):
        list_map[name] = 1

    elif isinstance(value, Tuple):
        tuple_map[name] = 1


    elif isinstance(value, Set):
        set_map[name] = 1

    elif isinstance(value, Call):
        value_func = value.func
        if isinstance(value_func, Name):
            func_name = value_func.id

            if func_name in class_count_map :
                count_class_into_map(value_func)
            elif func_name == 'dict' or func_name == 'defaultdict':
                dict_map[name] = 1
            elif func_name == 'map':
                map_map[name] = 1
            elif func_name == 'list':
                list_map[name] = 1
            elif func_name == 'set':
                set_map[name] = 1
            elif func_name == 'tuple':
                tuple_map[name] = 1

        elif isinstance(value_func, Attribute) and isinstance(value_func.value,
                                                              Name) and value_func.value.id == 'collections':
            if value_func.attr.find('dict') or value_func.attr.find('Dict'):
                dict_map[name] = 1
            elif value_func.attr.find('tuple'):
                tuple_map[name] = 1


def put_param_into_type_map(func_args, real_args):
    global dict_map
    global list_map
    global tuple_map
    global set_map
    global map_map

    for i in range(0, len(real_args)) :
        cur_real_args = ""
        if isinstance(real_args[i], Name):
            cur_real_args = real_args[i].id
        cur_func_args = func_args.args[i].arg

        if (isinstance(real_args[i], Subscript) and hasattr(real_args[i].slice, "value") and isinstance(real_args[i].slice.value, Str)) or \
                isinstance(real_args[i], Dict) or isinstance(real_args[i], DictComp) or cur_real_args in dict_map :
            if cur_func_args not in dict_map :
                dict_map[cur_func_args] = 1
            else :
                dict_map[cur_func_args] = dict_map[cur_func_args]+1

        if isinstance(real_args[i], Subscript) or isinstance(real_args[i], List) or isinstance(real_args[i], ListComp) or cur_real_args in list_map :
            if cur_func_args not in list_map :
                list_map[cur_func_args] = 1
            else :
                list_map[cur_func_args] = list_map[cur_func_args]+1

        if cur_real_args in tuple_map :
            if cur_func_args not in tuple_map :
                tuple_map[cur_func_args] = 1
            else :
                tuple_map[cur_func_args] = tuple_map[cur_func_args]+1

        if cur_real_args in set_map :
            if cur_func_args not in set_map :
                set_map[cur_func_args] = 1
            else :
                set_map[cur_func_args] = set_map[cur_func_args]+1

        if cur_real_args in map_map :
            if cur_func_args not in map_map :
                map_map[cur_func_args] = 1
            else :
                map_map[cur_func_args] = map_map[cur_func_args]+1


def count_object_type_in_method(body_list, parent_func_name, parent_recv_num):
    global loop_count
    global recv_count

    if parent_recv_num >= recv_count:
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

            if hasattr(a_body, 'args'):
                count_object_type_in_method(a_body.args, parent_func_name, parent_recv_num)

            if isinstance(a_body.func, Attribute):
                if str(type(a_body.func.attr)) == "<class 'str'>" and a_body.func.attr in func_node_map :
                    func_node = func_node_map[a_body.func.attr]
                    if a_body.func.attr == parent_func_name :
                        count_object_type_in_method(func_node.body, a_body.func.attr, parent_recv_num+1)
                    else :
                        put_param_into_type_map(func_node.args, a_body.args)
                        count_object_type_in_method(func_node.body, a_body.func.attr,
                                                    parent_recv_num)
                count_object_type_in_method([a_body.func], parent_func_name, parent_recv_num)
                continue

            if hasattr(a_body.func, 'value'):
                name = a_body.func.value.id
            elif hasattr(a_body.func, 'name'):
                name = a_body.func.name
            else:
                name = a_body.func.id

            if not name in func_node_map:
                if name in class_node_map :
                    count_object_type_in_method([class_node_map[name]], parent_func_name, parent_recv_num)
                else :
                    count_object_type_in_method([a_body.func], parent_func_name, parent_recv_num)
                continue
            func_node = func_node_map[name]

            if func_node != None:
                if name != parent_func_name:
                    put_param_into_type_map(func_node.args, a_body.args)
                    count_object_type_in_method(func_node.body, name, parent_recv_num)
                    count_func_into_map(func_node)
                else:
                    count_object_type_in_method(func_node.body, parent_func_name, parent_recv_num + 1)
                    count_func_into_map(func_node)

        elif isinstance(a_body, Assign):
            var_target = a_body.targets
            var_value = a_body.value

            if isinstance(var_target[0], Subscript):
                count_object_type_in_method(var_target, parent_func_name, parent_recv_num)
            elif isinstance(var_value, BinOp) and isinstance(var_value.left, List):
                count_var_into_map(var_target[0], var_value.left)
            elif isinstance(var_value, BinOp) and isinstance(var_value.right, List):
                count_var_into_map(var_target[0], var_value.right)
            else:
                count_var_into_map(var_target[0], var_value)

                if hasattr(var_value, "func") and hasattr(var_value.func, "attr") and var_value.func.attr == "split" \
                        and isinstance(var_target[0], Name):
                    global list_map
                    if var_target[0].id in list_map :
                        list_map[var_target[0].id] += 1
                    else :
                        list_map[var_target[0].id] = 1

            # count_object_type_in_method(var_target)
            count_object_type_in_method([var_value, None], parent_func_name, parent_recv_num)

        elif isinstance(a_body, Subscript):
            if a_body.slice is not None and isinstance(a_body.slice, Index):
                if isinstance(a_body.value, Subscript) or isinstance(a_body.value, Call):
                    count_object_type_in_method([a_body.value], parent_func_name, parent_recv_num)
                else:
                    count_var_into_map(a_body.value, a_body.slice)

        elif isinstance(a_body, If):
            count_object_type_in_method(a_body.body, parent_func_name, parent_recv_num)

            if hasattr(a_body, 'orelse'):
                count_object_type_in_method(a_body.orelse, parent_func_name, parent_recv_num)

            if hasattr(a_body.test, 'comparators'):
                count_object_type_in_method(a_body.test.comparators, parent_func_name, parent_recv_num)
                count_object_type_in_method([a_body.test.left], parent_func_name, parent_recv_num)

            if hasattr(a_body.test, 'values'):
                count_object_type_in_method(a_body.test.values, parent_func_name, parent_recv_num)

        elif isinstance(a_body, Name):
            count_var_into_map(a_body, None)

        elif isinstance(a_body, BinOp):
            count_object_type_in_method([a_body.left], parent_func_name, parent_recv_num)
            count_object_type_in_method([a_body.right], parent_func_name, parent_recv_num)

        elif isinstance(a_body, commalist):
            count_object_type_in_method(a_body, parent_func_name, parent_recv_num)

        elif isinstance(a_body, Expr):
            count_object_type_in_method([a_body.value], parent_func_name, parent_recv_num)

        elif hasattr(a_body, 'elts'):
            count_object_type_in_method([a_body.elts], parent_func_name, parent_recv_num)

        elif hasattr(a_body, 'body'):
            count_object_type_in_method([a_body.body], parent_func_name, parent_recv_num)

        elif hasattr(a_body, 'value'):
            count_object_type_in_method([a_body.value], parent_func_name, parent_recv_num)

        elif str(type(a_body)) == "<class 'list'>" and len(a_body)>1:
            count_object_type_in_method(a_body, parent_func_name, parent_recv_num)


def count_object_type(body_list):
    global loop_count
    global recv_count
    global func_node_map
    global class_node_map

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
            if hasattr(a_body, 'args'):
                count_object_type(a_body.args)

            if isinstance(a_body.func, Attribute):
                if str(type(a_body.func.attr)) == "<class 'str'>" and a_body.func.attr in func_node_map :
                    func_node = func_node_map[a_body.func.attr]
                    put_param_into_type_map(func_node.args, a_body.args)
                    count_object_type_in_method(func_node.body, a_body.func.attr, 0)
                count_object_type([a_body.func])
                continue

            if hasattr(a_body.func, 'value'):
                name = a_body.func.value.id
            elif hasattr(a_body.func, 'name'):
                name = a_body.func.name
            else:
                name = a_body.func.id

            if not name in func_node_map:
                if name in class_node_map :
                    count_object_type([class_node_map[name]])
                else :
                    count_object_type([a_body.func])
                continue

            func_node = func_node_map[name]

            if func_node is not None:
                put_param_into_type_map(func_node.args, a_body.args)
                count_object_type_in_method(func_node.body, name, 0)
                count_func_into_map(func_node)

        elif isinstance(a_body, Assign):
            var_target = a_body.targets
            var_value = a_body.value

            if isinstance(var_target[0], Subscript):
                count_object_type(var_target)
            elif isinstance(var_value, BinOp) and isinstance(var_value.left, List):
                count_var_into_map(var_target[0], var_value.left)
            elif isinstance(var_value, BinOp) and isinstance(var_value.right, List):
                count_var_into_map(var_target[0], var_value.right)
            else:
                count_var_into_map(var_target[0], var_value)

                if hasattr(var_value, "func") and hasattr(var_value.func, "attr") and var_value.func.attr == "split" \
                        and isinstance(var_target[0], Name):
                    global list_map
                    if var_target[0].id in list_map :
                        list_map[var_target[0].id] += 1
                    else :
                        list_map[var_target[0].id] = 1

            count_object_type([var_value])

        elif isinstance(a_body, Subscript):
            if a_body.slice is not None and isinstance(a_body.slice, Index):
                if isinstance(a_body.value, Subscript) or isinstance(a_body.value, Call):
                    count_object_type([a_body.value])
                else:
                    count_var_into_map(a_body.value, a_body.slice)

        elif isinstance(a_body, If):
            count_object_type(a_body.body)

            if hasattr(a_body, 'orelse'):
                count_object_type(a_body.orelse)
            if hasattr(a_body.test, 'comparators'):
                count_object_type(a_body.test.comparators)
                count_object_type([a_body.test.left])
            if hasattr(a_body.test, 'values'):
                count_object_type(a_body.test.values)

        elif isinstance(a_body, Name):
            count_var_into_map(a_body, None)

        elif isinstance(a_body, BinOp):
            count_object_type([a_body.left])
            count_object_type([a_body.right])

        elif isinstance(a_body, ClassDef):
            count_class_into_map(a_body)

        elif isinstance(a_body, Expr) :
            count_object_type([a_body.value])

        elif isinstance(a_body, commalist):
            count_object_type(a_body)

        elif hasattr(a_body, 'elts'):
            count_object_type([a_body.elts])

        elif hasattr(a_body, 'body'):
            count_object_type([a_body.body])

        elif hasattr(a_body, 'value'):
            count_object_type([a_body.value])

        elif hasattr(a_body, 'values'):
            count_object_type(a_body.values)

        elif str(type(a_body)) == "<class 'list'>" and len(a_body)>1:
            count_object_type(a_body)

def evaluate_using_json_data(wrong_dict, correct_total_dict):

    count_dict = correct_total_dict["count"]
    not_used_list = []

    #similarity
    sum_dict = correct_total_dict["sum"]
    similarity = 0
    for key in wrong_dict :
        similarity = similarity + (wrong_dict[key] - sum_dict[key])**2
    similarity = math.sqrt(similarity)

    for key in count_dict:
        if count_dict[key] >= 0.85 and wrong_dict[key] == 0:
            not_used_list.append(key)

    if len(not_used_list) > 0 :
        for key in not_used_list :
            if (key == "List" and "Array" in wrong_dict and wrong_dict["Array"] > 0) or (key == "Array" and wrong_dict["List"] > 0) :
                not_used_list.remove(key)
        if len(not_used_list) > 0 :
            return "사용 권장 데이터 타입 : "+str(not_used_list), similarity

    sum_of_wrong = 0
    for key in wrong_dict :
        sum_of_wrong = sum_of_wrong + wrong_dict[key]

    diff_dict = {}

    for key in wrong_dict:
        if wrong_dict[key] == 0 :
            continue

        #cur_diff = (abs(sum_dict[key] - wrong_dict[key])/sum_dict[key])*(wrong_dict[key]/sum_of_wrong)

        cur_diff = math.sqrt((sum_dict[key] - wrong_dict[key])**2+((count_dict[key]-1)*10)**2)
        diff_dict[key] = cur_diff

    def sort_for_value(x):
        return x[1]

    sorted_diff = sorted(diff_dict.items(), key=sort_for_value, reverse=True)

    solve = ""
    if len(sorted_diff) > 0 :
        solve = "\n"+sorted_diff[0][0]+" 사용 방식이 잘못되었습니다."

    return str(sorted_diff)+solve

def evaluate(training_src, test_src):
    training_array = count_total_data(training_src)
    test_array = count_total_data(test_src)

    max = 0
    max_index = 0

    for i in range(0, 5):
        if training_array[i] == 0 and test_array[i] > 0:
            if i == 0:
                return "List를 사용해 보세요"
            elif i == 1:
                return "Dictionary를 사용해 보세요"
            elif i == 2:
                return "Tuple을 사용해 보세요"
            elif i == 3:
                return "Set을 사용해 보세요"
            else:
                return "Map을 사용해 보세요"

        else:
            if test_array[i] == 0:
                continue
            cur = abs(test_array[i] - training_array[i]) / test_array[i]
            if cur > max:
                max = cur
                max_index = i

    if max == 0:
        return "사소한 값들이 잘못 설정되어있음"
    else:
        if max_index == 0:
            return "List 사용 방식이 잘못됨"
        elif max_index == 1:
            return "Dictionary 사용 방식이 잘못됨"
        elif max_index == 2:
            return "Tuple 사용 방식이 잘못됨"
        elif max_index == 3:
            return "Set 사용 방식이 잘못됨"
        elif max_index == 4:
            return "Map 사용 방식이 잘못됨"
        return ""


def dict_total_data(source_code):
    total_array = count_total_data(source_code)
    total_dict = {"List": total_array[0], "Dictionary": total_array[1], "Tuple": total_array[2], "Set": total_array[3],
                  "Map": total_array[4]}

    return total_dict


def count_total_data(source_code):
    global func_count_map
    global func_node_map
    global list_map
    global dict_map
    global tuple_map
    global set_map
    global map_map

    source_code = source_code.strip()
    new_src_code = ""
    for a_src in source_code.split("\n"):
        if a_src.find('class ') > -1 and a_src.find("()") > -1:
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


def total_list_data(list_map):
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


def total_set_data(set_map):
    sum = 0

    for key in set_map:
        sum = sum + set_map[key]

    return sum


def total_map_data(map_map):
    sum = 0

    for key in map_map:
        sum = sum + map_map[key]

    return sum
