# Overview
Computer Vision pipeline that connects live video feed of battleship board to game-state to be interpreted by internal game simulation 

# Setting Up
Print out aruco.pdf and paste the markers on the board similar to the fashion shown below. 

![](https://i.imgur.com/cSoSDOz.jpg)

Make sure a video camera is also connected to the current system and place it infront of the Battleship board in question

## Calibration 
The Battleship folder contains the file named `calibrate.py`. Adjust the offsets at the top of the file to fit the current arUco marker setup. 

# How to Run
The program runs through `game.py` located in the Battleship folder. This program takes the following arguments. 
* `--playermode` with 3 options, `hvh`, `hva`, and `ava` representing the modes human vs human, human vs ai, and ai vs ai 
* `--player1_usecamera` with options `yes` or `no` that enables or disables the camera. The default option is no. 
* `--player2_usecamera` with options `yes` or `no` that enables or disables the camera. The default option is no. 


# To Do
* conversion of bottom gameboard
* More robust AI (just guesses random spot right now)
* More accurate conversion of top board