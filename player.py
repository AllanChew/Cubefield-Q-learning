import playerhistory


class Player:
    player_x_step = 0

    # set gameref once its made
    gameref = None

    def __init__(self, start_coords, learning_rate, discount_factor, strategy, sensor):
        self.player_x_col = start_coords[0]
        self.player_y_row = start_coords[1]
        self.player_y_row_start = self.player_y_row
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.history = playerhistory.PlayerHistory(20)

        # PlayerStrategy
        self.strategy = strategy

        # Sensor
        self.sensor = sensor

        # QTable[state][action]
        self.QTable = [[0 for j in range(3)] for i in range(self.sensor.getStates())]

    def performStepDecision(self):
        # non optimized - each call results in 2 calls to getState() -> 1 will be duplicated next call
        state_copy = self.sensor.getState()
        action = self.strategy.getStrategyAction(self.QTable[state_copy])
        reward = self.ApplyAction(self.gameref, action)
        self.history.UpdateHistoryQueue(action, reward)
        new_state = self.sensor.getState()
        TD = reward + self.discount_factor*max(self.QTable[new_state]) - self.QTable[state_copy][action]
        self.QTable[state_copy][action] += self.learning_rate*TD # update Q value

    # updates player state and returns reward/punishment from applying action
    # looks into game state to determine reward/punishment
    def ApplyAction(self,gameref,action):
        # update x values (player_x_step and player_x_col)
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

        # update y value (player_y_row)
        old_player_y_row = (gameref.generation_y_index + self.player_y_row_start) % gameref.y_row_blocks
        moved_front_block = False
        if gameref.game_y_step == 0:
            moved_front_block = True
            self.player_y_row = (gameref.generation_y_index + self.player_y_row_start - 1) % gameref.y_row_blocks # move to forward block
        else:
            self.player_y_row = old_player_y_row

        if moved_left_right or moved_front_block: # will move to new block
            if gameref.block_array[self.player_x_col][self.player_y_row] == 1: # check new block
                return -1 # new location is a solid block
        if ( moved_left_right and moved_front_block and # will move diagonal
             gameref.block_array[self.player_x_col][old_player_y_row] == 1 and # check block immediately left/right
             gameref.block_array[old_player_x_col][self.player_y_row] == 1 ): # check block in front
            return -1 # hit due to squeezing between two solid block corners
        return 0
