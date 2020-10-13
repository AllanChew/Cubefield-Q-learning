import pygame
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import random

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

# initialize pygame
pygame.init()
# last row is out of view due to generation (remove '- block_offset' to see why)
window1 = pygame.display.set_mode((maindrawer.x_canvas_pixels,maindrawer.y_canvas_pixels - maindrawer.block_offset))

clock = pygame.time.Clock()
clock.tick()

state_delay = 50 # in ms
time_bank = 0 # keep initialized to 0
temp_left_down = 0 # temp for testing
temp_right_down = 0 # temp for testing
temp_action_table = [1,2,0,1] # 0, 1 or 2 (left, center, right) # temp for testing
epsilon = 0.3 # pre-set epsilon value (explore 30% of the time randomly)

# QTable[state][action]
QTable = [[0 for j in range(3)] for i in range(sensor.total_states)]
learning_rate = 0.2 # parameter that can be tweaked
discount_factor = 0.8 # parameter that can be tweaked

running = True
while running:
    time_bank += clock.tick()
    while time_bank >= state_delay:
        state_copy = player1sensor # for updating Q-value later (store in an array for multiple players)

        # Get action using epsilon-greedy
        if random.random() < epsilon:
            # explore
            temp_action = random.randint(0, 2)
        else:
            # exploit
            temp_action = QTable[state_copy].index(max(QTable[state_copy]))
            # temp_action = temp_action_table[2*temp_left_down + temp_right_down]

        reward = player1.ApplyAction(game1, temp_action) # apply action and update player state
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
            if event.key == pygame.K_LEFT:
                temp_left_down = 1
            elif event.key == pygame.K_RIGHT:
                temp_right_down = 1
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                temp_left_down = 0
            elif event.key == pygame.K_RIGHT:
                temp_right_down = 0

pygame.quit()
