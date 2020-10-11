import pygame

class Drawer:
    block_size = 50 # how many pixels wide for the square blocks
    line_thickness = 2 # how many pixels wide are the gridlines
    free_block_color = (255,255,255) # white
    solid_block_color = (125,125,125) # grey
    line_color = (0,0,0) # black
    def __init__(self, gameref):
        self.block_offset = self.line_thickness + self.block_size
        self.step_offset = self.block_offset/gameref.steps_per_block
        self.x_canvas_pixels = self.block_offset*gameref.x_col_blocks
        self.y_canvas_pixels = self.block_offset*gameref.y_row_blocks
    # fills the entire canvas with line_color (squares then get drawn on top)
    def DrawLines(self, window):
        pygame.draw.rect(window, self.line_color, (0, 0, self.x_canvas_pixels, self.y_canvas_pixels))
    # draw a single row (used as a helper for DrawRows
    def DrawRow(self, window, gameref, playerref, y_index, current_y):
        j = 0
        current_x = self.x_canvas_pixels/2 + self.line_thickness/2 - self.step_offset/2 - self.step_offset*playerref.player_x_step
        while (j < gameref.x_col_blocks):
            cur_block = gameref.block_array[(playerref.player_x_col + j) % gameref.x_col_blocks][y_index]
            square_color = self.free_block_color
            if cur_block == 1:
                square_color = self.solid_block_color
            
            # draw square
            pygame.draw.rect(window, square_color, (int(current_x), int(current_y), self.block_size, self.block_size))
            
            if (current_x + self.block_size) > self.x_canvas_pixels: # wrap around to left
                current_x -= self.x_canvas_pixels
                continue
            
            current_x += self.block_offset
            j += 1
    # draw all rows
    def DrawRows(self, window, gameref, playerref, y_lerp_offset):
        i = 0
        current_y = self.line_thickness/2 - self.step_offset*gameref.game_y_step + y_lerp_offset
        while (i < gameref.y_row_blocks):
            y_index = (gameref.generation_y_index + i) % gameref.y_row_blocks
            
            # draw row
            self.DrawRow(window, gameref, playerref, y_index, current_y)
            
            current_y += self.block_offset
            i += 1
    # draw blue circle w/ radius 3 pixels at where player is
    def DrawPlayerDot(self, window, player_pixel_loc):
        pygame.draw.circle(window, (0,0,255), (int(player_pixel_loc[0]),int(player_pixel_loc[1])), 3)
    # draw history queue
    def DrawHistoryQueue(self, window, histref, y_lerp_offset, player_pixel_loc):
        cur_x = player_pixel_loc[0]
        cur_y = player_pixel_loc[1] + y_lerp_offset
        for e in histref.q:
            color = (0,255,0) # green
            if (e[1] < 0): # if negative reward
                color = (255,0,0) # red
            pygame.draw.circle(window, color, (int(cur_x),int(cur_y)), 3) # draw the dot
            cur_x += (1 - e[0])*self.step_offset
            cur_y += self.step_offset
    # draw the player at the current game state
    # 0 <= alpha < 1 is how close to next game state
    def DrawPlayer(self, window, gameref, playerref, histref, alpha):
        y_lerp_offset = alpha*self.step_offset
        player_pixel_loc = (self.x_canvas_pixels/2, self.step_offset/2 + playerref.player_y_row_start*self.block_offset)
        self.DrawLines(window)
        self.DrawRows(window, gameref, playerref, y_lerp_offset)
        self.DrawHistoryQueue(window, histref, y_lerp_offset, player_pixel_loc)
        self.DrawPlayerDot(window, player_pixel_loc)

