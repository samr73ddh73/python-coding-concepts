# Concept: https://www.youtube.com/watch?v=aBxjDBC4M1U

class DisjointSet:
    def __init__(self, n):
        self.rank = [0 for _ in range(n)]
        self.parent = [i for i in range(n)]

    def unionByRank(self, u, v):
        pu, pv = self.findUltParent(u), self.findUltParent(v)
        if self.rank[pu] == self.rank[pv]:
            self.rank[pu] += 1
            self.parent[pv] = pu
        elif self.rank[pu] < self.rank[pv]:
            self.parent[pu] = pv
        else:
            self.parent[pv] = pu
        
    
    def findUltParent(self, u):
        if self.parent[u] == u:
            return u
        self.parent[u] = self.findUltParent(self.parent[u])
        return self.parent[u]


def main():
    d = DisjointSet(5)
    d.unionByRank(0,1)
    d.unionByRank(0,2)
    d.unionByRank(3,4)
    d.unionByRank(2,3)
    # print(d.findUltParent(3))
    # print(d.findUltParent(5))
    print(d.parent)
if __name__ == "__main__":
    main()

