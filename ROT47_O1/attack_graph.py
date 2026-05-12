class AttackGraph:
    def __init__(self):
        self.graph = {}
    def add_node(self, name: str):
        if name not in self.graph:
            self.graph[name] = []
        else:
            return None  
    def add_edge(self, src: str, dst: str, cost: float):
        if src in self.graph:
            self.graph[src].append([dst, cost])
        else:
            return None    
    def neighbors(self, name: str) -> list: 
        if name in self.graph:
            return self.graph[name]
        else:
            return []
    def has_cycle(self) -> bool:
        color = {}
        white = "WHITE"
        gray = "GRAY"
        black = "BLACK"
        for name in self.graph.keys():
            color[name] = white 
        def dfs(name):
            color[name] = gray
            for neighbor in self.neighbors(name):
                if color[neighbor[0]] == gray:
                    return True
                if  color[neighbor[0]] == white:
                    if dfs(neighbor[0]):
                        return True
            color[name] = black
            return False
        for name in color:
            if color[name] == white:
                if dfs(name):
                    return True
        return False  
    def topological_sort(self) -> list: 
        in_degree = {}  
        queue = []
        result = []
        for name in self.graph:
            in_degree[name] = 0
        for name in self.graph:
            for neighbor in self.neighbors(name):
                in_degree[neighbor[0]] += 1
        for name in in_degree:
            if in_degree[name] == 0:
                queue.append(name)
        while len(queue)  > 0:
            node = queue.pop(0)
            result.append(node) 
            for neighbor in self.neighbors(node):
                in_degree[neighbor[0]] -= 1
                if in_degree[neighbor[0]] == 0:
                    queue.append(neighbor[0])
        if len(result) != len(self.graph):
            raise ValueError("cycle detected")
        else:
            return result
    def cheapest_path(self, src: str, dst: str) -> tuple:
        dist = {}
        prev = {}
        for node in self.graph:
            dist[node] = float("infinity")
            prev[node] = None
        dist[src] = 0
        unvisited = set(self.graph.keys())
        path = []
        while unvisited:
            current = None
            for node in unvisited:
                if current is None or dist[current] > dist[node]:
                    current = node
            unvisited.remove(current)
            for neighbor in self.neighbors(current):
                new_dist = dist[current] + neighbor[1]
                if new_dist < dist[neighbor[0]]:
                    dist[neighbor[0]] = new_dist
                    prev[neighbor[0]] = current
        if dist[dst] == float("infinity"):
            raise ValueError
        current = dst
        while current is not None:
            path.append(current)
            current = prev[current]
        path.reverse()
        return (dist[dst],path)
if __name__ == "__main__":
    g = AttackGraph()
    for node in ['recon','env_audit','data_collect','model_probe','fgsm_attack','pgd_attack','transfer','exfil']:
        g.add_node(node)
    edges = [('recon','env_audit',1.0), ('recon','data_collect',2.0),('env_audit','model_probe',1.5), ('data_collect','model_probe',0.5),('model_probe','fgsm_attack',3.0), ('model_probe','pgd_attack',4.0),('fgsm_attack','transfer',1.0), ('pgd_attack','transfer',1.0),('transfer','exfil',0.5),]
    for s,d,c in edges: g.add_edge(s,d,c)
    print(g.topological_sort())
    print(g.cheapest_path('recon','exfil'))   
    # Injection 4: Self-loop
    g5 = AttackGraph()
    g5.add_node('A')
    g5.add_edge('A','A',0.0)
    print(g5.has_cycle())  # Must return True

