# reference: https://www.cnblogs.com/autoloop/p/15169642.html

import copy
import random
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
capacity = 200 # 容量上限
temperature=1000 # 初始温度
alpha=0.99 # 温度衰减系数
speed=1 # 车辆速度
HUGE=99999999 # 无穷大
early_unit_cost=0.2 # 提前服务时间的惩罚系数
late_unit_cost=0.5 # 延迟服务时间的惩罚系数
distance_unit_cost=1 # 距离的惩罚系数
best_sol=None # 最优解

class Node:
    def __init__(self):
        self.name = None
        self.x = None
        self.y = None
        self.demand = None # 需求量
        self.ready = None # 起始时间窗
        self.due = None # 结束时间窗
        self.service = None # 服务时间


class Sol:
    def __init__(self):
        self.path = []
        self.node = []
        self.cost=None

# TODO: 读取数据    
def read_data():
    sol = Sol()
    file_path = 'C101.txt'
    data = open(file_path, 'r')
    line_count = 0
    for line in data:
        line_count += 1
        if line_count < 10 or line_count>110:
            continue
        node = Node()
        cur_line = line[:-1].split(",")
        node.name = int(cur_line[0])
        node.x = int(cur_line[1])
        node.y = int(cur_line[2])
        node.demand = int(cur_line[3])
        node.ready = int(cur_line[4])
        node.due = int(cur_line[5])
        node.service = int(cur_line[6])
        sol.node.append(node)
    return sol


def init_code(sol):
    # 第0个点为起点
    sol.path = sol.node[1:]
    random.shuffle(sol.path)
    insert_depot(sol)
    # print([sol.path[i].name for i in range(len(sol.path))])

def insert_depot(sol):
    '''
    给sol插入起点
    '''
    sum_demand = 0
    cur_path = []
    for i in range(len(sol.path)):
        sum_demand += sol.path[i].demand
        if sum_demand > capacity: # 超过容量, 插入起点
            cur_path.append(sol.node[0])
            sum_demand=sol.path[i].demand
        cur_path.append(sol.path[i])
    sol.path=cur_path
    sol.path.append(sol.node[0])
    sol.path.insert(0,sol.node[0])


def get_distance(x1,y1,x2,y2):
    return np.hypot(x1-x2,y1-y2)


def get_cost(sol):
    total_cost=0
    distance_cost=0 # 行驶里程成本
    early_cost=0 # 时间窗早到成本
    late_cost=0 # 时间窗晚到成本
    sum_demand=0 # 载重成本
    now_time=0 # 当前时间
    for i in range(len(sol.path)):
        if i==0:
            continue # 起点无需处理
        distance=get_distance(sol.path[i-1].x,sol.path[i-1].y,sol.path[i].x,sol.path[i].y)
        distance_cost+=distance*distance_unit_cost
        now_time+=distance/speed
        sum_demand+=sol.path[i].demand
        if sum_demand>capacity:
            total_cost+=HUGE
        if now_time<sol.path[i].ready:
            early_cost+=(sol.path[i].ready-now_time)*early_unit_cost
            now_time=sol.path[i].ready
        if now_time>sol.path[i].due:
            late_cost += (now_time-sol.path[i].due) * late_unit_cost
        now_time+=sol.path[i].service
        if sol.path[i].name==0:
            now_time=0
            sum_demand=0
    total_cost+=distance_cost+early_cost+late_cost
    sol.cost=total_cost
    return total_cost

# 邻域搜索
def local_search(sol):
    global best_sol
    temp_sol=copy.deepcopy(sol)
    temp2_sol=copy.deepcopy(sol)
    for i in range(10):
        change(temp2_sol)
        if get_cost(temp2_sol)<get_cost(temp_sol):
            temp_sol=copy.deepcopy(temp2_sol)
    c1=get_cost(temp_sol)
    c2=get_cost(sol)
    if c1<c2:
        if c1<best_sol.cost:
            best_sol=temp_sol
        sol=temp_sol
    else:
        if np.exp((c2-c1)/temperature)<random.random(): #是否能被模拟退火准则接受
            sol = temp_sol
    return sol


def change(sol):
    pos1=random.randint(1,len(sol.path)-2)
    pos2=random.randint(1,len(sol.path)-2)
    sol.path[pos1],sol.path[pos2]=sol.path[pos2],sol.path[pos1]


def plot(sol):
    temp_path_x=[sol.path[0].x]
    temp_path_y=[sol.path[0].y]
    for i in range(len(sol.path)):
        if i==0:
            continue
        temp_path_x.append(sol.path[i].x)
        temp_path_y.append(sol.path[i].y)
        if sol.path[i].name==0:
            plt.plot(temp_path_x,temp_path_y)
            temp_path_x=[sol.path[i].x]
            temp_path_y=[sol.path[i].y]
    plt.show()


if __name__ == '__main__':
    sol=read_data()
    init_code(sol)
    print(get_cost(sol))
    best_sol=copy.deepcopy(sol)
    cost=[] # 记录邻域搜索每次迭代的cost
    for i in tqdm(range(2000)): # 迭代次数
        sol=local_search(sol)
        cost.append(sol.cost)
        temperature*=alpha
    plt.plot(cost) # 绘制cost收敛曲线
    plt.show()
    plot(best_sol)
    print([best_sol.path[i].name for i in range(len(best_sol.path))])





