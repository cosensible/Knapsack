# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import itemgetter

Item = namedtuple("Item", ['i', 'v', 'w', 'vpw'])


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
         (i.e. python solver.py ./data/ks_4_0)')
