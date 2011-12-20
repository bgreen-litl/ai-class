#!/usr/bin/env python2

from random import sample, random


class State:
    @staticmethod
    def init(tasks, resources, alpha=0.1, gamma=0.9):
        State.tasks = tasks
        State.resources = resources
        State.alpha = alpha  # learning rate
        State.gamma = gamma  # discount rate
        State.weights = dict(((t, r), 0.0) for r in resources for t in tasks)

    def __init__(self, mapping={}, pair=None, parent=None):
        self.mapping = mapping
        self.pair = pair
        self.parent = parent
        self.cost = 0

    def _select(self, task, scorer):
        resources = State.resources - set(self.mapping.values())
        best = (999, 0)
        for w, r in ((State.weights[task, r], r) for r in resources):
            aff = scorer(task, r, self.mapping)
            if w + aff < best[0]:
                best = (w + aff, r)
        return best[1]

    def child(self, scorer):
        tasks = State.tasks - set(self.mapping.keys())
        if tasks:
            task = sample(tasks, 1)[0]  # random selection for the task
            resource = self._select(task, scorer)  # greedy resource selection
            m = dict(self.mapping)
            m[task] = resource
            return State(m, (task, resource), self)

    def update(self, cost):
        node = self.parent
        last = cost
        while node and node.pair:
            weight = State.weights[node.pair]
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


def path(end):
    state = end
    while state:
        yield state
        state = state.parent


def search(start, scorer, end):
    cost = 999999
    while not end(cost):
        node = start
        while node:
            node.cost = node.path_cost(scorer)
            last = node
            node = node.child(scorer)
        cost = sum(scorer(t, r, last.mapping) for t, r in last.mapping.items())
        last.update(cost)  # update weights on path based on full score

    return last


def main():
    # fit 100 tasks to 100 resources - just ints here - could have properties
    tasks = set(i for i in xrange(100))
    resources = set(i for i in xrange(100))
    State.init(tasks, resources)

    # scorers return 0 for satisfaction through 1 for extreme dissatisfaction
    scorer = lambda t, r, m: abs(t - r) / 100.0

    # end condition defined the score total score required to stop
    end = lambda x: x == 0

    state = search(State(), scorer, end)
    print state.mapping, state.cost


if __name__ == '__main__':
    main()
