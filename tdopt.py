import sys
from random import sample


class State:
    @staticmethod
    def init(tasks, resources, scorer, alpha=0.1, gamma=0.9):
        State.tasks = tasks
        State.resources = resources
        State.alpha = alpha  # learning rate
        State.gamma = gamma  # discount rate
        State.weights = dict(((t, r), scorer(t, r, {}))
                             for t in tasks for r in resources)

    def __init__(self, mapping={}, pair=None, parent=None):
        self.mapping = mapping
        self.pair = pair
        self.parent = parent
        self.cost = 0

    def update(self, cost):
        node = self.parent
        last = cost
        while node and node.pair:
            weight = State.weights[node.pair]
            nudge = (State.alpha * (State.gamma * (last - weight)))
            State.weights[node.pair] += nudge
            last = weight
            node = node.parent


# --- tdopt search functions ---


def path_cost(node, scorer):
    cost = 0
    if node.parent:
        cost += (node.parent.cost +
                 scorer(node.pair[0], node.pair[1], node.mapping))
    return cost


def select_child(node, scorer):
    tasks = State.tasks.difference(node.mapping.keys())
    resources = State.resources.difference(node.mapping.values())
    if tasks and resources:
        r = sample(resources, 1)[0]
        task = max((State.weights[t, r], t) for t in tasks)[1]
        resource = min((State.weights[task, r], r) for r in resources)[1]
        m = dict(node.mapping)
        m[task] = resource
        return State(m, (task, resource), node)


def explore_path(start, scorer):
    node = start
    while node:
        node.cost = path_cost(node, scorer)
        last = node
        node = select_child(node, scorer)

    m = last.mapping
    cost = sum(scorer(t, r, m) for t, r in m.iteritems())
    last.update(cost)  # update weights on path based on full score
    return cost, last
    

def search(start, scorer, end):
    i = 0
    score = sys.maxint
    state = None
    last = score, state, 0
    try:
        while not end(score, i):
            score, state = explore_path(start, scorer)
            print state.mapping, score
            yield score, state, i
            last = score, state, i
            i += 1
    except KeyboardInterrupt:
        yield last


# --- optimization specific definitions ---


def scorer(task, resource, mapping):
    cost = 0
    if resource % 10 == 0 and resource == task:
        cost += 1000000
    else:
        cost += abs(resource - task) / float(len(State.tasks))
    return cost
        

def main():
    # fit 100 tasks to 100 resources - just ints here - could have properties
    tasks = set(i for i in xrange(100))
    resources = set(i for i in xrange(100))
    State.init(tasks, resources, scorer, alpha=0.001)

    # end condition can trigger based on total score or iterations
    end = lambda score, iterations: score < 0.8
    cost, state, i = min(search(State(), scorer, end))
    print("best: %s cost: %s iteration: %s" % (state.mapping, cost, i))


if __name__ == '__main__':
    main()
