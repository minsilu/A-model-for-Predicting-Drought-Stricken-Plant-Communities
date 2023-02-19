import numpy as np
import matplotlib.pyplot as plt
from config import *
from scipy.integrate import odeint
import random


def rainfall(t):
    drought_period = 12 # drought cycle period (in months)
    rain_period = 12 # rainfall cycle period (in months)
    irregular_stddev = IRR_LINE/2 # standard deviation of the irregular rainfall distribution

    # Generate the rainfall data for each pattern
    drought_rainfall = DROUGHT_LINE * np.sin(2*np.pi*t/drought_period) + DROUGHT_LINE
    rain_rainfall = RAIN_LINE * np.sin(2*np.pi*t/rain_period) + RAIN_LINE
    irregular_rainfall = np.random.normal(IRR_LINE, irregular_stddev, len(t))
    
    # irregular_rainfall = np.random.normal(IRR_LINE, irregular_stddev)
    # while irregular_rainfall < 0 or irregular_rainfall > 2*IRR_LINE:
    #     irregular_rainfall = np.random.normal(IRR_LINE, irregular_stddev)

    # plt.figure(figsize=(30, 5))
    # plt.plot(t, drought_rainfall, label='Drought Years(600mm/yr)')
    # plt.plot(t, rain_rainfall, label='Abundant Years(900mm/yr)')
    # plt.plot(t, irregular_rainfall, label='Irregular Years(900mm/yr)')
    # plt.xlabel('Time (months)')
    # plt.ylabel('Rainfall (mm)')
    # plt.legend()
    # plt.show()
    # 保存图片
    # plt.savefig('rainfall_120months.png')
    
    
    if WEATHER == 'drought':
        return drought_rainfall
    elif WEATHER == 'rainfall':
        return rain_rainfall
    elif WEATHER == 'irregular':
        return irregular_rainfall


def water_use_rate(t, plant_type):
    # Calculate available water based on rainfall
    available_water = rainfall(t)
    
    # Adjust available water based on plant type
    if plant_type == "wet":
        # available_water[ available_water < DROUGHT_LINE] *= 0
        # available_water[ (available_water>= DROUGHT_LINE) & (available_water<= RAIN_LINE)] *= 0.3
        # available_water[ available_water> RAIN_LINE] *= 0.7
        if available_water < DROUGHT_LINE:
            available_water = 0
        elif available_water >= DROUGHT_LINE and available_water <= RAIN_LINE:
            available_water *= 0.003
        elif available_water > RAIN_LINE:
            available_water *= 0.007
    elif plant_type == "xerophytic":
        # available_water *= 0.4
        available_water *= 0.004
    elif plant_type == "common":
        # available_water[ available_water <= DROUGHT_LINE] *= 0 
        # available_water[ available_water > DROUGHT_LINE] *= 0.5
        if available_water <= DROUGHT_LINE:
            available_water = 0
        elif available_water > DROUGHT_LINE:
            available_water *= 0.005
    # print(available_water)
    return available_water


def coef_competition(m):
    if m <= K/E:
        return 0
    elif m > K/E:
        return 1 - K/(E*m)


# def diff1(n, t):
#     n1,n2,n3 = n
#     w = np.array(water_use_rate(t, "common"))
#     b = coef_competition(m) 
#     dn1_dt = n1 * w * ( 1- n1/K - b * (n2+n3)/K )
#     dn2_dt = n2 * w * ( 1- n2/K - b * (n1+n3)/K )
#     dn3_dt = n3 * w * ( 1- n3/K - b * (n2+n3)/K )
#     return np.array([dn1_dt, dn2_dt, dn3_dt])


# 我们自己定义的积分函数,用于计算单个物种的生物量变化曲线
def species_population(n0, t, population_type="common", species_num = 3):
    result =[]
    global total
    total += n0
    n = n0 # 该物种当前生物量
    for i in np.nditer(t):
        total += n * water_use_rate(i, population_type) * ( 1- n/K - coef_competition(species_num) * (total-n)/K )
        n += n * water_use_rate(i, population_type) * ( 1- n/K - coef_competition(species_num) * (total-n)/K )
        result.append(n)
    return np.array(result)


# def pytask1():
#     N = odeint(diff1, N0, t)  
#     # N_total = np.sum(N, axis=1)
#     plt.figure(figsize=(9,6))
#     plt.plot(t, N[:,0], label="n1(t)")
#     plt.plot(t, N[:,1], label="n2(t)")
#     plt.plot(t, N[:,2], label="n3(t)")
#     # plt.plot(t, N_total, label="n(t)")
#     plt.xlabel('Time')
#     plt.ylabel('Population size')
#     plt.legend(loc='best')
#     plt.show()

def task1():
    t = np.linspace(0, 100, 101) # 时间周期，从0到100月, 一共101个点
    # N0 = 1 # 种群初始生物量
    m = 3 # 种群数量
    # 生成生态型列表，每个物种有三种生态型，每种生态型占1/3
    plant_type_list = ["wet", "xerophytic", "common"] * int(m/3)
    # 打乱生态型列表，使得每个物种的生态型随机
    random.shuffle(plant_type_list)
    result = np.zeros(len(t))
    # 原始假设：假设物种有30种，并且每个物种分为潮湿型、干旱性、常见型三种生态型，这三种类型分类依据是在不同的降雨条件下，物种的生长速率不同
    for i in range(m):
        result += species_population(N0,t, population_type= plant_type_list[i], species_num = m)
    
    # N_total = np.sum(N, axis=1)
    plt.figure(figsize=(9,6))
    plt.plot(t, result, label="n(t)")
    plt.xlabel('Time')
    plt.ylabel('Population size')
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    
    task1()
    # t = np.linspace(0, 120, 121)
    # rainfall(t)
    
    
    

 


    



