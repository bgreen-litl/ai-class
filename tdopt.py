class State:
    @staticmethod
    def init(tasks, resources, alpha=0.1, gamma=0.9):
        State.tasks = tasks
        State.resources = resources
        State.alpha = alpha  # learning rate
        State.gamma = gamma  # discount rate
        State.weights = {}

    @staticmethod
    def weight(pair):
        if pair in State.weights:
            return State.weights[pair]
        else:
            return 0.0

    def __init__(self, mapping={}, pair=None, parent=None):
        self.mapping = mapping
        self.pair = pair
        self.parent = parent
        self.cost = 0

    def update(self, cost):
        node = self.parent
        last = cost
        while node and node.pair:
            weight = State.weight(node.pair)
            delta = State.alpha * (State.gamma * (last - weight))
            if node.pair not in State.weights:
                State.weights[node.pair] = delta
            else:
                State.weights[node.pair] += delta
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
    mapping = node.mapping
    tasks = State.tasks.difference(mapping.keys())
    resources = State.resources.difference(mapping.values())
    if tasks and resources:
        adjust = lambda t, r, m: (State.weight((t, r)) + 
                                  scorer(t, r, mapping))
        task = max((adjust(t, max(resources), mapping), t) for t in tasks)[1]
        resource = min((State.weight((task, r)), r) for r in resources)[1]
        m = dict(mapping)  # copy parent's mapping
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
    last.update(cost)
    return cost, last
    

def search(start, scorer, end):
    n = 0
    state = None
    score = float('inf')
    last = score, state, 0
    try:
        while not end(score, n):
            score, state = explore_path(start, scorer)
            print state.mapping, score
            yield score, state, n
            last = score, state, n
            n += 1
    except KeyboardInterrupt:
        yield last


# --- optimization specific definitions ---


# here's a tricky scorer: even numbered tasks should generally be close to
# their resources, but multiple-of-ten tasks must not match exactly!
def scorer(task, resource, mapping):
    cost = 0
    if resource % 10 == 0 and resource == task:
        cost += 1000000
    elif resource % 2 == 0:
        cost += abs(resource - task) / float(len(State.tasks))
    return cost
        

def main():
    # fit 100 tasks to 100 resources - just ints here - could have properties
    tasks = set(i for i in xrange(100))
    resources = set(i for i in xrange(100))
    State.init(tasks, resources)
    # end condition can trigger based on total score or iterations
    end = lambda score, iterations: score < 3.6
    cost, state, n = min(search(State(), scorer, end))
    print("best: %s cost: %s iteration: %s" % (state.mapping, cost, n))


if __name__ == '__main__':
    main()
