# coding:utf-8

"""
temporal difference learning

This is an adaptation of Q-learning:

    Q(s,a) <- Q(s,a) + α(R(s) + γ * argmax_a'(Q(s',a')) - Q(s,a))

to neural network based value estimation rather than table lookup.
"""

import unittest
import sys

import neurolab as nl


class TD:
    def __init__(self, actions_func, reward_func, trans_func,
                 learning_rate=0.01, discount_rate=0.1):
        outputs = 1
        hiddens = 3

        self.nn = nl.net.newff([[0, 8], [-1.0, 1.0]],
                              [hiddens, outputs])
        nl.init.init_rand(self.nn.layers[0])
        nl.init.init_rand(self.nn.layers[1])

        self.actions_func = actions_func
        self.reward_func = reward_func
        self.trans_func = trans_func
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate

    def q(self, state, action):
        """expected value of action in state"""
        outputs = self.nn.sim([[state, action]])
        return outputs[0][0]

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
        q = self.q(float(state), float(action))
        state_ = self.trans_func(state, action)
        q_, _ = self.best_action(state_)
        reward = self.reward_func(state)
        delta = reward + self.discount_rate * q_ - q

        grad = nl.tool.ff_grad(self.nn,
                               [[state, action]],
                               [q + delta])[0]

        for ln, layer in enumerate(self.nn.layers):
            layer.np['w'] -= self.learning_rate * grad[ln]['w']
            layer.np['b'] -= self.learning_rate * grad[ln]['b']


class TdTest(unittest.TestCase):
    def setUp(self):
        self.actions = [-1, 1]
        self.states = [-1., 0, 0, 0, 0, 0, 0, 0, 1.]  # 1D world
        self.reward_func = lambda x: self.states[x]
        self.trans_func = lambda s, a: s + a
        self.actions_func = lambda s: self.actions
        self.q = TD(self.actions_func, self.reward_func, self.trans_func)

    def test_q(self):
        self.q.q(0, 1)

    def test_best(self):
        self.q.best_action(4)

    def test_update(self):
        for i in range(1000):
            state = 0
            while state < 9:
                #action = random.sample([-1, 1], 1)[0]
                action = 1
                self.q.update(state, action)
                state = self.trans_func(state, action)
            state = 8
            while state >= 0:
                action = -1
                self.q.update(state, action)
                state = self.trans_func(state, action)

        for s in range(len(self.states)):
            left = self.q.q(s, -1)
            right = self.q.q(s, +1)
            self.assertTrue(right > left)


if __name__ == '__main__':
    unittest.main()
