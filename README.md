# CVBattleship
Computer Vision pipeline that connects battleship board to game-state to be interpreted by an AI. 

# Timeline
## Progress Report 1 (Due April 13)
Should be finished by this point (probably do this in order)
### Consistently detect red and white dots on board 
3D kernel for red and white response?
Is it possible or even feasible to train a classifier for these dots? I'm just afraid of noise and other red/white stuff flagging.
Data for classifier we would just take the individual dots from the gameboard from the existing data. 

### A good approximation of the board corners
Collect feature points and somehow estimate a distance value such that every x y feature point is reachable from another feature through integer multiples of this distance.

What to do about the instance of having only one white dot? Is it possible to estimate the game board by looking at the dots of gameboard with no reference or identification of the red/white dots? 

Possible to use sobel filter here for traditional edge detection? 

###  Some conception of image rectification with found board corners
idk man

## Progress Report 2 (Due April 20) (I think??)
Should be finished by this point
###  Can accurately convert board into gamestate
###  Pipeline that connects our detector to battleship AI and simulation
###  Working version of battleship and/or API that works with our conversion to game states

Presentation (April 26)
###  Finish some kind of video demonstration by this point

Final code and report (April 27)

