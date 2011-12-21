#!/usr/bin/env python2

import sys


class State:
    @staticmethod
    def init(tasks, resources, alpha=0.1, gamma=0.9):
        State.tasks = tasks
        State.resources = resources
        State.weights = {}
        State.alpha = alpha  # learning rate
        State.gamma = gamma  # discount rate

    @staticmethod
    def weight(pair):
        if not pair in State.weights:
            State.weights[pair] = 0.0
        return State.weights[pair]

    def __init__(self, mapping={}, pair=None, parent=None):
        self.mapping = mapping
        self.pair = pair
        self.parent = parent
        self.cost = 0

    def child(self, scorer):
        tasks = State.tasks.difference(self.mapping.keys())
        resources = State.resources.difference(self.mapping.values())
        if tasks and resources:
            task = min(tasks)
            resource = min((State.weight((task, r)), r) for r in resources)[1]
            m = dict(self.mapping)
            m[task] = resource
            return State(m, (task, resource), self)

    def update(self, cost):
        node = self.parent
        last = cost
        while node and node.pair:
            weight = State.weight(node.pair)
            nudge = (State.alpha * (State.gamma * (last - weight)))
            State.weights[node.pair] += nudge
            last = weight
            node = node.parent

    def path_cost(self, scorer):
        cost = 0
        if self.parent:
            cost += self.parent.cost
            cost += scorer(self.pair[0], self.pair[1], self.mapping)
        return cost


def walk(start, scorer):
    node = start
    while node:
        node.cost = node.path_cost(scorer)
        last = node
        node = node.child(scorer)

    m = last.mapping
    cost = sum(scorer(t, r, m) for t, r in m.iteritems())
    last.update(cost)  # update weights on path based on full score
    return cost, last
    

def search(start, scorer, end):
    i = 0
    score, path = sys.maxint, None
    while not end(score, i):
        score, path = walk(start, scorer)
        print path.mapping, score
        yield score, path
        i += 1


def main():
    # fit 100 tasks to 100 resources - just ints here - could have properties
    tasks = set(i for i in xrange(100))
    resources = set(i for i in xrange(100))
    State.init(tasks, resources)

    # scorers return 0 for satisfaction through 1 for extreme dissatisfaction
    scorer = lambda t, r, m: abs(t - r) / 100.0 if t % 2 == 0 else 0.0

    # end condition can trigger based on total score or iterations
    end = lambda x, y: x == 0 or y >= 500

    cost, path = min(search(State(), scorer, end))
    print path.mapping, cost


if __name__ == '__main__':
    main()
