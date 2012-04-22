# coding:utf-8

"""
q-learning reference implementation

Q(s,a) <- Q(s,a) + α(R(s) + γ * argmax_a'(Q(s',a')) - Q(s,a))

"""

import unittest
import random
import sys


class Q:
    def __init__(self, actions_func, reward_func, trans_func,
                 learning_rate=0.1, discount_rate=1):
        self.Q = {}
        self.actions_func = actions_func
        self.reward_func = reward_func
        self.trans_func = trans_func
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate

    def q(self, state, action):
        """expected value of action in state"""
        if not (state, action) in self.Q:
            self.Q[state, action] = 0

        return self.Q[state, action]

    def best_action(self, state):
        """best expected (value, action) aka argmax_a(Q(s,a))"""
        best = (-sys.maxint, None)
        actions = self.actions_func(state)
        for action in actions:
            val = self.q(state, action)
            if val > best[0]:
                best = (val, action)
        return best

    def update(self, state, action):
        """update the expected value of action in state"""
        cur = self.q(state, action)
        state_ = self.trans_func(state, action)
        val_, action_ = self.best_action(state_)
        delta = (self.learning_rate *
                 (self.reward_func(state_) + self.discount_rate * val_ - cur))
        self.Q[state, action] += delta


class QTest(unittest.TestCase):
    def setUp(self):
        self.actions = [-1, 1]
        self.states = [-10, -10, -10, -10, -10, -10, -10, -10, 100]  # 1D world
        self.reward_func = lambda x: self.states[x]
        self.trans_func = lambda s, a: max(0, min(len(self.states) - 1, s + a))
        self.actions_func = lambda s: self.actions
        self.q = Q(self.actions_func, self.reward_func, self.trans_func)

    def test_q(self):
        self.assertEquals(0, self.q.q('foo', 'bar'))

    def test_best(self):
        best = self.q.best_action(4)
        self.assertEquals(0, best[0])

    def test_update(self):
        for i in range(1000):
            state = 0
            while state < 8:
                action = random.sample([-1, 1], 1)[0]
                self.q.update(state, action)
                state = self.trans_func(state, action)
        print sorted(self.q.Q.iteritems())


if __name__ == '__main__':
    unittest.main()
