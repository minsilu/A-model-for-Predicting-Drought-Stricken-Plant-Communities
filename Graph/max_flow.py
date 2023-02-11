# Maximum Flow Problem，MFP
# reference: https://www.cnblogs.com/youcans/p/15181104.html
import matplotlib.pyplot as plt 
import networkx as nx  
from networkx.algorithms.flow import edmonds_karp 

if __name__ == '__main__':
    # 创建有向图
    G1 = nx.DiGraph()  
    G1.add_edge('s', 'a', capacity=6)  
    G1.add_edge('s', 'c', capacity=8)
    G1.add_edge('a', 'b', capacity=3)
    G1.add_edge('a', 'd', capacity=3)
    G1.add_edge('b', 't', capacity=10)
    G1.add_edge('c', 'd', capacity=4)
    G1.add_edge('c', 'f', capacity=4)
    G1.add_edge('d', 'e', capacity=3)
    G1.add_edge('d', 'g', capacity=6)
    G1.add_edge('e', 'b', capacity=7)
    G1.add_edge('e', 'j', capacity=4)
    G1.add_edge('f', 'h', capacity=4)
    G1.add_edge('g', 'e', capacity=7)
    G1.add_edge('h', 'g', capacity=1)
    G1.add_edge('h', 'i', capacity=3)
    G1.add_edge('i', 'j', capacity=3)
    G1.add_edge('j', 't', capacity=5)

    # 求网络最大流
    maxFlowValue, maxFlowDict = nx.maximum_flow(G1, 's', 't', flow_func=edmonds_karp)  # flow_func: 'edmonds_karp', 'shortest_augmenting_path', 'dinitz', 'preflow_push', 'boykov_kolmogorov'

    # 最大流途径
    edgeCapacity = nx.get_edge_attributes(G1, 'capacity')
    edgeLabel = {}  # 边的标签
    for i in edgeCapacity.keys():  # 整理边的标签，用于绘图显示
        edgeLabel[i] = f'c={edgeCapacity[i]:}'  # 边的容量
    edgeLists = []  # 最大流的边的 list
    for i in maxFlowDict.keys():
        for j in maxFlowDict[i].keys():
            edgeLabel[(i, j)] += ',f=' + str(maxFlowDict[i][j])  # 取出每条边流量信息存入边显示值
            if maxFlowDict[i][j] > 0:  # 网络最大流的边（流量>0）
                edgeLists.append((i,j))

    # 输出显示
    print("最大流值: ", maxFlowValue)
    print("最大流的途径及流量: ", maxFlowDict)  # 输出最大流的途径和各路径上的流量
    print("最大流的路径：", edgeLists)  # 输出最大流的途径

    # 绘制有向网络图
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = {'s': (1, 8), 'a': (6, 7.5), 'b': (9, 8), 'c': (1.5, 6), 'd': (4, 6), 'e': (8, 5.5),  # 指定顶点绘图位置
        'f': (2, 4), 'g': (5, 4), 'h': (1, 2), 'i': (5.5, 2.5), 'j': (9.5, 2), 't': (11, 6)}
    edge_labels = nx.get_edge_attributes(G1, 'capacity')
    ax.set_title("Maximum flow of petroleum network with NetworkX")  # 设置标题
    nx.draw(G1, pos, with_labels=True, node_color='c', node_size=300, font_size=10)  # 绘制有向图，显示顶点标签
    nx.draw_networkx_edge_labels(G1, pos, edgeLabel, font_color='navy')  # 显示边的标签：'capacity' + maxFlow
    nx.draw_networkx_edges(G1, pos, edgelist=edgeLists, edge_color='m')  # 设置指定边的颜色、宽度
    plt.axis('on')  
    plt.show()
