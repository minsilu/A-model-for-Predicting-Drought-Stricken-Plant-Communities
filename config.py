# globe variables

WEATHER = 'drought'# 气候类型, 目前可选项有：'drought', 'rainfall', 'irregular'

# 不同天气类型下平均降水量
DROUGHT_LINE = 600/365
RAIN_LINE = 900/365
IRR_LINE = 900/365

K = 90 # 环境容纳量 单位是Mg/ha  1 Mg/ha = 10 g/(m^2)
E = 1 # 物种平均生态位
total = 0 # 群落初始总生物量
N0 = 0.01 # 物种初始总生物量