import pygame
import drawer

class UI:
    def __init__(self,gameref):
        self.gamedrawer = drawer.Drawer(gameref)
        self.temp_surface = self.gamedrawer.CreateSurface() # gets blitted onto mainwindow
    def DrawGameSurfaces(self,window,game,lerp_alpha):
        x_offset = 10
        y_offset = 10
        # draw all the players
        for player in game.players:
            # draw the player onto temp_surface
            self.gamedrawer.DrawPlayer(self.temp_surface,player,lerp_alpha)
            # TODO: text for total collisions for the player
            #         consider using alpha transparency
            #       text for player.name
            #       text for annealing values?
            # then blit the surface onto the window
            window.blit(self.temp_surface,(x_offset,y_offset))
            x_offset += 300
            if x_offset >= 1000:
                x_offset = 10
                y_offset += 340
    def DrawGame(self,window,game,lerp_alpha):
        self.DrawGameSurfaces(window,game,lerp_alpha)
        # TODO: text for current iteration number (e.g. 5000)
        #         bottom left maybe?
        #       instructions for what keys do
        #         e.g. Press P to pause, arrow up to speed up, etc.
