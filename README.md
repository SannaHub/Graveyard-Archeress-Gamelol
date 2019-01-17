# Graveyard-Archeress-Game
A game code created by the Lyon group for our Basic Programming group project

*Creators:* Sanna Bashir, Geanina Verestiuc and Aidan Ward

*Course:* Basic Programming

*Study Program:* Cognitive Science and Artificial Intelligence, year 1

*Instructors:* Dr. F. Hermens and E. van Miltenburg 



# Description
This code serves as a platformer, PvE (player versus enemy) game. The code is written using the python programming language and pygames as the main library. The purpose of this game is to defeat all the enemies without the character dying. A powerup is available throughout the game. This powerup attack decreases the enemies health more than the normal player attack. This powerup is in the form of a potion and can be found across the screen. There is more than one potion, each potion gives the player one chance at a special attack.

# Requirements
*Libraries:*

    ○ Pygame 1.9.4
    ○ Random
    ○ Os
    ○ Sys

Python version 3.7.1 was used to create the game.

The game was tested and cleared to be working properly on versions 3.7.1, 3.6, 3.6.5, 3.3.2 of Python.

It worked on both Windows and MacOs.

Tested with the following IDE's:

    ○ Python's build-in IDLE
    ○ Anaconda's Spyder
    ○ PyCharm 3.4
    
Python was downloaded using this site: https://www.python.org/downloads/

Anaconda from https://www.anaconda.com/download/#macos

Python's IDLE was the one used to create this game. 

The code works fine in Spyder _ONLY_ if you change the last sentence from 'sys.exit()' to 'exit()'. It is unknown to us why this is a requirement, but after some research, we suspect it has something to do with the implementation detail of python in IPython and CPython.

# Instructions

*Goal:*
The goal is to kill all the enemies using either the attack or the powerup attack, without letting your player die. Each enemy has a health of 100. The first enemy; the zombies are the easiest to defeat. The next enemies; the orks are a little harder to defeat. The last enemy: the Desert Robot is the hardest to defeat and also has its own attack.

*Controls/operation:*
There are two ways to control the character in the game. Either using the arrow or WASD keys on the players keyboard. Each key's function is defined below.

    'esc' = escape/quit game
    'spacebar' = shoot player's attack

    'w' = jump
    'a' = move left
    's' = _does nothing_
    'd' = move right
    'q' = escape/quit game
    'e' = shoot player's powerup attack

    Up arrow = jump
    Left arrow = move left
    Down arrow = _does nothing_
    Right arrow = move right
    '/' = shoot player's powerup attack

*Adjusting speed of code:*
After running the code succesfully for the first time, check if the game is not too slow or fast. If it is too slow, change the FPS settings at the beginning of the code to be a little higher. If the game seems too fast, lower the FPS. Test the new setttings and settle on a FPS that suits you and your computer. (this is addressed in the report)


# Acknowledgements
We'd like to thank the following youtube channels for helping us with getting to know the pygame module:

https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg

We'd like to thank ... for testing our game.

We'd like to thank everybody that provides free sprites and sound effects, without them this game wouldn't be what it is today.

# Credits

Images/sprites

Background:
https://craftpix.net/freebies/free-halloween-2d-game-backgrounds/


Player: 
https://free-game-assets.itch.io/free-2d-woman-warrior-sprite-sheets


Zombie:

https://free-game-assets.itch.io/free-2d-game-zombie-sprite/


Orks:
https://free-game-assets.itch.io/2d-trolls-free-sprite


Desert Robot:
https://free-game-assets.itch.io/free-2d-robot-sprite


Potion:
https://free-game-assets.itch.io/free-game-icons-potions/download/eyJleHBpcmVzIjoxNTQ3NTU5MTM0LCJpZCI6MTQ1NTE1fQ%3d%3d%2e%2fmgG4VvNONaNJRnbDatB0tPNOd8%3d

Arrow:
https://free-game-assets.itch.io/free-2d-woman-warrior-sprite-sheets


Powerup:
https://pngimage.net/fire-arrow-png-3

Platforms/ground tiles/visualstuff:

https://www.gameart2d.com/free-graveyard-platformer-tileset.html



Sound effects:

Bg music:
https://opengameart.org/content/spooky-dungeon

Starting sound:
https://opengameart.org/content/voice-samples

Arrow shooting:

Zombie hit:

Ork hit:

Desert Robot hit:

Player hit:

Losing sound:
https://freesound.org/people/Mattix/sounds/435196/
Winning sound:




