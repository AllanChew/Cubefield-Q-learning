# example usage: PlayerState(3,5)
class PlayerState:
    player_x_step = 0
    def __init__(self,player_x_col,player_y_row_start):
        self.player_x_col = player_x_col
        self.player_y_row_start = player_y_row_start
        self.player_y_row = player_y_row_start
    # updates player state and returns reward/punishment from applying action
    # looks into game state to determine reward/punishment
    def ApplyAction(self,gameref,action):
        self.player_x_step += action - 1
        moved_left_right = False
        old_player_x_col = self.player_x_col # used for checks below
        if self.player_x_step < 0:
            moved_left_right = True
            self.player_x_col = (self.player_x_col + gameref.x_col_blocks - 1) % gameref.x_col_blocks # move to left block
            self.player_x_step = gameref.steps_per_block - 1 # at very right of left block
        elif self.player_x_step == gameref.steps_per_block:
            moved_left_right = True
            self.player_x_col = (self.player_x_col + 1) % gameref.x_col_blocks # move to right block
            self.player_x_step = 0 # at very left of right block
        
        current_y = (gameref.generation_y_index + self.player_y_row_start) % gameref.y_row_blocks
        if moved_left_right: # will move left/right
            if gameref.block_array[self.player_x_col][current_y] == 1: # check block immediately left/right
                return -1 # hit left/right
        if gameref.game_y_step == 0: # will move to forward block
            current_y = (current_y + gameref.y_row_blocks - 1) % gameref.y_row_blocks
            if gameref.block_array[old_player_x_col][current_y] == 1: # check block in front
                return -1 # hit front
        if moved_left_right and gameref.game_y_step == 0: # will move diagonal
            if gameref.block_array[self.player_x_col][current_y] == 1: # check new location
                return -1 # hit diagonal
        return 0

