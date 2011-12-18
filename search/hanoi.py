import heapq

      
class State:
    def __init__(self, towers=([1, 2, 3, 4], [], [])):
        self.towers = towers
        self.f = self.g = self.h = 0
        self.parent = None

    def __hash__(self):
        return reduce(lambda x, y : x * 17 + y, [7] + sum(self.towers, []))

    def __eq__(self, other):
        return self.towers == other.towers

    def __repr__(self):
        return '%s (%s)' % (repr(self.towers), hash(self))

    def adjacents(self):
        """Return a list of legal successor states"""
        adjs = []
        for i, ti in enumerate(self.towers):
            if not ti:
                continue
            for j in [(i + d) % 3 for d in [1, 2]]:
                tj = self.towers[j]
                if (not tj) or tj[0] > ti[0]:
                    adj = [[], [], []]
                    adj[i] = ti[1:]
                    adj[j] = [ti[0]] + tj
                    k = [x for x in range(3) if x not in [i, j]][0]
                    adj[k] = self.towers[k]
                    state = State(adj)
                    adjs.append(state)
        return adjs

    def update(self, parent):
        self.parent = parent
        self.g = parent.g + 1
        self.h = 4 - len(self.towers[2])
        self.f = self.g + self.h

    def path(self):
        path = []
        state = self
        while state.parent:
            path.append(state)
            state = state.parent
        path.reverse()
        return path
            

frontier = []
heapq.heapify(frontier)
visited = set()

def search(start, end):
    expanded = 0
    heapq.heappush(frontier, (start.f, start))
    while frontier:
        h, state = heapq.heappop(frontier)
        visited.add(state)
        expanded += 1
        if state == end:
            return expanded, state.path()
        new = lambda x: x not in visited and x not in [b for a, b in frontier]
        for c in filter(new, state.adjacents()):
            c.update(state)
            heapq.heappush(frontier, (c.f, c))
    return expanded, []


def main():
    nodes, path = search(State(), State([[], [], [1, 2, 3, 4]]))
    print("Expanded %s nodes and to discover the following solution in %s "
          "steps" % (nodes, len(path)))
    for step in path:
        print step


if __name__ == '__main__':
    main()
