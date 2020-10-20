# sensorstate should be initialized to 4095 (nothing ahead)
MAX_BLOCK_DETECTION = 3

# returns an integer in [0,3] and starting y index for double sensor
def GetSingleSensor(gameref, x_start, y_start):
    cur_y = y_start
    for i in range(MAX_BLOCK_DETECTION):
        next_y = (cur_y + gameref.y_row_blocks - 1) % gameref.y_row_blocks
        if gameref.block_array[x_start][cur_y] == 1:
            return i,next_y
        cur_y = next_y
    return MAX_BLOCK_DETECTION, cur_y


class TripleSensor:
    gameref = None

    def getStates(self):
        return 64

    def getState(self,playerref):
        gameref = self.gameref
        x_middle = playerref.player_x_col
        x_left = (x_middle + gameref.x_col_blocks - 1) % gameref.x_col_blocks
        x_right = (x_middle + 1) % gameref.x_col_blocks
        y_sides = playerref.player_y_row
        y_middle = (y_sides + gameref.y_row_blocks - 1) % gameref.y_row_blocks
        left_sensor_val = GetSingleSensor(gameref, x_left, y_sides)[0]
        middle_sensor_val = GetSingleSensor(gameref, x_middle, y_middle)[0]
        right_sensor_val = GetSingleSensor(gameref, x_right, y_sides)[0]
        # print(left_sensor_val,middle_sensor_val,right_sensor_val) # debug
        return left_sensor_val*4*4 + middle_sensor_val*4 + right_sensor_val
