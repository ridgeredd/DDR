# Ridge Redding usy7dp
# West Plowman dzy5mz

"""
Game idea:
Dance Dance Revolution type game
Directional arrows will drop down from the top of the screen
The player must hit the corresponding arrow on their keyboard when the arrows hit a line at the bottom of the camera
There will be a score tally and health meter at the side of the screen
The closer you are to hitting the arrow right as it touches the line the more points you get
Text will flash on the screen representing how close the player was to hitting it perfectly
As you either miss, hit the wrong arrow button, or press a button too early, you will lose health
If you hit enough consecutive arrow you start to slowly regain health
As time goes on, the arrows speed up
If health drops to 0, the game ends
Displays game over and top 5 players and their scores
Gives you option to save your name and score to a high score file

Basic Features:

User Input: user inputs arrows corresponding to the ones on screen. If input matches nearest arrow and hit within
acceptable distance, user gets points otherwise loses health

Game Over: games ends when health drops to 0. Displays game over screen

Graphics: Arrows dropping down will be different colored graphics. The targets at bottom of screen will light up to
represent the arrow of the users last input

Additonal Features:

Health Bar: displayed at the top of the screen. As arrows are missed you lose health. If health drops to or below 0,
game ends

Inter-session Progress: after game, prompts you to add your name and takes your score to add to a high scores file.

Sprite animation: When users hit arrow within acceptable window, the arrow will change to a gray version of itself.
When users miss an arrow by pressing the wrong key, the missed arrow will show up as red before disappearing. Lastly,
The targets at the bottom of the screen will change colors when its key is hit. The left arrow target will light up
when the left arrow key is hit and so on.

Feedback and streak display: when users hit an arrow, gives feedback on how well arrow was hit, "perfect", "good",
"okay", etc. Also displays the number of consecutive arrows hit.
"""