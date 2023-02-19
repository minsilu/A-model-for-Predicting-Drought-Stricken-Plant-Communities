# globe variables

WEATHER = 'drought' # 气候类型, 目前可选项有：'drought', 'rainfall', 'irregular'

# 不同天气类型下平均降水量
DROUGHT_LINE = 600/12
RAIN_LINE = 900/12
IRR_LINE = 900/12

K = 10000 # 环境容纳量
E = 100 # 物种平均生态位
total = 0 # 群落初始总生物量
N0 = 1 # 物种初始总生物量