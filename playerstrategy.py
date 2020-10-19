import random
import math


class Strategy:

    def getStrategyAction(self, action_q_values):
        raise NotImplementedError("implemented in sub class")


class PlayerStrategy(Strategy):
    key = 1

    def getStrategyAction(self, action_q_values):
        ret = self.key
        self.key = 1
        return ret


class GreedyStrategy(Strategy):

    def getStrategyAction(self, action_q_values):
        return action_q_values.index(max(action_q_values))


class EpsilonGreedyStrategy(GreedyStrategy):
    epsilon = 1

    def __init__(self, iterations):
        self.epsilon_offset = self.epsilon/iterations

    def getStrategyAction(self, action_q_values):
        if (self.epsilon < 0):
            return super().getStrategyAction(action_q_values)
        ret_val = random.randint(0,2) if random.random() < self.epsilon else super().getStrategyAction(action_q_values)
        self.epsilon -= self.epsilon_offset
        return ret_val


class SoftMaxStrategy(GreedyStrategy):
    min_temperature = 0.001
    temperature = 15

    def __init__(self, iterations):
        self.anneal_mult = (self.min_temperature/self.temperature)**(1/iterations)

    def getStrategyAction(self, action_q_values):
        if self.temperature < self.min_temperature:
            return super().getStrategyAction(action_q_values)
        ret_val = random.choices(range(len(action_q_values)), [math.exp(q/self.temperature) for q in action_q_values])[0]
        self.temperature *= self.anneal_mult
        return ret_val
