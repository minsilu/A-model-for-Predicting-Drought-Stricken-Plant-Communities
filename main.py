import numpy as np
import matplotlib.pyplot as plt
from config import *
from scipy.integrate import odeint
import random
from matplotlib.colors import LinearSegmentedColormap


def rainfall(t):
    drought_period = 365/2 # drought cycle period (in months)
    rain_period = 365/2 # rainfall cycle period (in months)
    irregular_stddev = IRR_LINE/2 # standard deviation of the irregular rainfall distribution

    # Generate the rainfall data for each pattern
    drought_rainfall = DROUGHT_LINE * np.sin(2*np.pi*t/drought_period) + DROUGHT_LINE
    rain_rainfall = RAIN_LINE * np.sin(2*np.pi*t/rain_period) + RAIN_LINE
    dryseason_rainfall = RAIN_LINE - RAIN_LINE * np.sin(2*np.pi*t/rain_period) 
    # irregular_rainfall = np.random.normal(IRR_LINE, irregular_stddev, len(t))
    
    irregular_rainfall = np.random.normal(IRR_LINE, irregular_stddev)
    while irregular_rainfall < 0 or irregular_rainfall > 2*IRR_LINE:
        irregular_rainfall = np.random.normal(IRR_LINE, irregular_stddev)

    # plt.figure(figsize=(16, 5))
    # plt.plot(t, drought_rainfall, label='Rainy Season(900mm/yr)')
    # plt.plot(t, dryseason_rainfall, label='Dry Season(900mm/yr)')
    # plt.plot(t, irregular_rainfall, label='Irregular Circle(900mm/yr)')
    # plt.xlabel('Time (days)')
    # plt.ylabel('Rainfall (mm)')
    # plt.legend()
    # plt.show()
    
    if WEATHER == 'drought':
        return drought_rainfall
    elif WEATHER == 'rainfall':
        return rain_rainfall
    elif WEATHER == 'irregular':
        return irregular_rainfall
    elif WEATHER == 'dryseason':
        return dryseason_rainfall

def water_use_rate(t, plant_type):
    # Calculate available water based on rainfall
    # available_water = rainfall(t)
    available_water = rainfall(t) #------------------------task4 chang!---------------------------------
    
    # Adjust available water based on plant type
    if plant_type == "wet":
        # available_water[ available_water < DROUGHT_LINE] *= 0
        # available_water[ (available_water>= DROUGHT_LINE) & (available_water<= RAIN_LINE)] *= 0.3
        # available_water[ available_water> RAIN_LINE] *= 0.7
        if available_water < DROUGHT_LINE:
            available_water = 0
        elif available_water >= DROUGHT_LINE and available_water <= RAIN_LINE:
            available_water *= 0.03 *0.28
        elif available_water > RAIN_LINE:
            available_water *= 0.07 *0.28
    elif plant_type == "xerophytic":
        # available_water *= 0.4
        available_water *= 0.04 *0.28
    elif plant_type == "common":
        # available_water[ available_water <= DROUGHT_LINE] *= 0 
        # available_water[ available_water > DROUGHT_LINE] *= 0.5
        if available_water <= DROUGHT_LINE:
            available_water = 0
        elif available_water > DROUGHT_LINE:
            available_water *= 0.05 *0.28
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
    stable_time = None
    flag = False
    for i in np.nditer(t):
        temp = n * water_use_rate(i, population_type) * ( 1- n/E - coef_competition(species_num) * (total-n)/E )
        if temp < 0: 
            temp = 0
        total += n * temp
        n += n * temp
        result.append(n)
        if n >= 0.99*E and flag == False:
            stable_time = i
            flag = True
            # print(n, stable_time)
    return np.array(result), stable_time


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
    global WEATHER, total
    weather_list = [ "rainfall", "irregular","dryseason"]
    change_weather_result = []
    for i in range(3):
        WEATHER = weather_list[i]
        total = 0
        
        t = np.linspace(25, 145, 121)
        m = 3 # 种群数量
        # 生成生态型列表，每个物种有三种生态型，每种生态型占1/3
        plant_type_list = ["wet", "common", "xerophytic"] * int(m/3)
        
        # # 打乱生态型列表，使得每个物种的生态型随机
        # random.shuffle(plant_type_list)
        
        community = np.zeros(len(t))
        # 原始假设：假设物种有3种，并且每个分别潮湿型、干旱性、常见型三种生态型，这三种类型分类依据是在不同的降雨条件下，物种的生长速率不同
        species = []
        stable_time = []
        bio_mass = []
        for i in range(m):
            one, time = species_population(N0,t, population_type= plant_type_list[i], species_num = m)
            species.append(one)
            stable_time.append(time)
            bio_mass.append(one[-1])
            community += one
        bio_mass.append(community[-1])
        

        plt.figure(figsize=(9,6))
        plt.plot(t, species[0], label="Wet")
        plt.plot(t, species[1], label="Common")
        plt.plot(t, species[2], label="Xerophytic")
        plt.plot(t, community, label="Community")
        plt.xlabel('Time(Days)')
        plt.ylabel('Biomass(Mg/ha)')
        plt.legend(loc='best')
        plt.show()
        
        print(WEATHER)
        print (stable_time)
        print (bio_mass)
        change_weather_result.append(community)
        
    plt.figure(figsize=(9,6))
    plt.plot(t, change_weather_result[0], label="Rainy season")
    plt.plot(t, change_weather_result[1], label="Irregular cycle")
    plt.plot(t, change_weather_result[2], label="Dry season")
    plt.xlabel('Time(Days)')
    plt.ylabel('Community Biomass(Mg/ha)')
    plt.legend(loc='best')
    plt.show()




def task2():
    t = np.linspace(1, 365, 365)
    m = np.linspace(0, 100, 101)
    global total
    bio_mass = []
    max_biomass = 0
    max_biomass_index = 0
    boundary_biomass_index = []
    boundary_biomass = []
    
    global mean_rainfall
    mean_rainfall = 400/365
    
    for i in np.nditer(m):
        total = 0 
        num = int(i)
        # 生成生态型列表
        plant_type_list = ["wet", "common", "xerophytic"]
        # 打乱生态型列表
        random.shuffle(plant_type_list)
        
        community = np.zeros(len(t))
        
        for j in range(num):
            one, time = species_population(N0, t, population_type= plant_type_list[random.randint(0,2)], species_num = num)
            community += one
        
        mass = community[-1]
        if mass > max_biomass:
            max_biomass = mass
            max_biomass_index = num
        if mass > 0.9*20 and mass < 1.1*20:
            boundary_biomass_index.append(num)
            boundary_biomass.append(mass)
        
        bio_mass.append(mass)
        print("Number of species: ", i)
    
    print ("Max biomass: ", max_biomass)
    print ("Max biomass index: ", max_biomass_index)
    print ("Boundary biomass index: ", boundary_biomass_index)
    print ("Boundary biomass: ", boundary_biomass)
    
    plt.figure(figsize=(9,6))
    plt.plot(m, bio_mass)
    plt.xlabel('Number of species')
    plt.ylabel('Biomass(Mg/ha)')
    plt.legend(loc='best')
    plt.show()
    
    return


def task3():
    global WEATHER, total
    plant_list = [ "wet", "common", "xerophytic"]
    change_plant_result = []
    for j in range(3):
        total = 0

        t = np.linspace(0, 365, 366)
        m = 3 # 种群数量
        community = np.zeros(len(t))
        
        bio_mass = []
        for i in range(m):
            one, time = species_population(N0,t, population_type= plant_list[j], species_num = m)
            community += one
        bio_mass.append(community[-1])
        

        print(plant_list[j])
        print (bio_mass)
        change_plant_result.append(community)
        
    plt.figure(figsize=(9,6))
    plt.plot(t, change_plant_result[0], label="wet")
    plt.plot(t, change_plant_result[1], label="common")
    plt.plot(t, change_plant_result[2], label="xerophytic")
    plt.xlabel('Time(Days)')
    plt.ylabel('Community Biomass(Mg/ha)')
    plt.legend(loc='best')
    plt.show()



def task4_rainfall(t):
    period = 365 / frequency
    rainfall = mean_rainfall * np.sin(2*np.pi*t/period) + mean_rainfall
    return rainfall

def task4_function(f,r):
    global frequency , mean_rainfall, total, K
    frequency = int(f)
    mean_rainfall = int(r/365)
    total = 0
    t = np.linspace(1, 365, 365)
    num = 50

    plant_type_list = ["wet", "common", "xerophytic"]
    random.shuffle(plant_type_list)
    community = np.zeros(len(t))
    
    for j in range(num):
        one, time = species_population(N0, t, population_type= plant_type_list[random.randint(0,2)], species_num = num)
        community += one
        
    mass = community[-1]
    return mass


def task4():
    # global K
    # K = mean_rainfall/1000 *100
    
    biomass_matrix = np.random.rand(10, 10)
    for i in range(10):
        for j in range(10):
            biomass_matrix[i, j] = task4_function( i+1, 100 + 100*j )
    print(biomass_matrix)
    
    part1 = biomass_matrix[:, :3]
    part2 = biomass_matrix[:, 3:7]
    part3 = biomass_matrix[:, 7:]

    start = [100,400,800]
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4))

    for i, part in enumerate([part1, part2, part3]):
        im = axes[i].imshow(part, cmap='coolwarm')
        axes[i].set_xticks(np.arange(0, part.shape[1], step=1))
        axes[i].set_xticklabels(np.arange(start[i], part.shape[1]*100 + start[i] , step= 100))
        axes[i].set_yticks(np.arange(0, part.shape[0], step=1))
        axes[i].set_yticklabels(np.arange(1 , 11, step= 1))
        cbar = axes[i].figure.colorbar(im, ax=axes[i])
        cbar.ax.set_ylabel('Biomass')

    # 调整子图布局和间距
    fig.tight_layout(pad=3.0)

    plt.show()
    
    # plt.imshow(biomass_matrix, cmap='hot')
    # plt.xticks(np.arange(0, 3, step=1), np.arange(100, 400, step= 100))
    # plt.yticks(np.arange(0, 10, step=1), np.arange(10, 0, step=-1))
    # cbar = plt.colorbar()
    # cbar.ax.set_ylabel('Color Depth')
    # plt.show()

    return

def task5_function(capacity):
    global K
    K = capacity
    
    t = np.linspace(0, 365, 366)
    num = 3
    plant_type_list = ["wet", "common", "xerophytic"]
    random.shuffle(plant_type_list)
    community = np.zeros(len(t))
    
    for j in range(num):
        one, time = species_population(N0, t, population_type= plant_type_list[random.randint(0,2)], species_num = num)
        community += one
    
    return community[-1]

def task5():
    D = 0.2
    dt = 1
    K_max = 100
    a = 5
    C_50 = 0.5

    C = np.zeros((100, 100))
    C[random.randint(20,80), random.randint(20,80)] = 2000

    for t in np.arange(0, 365, dt):
        C[1:-1, 1:-1] += D*dt*(C[2:, 1:-1] - 2*C[1:-1, 1:-1] + C[:-2, 1:-1] +
                                C[1:-1, 2:] - 2*C[1:-1, 1:-1] + C[1:-1, :-2])

    C = np.subtract(1, C)

    K_matrix  = K_max / (1 + np.exp(-a*(C - C_50)))
    
    biomass_matrix = np.zeros((100, 100))
    for i in range(100):
        print ("The progress is",i+1,"/100")
        for j in range(100):
            biomass_matrix[i, j] = task5_function(K_matrix[i, j])
    
    C_map = plt.imshow(C, cmap='viridis')
    C_colorbar = plt.colorbar(C_map)
    C_colorbar.set_label('Pollution Concentration')
    plt.show()

    K_map = plt.imshow(K_matrix, cmap='viridis')
    K_colorbar = plt.colorbar(K_map)
    K_colorbar.set_label('Environmental capacity after contamination')
    plt.show()
    
    cmap_colors = [(1.0, 0.9490196078431372, 0.0), (0.13333333333333333, 0.6941176470588235, 0.2980392156862745)]
    custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", cmap_colors)
    bio_map = plt.imshow(biomass_matrix, cmap=custom_cmap)
    bio_colorbar = plt.colorbar(bio_map)
    bio_colorbar.set_label('Biomass after contamination')
    plt.show()
    
    return


if __name__ == '__main__':
    # t = np.linspace(25, 145, 121)
    # rainfall(t)
    # task1()
    task5()
    # task4()
    
    
    

 


    



