# sensorstate should be initialized to 4095 (nothing ahead)

max_block_detection = 3
total_states = 4096

# returns an integer in [0,3] and starting y index for double sensor
def GetSingleSensor(gameref, x_start, y_start):
    cur_y = y_start
    for i in range(max_block_detection):
        next_y = (cur_y + gameref.y_row_blocks - 1) % gameref.y_row_blocks
        if gameref.block_array[x_start][cur_y] == 1:
            return i,next_y
        cur_y = next_y
    return max_block_detection,cur_y

# returns an integer in [0,15]
def GetDoubleSensor(gameref, x_start, y_start):
    a,y_double1 = GetSingleSensor(gameref, x_start, y_start)
    b,y_double2 = GetSingleSensor(gameref, x_start, y_double1)
    return a*4 + b

# returns an integer in [0,4095]
def GetSensorState(gameref, playerref):
    x_middle = playerref.player_x_col
    x_left = (x_middle + gameref.x_col_blocks - 1) % gameref.x_col_blocks
    x_right = (x_middle + 1) % gameref.x_col_blocks
    y_sides = playerref.player_y_row
    y_middle = (y_sides + gameref.y_row_blocks - 1) % gameref.y_row_blocks
    left_sensor_val = GetDoubleSensor(gameref, x_left, y_sides)
    middle_sensor_val = GetDoubleSensor(gameref, x_middle, y_middle)
    right_sensor_val = GetDoubleSensor(gameref, x_right, y_sides)
    # print(left_sensor_val//4,left_sensor_val%4,middle_sensor_val//4,middle_sensor_val%4,right_sensor_val//4,right_sensor_val%4) # debug
    return left_sensor_val*16*16 + middle_sensor_val*16 + right_sensor_val
