import random
import math


class Strategy:

    def __init__(self, iterations):
        self.iterations = iterations

    def getStrategyAction(self, action_q_values):
        raise NotImplementedError("implemented in sub class")

    def getStrategyText(self):
        return "" # player and greedy don't print anything


class PlayerStrategy(Strategy):
    left_down = 0
    right_down = 0

    def getStrategyAction(self, action_q_values):
        return self.right_down - self.left_down + 1


class GreedyStrategy(Strategy):

    def getStrategyAction(self, action_q_values):
        return action_q_values.index(max(action_q_values))


class EpsilonGreedyStrategy(GreedyStrategy):
    epsilon = 1
    iteration_val = 0 # so that fixed epsilon knows when training is over (switch to greedy)

    def __init__(self, iterations):
        super().__init__(iterations)  # super init sets self.iterations
        self.epsilon_offset = self.epsilon/iterations

    def getDoneTraining(self):
        return self.epsilon < 0 or self.iteration_val >= self.iterations

    def getStrategyAction(self, action_q_values):
        if self.getDoneTraining():
            return super().getStrategyAction(action_q_values)
        ret_val = random.randint(0,2) if random.random() < self.epsilon else super().getStrategyAction(action_q_values)
        self.epsilon -= self.epsilon_offset
        self.iteration_val += 1
        return ret_val

    def getStrategyText(self):
        if self.getDoneTraining():
            return " Using greedy "
        return " epsilon = {} ".format(round(self.epsilon,4))


class SoftMaxStrategy(GreedyStrategy):
    min_temperature = 0.01
    temperature = 15

    def __init__(self, iterations):
        super().__init__(iterations)  # super init sets self.iterations
        self.anneal_mult = (self.min_temperature/self.temperature)**(1/iterations)

    def getDoneTraining(self):
        return self.temperature < self.min_temperature

    def getStrategyAction(self, action_q_values):
        if self.getDoneTraining():
            return super().getStrategyAction(action_q_values)
        ret_val = random.choices(range(len(action_q_values)), [math.exp(q/self.temperature) for q in action_q_values])[0]
        self.temperature *= self.anneal_mult
        return ret_val

    def getStrategyText(self):
        if self.getDoneTraining():
            return " Using greedy "
        return " Temp = {} ".format(round(self.temperature,4))
