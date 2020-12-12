import pygame
import drawer

def clamp(x, min_val=0, max_val=1):
    if x < min_val:
        return min_val
    if x > max_val:
        return max_val
    return x

class UI:
    font = pygame.font.SysFont("Comic Sans MS", 16) # text font for iteration number
    def __init__(self,gameref,training_iterations,total_iterations,window_x_len,window_y_len):
        self.gamedrawer = drawer.Drawer(gameref)
        self.temp_surface = self.gamedrawer.CreateSurface() # gets blitted onto mainwindow
        self.training_iterations = training_iterations
        self.total_iterations = total_iterations
        self.window_x_len = window_x_len
        self.window_y_len = window_y_len
    def DrawGameSurfaces(self,window,game,lerp_alpha):
        x_offset = 10
        y_offset = 10
        # draw all the players
        for player in game.players:
            # draw the player onto temp_surface
            self.gamedrawer.DrawPlayer(self.temp_surface,player,lerp_alpha)
            self.gamedrawer.DrawTotalCollisions(self.temp_surface, player.total_collisions)
            self.gamedrawer.DrawPolicyName(self.temp_surface, player.name)
            self.gamedrawer.DrawStrategyText(self.temp_surface, player.strategy.getStrategyText())
            # then blit the surface onto the window
            window.blit(self.temp_surface,(x_offset,y_offset))
            x_offset += 300
            if x_offset >= 1000:
                x_offset = 10
                y_offset += 340
    def DrawProgressInfo(self,surface,iter_val):
        # can move these into member variables
        total_width = 200
        total_height = 20
        separator_width = 10
        training_bar_color = (0,255,255) # cyan
        training_background_color = (128,128,128) # grey
        testing_bar_color = (255,223,0) # golden yellow
        testing_background_color = (128,128,128) # grey

        training_alpha = clamp(iter_val/self.training_iterations)
        testing_alpha = clamp((iter_val - self.training_iterations)/(self.total_iterations - self.training_iterations))
        training_width = int(total_width*self.training_iterations/self.total_iterations)
        testing_width = total_width - training_width

        # draw training progress bar
        cur_x = int((self.window_x_len - total_width - separator_width)/2) # could cache as member variable
        cur_y = self.window_y_len - total_height - 10 # could cache as member variable
        pygame.draw.rect(surface, training_background_color, (cur_x, cur_y, training_width, total_height)) # draw training background
        pygame.draw.rect(surface, training_bar_color, (cur_x, cur_y, int(training_alpha*training_width), total_height)) # draw training bar

        # draw testing progress bar
        cur_x += training_width + separator_width
        pygame.draw.rect(surface, testing_background_color, (cur_x, cur_y, testing_width, total_height)) # draw testing background
        pygame.draw.rect(surface, testing_bar_color, (cur_x, cur_y, int(testing_alpha*testing_width), total_height)) # draw testing bar

        # draw iteration number
        cur_x += testing_width + 20
        cur_y -= 2
        textSurface = self.font.render(str(iter_val), 1, (255,255,255)) # white
        surface.blit(textSurface, (cur_x,cur_y))
    def DrawSpeedIndicator(self,surface,state_delay):
        speedText = " Speed: = {} ".format(round(1000/state_delay,1))
        textSurface = self.font.render(speedText, 1, (255,255,255)) # white
        surface.blit(textSurface, (0, self.window_y_len - 25))
    def DrawGame(self,window,game,lerp_alpha,iter_val):
        window.fill((0,0,0)) # this is required since IterNum text needs to be cleared
        self.DrawGameSurfaces(window,game,lerp_alpha)
        self.DrawProgressInfo(window,iter_val)
        self.DrawSpeedIndicator(window,game.state_delay)
