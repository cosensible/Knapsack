# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import itemgetter
from queue import PriorityQueue

Item = namedtuple("Item", ['i', 'v', 'w', 'vpw'])
Node = namedtuple("Node", ['est', 'cv', 'cw', 'ci', 'tk'])


def parse_input(input_data):
    global items, capacity, item_num, taken, sol, best_value, cur_value, cur_weight
    # parse the input
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_num = int(firstLine[0])
    capacity = int(firstLine[1])
    taken = [0] * item_num
    sol = []
    best_value = cur_value = cur_weight = 0

    items = []
    for i in range(1, item_num + 1):
        line = lines[i]
        parts = line.split()
        v = int(parts[0])
        w = int(parts[1])
        items.append(Item(i - 1, v, w, v / w))
    items.sort(key=itemgetter(3), reverse=True)


def greedy():
    global g_sol
    g_sol = [0]*item_num
    g_best_value = g_cur_weight = 0

    for it in items:
        if it.w+g_cur_weight <= capacity:
            g_best_value += it.v
            g_cur_weight += it.w
            g_sol[it.i] = 1
    return g_best_value


def bound(i):
    bound = cur_value
    cleft = capacity - cur_weight
    while (i < item_num and items[i].w <= cleft):
        bound += items[i].v
        cleft -= items[i].w
        i += 1
    if i < item_num:
        bound += cleft * items[i].vpw
    return bound


def trace(i):
    ''' Depth-first search strategies '''
    global taken, best_value, cur_weight, cur_value, sol
    if i == item_num:
        # print("find a feasible solution:")
        # print(taken)
        # print("The value is:",value)
        if cur_value > best_value:
            sol = list(taken)
            best_value = cur_value
        return

    it = items[i]
    if cur_weight + it.w <= capacity:
        cur_value += it.v
        cur_weight += it.w
        taken[it.i] = 1
        trace(i+1)
        cur_value -= it.v
        cur_weight -= it.w
        taken[it.i] = 0

    if bound(i+1) > best_value:
        trace(i+1)


def best_first_search():
    global taken, best_value, cur_weight, cur_value, sol
    q = PriorityQueue()
    q.put(Node(-bound(0), 0, 0, 0, 1))
    while not q.empty():
        node = q.get()
        if -node.est <= best_value:
            break

        if node.ci == item_num and node.cv > best_value:
            best_value = node.cv
            print(best_value)
            continue

        it = items[node.ci]
        cur_value = node.cv
        cur_weight = node.cw
        if (node.cw+it.w) <= capacity:
            q.put(Node(node.est, node.cv+it.v, node.cw+it.w, node.ci+1, 1))

        up = bound(node.ci+1)
        if up > best_value:
            q.put(Node(-up, node.cv, node.cw, node.ci+1, 0))


def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    global best_value, sol
    is_optimal = 1
    parse_input(input_data)
    best_value = greedy()

    try:
        trace(0)
    except Exception as e:
        print(e)
        if not sol:
            sol = g_sol
        is_optimal = 0

    # best_first_search()

    # prepare the solution in the specified output format
    output_data = str(best_value) + ' ' + str(is_optimal) + '\n'
    output_data += ' '.join(map(str, sol))
    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory.\
         (i.e. python solver1.py ./data/ks_4_0)')
