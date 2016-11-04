# ===========================================================
# Raindrops
# (GNU GPL3) Andy Bray and James Bray 16th October 2016
# Github repo: https://github.com/bueller314/raindrops
#
# Simple Python game for the BBC Microbit (5x5 LED + 2 btn)
# Designed by James (12), coded by Andy (Dad).
#
# Mission: Dodge the rain and survive as long as you can !
# Keys:    Restart    = [Reset]
#          Move left  = [A]
#          Move right = [B]
# ===========================================================

# Imports
from   microbit import *
import random
import microbit

# Game parameters
rain_speed        = 0.1      # Higher number = faster rain
rain_probability  = 20       # Higher number = less rain
rain_acceleration = 0.001    # Higher number = rain accelerates faster
game_delay        = 65       # Higher number = slower game 
player_position   = 2        # Starts in the middle (0-4)

# Global variables
dry_time  = microbit.running_time()
raindrops = [0.0, 0.0, 0.0, 0.0, 0.0]

# If a new raindrop is required, attempt to pick a free slot
def start_raindrop (raindrops):
    pick_raindrop = random.randint(0, 4)
    if raindrops[pick_raindrop] == 0.0:
        raindrops[pick_raindrop] = 1.0
    return;

# Move the player left/right based on command and within limits
def move_player (position, direction):
    if direction == "L":
        if position > 0:
            position -= 1
    if direction == "R":
        if position < 4:
            position += 1
    return position;

# Render the screen based on array of raindrops and player position
def draw_screen(raindrops, player_position):
    lights = [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]]

    # Set the above 2D array to 9 or 6 (rain drop or trail)
    for array_col in range (0, 5):
        array_row = int(raindrops[array_col])
        lights [array_row][array_col] = 9
        if array_row > 0:
            lights [array_row - 1][array_col] = 6

    # Set the player position to 9 (on)
    lights [5][player_position] = 9

    # Turn the 2D array into lights on/off
    for row in range (0, 5):
        for col in range (0, 5):
            display.set_pixel (col, row, lights[row + 1][col])

    sleep(game_delay)
    return;

# Any raindrops in flight, move them down
def advance_rain(raindrops, rain_speed):
    for raindrop in range (0, 5):
        if raindrops [raindrop] > 0.0:
            raindrops [raindrop] += rain_speed
            if raindrops [raindrop] >= 6.0:
                raindrops [raindrop] = 0.0
    return raindrops;

# Check if the player is still dry
def player_dry(raindrops, player_position):
    return (raindrops[player_position] < 5.0);

# Game over (player was wet)
def game_over(dry_time):
    score = str(int((microbit.running_time() - dry_time) / 1000))
    while True:
        display.show(Image.SAD)
        sleep(2000)
        display.scroll("Score: " + score)
    return;

# ============= > main game loop < =============

# Welcome message
display.scroll("RAINDROPS", delay = 100)

while True:
    
    # If random event, try to start some rain 
    if random.randint(1, rain_probability) == 1:
        start_raindrop(raindrops)

    # Button handler (left)
    if button_a.is_pressed():
        player_position = move_player (player_position, "L")
        
    # Button handler (right)
    if button_b.is_pressed():
        player_position = move_player (player_position, "R")

    # Move rain down the screen
    raindrops = advance_rain(raindrops, rain_speed)

    # Keep going while the player is dry, otherwise game over !
    if player_dry(raindrops, player_position):
        draw_screen(raindrops, player_position)
    else:
        game_over(dry_time)

    # Gradually get faster
    rain_speed += rain_acceleration
