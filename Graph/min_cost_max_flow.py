# Minimum Cost Maximum Flow, MCMF
# reference: https://www.cnblogs.com/youcans/p/15181104.html

import numpy as np
import matplotlib.pyplot as plt 
import networkx as nx  

G3 = nx.DiGraph()  # 创建一个有向图 DiGraph
G3.add_edges_from([('s','v1',{'capacity': 13, 'weight': 7}),
                  ('s','v2',{'capacity': 9, 'weight': 9}),
                  ('v1','v3',{'capacity': 6, 'weight': 6}),
                  ('v1','v4',{'capacity': 5, 'weight': 5}),
                  ('v2','v1',{'capacity': 4, 'weight': 4}),
                  ('v2','v3',{'capacity': 5, 'weight': 2}),
                  ('v2','v5',{'capacity': 5, 'weight': 5}),
                  ('v3','v4',{'capacity': 5, 'weight': 2}),
                  ('v3','v5',{'capacity': 4, 'weight': 1}),
                  ('v3','t',{'capacity': 4, 'weight': 4}),
                  ('v4','t', {'capacity': 9, 'weight': 7}),
                  ('v5','t',{'capacity': 9, 'weight': 5})]) # 添加边的属性 'capacity', 'weight'

# 求最小费用最大流
minCostFlow = nx.max_flow_min_cost(G3, 's', 't')  # 求最小费用最大流
minCost = nx.cost_of_flow(G3, minCostFlow)  # 求最小费用的值
maxFlow = sum(minCostFlow['s'][j] for j in minCostFlow['s'].keys())  # 求最大流量的值

# # 数据格式转换
edgeLabel1 = nx.get_edge_attributes(G3,'capacity')  # 整理边的标签，用于绘图显示
edgeLabel2 = nx.get_edge_attributes(G3,'weight')
edgeLabel={}
for i in edgeLabel1.keys():
    edgeLabel[i]=f'({edgeLabel1[i]:},{edgeLabel2[i]:})'  # 边的(容量，成本)
edgeLists = []
for i in minCostFlow.keys():
    for j in minCostFlow[i].keys():
        edgeLabel[(i, j)] += ',f=' + str(minCostFlow[i][j])  # 将边的实际流量添加到 边的标签
        if minCostFlow[i][j]>0:
            edgeLists.append((i,j))

print("最小费用最大流的路径及流量: ", minCostFlow)  # 输出最大流的途径和各路径上的流量
print("最小费用最大流的路径：", edgeLists)  # 输出最小费用最大流的途径
print("最大流量: ", maxFlow)  # 输出最大流量的值
print("最小费用: ", minCost)  # 输出最小费用的值

# 绘制有向网络图
pos={'s':(0,5), 'v1':(3,9), 'v2':(3,1), 'v3':(6,5), 'v4':(9,9),'v5':(9,1), 't':(12,5)}  # 指定顶点绘图位置
fig, ax = plt.subplots(figsize=(8,6))
ax.text(5,1.5,"youcans-xupt",color='gainsboro')
ax.set_title("Minimum Cost Maximum Flow with NetworkX")
nx.draw(G3,pos,with_labels=True,node_color='c',node_size=300,font_size=10)   # 绘制有向图，显示顶点标签
nx.draw_networkx_edge_labels(G3,pos,edgeLabel,font_size=10)  # 显示边的标签：'capacity','weight' + minCostFlow
nx.draw_networkx_edges(G3,pos,edgelist=edgeLists,edge_color='m',width=2)  # 设置指定边的颜色、宽度
plt.axis('on') # Youcans@XUPT
plt.show()
