import numpy as np
import matplotlib.pyplot as plt
from config import *
from scipy.integrate import odeint
import random
from matplotlib.colors import LinearSegmentedColormap


def is_dry(t):
    len_rain = int((365 - 30 * frequency)/(12-frequency))
    if len_rain < 0: 
        len_rain = 0
    if (t % (len_rain+30)) > len_rain:
        return 1
    elif (t % (len_rain+30)) == len_rain and len_rain != 0:
        return 2
    return 0


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
        # if is_dry(t):
        #     return irregular_rainfall/3
        # else :
        #     return irregular_rainfall
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
        total += temp
        n += temp
        result.append(n)
        if n >= 0.99*E and flag == False:
            stable_time = i
            flag = True
            # print(n, stable_time)
        # if is_dry(i) ==2:
        #     total -= 0.1 * n 
        #     n *= 0.9
        
        
    return np.array(result), stable_time



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
    global frequency , IRR_LINE, total, dry_list
    
    frequency = int(f)
    IRR_LINE = int(r/365)
    
    total = 0
    t = np.linspace(1, 365, 365)
    
    num = 10
    plant_type_list = ["wet", "common", "xerophytic"]
    
    community = np.zeros(len(t))
    
    for j in range(num):
        one, time = species_population(N0, t, population_type= plant_type_list[random.randint(0,2)], species_num = num)
        community += one
     
    return community[-1]


def task4():

    # biomass_matrix = np.random.rand(10, 10)
    # for i in range(10):
    #     for j in range(10):
    #         biomass_matrix[i, j] = task4_function( i+1, 100 + 100*j )
    # print(biomass_matrix)
    
    # part1 = biomass_matrix[:, :3]
    # part2 = biomass_matrix[:, 3:7]
    # part3 = biomass_matrix[:, 7:]

    # start = [100,400,800]
    # fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4))

    # for i, part in enumerate([part1, part2, part3]):
    #     im = axes[i].imshow(part, cmap='coolwarm')
    #     axes[i].set_xticks(np.arange(0, part.shape[1], step=1))
    #     axes[i].set_xticklabels(np.arange(start[i], part.shape[1]*100 + start[i] , step= 100))
    #     axes[i].set_yticks(np.arange(0, part.shape[0], step=1))
    #     axes[i].set_yticklabels(np.arange(1 , 11, step= 1))
    #     cbar = axes[i].figure.colorbar(im, ax=axes[i])
    #     cbar.ax.set_ylabel('Biomass')

    # # 调整子图布局和间距
    # fig.tight_layout(pad=3.0)

    # plt.show()
    
    
    # 干旱范围更广的实验
    matrix = np.zeros((100, 100))

    percentage = 0.3
    num_points = int(percentage * matrix.size)
    indices = np.random.choice(range(matrix.size), num_points, replace=False)
    matrix.flat[indices] = random.randint(300, 600)
    matrix.flat[np.setdiff1d(range(matrix.size), indices)] = random.randint(600, 1200)
    
    biomass_matrix = np.zeros((100, 100))
    for i in range(100):
        print ("The progress is",i+1,"/100")
        for j in range(100):
            biomass_matrix[i, j] = task4_function(0, matrix[i, j])
    
    cmap_colors = [(1.0, 0.9490196078431372, 0.0), (0.13333333333333333, 0.6941176470588235, 0.2980392156862745)]
    custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", cmap_colors)
    bio_map = plt.imshow(biomass_matrix, cmap=custom_cmap)
    bio_colorbar = plt.colorbar(bio_map)
    bio_colorbar.set_label('Biomass distribution (drought range 70%)')
    plt.show()
    
    
    return

def task5_function(capacity):
    global K, total
    total = 0
    K = capacity
    
    t = np.linspace(1, 365, 365)
    num = 10
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


def sensitivity1():
    global total, DROUGHT_LINE
    line_list = [ 400/365,500/365,600/365,700/365,800/365]
    result = []
    for i in range(len(line_list)):
        DROUGHT_LINE = line_list[i]
        total = 0
        
        t = np.linspace(0, 365, 366)
        m = 30 # 种群数量
      
        plant_type_list = ["wet", "common", "xerophytic"] * int(m/3)
        
        community = np.zeros(len(t))

        species = []
        for j in range(m):
            one, time = species_population(N0,t, population_type= plant_type_list[j], species_num = m)
            species.append(one)
            community += one
        
        result.append(community)
        
    plt.figure(figsize=(9,6))
    plt.plot(t, result[0], label="400mm/365")
    plt.plot(t, result[1], label="500mm/365")
    plt.plot(t, result[2], label="600mm/365")
    plt.plot(t, result[3], label="700mm/365")
    plt.plot(t, result[4], label="800mm/365")
    plt.xlabel('Time(Days)')
    plt.ylabel('Community Biomass(Mg/ha)')
    plt.title('Community Biomass under different Drought Line')
    plt.legend(loc='best')
    plt.show()


def sensitivity2():
    global total, RAIN_LINE
    line_list = [ 700/365,800/365,900/365,1000/365,1100/365]
    result = []
    for i in range(len(line_list)):
        RAIN_LINE = line_list[i]
        total = 0
        
        t = np.linspace(0, 365, 366)
        m = 30 # 种群数量
      
        plant_type_list = ["wet", "common", "xerophytic"] * int(m/3)
        
        community = np.zeros(len(t))

        species = []
        for j in range(m):
            one, time = species_population(N0,t, population_type= plant_type_list[j], species_num = m)
            species.append(one)
            community += one
        
        result.append(community)
        
    plt.figure(figsize=(9,6))
    plt.plot(t, result[0], label="700mm/365")
    plt.plot(t, result[1], label="800mm/365")
    plt.plot(t, result[2], label="900mm/365")
    plt.plot(t, result[3], label="1000mm/365")
    plt.plot(t, result[4], label="1100mm/365")
    plt.xlabel('Time(Days)')
    plt.ylabel('Community Biomass(Mg/ha)')
    plt.title('Community Biomass under different Rain Line')
    plt.legend(loc='best')
    plt.show()
    
def sensitivity3():
    global total, N0
    line_list = [ 0.0001, 0.001, 0.01, 0.1]
    result = []
    for i in range(len(line_list)):
        N0 = line_list[i]
        total = 0
        
        t = np.linspace(0, 365, 366)
        m = 30 # 种群数量
      
        plant_type_list = ["wet", "common", "xerophytic"] * int(m/3)
        
        community = np.zeros(len(t))

        species = []
        for j in range(m):
            one, time = species_population(N0,t, population_type= plant_type_list[j], species_num = m)
            species.append(one)
            community += one
        
        result.append(community)
        
    plt.figure(figsize=(9,6))
    plt.plot(t, result[0], label="N0 = 0.0001 Mg/ha")
    plt.plot(t, result[1], label="N0 = 0.001 Mg/ha")
    plt.plot(t, result[2], label="N0 = 0.01 Mg/ha")
    plt.plot(t, result[3], label="N0 = 0.1 Mg/ha")
  
    
    plt.xlabel('Time(Days)')
    plt.ylabel('Community Biomass(Mg/ha)')
    plt.title('Community Biomass under different N0')
    plt.legend(loc='best')
    plt.show()

def sensitivity4():
    global total, E
    line_list = [0.5, 1, 3, 5, 10, 20]
    result = []
    for i in range(len(line_list)):
        E = line_list[i]
        total = 0
        
        t = np.linspace(0, 1500, 1501)
        m = 30 # 种群数量
      
        plant_type_list = ["wet", "common", "xerophytic"] * int(m/3)
        
        community = np.zeros(len(t))

        species = []
        for j in range(m):
            one, time = species_population(N0,t, population_type= plant_type_list[j], species_num = m)
            species.append(one)
            community += one
        
        result.append(community)
        
    plt.figure(figsize=(9,6))
    plt.plot(t, result[0], label="Mean niche 0.5 Mg/ha")
    plt.plot(t, result[1], label="Mean niche 1 Mg/ha")
    plt.plot(t, result[2], label="Mean niche 3 Mg/ha")
    plt.plot(t, result[3], label="Mean niche 5 Mg/ha")
    plt.plot(t, result[4], label="Mean niche 10 Mg/ha")
    plt.plot(t, result[5], label="Mean niche 20 Mg/ha")
  
    
    plt.xlabel('Time(Days)')
    plt.ylabel('Community Biomass(Mg/ha)')
    plt.title('Community Biomass under different Mean niche')
    plt.legend(loc='best')
    plt.show()

def sensitivity4():
    global total, E
    line_list = [0.5, 1, 3, 5, 10, 20]
    result = []
    for i in range(len(line_list)):
        E = line_list[i]
        total = 0
        
        t = np.linspace(0, 1500, 1501)
        m = 30 # 种群数量
      
        plant_type_list = ["wet", "common", "xerophytic"] * int(m/3)
        
        community = np.zeros(len(t))

        species = []
        for j in range(m):
            one, time = species_population(N0,t, population_type= plant_type_list[j], species_num = m)
            species.append(one)
            community += one
        
        result.append(community)
        
    plt.figure(figsize=(9,6))
    plt.plot(t, result[0], label="Mean niche 0.5 Mg/ha")
    plt.plot(t, result[1], label="Mean niche 1 Mg/ha")
    plt.plot(t, result[2], label="Mean niche 3 Mg/ha")
    plt.plot(t, result[3], label="Mean niche 5 Mg/ha")
    plt.plot(t, result[4], label="Mean niche 10 Mg/ha")
    plt.plot(t, result[5], label="Mean niche 20 Mg/ha")
  
    
    plt.xlabel('Time(Days)')
    plt.ylabel('Community Biomass(Mg/ha)')
    plt.title('Community Biomass under different Mean niche')
    plt.legend(loc='best')
    plt.show()

def sensitivity5():
    global total, K
    line_list = np.linspace(0, 100, 101)
    result = []
    
    for i in range(len(line_list)):
        K = line_list[i]
        total = 0
        
        t = np.linspace(0, 365, 366)
        m = 30 # 种群数量
      
        plant_type_list = ["wet", "common", "xerophytic"] * int(m/3)
        
        community = np.zeros(len(t))

        species = []
        for j in range(m):
            one, time = species_population(N0,t, population_type= plant_type_list[j], species_num = m)
            species.append(one)
            community += one
        
        result.append(community[-1])
        # print('process: ', i, '/100', 'total: ', community[-1])
        print(K, community[-1])
        
    plt.figure(figsize=(9,6))
    plt.plot(line_list, result)
    plt.xlabel('K(Mg/ha)')
    plt.ylabel('Community Biomass(Mg/ha)')
    plt.title('Biomass of communities under different K')
    plt.legend(loc='best')
    plt.show()


def water_draw(available_water, plant_type):
    # Adjust available water based on plant type
    if plant_type == "wet":
        available_water[ available_water < DROUGHT_LINE] *= 0
        available_water[ (available_water>= DROUGHT_LINE) & (available_water<= RAIN_LINE)] *= 0.03 * 0.28
        available_water[ available_water> RAIN_LINE] *= 0.07 * 0.28
        # if available_water < DROUGHT_LINE:
        #     available_water = 0
        # elif available_water >= DROUGHT_LINE and available_water <= RAIN_LINE:
        #     available_water *= 0.03 *0.28
        # elif available_water > RAIN_LINE:
        #     available_water *= 0.07 *0.28
    elif plant_type == "xerophytic":
        available_water *= 0.04 *0.28
    elif plant_type == "common":
        available_water[ available_water <= DROUGHT_LINE] *= 0 
        available_water[ available_water > DROUGHT_LINE] *= 0.05 *0.28
        # if available_water <= DROUGHT_LINE:
        #     available_water = 0
        # elif available_water > DROUGHT_LINE:
        #     available_water *= 0.05 *0.28
    # print(plant_type)
    # print(available_water)
    
    return available_water

def plant():
    
    plant_list = ["wet", "common", "xerophytic"] 
    result = []
    
    # ranfall = ranfall / 365
    # print(ranfall)
    
    for j in range(3):
        ranfall = np.linspace(0, 1500, 1501) / 365
        result.append(water_draw(ranfall, plant_list[j]))
        # print (water_draw(ranfall, plant_list[j]))
    
    ranfall = np.linspace(0, 1500, 1501) / 365
    plt.figure(figsize=(9,6))
    plt.plot(ranfall, result[0], label="Wet")
    plt.plot(ranfall, result[1], label="Common")
    plt.plot(ranfall, result[2], label="Xerophytic")
    plt.xlabel('Ranfall(mm/day)')
    plt.ylabel('Water Use Efficiency')
    plt.legend(loc='best')
    plt.show()
        
    return

if __name__ == '__main__':
    # t = np.linspace(25, 145, 121)
    # rainfall(t)
    # task1()
    # task2()
    plant()
    #sensitivity2()
    
    

 


    



