# FlaPyBird dimensions

As I didn't code the game, this is the result of my research and tests to acquire the dimensions and boundaries of this game.

All measurements are in pixels.

## Window

It's a 288x512 square. 288 pixels width and 512 pixels height.

Check line 24 of "flappy.py".

## X boundaries

The initial distance to the pipe is 439.

When it reaches zero, the next pipe is 193 pixels away. This repeats for every next pipe (distance between pipes is 193)

## Y boundaries

PS: the higher the bird goes, the smaller the position value)

Screen top: 0
Screen bottom: 512
Max accessible height: -36
Min surviving heigh* (just before collision with ground): 393

*during the tests, when I threw the bird on the ground, the final position printed was not always the same. Some of them were:
- 393.5
- 394
- 395
- 395.5
- 397.5
- 398
- 398.48