# Welocme to not so super mario!


# Introduction to the project:

This game is a rip off of the classic Super Mario Bros. It is crated using python3, for the assignment of SSAD course at IIIT Hyderabad.

Date: 23rd August, 2018.
Place: Room 258, Bakul Niwas, IIIT Hyderabad.
Owner: Aditya Morolia


# File Structure:

- Directory contains the following files:
    -main.py
        This file contains the main game loop.
    -characters.py
        Contains the classes that represents the various characters in the game.
    -config.py
        Contains general information used by a lot of functions in the project. Also contains the input accepting function.
    -board.py
        Handles the grid to be printed on the screen.
    -objects.py
        Handles the various obstacles, scenery, etc. in the game.
    -readme.md
        Contains general information about the project and this particular file.
    -requirements.txt
        Contains the names of all the packages used in the project.


# Features:

	- Normal enemy 'E', can be killed by jumping on him.
    - Smart Enemy, 'SE', can be only killed by lazer(operated by pressing ' ' [SPACE KEY]).
    - If any of the above two enemies hit you in any other way, you die.
    - Green coloured pipes are 'obstacles'. Jump over them to move forward.
    - Gameplay is time based. So if you try to stay at one place for too long, you will be swamped with enemies.
    - You can jump over bridges ('[]')
    - Hitting blocks having a '?' with your head for first time gives you strength, and your height increases.
    - Hitting on it the second time (i.e., while are in 'super' state) you get the power to fire lazer.
    - Each mystery block ('?') works only once.
    - The game is infinitely long. I expect you to play for a few minutes and then get on with your life. 
    - Jump on springs to jump higher than usual. No point of this feature, just there because it was a requirement in the assignment.
    - Might add modifications later.


# Controls:

	- 'D': Move forward
	- 'A': Move backward. Can only move in the frame length in this direction.
	- 'W': Jump up
	- ' '(space key): Lazer, when power mode is on.


## Running the program:

- First, install all the requirements:
	- `pip install -r requirements.txt`
- Now, simply replace the first line of `main.py` with the location of your python installation
	- `#!/usr/bin/env python`
- Running the program is easy
	- `./main.py`
