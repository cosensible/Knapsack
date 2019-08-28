# -*- coding: utf-8 -*-

from mbo import MBO

class Knapsack(object):

    def __init__(self,input_data):
        lines = input_data.split('\n')
        firstLine = lines[0].split()
        self.item_num = int(firstLine[0])
        self.capacity = int(firstLine[1])

        self.values = []
        self.weights = []
        for i in range(1, self.item_num + 1):
            line = lines[i]
            parts = line.split()
            self.values.append(int(parts[0]))
            self.weights.append(int(parts[1]))


    def solve_it(self):
        # Modify this code to run your optimization algorithm
        mbo = MBO(item_num=self.item_num, values=self.values, weights=self.weights, weight_max=self.capacity, sper_size=15, larva_max=10,
                  iters=50)
        mbo.run()

        # prepare the solution in the specified output format
        output_data = str(mbo.best_value) + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, mbo.best_sol))
        return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
            ks = Knapsack(input_data)
        print(ks.solve_it())
    else:
        print('This test requires an input file.  Please select one from the data directory.\
         (i.e. python solver.py ./data/ks_4_0)')
