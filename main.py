import pygame
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

import gamestate
import playerstate
import playerhistory
import drawer

# ===== Sensors =====

# looks into game state and player state to determine sensor state

sensor_state = 0

# ===== Game Loop =====

game1 = gamestate.GameState(7,9,8)
player1 = playerstate.PlayerState(3,5)
player1hist = playerhistory.PlayerHistory(20)
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

running = True
while running:
    time_bank += clock.tick()
    while time_bank >= state_delay:
        state_copy = sensor_state # for updating Q-value later (store in an array for multiple players)
        
        # get action using epsilon-greedy, softmax, etc.
        temp_action = temp_action_table[2*temp_left_down + temp_right_down]
        
        reward = player1.ApplyAction(game1, temp_action) # apply action and update player state
        player1hist.UpdateHistoryQueue(temp_action, reward)
        
        # can repeat the above in a loop for multiple players
        
        game1.UpdateGame() # done once per loop
        
        # make sure to update sensor_state
        
        # Q[state_copy,action] += ... use sensor_state and reward to update Q value
        
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
