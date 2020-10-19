# 'Global' imports
import pygame
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

# 'Local' imports
import drawer
import player
import generator
import playerstrategy
import sensor

DEFAULT_ITERATIONS = 100000
DEFAULT_STATE_DELAY = 50
DEFAULT_COLS = 7
DEFAULT_ROWS = 12
DEFAULT_STEPS = 8
DEFAULT_PLAYER_START_CORD = (3, 8)  # screen moves around player
DEFAULT_LEARNING_RATE = 0.2 # parameter that can be tweaked
DEFAULT_DISCOUNT_FACTOR = 0.8 # parameter that can be tweaked

# # Make these in here sort of.
# game1 = gamestate.GameState(7,12,8)
# player1 = playerstate.PlayerState(3,6)
# player1hist = playerhistory.PlayerHistory(20)
# player1sensor = sensor.GetSensorState(game1,player1)


class Cubefield(object):

    state_delay = DEFAULT_STATE_DELAY
    game_y_step =  0 # step from 0 to steps_per_block-1
    generation_y_index = 0 # TODO: Rename maybe - not very descriptive

    # Set after main() is called to assign the pygame window to this
    window = None

    def __init__(self, player,
                 num_cols=DEFAULT_COLS,
                 num_rows=DEFAULT_ROWS,
                 num_steps=DEFAULT_STEPS):
        self.x_col_blocks = num_cols
        self.y_row_blocks = num_rows
        self.steps_per_block = num_steps
        self.block_array = [[0 for j in range(self.y_row_blocks)] for i in range(self.x_col_blocks)]

        # Player - currently only support a single player as drawing is centered on a player
        # and does not extend well.
        self.player = player

        # create drawer
        self.drawer = drawer.Drawer(self)

        # Row Generator
        self.generator = generator.FloodFillGenerator(self)

    def _advance_y_step(self):
        self.game_y_step = (self.game_y_step - 1) % (self.steps_per_block)

    def _advance_y_index(self):
        self.generation_y_index = (self.generation_y_index -1) % self.y_row_blocks

    def advanceStep(self):
        player.performStepDecision()
        # if y step is 0, we generate
        if self.game_y_step == 0:
            self._advance_y_index()
            self.generator.generateNewRow()
        self._advance_y_step()


# kind of a cheat, but helps debugging
# create game at global level, so it isnt reset by recalling main
# could also abstract this into Cubefield.play() or some such method
# strategy = playerstrategy.PlayerStrategy()
# strategy = playerstrategy.GreedyStrategy()
# strategy = playerstrategy.EpsilonGreedyStrategy(DEFAULT_ITERATIONS)
sensor = sensor.TripleSensor()
strategy = playerstrategy.SoftMaxStrategy(DEFAULT_ITERATIONS)
player = player.Player(DEFAULT_PLAYER_START_CORD,
                       DEFAULT_LEARNING_RATE,
                       DEFAULT_DISCOUNT_FACTOR,
                       strategy,
                       sensor)
game = Cubefield(player)
# bad - just lazy :)
player.gameref = game
sensor.gameref = game
def main():
    # initialize pygame
    pygame.init()
    # last row is out of view due to generation (remove '- block_offset' to see why)
    maindrawer = game.drawer
    mainwindow = pygame.display.set_mode(
        (maindrawer.x_canvas_pixels,maindrawer.y_canvas_pixels - maindrawer.block_offset)
    )
    game.window = mainwindow
    clock = pygame.time.Clock()
    clock.tick()

    running = True
    time_bank = 0 # keep initialized to 0
    while running:
        time_bank += clock.tick()
        while time_bank >= game.state_delay:
            game.advanceStep()
            time_bank -= game.state_delay

        # re-draw, then update the display
        maindrawer.update(time_bank/game.state_delay)
        pygame.display.update()

        for event in GAME_EVENTS.get():
            if event.type == GAME_GLOBALS.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    if game.state_delay >= 20:
                        game.state_delay -= 10
                elif event.key == pygame.K_DOWN:
                    game.state_delay += 10
            # TODO; WHY DOES THIS WORK WHEN KEYDOWN DOESNT EXIST FOR ALL STRATEGIES
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    strategy.key = 0
                elif event.key == pygame.K_RIGHT:
                    strategy.key = 2
    pygame.quit()

main()