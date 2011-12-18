import sys
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
                    yield State(adj)

    def update(self, parent):
        self.parent = parent
        self.g = parent.g + 1
        self.h = 4 - len(self.towers[2])
        self.f = self.g + self.h

    def path(end):
        state = end
        while state:
            yield state.towers
            state = state.parent


frontier = []
heapq.heapify(frontier)
visited = set()


def search(start, end):
    heapq.heappush(frontier, (start.f, start))
    while frontier:
        h, state = heapq.heappop(frontier)
        visited.add(state)
        if state == end:
            return len(visited), state.path()
        new = lambda x: x not in visited and x not in [b for a, b in frontier]
        for c in filter(new, state.adjacents()):
            c.update(state)
            heapq.heappush(frontier, (c.f, c))
    return len(visited), []


def main():
    nodes, path = search(State(), State([[], [], [1, 2, 3, 4]]))
    map(lambda x: sys.stdout.write(repr(x) + '\n'), path)


if __name__ == '__main__':
    main()
