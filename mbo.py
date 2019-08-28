import numpy as np


class MBO(object):

    def __init__(self, item_num, values, weights, weight_max, sper_size, larva_max, alpha=0.9, mutation_prob=0.1,
                 iters=100):
        """
        item_num：物品个数
        values：价值集
        weights：重量集
        weight_max：背包容量
        sper_size：受精囊大小
        larva_max：产生幼虫数
        alpha：速度衰减因子
        mutation_prob：变异概率
        iters：迭代次数（遗传代数）
        """
        self.item_num = item_num
        self.values = np.array(values)
        self.weights = np.array(weights)
        self.weight_max = weight_max
        self.mutation_prob = mutation_prob

        self.sper_size = sper_size
        self.larva_max = larva_max
        self.alpha = alpha
        self.iters = iters

        # 随机初始化产生初始解
        # 并采用启发式方法来改进
        self.init_sol = self.random_solution(item_num)
        self.best_sol = self.improve_solution(self.init_sol)
        self.best_value = self.cal_value(self.best_sol)
        self.best_weight = self.cal_weight(self.best_sol)

        self.energy = 0.0  # 能量
        self.speed = 0.0  # 速度
        self.spers = []  # 受精囊
        self.larvas = []  # 幼虫

        # 保存迭代过程中的解，用于画图
        self.iter_values = []
        self.iter_weights = []

    def random_solution(self, n):
        """
        随机产生大小为n的解（蜂后）
        解必须满足背包条件
        """
        while True:
            solution = np.random.randint(0, 2, n)
            if self.lower_weight_max(solution):  # 如果能装包则退出 否则一直生成解
                break
        return solution

    def random_drone(self):
        """
        随机产生半解（雄蜂）
        返回值包括雄峰的基因和它的标记情况
        标记表示为1，标记基因为雄峰不存在基因
        """
        drone = np.random.randint(0, 2, self.item_num)
        drone_mark = np.array([0] * int(self.item_num / 2) + [1] * int(self.item_num - self.item_num / 2))
        np.random.shuffle(drone_mark)
        return (drone, drone_mark)

    def improve_solution(self, solution):
        """
        启发式改进这个解（工蜂照顾）
        在大小为1的邻域内逐步寻找局部最优解
        """
        new_solution = solution.copy()
        # 如果此解大过了背包容量，则随机逐件抽取物品直到小于背包容量
        while self.lower_weight_max(new_solution) == False:
            new_solution[np.random.randint(0, self.item_num)] = 0

        for i in range(self.item_num):
            tmp_solution = new_solution.copy()

            while True:  # 随机找一个要改变的0
                randint = np.random.randint(0, self.item_num)
                if tmp_solution[randint] == 0:
                    break
            tmp_solution[randint] = 1
            if self.lower_weight_max(tmp_solution) == False:
                continue
            if self.cal_value(tmp_solution) > self.cal_value(new_solution):
                new_solution = tmp_solution
        return new_solution

    def lower_weight_max(self, solution):
        """
        判断该解是否能装包
        """
        return sum(self.weights[solution == 1]) <= self.weight_max

    def cal_value(self, solution):
        """
        计算价值（适应度函数）
        """
        return sum(self.values[solution == 1])

    def cal_weight(self, solution):
        """
        计算重量
        """
        return sum(self.weights[solution == 1])

    def cal_prob(self, solution, drone):
        """
        计算蜂后和雄峰的交配概率
        """
        return np.exp((-abs(self.cal_value(solution) - self.cal_value(drone)) / self.weight_max) / self.speed)

    def crossover(self, solution, drone, drone_mark):
        """
        蜂后与雄蜂交配，产生幼虫
        """
        larva = np.array([0] * self.item_num)
        for i in range(self.item_num):
            # drone_mark[i]==1 表示标记基因，即雄蜂不存在基因
            larva[i] = solution[i] if drone_mark[i] == 1 else drone[i]
        return larva

    def mutation(self, solution):
        """
        变异操作
        """
        mutation_index = np.random.rand(self.item_num) < self.mutation_prob
        for i in range(self.item_num):
            if mutation_index[i]:
                solution[i] = 1 if solution[i] == 0 else 0

    def run(self):
        """
        运行MBO算法
        """
        for i in range(self.iters):  # 蜂后飞行次数

            # 保存当前解用于画图
            self.iter_values.append(self.best_value)
            self.iter_weights.append(self.best_weight)

            # 1.初始化能量和速度
            self.energy = np.random.uniform(0.5, 1)
            self.speed = np.random.uniform(0.5, 1)
            gamma = self.energy * 0.5 / self.sper_size  # 能量递减量

            # 2.获取雄蜂
            tmp_sol = self.best_sol.copy()
            while (self.energy > 0) and (len(self.spers) < self.sper_size):  # 等蜂后能量耗尽或受精囊满
                (drone, drone_mark) = self.random_drone()
                prob = self.cal_prob(tmp_sol, drone)  # 计算蜂后和雄峰交配的概率

                if np.random.rand() < prob:
                    self.spers.append((drone, drone_mark))  # 将雄蜂装进受精囊
                # 以speed概率将蜂后各个基因位翻转
                change_index = np.random.rand(self.item_num) < self.speed
                for j in range(self.item_num):
                    if change_index[j]:
                        tmp_sol[j] = 1 if tmp_sol[j] == 0 else 0

                # 更新能量和速度
                self.energy -= gamma
                self.speed *= self.alpha

            # 3.产生幼虫
            while (len(self.larvas) < self.larva_max) and len(self.spers) > 0:
                # 从受精囊随机选择一个雄蜂
                randi = np.random.randint(0, len(self.spers))
                drone, drone_mark = self.spers[randi]
                # 交配一次后雄蜂死掉
                del self.spers[randi]
                # 交配
                larva = self.crossover(self.best_sol, drone, drone_mark)
                # 变异
                self.mutation(larva)
                # 启发式改进新解（工蜂照顾幼虫）
                larva = self.improve_solution(larva)
                # 添加到幼虫堆
                self.larvas.append(larva)

            # 4.产生新蜂后
            fitnesses = [self.cal_value(larva) for larva in self.larvas]  # 计算适应度
            best_fit = max(fitnesses)
            if best_fit > self.best_value:  # 最优幼虫比当前蜂后好，则替代
                self.best_value = best_fit
                self.best_sol = self.larvas[fitnesses.index(best_fit)]
                self.best_weight = self.cal_weight(self.best_sol)
            self.larvas = []  # 杀死所有幼虫


if __name__=="__main__":
    # 物品个数
    item_num = 20
    # 物品价值
    values = [92, 4, 43, 83, 84, 68, 92, 82, 6, 44, 32, 18, 56, 83, 25, 96, 70, 48, 14, 58]
    # 物品重量
    weights = [44, 46, 90, 72, 91, 40, 75, 35, 8, 54, 78, 40, 77, 15, 61, 17, 75, 29, 75, 63]
    # 背包容量
    weight_max = 878

    """
    这里设置受精囊大小=15，幼虫最大数=10，迭代次数=50
    默认速度衰减因子=0.9，变异概率=0.1
    """
    mbo = MBO(item_num=item_num, values=values, weights=weights, weight_max=weight_max, sper_size=15, larva_max=10,
              iters=50)
    mbo.run()
    print("最优解：", mbo.best_sol)
    print("最优解重量：", mbo.best_weight)
    print("最优解价值：", mbo.best_value)