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

    def __init__(self, mapping={}, pair=None, parent=None, scorer=None):
        if not scorer:
            scorer = parent.scorer
        self.scorer = scorer
        self.mapping = mapping
        self.pair = pair
        self.parent = parent
        self.cost = 0

    def __hash__(self):
        return reduce(lambda x, y : x * 17 + hash(y), 
                      [7] + self.mapping.items())

    def __eq__(self, other):
        return self.mapping == other.mapping

    def __repr__(self):
        return str(self.mapping)

    def _select(self, task):
        resources = State.resources - set(self.mapping.values())
        best = (999, 0)
        for w, r in ((State.weights[task, r], r) for r in resources):
            aff = self.scorer(task, r, self.mapping)
            if w + aff < best[0]:
                best = (w + aff, r)
        return best[1]

    def child(self):
        tasks = State.tasks - set(self.mapping.keys())
        if tasks:
            task = sample(tasks, 1)[0]  # random selection for the task
            resource = self._select(task)  # greedy selection given the task
            m = dict(self.mapping)
            m[task] = resource
            return State(m, (task, resource), self)

        # leaf node - update weights with q-learning update rule
        score = self.scorer
        tot = sum(score(t, r, self.mapping) for t, r in self.mapping.items())
        node = self.parent
        last = tot
        while node and node.pair:
            weight = State.weights[node.pair]
            nudge = (State.alpha * (State.gamma * (last - weight)))
            State.weights[node.pair] += nudge
            last = weight
            node = node.parent

    def path_cost(self):
        cost = 0
        if self.parent:
            cost += self.parent.cost
            cost += self.scorer(self.pair[0], self.pair[1], self.mapping)
        return cost


def path(end):
    state = end
    while state:
        yield state
        state = state.parent


def search(start):
    node = start
    while node:
        node.cost = node.path_cost()
        last = node
        node = node.child()
    return last


def main():
    # fit 100 tasks to 100 resources - just ints here - could have properties
    tasks = set(i for i in xrange(100))
    resources = set(i for i in xrange(100))
    State.init(tasks, resources)

    # scorers return 0 for satisfaction through 1 for extreme dissatisfaction
    scorer0 = lambda t, r, m: abs(t - r) / 100.0
    scorer1 = lambda t, r, m: abs(t - r) / 100.0 if t % 2 == 0 else 0.0
    scorer2 = lambda t, r, m: abs(t - r) / 100.0 if t % 5 == 0 else 0.0

    cost = 100
    # iterate until we find a perfect score - might want better stop condition
    while cost > 0:
        start = State(scorer=scorer0)
        state = search(start)
        cost = state.path_cost()
        print state.mapping, cost


if __name__ == '__main__':
    main()
