import random

# example usage: GameState(7,9,8)
class GameState:
    game_y_step = 0
    generation_y_index = 0
    def __init__(self,x_col_blocks,y_row_blocks,steps_per_block):
        self.x_col_blocks = x_col_blocks
        self.y_row_blocks = y_row_blocks
        self.steps_per_block = steps_per_block
        self.block_array = [[0 for j in range(y_row_blocks)] for i in range(x_col_blocks)]
    def UpdateGame(self):
        # update y values
        self.game_y_step -= 1
        if self.game_y_step < 0: # next block reached
            self.game_y_step = self.steps_per_block - 1
            self.generation_y_index -= 1
            if self.generation_y_index < 0:
                self.generation_y_index = self.y_row_blocks - 1
            # generate new row
            for i in range(self.x_col_blocks):
                self.block_array[i][self.generation_y_index] = random.randint(0,1) # currently no checks for random generation

