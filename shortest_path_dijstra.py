# single source shortest path algorithm for non-negative weight networks
# reference: https://blog.csdn.net/feriman/article/details/113619939



class Dijkstra:
    def __init__(self, graph, start, goal):
        self.graph = graph      # adjacency list
        self.start = start      # start
        self.goal = goal        # end

        # open list: the accessed nodes that have paths from the starting node
        # closed list：the nodes that optimal path has been found
        # parent: the parent-child relationship of the nodes
        self.open_list = {}  
        self.closed_list = {}  
        self.open_list[start] = 0.0     
        self.parent = {start: None}     # key is child, value is parent
        self.min_dis = None             # the length of the shortest path

    def shortest_path(self):

        while True:
            if self.open_list is None:
                print('search failed, over!')
                break
            distance, min_node = min(zip(self.open_list.values(), self.open_list.keys()))      # get the node with the smallest distance in open_list
            self.open_list.pop(min_node)                                                       # remove the node from open_list

            self.closed_list[min_node] = distance                  # add the node into closed_list 

            if min_node == self.goal:                             
                self.min_dis = distance
                shortest_path = [self.goal]                        
                father_node = self.parent[self.goal]           # backtracking
                while father_node != self.start:
                    shortest_path.append(father_node)
                    father_node = self.parent[father_node]
                shortest_path.append(self.start)
                
                print(shortest_path[::-1])                         # reverse the path
                print('the length of shortest path is ：{}'.format(self.min_dis))  
                print('fine the shortest path, over!')
                
                return shortest_path[::-1], self.min_dis			

            for node in self.graph[min_node].keys():               
                if node not in self.closed_list.keys():            
                    if node in self.open_list.keys():              
                        if self.graph[min_node][node] + distance < self.open_list[node]:
                            self.open_list[node] = distance + self.graph[min_node][node]         
                            self.parent[node] = min_node           
                    else:                                          
                        self.open_list[node] = distance + self.graph[min_node][node]            
                        self.parent[node] = min_node               


if __name__ == '__main__':
    # TODO: change the graph to your own graph
    # using adjacency list to represent the graph
    g = {'1': {'2': 2, '4': 1},
         '2': {'4': 3, '5': 11},
         '3': {'1': 4, '6': 5},
         '4': {'3': 2, '6': 8, '7': 4, '5': 2},
         '5': {'7': 6},
         '7': {'6': 1}
         }
    start = '1'
    goal = '6'
    dijk = Dijkstra(g, start, goal)
    dijk.shortest_path()

