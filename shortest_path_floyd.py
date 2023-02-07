# calculate the shortest path between any two points
import math

def floyed(graph):
    n_p = len(graph)
    dis = graph.copy()
    
    for k in range(n_p):
        dis_k = dis.copy()
        for i in range(n_p):
            for j in range(n_p):
                if dis[i][k] + dis[k][j] < dis[i][j]:
                    dis_k[i][j] = dis[i][k] + dis[k][j]
        dis = dis_k.copy()
    
    return dis_k

if __name__ == "__main__":
    inf = math.inf
    graph=[[0,inf,10,inf,30,100],
           [inf,0,5,inf,inf,inf],
           [inf,inf,0,50,inf,inf],
           [inf,inf,inf,0,inf,10],
           [inf,inf,inf,20,0,60],
           [inf,inf,inf,inf,inf,0]]
    print(floyed(graph))