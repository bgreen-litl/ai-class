import sys
import heapq

      
class State:
    PEGS = 3

    def __init__(self, discs):
        self.discs = discs
        self.f = self.g = self.h = 0
        self.parent = None

    def __hash__(self):
        return hash(self.discs)

    def __eq__(self, other):
        return self.discs == other.discs

    def adjacents(self):
        pegs = [len(self.discs)] * State.PEGS
        for d, p in enumerate(self.discs):
            pegs[p] = min(pegs[p], d)
        for d, p in enumerate(self.discs):
            if pegs[p] == d:
                for q in filter(lambda x: x != p, range(State.PEGS)):
                    discs = list(self.discs[:])
                    if d < pegs[q]:
                        discs[d] = q
                        yield State(tuple(discs))
                    
    def update(self, parent):
        self.parent = parent
        self.g = parent.g + 1
        self.h = max(self.discs) + 1 - len([d for d in self.discs if d==2])
        self.f = self.g + self.h

    def path(end):
        state = end
        while state:
            yield str(state.discs)
            state = state.parent


def search(start, end):
    frontier = []
    heapq.heapify(frontier)
    visited = set()
    heapq.heappush(frontier, (start.f, start))
    while frontier:
        h, state = heapq.heappop(frontier)
        visited.add(state)
        if state == end:
            return state.path()
        new = lambda x: x not in visited and x not in (b for a, b in frontier)
        for c in filter(new, state.adjacents()):
            c.update(state)
            heapq.heappush(frontier, (c.f, c))


def main():
    path = search(State((0, 0, 0, 0)), State((2, 2, 2, 2)))
    map(sys.stdout.write, (p + '\n' for p in path))


if __name__ == '__main__':
    main()
