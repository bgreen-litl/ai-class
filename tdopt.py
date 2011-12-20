import sys
import heapq
from random import sample, random


class Task:
    def __init__(self, idx):
        self.idx = idx

    def __repr__(self):
        return str(self.idx)

    def affinity(self, resource, mapping):
        return abs(self.idx - resource) / 100.0

    def allows(self, resource, mapping):
        return True


class State:
    @staticmethod
    def init(tasks, resources, alpha=0.1, gamma=0.9):
        State.tasks = tasks
        State.resources = resources
        State.alpha = alpha
        State.gamma = gamma
        State.weights = {}
        for t in tasks:
            for r in resources:
                State.weights[t, r] = t.affinity(r, {})
                #State.weights[t, r] = random()

    def __init__(self, mapping={}, pair=None, parent=None):
        self.mapping = mapping
        self.pair = pair
        self.parent = parent
        self.g = 0
        self.f = self.h = self.heuristic()

    def __hash__(self):
        return reduce(lambda x, y : x * 17 + hash(y), 
                      [7] + self.mapping.items())

    def __eq__(self, other):
        return self.mapping == other.mapping

    def __repr__(self):
        print self.mapping

    def select(self, task):
        resources = State.resources - set(self.mapping.values())
        tot = sum(State.weights[task, r] for r in resources)

        best = (999, 0)
        for w, r in ((State.weights[task, r], r) for r in resources):
            if w < best[0] and random() < 0.99:
                best = (w, r)
        return best[1]

        #while resources:
        #rtot = 0 
        #rw = random()
        #for r in resources:
        #    weight = max(0, 1.0 - State.weights[task, r])
        #    sliver = (rtot + weight + 1) / (tot + len(resources))
        #    rtot += sliver
        #    if rw < rtot:
        #        resources.remove(r)
        #        return r

    def child(self):
        # choose a task from the unmapped set
        # this could probably be cached per search
        tasks = [t for t in State.tasks if t not in self.mapping]
        if tasks:
            #task = sample(tasks, 1)[0]
            task = tasks[0]

            # probalistically choose a mapping for that task based on:
            # task requirements, task preferences, previous rewards
            resource = self.select(task)
            if resource >= 0:
                if task.allows(resource, self.mapping):
                    m = dict(self.mapping)
                    m[task] = resource
                    return State(m, (task, resource), self)

        # we've reached a leaf node - update weights
        tot = sum(t.affinity(r, self.mapping) for t, r in self.mapping.items())
        node = self.parent
        last = tot
        while node and node.pair:
            w0 = State.weights[node.pair]
            
            # update rules (q-learning!)
            State.weights[node.pair] += State.alpha * (State.gamma * (last - w0))
            #cost = self.pair[0].affinity(node.pair[1], self.mapping)
            #State.weights[node.pair] -= State.alpha * (cost + State.gamma * (last - w0))
            #State.weights[node.pair] -= 0.25 * ((1 - cost) - (last - w0))
            #State.weights[node.pair] += 0.1 * (cost - w0)
            #State.weights[node.pair] = 1 - cost

            last = w0
            node = node.parent

    def path_cost(self):
        parent_cost = self.parent.g if self.parent else 0        
        cost = self.pair[0].affinity(self.pair[1], self.mapping)
        return parent_cost + cost

    def heuristic(self):
        return len(State.tasks) - len(self.mapping)

    def end(self):
        return len(self.mapping) == len(State.tasks)


def update(node):
    node.g = node.path_cost()
    node.h = node.heuristic()
    node.f = node.g + node.h

                    
def path(end):
    state = end
    while state:
        yield state
        state = state.parent


def search(start):
    print 'searching'
    frontier = []
    heapq.heapify(frontier)
    visited = set()
    heapq.heappush(frontier, (start.f, start))
    while frontier:
        h, state = heapq.heappop(frontier)
        visited.add(state)

        c = state.child()
        if not c:
            return state

        update(c)
        heapq.heappush(frontier, (c.f, c))


def main():
    tasks = [Task(i) for i in xrange(100)]
    resources = set(range(100))

    State.init(tasks, resources)

    cost = 100
    while cost > 0:
        state = search(State())
        print state.mapping, len(state.mapping), state.g
        cost = state.g


if __name__ == '__main__':
    main()
