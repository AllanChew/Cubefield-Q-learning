# NOTE: This script is just for testing and future reference
#       Use Left/Right arrow keys to move and Esc to quit

import random # for generating blocks
import pygame
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

# ===== Game State =====

x_col_blocks = 7 # how many columns of blocks
y_row_blocks = 9 # how many row of blocks (last row is out of view due to generation; see comment below)

steps_per_block = 8 # how many steps each block is subdivided into (>= 1)
game_y_step = 0 # goes from 0 to steps_per_block - 1, then decreases back to 0 (i.e. decreases and wraps around)

generation_y_index = 0 # goes from 0 to y_row_blocks - 1, then decreases back to 0 (i.e. decreases and wraps around

block_array = [[0 for j in range(y_row_blocks)] for i in range(x_col_blocks)]

# update game state (game_y_step decrements and new row may be generated)
def UpdateGame():
    global game_y_step
    global generation_y_index
    # update y values
    game_y_step -= 1
    if game_y_step < 0: # next block reached
        game_y_step = steps_per_block - 1
        generation_y_index -= 1
        if generation_y_index < 0:
            generation_y_index = y_row_blocks - 1
        # generate new row
        for i in range(x_col_blocks):
            block_array[i][generation_y_index] = random.randint(0,1) # currently no checks for random generation

# ===== Player State =====

player_x_col = 3 # current x index in the block array
player_x_step = 0 # a number between 0 and steps_per_block - 1 (keep initialized to 0)

player_y_row_start = 5
player_y_row = player_y_row_start

# updates player state and returns reward/punishment from applying action
# looks into game state to determine reward/punishment
def ApplyAction(action):
    global player_x_col
    global player_x_step
    x_step_offset = action - 1
    player_x_step += x_step_offset
    moved_left_right = False
    old_player_x_col = player_x_col # used for checks below
    if player_x_step < 0:
        moved_left_right = True
        player_x_col = (player_x_col + x_col_blocks - 1) % x_col_blocks # move to left block
        player_x_step = steps_per_block - 1 # at very right of left block
    elif player_x_step == steps_per_block:
        moved_left_right = True
        player_x_col = (player_x_col + 1) % x_col_blocks # move to right block
        player_x_step = 0 # at very left of right block

    current_y = (generation_y_index + player_y_row_start) % y_row_blocks
    if moved_left_right: # will move left/right
        if block_array[player_x_col][current_y] == 1: # check block immediately left/right
            return -1 # hit left/right
    if game_y_step == 0: # will move to forward block
        current_y = (current_y + y_row_blocks - 1) % y_row_blocks
        if block_array[old_player_x_col][current_y] == 1: # check block in front
            return -1 # hit front
    if moved_left_right and game_y_step == 0: # will move diagonal
        if block_array[player_x_col][current_y] == 1: # check new location
            return -1 # hit diagonal
    return 0

# ===== Player History =====

from collections import deque

# each element is of the form (action,reward)
player_history_queue = deque() # most recent to least recent

# called after applying each action
def UpdateHistoryQueue(q,action,reward):
    while len(q) > 20: # remove old entries
        q.pop() # removes least recent (oldest)
    q.appendleft((action,reward)) # add current value to queue

# ===== Render Game =====

# looks into game state, player state, and player history to determine how to render

block_size = 50 # how many pixels wide for the square blocks
line_thickness = 2 # how many pixels wide are the gridlines
block_offset = line_thickness + block_size # used for calculations later
step_offset = block_offset/steps_per_block # used for calculations later

free_block_color = (255,255,255) # white
solid_block_color = (125,125,125) # grey
line_color = (0,0,0) # black

x_canvas_pixels = block_offset*x_col_blocks # used for calculations later
y_canvas_pixels = block_offset*y_row_blocks # used for calculations later

# initialize pygame
pygame.init()
# last row is out of view due to generation (remove '- block_offset' to see why)
window = pygame.display.set_mode((x_canvas_pixels,y_canvas_pixels - block_offset))

# fills the entire canvas with line_color (squares then get drawn on top)
def DrawLines():
    pygame.draw.rect(window, line_color, (0, 0, x_canvas_pixels, y_canvas_pixels))

# draw a single row (used as a helper for DrawRows
def DrawRow(y_index, current_y):
    j = 0
    current_x = x_canvas_pixels/2 + line_thickness/2 - step_offset/2 - step_offset*player_x_step
    while (j < x_col_blocks):
        cur_block = block_array[(player_x_col + j) % x_col_blocks][y_index]
        square_color = free_block_color
        if cur_block == 1:
            square_color = solid_block_color

        # draw square
        pygame.draw.rect(window, square_color, (int(current_x), int(current_y), block_size, block_size))

        if (current_x + block_size) > x_canvas_pixels: # wrap around to left
            current_x -= x_canvas_pixels
            continue

        current_x += block_offset
        j += 1

# draw all rows
def DrawRows(y_lerp_offset):
    i = 0
    current_y = line_thickness/2 - step_offset*game_y_step + y_lerp_offset
    while (i < y_row_blocks):
        y_index = (generation_y_index + i) % y_row_blocks

        # draw row
        DrawRow(y_index, current_y)

        current_y += block_offset
        i += 1

# draw blue circle w/ radius 3 pixels at where player is
def DrawPlayer(player_pixel_loc):
    pygame.draw.circle(window, (0,0,255), (int(player_pixel_loc[0]),int(player_pixel_loc[1])), 3)

# draw history queue
def DrawHistoryQueue(q, y_lerp_offset, player_pixel_loc):
    cur_x = player_pixel_loc[0]
    cur_y = player_pixel_loc[1] + y_lerp_offset
    for e in q:
        color = (0,255,0) # green
        if (e[1] < 0): # if negative reward
            color = (255,0,0) # red
        pygame.draw.circle(window, color, (int(cur_x),int(cur_y)), 3) # draw the dot
        cur_x += (1 - e[0])*step_offset
        cur_y += step_offset

# draw the current game state
# 0 <= alpha < 1 is how close to next game state
def DrawGame(alpha):
    y_lerp_offset = alpha*step_offset
    player_pixel_loc = (x_canvas_pixels/2, step_offset/2 + player_y_row_start*block_offset)
    DrawLines()
    DrawRows(y_lerp_offset)
    DrawHistoryQueue(player_history_queue, y_lerp_offset, player_pixel_loc)
    DrawPlayer(player_pixel_loc)

# ===== Sensors =====

# looks into game state and player state to determine sensor state

sensor_state = 0

# ===== Game Loop =====

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
        
        reward = ApplyAction(temp_action) # apply action and update player state
        UpdateHistoryQueue(player_history_queue, temp_action, reward)
        
        # can repeat the above in a loop for multiple players
        
        UpdateGame() # done once per loop
        
        # make sure to update sensor_state
        
        # Q[state_copy,action] += ... use sensor_state and reward to update Q value
        
        # can repeat the above in a loop to update the Q-value for each player

        time_bank -= state_delay

    DrawGame(time_bank/state_delay)
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
