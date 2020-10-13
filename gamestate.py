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
    def CheckGenPoint(self, start_point, max_island_size): # helper function for GenerateNewRowAllan
        y_ignore = (start_point[1] + self.y_row_blocks - 1) % self.y_row_blocks # flood down from generation_y_index
        seen_list = [(0,0)]
        frontier = [(0,0)]
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        while len(seen_list) <= max_island_size and len(frontier) > 0:
            cur_offset = frontier.pop()
            for direction in ((1,0),(-1,0),(0,1),(0,-1),(-1,1),(1,-1),(-1,-1),(1,1)): # add neighbours
                new_offset_y = cur_offset[1] + direction[1]
                if new_offset_y == -1:
                    continue
                new_offset_x = cur_offset[0] + direction[0]
                new_y = (start_point[1] + new_offset_y + self.y_row_blocks) % self.y_row_blocks
                new_x = (start_point[0] + new_offset_x + self.x_col_blocks) % self.x_col_blocks
                if self.block_array[new_x][new_y] == 0 or (new_offset_x, new_offset_y) in seen_list:
                    continue
                seen_list.append((new_offset_x, new_offset_y))
                if len(seen_list) > max_island_size:
                    break
                if new_offset_x < min_x:
                    min_x = new_offset_x
                elif new_offset_x > max_x:
                    max_x = new_offset_x
                if new_offset_y < min_y:
                    min_y = new_offset_y
                elif new_offset_y > max_y:
                    max_y = new_offset_y
                frontier.append((new_offset_x, new_offset_y))
        return len(seen_list) <= max_island_size, max_x - min_x + 1, max_y - min_y + 1
    def GenerateNewRowAllan(self):
        # first clear the row
        for i in range(self.x_col_blocks):
            self.block_array[i][self.generation_y_index] = 0
        # then generate
        for i in range(self.x_col_blocks):
            island_valid,island_width,island_height = self.CheckGenPoint((i, self.generation_y_index), 3)
            if random.randint(0,2) > 0 and island_valid and (island_width < 3 or island_width <= island_height):
                self.block_array[i][self.generation_y_index] = 1
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
            # self.GenerateNewRowAllan()

