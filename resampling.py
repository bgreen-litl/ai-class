import random


def resample(values, weights, num):
    """Sample values proportional to their weights"""
    assert len(values) == len(weights)

    max_weight = max(weights)
    samples = []
    index = random.randint(0, len(values))
    beta = 0
    for i in xrange(num):
        beta += random.random() * 2 * max_weight
        while weights[index] < beta:
            beta -= weights[index]
            index = (index + 1) % len(values)
        samples.append(values[index])
    return samples


if __name__ == "__main__":
    values = range(100)
    weights = [random.random() for v in values]
    samples = resample(values, weights, 100)
    for i in xrange(len(samples)):
        print (values[i], weights[i])
