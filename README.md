# 3D Snake Game

This is a 3D remake of the classic Nokia Snake game, developed as a course project for CSE423 (Computer Graphics). It brings the nostalgic experience of the original Snake game into a fully rendered modern 3D environment, enriched with level progression, obstacles, dynamic camera control, and more exciting features.
All features are implemented using PyOpenGL.

<h2>Game Features</h2>

<h3>3 Unique Levels</h3>
<ul>
  <li>Distinct board layouts</li>
  <li>Different food colors</li>
  <li>Increasingly complex obstacle patterns</li>
</ul>

<h3>Two Types of Food</h3>
<ul>
  <li>Normal Food: Increases score by 10</li>
  <li>Bonus Food: Appears occasionally and scores 20</li>
</ul>

<h3>Snake Growth & Collision</h3>
<ul>
  <li>Snake’s length increases with each food consumed</li>
  <li>Collision with own body (head-to-tail) or obstacles results in game over</li>
</ul>

<h3>Teleportation Holes</h3>
<ul>
  <li>3 teleportation holes per level to instantly transport the snake to different areas of the board</li>
</ul>

<h3>Level Progression</h3>
<ul>
  <li>Score increases with food intake</li>
  <li>Every 100 points = level up, introducing new board designs and challenges</li>
  <li>A message appears before each level-up</li>
</ul>

<h3>Game Controls</h3>
<ul>
  <li>Includes Pause and Reset options for flexible gameplay</li>
</ul>

<h3>Camera Movement</h3>
<ul>
  <li>Enhances visibility and immersion in the 3D environment</li>
  <li>Move camera up/down using <b>UP</b> and <b>DOWN</b> arrow keys</li>
  <li>Rotate camera around the game board using <b>LEFT</b> and <b>RIGHT</b> arrow keys</li>
</ul>


| buttons (keyboard) | features |
| :-------: |  :-------: | 
|    g  |      snake moves leftward   |
|    h     |      snake moves rightward      |
|    b   |      snake moves downward |
|    y  |      snake moves upward     |
|    r  |      reset the game    |
|    p |      pause the game    |



## Screens from the Game

| | |
|:--:|:--:|
| <img src="images/level 1 board.png" alt="Level 1" width="400px"><br>Level 1 Board | <img src="images/level 2 board.png" alt="Level 2" width="400px"><br>Level 2 Board |
| <img src="images/level 3 board.png" alt="Level 3" width="400px"><br>Level 3 Board | <img src="images/level 2 up message.png" alt="Level 2 Up" width="400px"><br>Level 2 Up Message |
| <img src="images/level 3 up message.png" alt="Level 3 Up" width="400px"><br>Level 3 Up Message | <img src="images/bonus food.png" alt="Bonus Food" width="400px"><br>Bonus Food |
