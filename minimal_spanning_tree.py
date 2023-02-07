INF = 9999

class Graph(object):
    def __init__(self, maps):
        self.maps = maps
        self.nodenum = self.get_nodenum()
        self.edgenum = self.get_edgenum()
 
    def get_nodenum(self):
        return len(self.maps)
 
    def get_edgenum(self):
        count = 0
        for i in range(self.nodenum):
            for j in range(i):
                if self.maps[i][j] > 0 and self.maps[i][j] < INF:
                    count += 1
        return count
 
    # use for sparse graphs
    def kruskal(self):
        res = []
        if self.nodenum <= 0 or self.edgenum < self.nodenum-1:
            return res
        edge_list = []
        for i in range(self.nodenum):
            for j in range(i,self.nodenum):
                if self.maps[i][j] < INF:
                    edge_list.append([i, j, self.maps[i][j]])#按[begin, end, weight]形式加入
        edge_list.sort(key=lambda a:a[2])#已经排好序的边集合
        
        group = [[i] for i in range(self.nodenum)]
        for edge in edge_list:
            for i in range(len(group)):
                if edge[0] in group[i]:
                    m = i
                if edge[1] in group[i]:
                    n = i
            if m != n:
                res.append(edge)
                group[m] = group[m] + group[n]
                group[n] = []
        return res
 
    # use for dense graphs
    def prim(self):
        res = []
        if self.nodenum <= 0 or self.edgenum < self.nodenum-1:
            return res
        res = []
        seleted_node = [0]
        candidate_node = [i for i in range(1, self.nodenum)]
        
        while len(candidate_node) > 0:
            begin, end, minweight = 0, 0, 9999
            for i in seleted_node:
                for j in candidate_node:
                    if self.maps[i][j] < minweight:
                        minweight = self.maps[i][j]
                        begin = i
                        end = j
            res.append([begin, end, minweight])
            seleted_node.append(end)
            candidate_node.remove(end)
        return res


if __name__ == '__main__':
    # TODO: replace the graph with your own (adjacency matrix)
    maps = [[0,7,INF,INF,INF,5], 
            [7,0,9,INF,3,INF], 
            [INF,9,0,6,INF,INF],
            [INF,INF,6,0,8,10], 
            [INF,3,INF,8,0,4], 
            [5,INF,INF,10,4,0]]
    graph = Graph(maps)
    
    print('------kruskal------')
    print(graph.kruskal())
    print('-------prim--------')
    print(graph.prim())