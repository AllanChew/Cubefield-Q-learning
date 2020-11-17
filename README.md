# CS486 Final Project - Cubefield Q-Learning Analysis

Welcome to our CS486 final project. In this project, we implemented an AI to play the game Cubefield, in order to analyze the effectiveness of different behaviour policies for the Q-learning algorithm. All experimentation was conducted within a simplified 2-D version of the Cubefield game. We built out the game using the **Pygame module** and natively implemented the sensors and policies. As a result, other than Pygame, **there are no additional libraries that need to be installed**.    

### Screenshot and Features

The following is a screenshot of our game. As you can see, each square is either grey (representing an obstacle), or white (representing empty space). As the squares scroll downwards, the player has the option of moving left, right, or staying in the same column in order to avoid colliding with incoming obstacles. To aid visual feedback and help us better trace the agent's travelled path, we added room below the player where green and red dots show the last 20 moves of the player. A red dot is used to represent a collision with a block, otherwise a green dot is used. These red and green dots are purely graphical and have no impact on the game's mechanics. 

<img src="/cubefield-screenshot.png" width = "500">

In addition to the option of playing the game, our team has implemented the different behaviour policies and presented the AI's gameplay simultaneously on 7 screens, as shown below:

<img src="/seven-agents-cubefield.png">

### Commands

To start the game play, you can run the command:

```
python3 main.py
```

You should see Pygame start up and showcase the screenshots as shown above.

Note: This game will not run if the build system is Python 2. 
