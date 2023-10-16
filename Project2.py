import turtle as Game
import random
import time
# Screen setup
wn = Game.Screen()
wn.title("Fruit Ninja")
wn.bgpic("background.gif")
wn.setup(width=800, height=600)
wn.tracer(0)  # Turn off automatic screen updates
appleimage = "apple.gif"
wn.addshape(appleimage)
apple = Game.Turtle(appleimage)
apple.hideturtle()
orangeimage = "orange.gif"
wn.addshape(orangeimage)
orange = Game.Turtle(orangeimage)
orange.hideturtle()
banannaimage = "bananna.gif"
wn.addshape(banannaimage)
bananna = Game.Turtle(banannaimage)
bananna.hideturtle()
bombimage = "bomb.gif"
wn.addshape(bombimage)
bomb = Game.Turtle(bombimage)
bomb.hideturtle()
bomb.penup()

# Fruits
fruits = []

def create_fruit():
    fruit = Game.Turtle()
    fruit.penup()
    fruit.shape(random.choice([appleimage, orangeimage,banannaimage]))
    fruit.goto(random.randint(-390, 390), 290)
    fruit.dy = random.uniform(-.52,-0.45)  # Random initial downward speed
    fruits.append(fruit)



#bombs
bombs = []

def create_bombs():
    bomb = Game.Turtle()
    bomb.penup()
    bomb.shape(random.choice([bombimage]))
    bomb.goto(random.randint(-390, 390), 290)
    bomb.dy = random.uniform(-.52,-0.45)  # Random initial downward speed
    bombs.append(bomb)
    bomb.penup()



#ninja create/move
ninjaimage = "Ninja.gif"
wn.addshape(ninjaimage)
ninja = Game.Turtle(ninjaimage)
ninja.penup()

# Functions
def move_ninja(x, y):
    ninja.goto(x, y)


def slice_fruit():
    global score
    for apple in fruits:
        if ninja.distance(apple) < 40:
            x = random.randint(-390, 390)
            y = random.randint(100, 290)
            apple.goto(x, y)
            score += 10


def slice_bomb():
    global score
    for bomb in bombs:
        if ninja.distance(bomb) < 40:
            x = random.randint(-390, 390)
            y = random.randint(100, 290)
            bomb.goto(x, y)
            score -= 5

#timer
timer = 10
counter_interval = 1000 
timer_up = False

counter =  Game.Turtle()
counter.penup()
counter.goto(-75, 230)
counter.hideturtle()

final_score = Game.Turtle()
final_score.penup()
final_score.goto(-200,0)
final_score.hideturtle()

def countdown():
  global timer, timer_up
  counter.clear()
  if timer <= 0:
    counter.write("Time's Up", font=("Courier", 24, "normal"))
    final_score.write("Final Score:" + str(player_name) + str(score), font=("Courier", 24 ,"normal"))
    timer_up = True
    wn.mainloop()
   
    
  else:
    counter.write("Timer: " + str(timer), font=("Courier", 24,"normal"))
    timer -= 1
    counter.getscreen().ontimer(countdown, counter_interval) 

# Score
score = 0
score_display = Game.Turtle()
score_display.speed(0)
score_display.color("black")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.penup()
score_display.write("Score: 0", align="center", font=("Courier", 24, "normal"))

# Keyboard bindings
ninja.ondrag(move_ninja)
player_name = input("Please enter you name")
wn.ontimer(countdown, counter_interval)
for i in range(6):
    create_fruit()
for i in range(2):
    create_bombs()

# Main game loop
while True:
    wn.update()
    
    for fruit in fruits:
        fruit.sety(fruit.ycor() + fruit.dy)

        # Check for fruit hitting the bottom
        if fruit.ycor() < -400:
            x = random.randint(-390, 390)
            y = random.randint(100, 290)
            fruit.goto(x, y)
    for bomb in bombs:
        bomb.sety(bomb.ycor() + bomb.dy)

        # Check for fruit hitting the bottom
        if bomb.ycor() < -400:
            x = random.randint(-390, 390)
            y = random.randint(100, 290)
            bomb.goto(x, y)

    # Check for slicing
    slice_fruit()
    slice_bomb()
    # Update the score
    score_display.clear()
    score_display.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))
    score_display.clear()


