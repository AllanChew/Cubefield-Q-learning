# 'Global' imports
import pygame
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

# 'Local' imports
import ui
import player
import generator
import playerstrategy
import sensor

DEFAULT_ITERATIONS = 5000
DEFAULT_STATE_DELAY = 50
DEFAULT_COLS = 7
DEFAULT_ROWS = 9
DEFAULT_STEPS = 8
DEFAULT_PLAYER_START_CORD = (3, 5)  # screen moves around player
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

    def __init__(self,
                 num_cols=DEFAULT_COLS,
                 num_rows=DEFAULT_ROWS,
                 num_steps=DEFAULT_STEPS):
        self.x_col_blocks = num_cols
        self.y_row_blocks = num_rows
        self.steps_per_block = num_steps
        self.block_array = [[0 for j in range(self.y_row_blocks)] for i in range(self.x_col_blocks)]

        self.players = []

        # Row Generator
        self.generator = generator.FloodFillGenerator(self)

    def AddPlayer(self, player):
        player.gameref = self
        self.players.append(player)

    def _advance_y_step(self):
        self.game_y_step = (self.game_y_step - 1) % (self.steps_per_block)

    def _advance_y_index(self):
        self.generation_y_index = (self.generation_y_index -1) % self.y_row_blocks

    def advanceStep(self):
        for player in self.players:
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
game = Cubefield()
sensor = sensor.TripleSensor()
sensor.gameref = game # bad - just lazy :)
strategy = playerstrategy.PlayerStrategy(DEFAULT_ITERATIONS) # for human to test game
# first player (greedy)
strategy1 = playerstrategy.GreedyStrategy(DEFAULT_ITERATIONS)
# second player (fixed epsilon = 0.25)
strategy2 = playerstrategy.EpsilonGreedyStrategy(DEFAULT_ITERATIONS)
strategy2.epsilon_offset = 0 # epsilon doesn't change
strategy2.epsilon = 0.25
# third player (fixed epsilon = 0.5)
strategy3 = playerstrategy.EpsilonGreedyStrategy(DEFAULT_ITERATIONS)
strategy3.epsilon_offset = 0 # epsilon doesn't change
strategy3.epsilon = 0.5
# fourth player (fixed epsilon = 0.75)
strategy4 = playerstrategy.EpsilonGreedyStrategy(DEFAULT_ITERATIONS)
strategy4.epsilon_offset = 0 # epsilon doesn't change
strategy4.epsilon = 0.75
# fifth player (random)
strategy5 = playerstrategy.EpsilonGreedyStrategy(DEFAULT_ITERATIONS)
strategy5.epsilon_offset = 0 # epsilon stays at 1 so always random
# sixth player (epsilon greedy)
strategy6 = playerstrategy.EpsilonGreedyStrategy(DEFAULT_ITERATIONS)
# seventh player (softmax)
strategy7 = playerstrategy.SoftMaxStrategy(DEFAULT_ITERATIONS)
strategies = ((strategy1,"Fixed Epsilon = 0 (greedy)"),
              (strategy2,"Fixed Epsilon = 0.25"),
              (strategy3,"Fixed Epsilon = 0.5"),
              (strategy4,"Fixed Epsilon = 0.75"),
              (strategy5,"Fixed Epsilon = 1 (random)"),
              (strategy6,"Epsilon Greedy"),
              (strategy7,"Softmax"))
for strat_tuple in strategies:
    game.AddPlayer(player.Player(DEFAULT_PLAYER_START_CORD,
                                 DEFAULT_LEARNING_RATE,
                                 DEFAULT_DISCOUNT_FACTOR,
                                 strat_tuple[0],
                                 sensor,
                                 strat_tuple[1])
                   )

mainui = ui.UI(game)

def main(iterations = 2*DEFAULT_ITERATIONS):
    # initialize pygame
    pygame.init()

    mainwindow = pygame.display.set_mode((1280,720)) # this gets UI drawn on top
    clock = pygame.time.Clock()
    clock.tick()

    iteration_val = 0
    paused = False
    running = True
    time_bank = 0 # keep initialized to 0
    while running:
        time_bank += clock.tick()
        while time_bank >= game.state_delay:
            if iteration_val >= iterations:
                paused = True
            if not paused:
                iteration_val += 1
                game.advanceStep()
            time_bank -= game.state_delay

        # draw all the game surfaces then update display
        if not paused:
            mainui.DrawGame(mainwindow, game, time_bank/game.state_delay)
            pygame.display.update()

        for event in GAME_EVENTS.get():
            if event.type == GAME_GLOBALS.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_UP:
                    if game.state_delay >= 6:
                        game.state_delay -= 5
                elif event.key == pygame.K_DOWN:
                    game.state_delay += 5
                elif event.key == pygame.K_PRINT:
                    pygame.image.save(mainwindow,"screenshot.png")
                elif event.key == pygame.K_LEFT:
                    strategy.left_down = 1
                elif event.key == pygame.K_RIGHT:
                    strategy.right_down = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    strategy.left_down = 0
                elif event.key == pygame.K_RIGHT:
                    strategy.right_down = 0
    pygame.quit()
