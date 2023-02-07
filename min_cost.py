# Minimum Cost Flow, MCF
# reference: https://www.cnblogs.com/youcans/p/15181104.html

import matplotlib.pyplot as plt # 导入 Matplotlib 工具包
import networkx as nx  # 导入 NetworkX 工具包

if __name__ == '__main__':
    # 创建有向图, weight为边的成本，capacity为边的容量
    G2 = nx.DiGraph() 
    G2.add_edges_from([('s','v1',{'capacity': 7, 'weight': 4}),
                    ('s','v2',{'capacity': 8, 'weight': 4}),
                    ('v1','v3',{'capacity': 9, 'weight': 1}),
                    ('v2','v1',{'capacity': 5, 'weight': 5}),
                    ('v2','v4',{'capacity': 9, 'weight': 4}),
                    ('v3','v4',{'capacity': 6, 'weight': 2}),
                    ('v3','t',{'capacity': 10, 'weight': 6}),
                    ('v4','v1',{'capacity': 2, 'weight': 1}),
                    ('v4','t',{'capacity': 5, 'weight': 2})]) 
   
    # 整理边的标签，用于绘图显示
    edgeLabel1 = nx.get_edge_attributes(G2, 'capacity')
    edgeLabel2 = nx.get_edge_attributes(G2, 'weight')
    edgeLabel = {}
    for i in edgeLabel1.keys():
        edgeLabel[i] = f'({edgeLabel1[i]:},{edgeLabel2[i]:})'  # 边的(容量，成本)

    # 计算最短路径---非必要，用于与最小费用流的结果进行比较
    lenShortestPath = nx.shortest_path_length(G2, 's', 't', weight="weight")
    shortestPath = nx.shortest_path(G2, 's', 't', weight="weight")
    print("\n最短路径: ", shortestPath)  # 输出最短路径
    print("最短路径长度: ", lenShortestPath)  # 输出最短路径长度

    # 计算最小费用最大流---非必要，用于与最小费用流的结果进行比较
    minCostFlow = nx.max_flow_min_cost(G2, 's', 't')  # 求最小费用最大流
    minCost = nx.cost_of_flow(G2, minCostFlow)  # 求最小费用的值
    maxFlow = sum(minCostFlow['s'][j] for j in minCostFlow['s'].keys())  # 求最大流量的值
    print("\n最大流量: {}".format(maxFlow))  # 输出最小费用的值
    print("最大流量的最小费用: {}\n".format(minCost))  # 输出最小费用的值

    # v = input("Input flow (v>=0):")
    v = 0
    while True:
        v += 1  # 最小费用流的流量
        G2.add_node("s", demand=-v)  # nx.min_cost_flow() 的设置要求
        G2.add_node("t", demand=v)  # 设置源点/汇点的流量

        try: # Youcans@XUPT
            # 求最小费用流(demand=v)
            minFlowCost = nx.min_cost_flow_cost(G2)  # 求最小费用流的费用
            minFlowDict = nx.min_cost_flow(G2)  # 求最小费用流
            print("流量: {:2d}\t最小费用:{}".format(v, minFlowCost))  # 输出最小费用的值(demand=v)
            # print("最小费用流的路径及流量: ", minFlowDict)  # 输出最大流的途径和各路径上的流量
        except Exception as e:
            print("流量: {:2d}\t超出网络最大容量，没有可行流。".format(v))
            print("\n流量 v={:2d}：计算最小费用流失败({})。".format(v, str(e)))
            break  # 结束 while True 循环

    edgeLists = []
    for i in minFlowDict.keys():
        for j in minFlowDict[i].keys():
            edgeLabel[(i, j)] += ',f=' + str(minFlowDict[i][j])  # 取出每条边流量信息存入边显示值
            if minFlowDict[i][j] > 0:
                edgeLists.append((i, j))

    maxFlow = sum(minFlowDict['s'][j] for j in minFlowDict['s'].keys())  # 求最大流量的值
    print("\n最大流量: {:2d},\t最小费用:{}".format(maxFlow, minFlowCost))  # 输出最小费用的值
    print("最小费用流的路径及流量: ", minFlowDict)  # 输出最小费用流的途径和各路径上的流量
    print("最小费用流的路径：", edgeLists)  # 输出最小费用流的途径

    # 绘制有向网络图
    pos={'s':(0,5),'v1':(4,2),'v2':(4,8),'v3':(10,2),'v4':(10,8),'t':(14,5)}  # 指定顶点绘图位置
    fig, ax = plt.subplots(figsize=(8,6))
    ax.text(6,2.5,"youcans-xupt",color='gainsboro')
    ax.set_title("Minimum Cost Maximum Flow with NetworkX")
    nx.draw(G2,pos,with_labels=True,node_color='c',node_size=300,font_size=10)   # 绘制有向图，显示顶点标签
    nx.draw_networkx_edge_labels(G2,pos,edgeLabel,font_size=10)  # 显示边的标签：'capacity','weight' + minCostFlow
    nx.draw_networkx_edges(G2,pos,edgelist=edgeLists,edge_color='m',width=2)  # 设置指定边的颜色、宽度
    plt.axis('on')
    plt.show()
