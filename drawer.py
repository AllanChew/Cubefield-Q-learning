import pygame
import sys

pygame.font.init() # initialize the font module

class Drawer:
    block_size = 38 # how many pixels wide for the square blocks
    line_thickness = 2 # how many pixels wide are the gridlines
    free_block_color = (255,255,255) # white
    solid_block_color = (125,125,125) # grey
    line_color = (0,0,0) # black
    font = pygame.font.SysFont("Comic Sans MS", 16) # text font for our labels

    def __init__(self, gameref):
        self.block_offset = self.line_thickness + self.block_size
        self.step_offset = self.block_offset/gameref.steps_per_block
        self.x_canvas_pixels = self.block_offset*gameref.x_col_blocks
        self.y_canvas_pixels = self.block_offset*gameref.y_row_blocks
        self.gameref = gameref

    def CreateSurface(self):
        # last row is out of view due to generation (remove '- block_offset' to see why)
        return pygame.Surface((self.x_canvas_pixels,self.y_canvas_pixels - self.block_offset))

    # fills the entire canvas with line_color (squares then get drawn on top)
    def DrawLines(self, surface):
        surface.fill(self.line_color)

    # draw a single row (used as a helper for DrawRows
    def DrawRow(self, surface, gameref, playerref, y_index, current_y):
        j = 0
        current_x = self.x_canvas_pixels/2 + self.line_thickness/2 - self.step_offset/2 - self.step_offset*playerref.player_x_step
        while (j < gameref.x_col_blocks):
            cur_block = gameref.block_array[(playerref.player_x_col + j) % gameref.x_col_blocks][y_index]
            square_color = self.free_block_color
            if cur_block == 1:
                square_color = self.solid_block_color

            # draw square
            pygame.draw.rect(surface, square_color, (int(current_x), int(current_y), self.block_size, self.block_size))

            if (current_x + self.block_size) > self.x_canvas_pixels: # wrap around to left
                current_x -= self.x_canvas_pixels
                continue

            current_x += self.block_offset
            j += 1
    # draw all rows
    def DrawRows(self, surface, gameref, playerref, y_lerp_offset):
        i = 0
        current_y = self.line_thickness/2 - self.step_offset*gameref.game_y_step + y_lerp_offset
        while (i < gameref.y_row_blocks):
            y_index = (gameref.generation_y_index + i) % gameref.y_row_blocks

            # draw row
            self.DrawRow(surface, gameref, playerref, y_index, current_y)

            current_y += self.block_offset
            i += 1
    # draw blue circle w/ radius 3 pixels at where player is
    def DrawPlayerDot(self, surface, player_pixel_loc):
        pygame.draw.circle(surface, (0,0,255), (int(player_pixel_loc[0]),int(player_pixel_loc[1])), 3)
    # draw history queue
    def DrawHistoryQueue(self, surface, histref, y_lerp_offset, player_pixel_loc):
        cur_x = player_pixel_loc[0]
        cur_y = player_pixel_loc[1] + y_lerp_offset
        for e in histref.q:
            color = (0,255,0) # green
            if (e[1] < 0): # if negative reward
                color = (255,0,0) # red
            pygame.draw.circle(surface, color, (int(cur_x),int(cur_y)), 3) # draw the dot
            cur_x += (1 - e[0])*self.step_offset
            cur_y += self.step_offset

    # draw the player at the current game state
    # 0 <= alpha < 1 is how close to next game state
    def DrawPlayer(self, surface, playerref, alpha):
        gameref = self.gameref
        histref = playerref.history
        y_lerp_offset = alpha*self.step_offset
        player_pixel_loc = (self.x_canvas_pixels/2,
                            self.step_offset/2 + playerref.player_y_row_start*self.block_offset)
        self.DrawLines(surface)
        self.DrawRows(surface, gameref, playerref, y_lerp_offset)
        self.DrawHistoryQueue(surface, histref, y_lerp_offset, player_pixel_loc)
        self.DrawPlayerDot(surface, player_pixel_loc)

    # draw text onto input surface
    def DrawText(self, surface, text):
        textSurface = self.font.render(text, 1, (200, 0, 0), (255,255,255)) # red text color, white background
        surface.blit(textSurface, (0, 0))

    # draw total number of collisions onto the surface
    def DrawTotalCollisions(self, name, surface, total_collisions):
        collisionStatement = "  " + name + " - Total Collisions: " + str(total_collisions) + "  "
        self.DrawText(surface, collisionStatement)

