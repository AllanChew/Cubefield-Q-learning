import pygame
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

# needed for epsilon-greedy and softmax (move into Q-learning module in the future)
import random
import math

import gamestate
import playerstate
import playerhistory
import drawer
import sensor

game1 = gamestate.GameState(7,12,8)
player1 = playerstate.PlayerState(3,8)
player1hist = playerhistory.PlayerHistory(20)
player1sensor = sensor.GetSensorState(game1,player1)
maindrawer = drawer.Drawer(game1)

state_delay = 50 # in ms
#temp_left_down = 0 # temp for testing
#temp_right_down = 0 # temp for testing
#temp_action_table = [1,2,0,1] # 0, 1 or 2 (left, center, right) # temp for testing
#temp_action = temp_action_table[2*temp_left_down + temp_right_down]

# QTable[state][action]
QTable = [[0 for j in range(3)] for i in range(sensor.total_states)]
learning_rate = 0.2 # parameter that can be tweaked
discount_factor = 0.8 # parameter that can be tweaked

def GetGreedyAction(action_q_values):
    return action_q_values.index(max(action_q_values))

training_iterations = 10000 # game iterations
epsilon = 1 # starting value for epsilon (decreases over time)
epsilon_offset = epsilon/training_iterations
def GetActionEpsilonGreedy(action_q_values):
    global epsilon
    if (epsilon < 0):
        return GetGreedyAction(action_q_values)
    ret_val = random.randint(0,2) if random.random() < epsilon else GetGreedyAction(action_q_values)
    epsilon -= epsilon_offset
    return ret_val

temperature = 15 # starting value for temperature (decreases over time)
min_temperature = 0.001 # minimum tempereature before using greedy
anneal_mult = (min_temperature/temperature)**(1/training_iterations)
def GetActionSoftmax(action_q_values):
    global temperature
    if temperature < min_temperature:
        return GetGreedyAction(action_q_values)
    ret_val = random.choices(range(len(action_q_values)), [math.exp(q/temperature) for q in action_q_values])[0]
    temperature *= anneal_mult
    return ret_val

def RewardFunc1(action_result):
    if action_result[2]:
        return -1 # collided
    return 0

def RewardFunc2(action_result):
    if action_result[2]:
        return -8 # collided
    return 1

def main():
    global player1sensor
    global state_delay

    # initialize pygame
    pygame.init()
    # last row is out of view due to generation (remove '- block_offset' to see why)
    window1 = pygame.display.set_mode((maindrawer.x_canvas_pixels,maindrawer.y_canvas_pixels - maindrawer.block_offset))

    clock = pygame.time.Clock()
    clock.tick()

    running = True
    time_bank = 0 # keep initialized to 0
    while running:
        time_bank += clock.tick()
        while time_bank >= state_delay:
            state_copy = player1sensor # for updating Q-value later (store in an array for multiple players)

            #temp_action = GetActionSoftmax(QTable[state_copy]) # Get action using softmax
            temp_action = GetActionEpsilonGreedy(QTable[state_copy]) # Get action using epsilon-greedy
            #temp_action = temp_action_table[2*temp_left_down + temp_right_down] # Get action using input

            reward = RewardFunc1(player1.ApplyAction(game1, temp_action)) # apply action and update player state
            player1hist.UpdateHistoryQueue(temp_action, reward)

            # can repeat the above in a loop for multiple players
            game1.UpdateGame() # done once per loop

            # make sure to update sensor (and get new state)
            player1sensor = sensor.GetSensorState(game1,player1)

            TD = reward + discount_factor*max(QTable[player1sensor]) - QTable[state_copy][temp_action]
            QTable[state_copy][temp_action] += learning_rate*TD # update Q value

            # can repeat the above in a loop to update the Q-value for each player

            time_bank -= state_delay

        maindrawer.DrawPlayer(window1, game1, player1, player1hist, time_bank/state_delay)
        pygame.display.update()

        for event in GAME_EVENTS.get():
            if event.type == GAME_GLOBALS.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    if state_delay >= 6:
                        state_delay -= 5
                elif event.key == pygame.K_DOWN:
                    state_delay += 5
                elif event.key == pygame.K_PRINT:
                    pygame.image.save(window1,"screenshot.png")
                #elif event.key == pygame.K_LEFT:
                    #temp_left_down = 1
                #elif event.key == pygame.K_RIGHT:
                    #temp_right_down = 1
            #elif event.type == pygame.KEYUP:
                #if event.key == pygame.K_LEFT:
                    #temp_left_down = 0
                #elif event.key == pygame.K_RIGHT:
                    #temp_right_down = 0

    pygame.quit()
main()
