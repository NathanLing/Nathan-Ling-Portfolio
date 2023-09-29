import turtle as Game
import random

# Register custom images

Game.register_shape("assets/apple.gif")
Game.register_shape("assets/bullet.gif")
       
Game.register_shape("assets/happy.gif")
Game.register_shape("assets/sad.gif")
Game.register_shape("assets/uhoh.gif")

# Main Game Function
def game():

    # Function for stopping game loop
    def byebye():
        # Global but for basically neseted functions 
        nonlocal GameRunning
        GameRunning = False
    
    Game.goto(0,0)
    
    # Resets screen if decided to play again
    Game.resetscreen()
    Game.clearscreen()
    
    # Creating variables for game elements
    apples = []
    waters = []
    rockets = []
    teleporters = []

    createdRockets = []

    appleSize = 1
    reason = ""
    GameRunning = True

    # Screen dimensions
    screen_width = Game.window_width()
    screen_height = Game.window_height()

    # Turns off animations
    Game.tracer(False)

    # A function that creates an apple
    def createApple():
        # Create apple
        apple = Game.Turtle()
        # Set apple to picture
        apple.shape("assets/apple.gif")
        apple.shapesize(30, 30)
        
        apple.up()
       
        leftMostOfScreen = -(screen_width / 2) + 60
        rightMostOfScreen = (screen_width / 2) - 60
        
        lowestOfScreen = -(screen_height / 2) + 60
        highestOfScreen = (screen_height / 2) - 60
        
        randomX = random.randint(leftMostOfScreen, rightMostOfScreen)
        randomY = random.randint(lowestOfScreen, highestOfScreen)
        
        # Make sure apple isnt drawn on another apple or water
        while checkApple(randomX, randomY) or checkWater(randomX, randomY):
            randomX = random.randint(leftMostOfScreen, rightMostOfScreen)
            randomY = random.randint(lowestOfScreen, highestOfScreen)

        apple.goto(randomX, randomY)

        apples.append(apple)

           
    def createWater():
        # Create water
        water = Game.Turtle()
        water.pencolor("black")
        water.fillcolor("blue")
        water.shape("square")
        
        tilt = random.choice( [0, 90, 180, 270] )
        water.tilt(tilt)
        
        waterWidth = random.uniform(1.3, 2.5)
        waterLength = random.randint(2,5)
        
        water.shapesize(waterWidth, waterLength)
        
        water.up()
       
        leftMostOfScreen = -(screen_width / 2) + 60
        rightMostOfScreen = (screen_width / 2) - 60
        
        lowestOfScreen = -(screen_height / 2) + 60
        highestOfScreen = (screen_height / 2) - 60
        
        randomX = random.randint(leftMostOfScreen, rightMostOfScreen)
        randomY = random.randint(lowestOfScreen, highestOfScreen)
        
        # Make sure water isn't borders or fill isn't drawn on snake starting position
        while checkApple(randomX, randomY) or (abs(randomX - Game.xcor()) < 60 and abs(randomY - Game.ycor()) < 60):
            randomX = random.randint(leftMostOfScreen, rightMostOfScreen)
            randomY = random.randint(lowestOfScreen, highestOfScreen)
       
        water.goto(randomX, randomY)
       
        # Make x,y range of water while depending on tilt
        
        waterXCor = water.xcor()
        waterYCor = water.ycor()
        
        waterWidth = (water.shapesize()[0] * 10)
        waterLength = (water.shapesize()[1] * 10)
        
        if tilt == 90 or tilt == 270:
            xRange = [waterXCor - waterWidth, waterXCor + waterLength]
            
            yRange = [waterYCor - waterLength, waterYCor + waterLength]
        else:
            xRange = [waterXCor - waterLength, waterXCor + waterLength]
            
            yRange = [waterYCor - waterWidth, waterYCor + waterWidth]
       
        waters.append([water, xRange, yRange, tilt])


    def createTeleporter():
        teleporter = Game.Turtle()
        teleporter.pencolor("black")
        teleporter.fillcolor("purple")
        teleporter.shape("square")
        teleporter.shapesize(3, 3)
        teleporter.up()
       
        leftMostOfScreen = -(screen_width / 2) + 60
        rightMostOfScreen = (screen_width / 2) - 60
        
        lowestOfScreen = -(screen_height / 2) + 60
        highestOfScreen = (screen_height / 2) - 60
        
        randomX = random.randint(leftMostOfScreen, rightMostOfScreen)
        randomY = random.randint(lowestOfScreen, highestOfScreen)
        
        # Make sure teleporter isn't drawn on snake starting position or water, or apple
        while checkApple(randomX, randomY) or checkWater(randomX, randomY) or (abs(randomX - Game.xcor()) < 60 and abs(randomY - Game.ycor()) < 60):
            randomX = random.randint(leftMostOfScreen, rightMostOfScreen)
            randomY = random.randint(lowestOfScreen, highestOfScreen)
       
        teleporter.goto(randomX, randomY)
       
        teleporters.append(teleporter)


    # Create a function that checks if x and y are within an apple
    def checkApple(x, y):
        for apple in apples:
            
            distanceBetweenAppleX = abs(x - apple.xcor())
            distanceBetweenAppleY = abs(y - apple.ycor())
            
            borderAroundApple = (appleSize * 40)
            
            if ( distanceBetweenAppleX < borderAroundApple and distanceBetweenAppleY < borderAroundApple ):
                return True
            
        return False
    
    def checkWater(x, y): 
        for water in waters:
            # Water object: [water, xRange, yRange, tilt]
            
            waterXRange = water[1]
            waterYRange = water[2]
           
            waterXMin = waterXRange[0]
            waterXMax = waterXRange[1]
            
            waterYMin = waterYRange[0]
            waterYMax = waterYRange[1]
            
            borderAroundXPos = (x + 10)
            borderAroundYPos = (y + 10)
            
            borderAroundXNeg = (x - 10)
            borderAroundYNeg = (y - 10)
            
            # Example
            # x,y : 5, 3
            # X Range: MIN [x1, x2] MAX -10, 10
            # Y Range: MIN [y1, y2] MAX -5, 5
            
            withinXRange = waterXMin < borderAroundXPos < waterXMax 
            WithinYRange = waterYMin < borderAroundYPos < waterYMax
            withinPosRange = withinXRange and WithinYRange
            
            withinXRangeNeg = waterXMin < borderAroundXNeg < waterXMax
            withinYRangeNeg = waterYMin < borderAroundYNeg < waterYMax
            withinNegRange = withinXRangeNeg and withinYRangeNeg
            
            
            # Check if snake hit the lake, including its border/edges

            if ((withinPosRange) or (withinNegRange)):
                return True
            
        return False

    
    for _ in range(random.randint(5, 15)):
        createApple()
    #print("Apples created")
    
    for _ in range(random.randint(3, 7)):
        createWater()
    #print("Water created")
    
    for _ in range(random.randint(3, 5)):
        createTeleporter()
    #print("Teleporters created")
    
    # Screen is only updated when update() is called
    Game.update()

    Snake = Game.Turtle()
    Snake.shape("assets/happy.gif")
    Snake.color("black")
    Snake.penup()
   
    # Speed of the turtle
    speed = random.uniform(0.5, 0.7) + 0.1


    # define rotation of each key
    def up ():
        # If snake is not going down, then it can go up
        if int(Snake.heading()) != 270:
            Snake.setheading(90)
            
    def right():
        # If snake is not going left, then it can go right
        if int(Snake.heading()) != 180:
            Snake.setheading(0)
            
    def left():
        # If snake is not going right, then it can go left
        if int(Snake.heading()) != 0:
            Snake.setheading(180)
            
    def down():
        # If snake is not going up, then it can go down
        if int(Snake.heading()) != 90:
            Snake.setheading(270)


    def deleteApple(appl):
        # Delete apple
        apples.remove(appl)
        appl.hideturtle()
       
        # Create new apple
        createApple()
       
        # Create bullet 
        rocket = Game.Turtle()
        rocket.shape("assets/bullet.gif")
        rocket.penup()
        
        rockets.append(rocket)

    wn = Game.Screen()
    wn.listen()

    wn.bgcolor('white')

    wn.onkey(up, 'Up')
    wn.onkey(up, 'w')

    wn.onkey(right, 'Right')
    wn.onkey(right, 'd')


    wn.onkey(left, 'Left')
    wn.onkey(left, 'a')


    wn.onkey(down, 'Down')
    wn.onkey(down, 's')
   
    wn.onkey(byebye, 'Escape')

    topleftMostX = -screen_width / 2
    topleftMostY = screen_height / 2

    corners = [
        [topleftMostX, topleftMostY], 
        [topleftMostX, -topleftMostY], 
        [-topleftMostX, topleftMostY], 
        [-topleftMostX, -topleftMostY]
        ]
   
    while GameRunning:
        tooClose = False
        KindaClose = False
        
        # Move snake
        Snake.forward(speed)
       
        # Everytime a rocket is created, put it at 4 possible positions, 1. top left corner, 2. top right corner, 3. bottom left corner, 4. bottom right corner
        # Once rocket is spawned add it to a list of spawned rockets where its position is stored at all times so if it hits the snake, the game ends
        for rocket in rockets:
            # Spawn at random corner
            if rocket not in createdRockets:
                randomCorner = random.choice(corners)
                rocket.goto(randomCorner[0], randomCorner[1])
                createdRockets.append(rocket)
            else:
                # Check if rocket hits snake
                tooCloseX = abs(Snake.xcor() - rocket.xcor()) < 10
                tooCloseY = abs(Snake.ycor() - rocket.ycor()) < 10
                if ( tooCloseX and tooCloseY ):
                    reason = "rockets"
                    GameRunning = False
       
        for homingRockets in createdRockets:
            # Based on distance from snake, change snake picture to happy, sad, or uhoh
            
            within100PixelsX = abs(Snake.xcor() - homingRockets.xcor()) < 100
            within100PixelsY = abs(Snake.ycor() - homingRockets.ycor()) < 100
            
            within300PixelsX = abs(Snake.xcor() - homingRockets.xcor()) < 300
            within300PixelsY = abs(Snake.ycor() - homingRockets.ycor()) < 300
            
            if ( within100PixelsX and within100PixelsY ):
                tooClose = True
            elif ( within300PixelsX and within300PixelsY):
                KindaClose = True
            
            angle = homingRockets.towards(Snake)
            
            randomSpeed = speed / (random.uniform(1.1, 1.7) * 2)
            
            homingRockets.setheading(angle)
            homingRockets.forward(randomSpeed)
           
        for teleporter in teleporters:
            # Teleport to another random teleporter
            
            withinTeleporterX = abs(Snake.xcor() - teleporter.xcor()) < 35
            withinTeleporterY = abs(Snake.ycor() - teleporter.ycor()) < 35
            
            if ( withinTeleporterX and withinTeleporterY ):
                randomTeleporter = random.choice(teleporters)
                
                posOutsideOfTele = random.randint(-40, 40)
                
                Snake.goto(randomTeleporter.xcor() + posOutsideOfTele, randomTeleporter.ycor() + posOutsideOfTele)
                
        for apple in apples:
            tooCloseOnXAxis = abs(Snake.xcor() - apple.xcor()) < (appleSize * 17)
            tooCloseOnYAxis = abs(Snake.ycor() - apple.ycor()) < (appleSize * 17)

            if (tooCloseOnXAxis and tooCloseOnYAxis):
                deleteApple(apple)
                speed += random.uniform(0.06, 0.15)



        for water in waters:
            # Check if snake is within the range of water body
            waterXRange = water[1]
            waterYRange = water[2]
            
            # Check if snake hit the lake, including its border/edges
            if ((waterXRange[0] < Snake.xcor() + 10 < waterXRange[1] and waterYRange[0] < Snake.ycor() + 10 < waterYRange[1]) or (
                    waterXRange[0] < Snake.xcor() - 10 < waterXRange[1] and waterYRange[0] < Snake.ycor() - 10 < waterYRange[1])):
                reason = "falling into a lake"
                GameRunning = False
               
        # Make sure snake doesn't go out of bounds
        if (Snake.xcor() > screen_width / 2 or Snake.xcor() < -screen_width / 2 or Snake.ycor() > screen_height / 2 or Snake.ycor() < -screen_height / 2):
            reason = "falling out of bounds :("
            GameRunning = False

        if tooClose:
            Snake.shape("assets/sad.gif")
        
        elif KindaClose:
            Snake.shape("assets/uhoh.gif")
        
        else:
            Snake.shape("assets/happy.gif")
        
        Game.update()
   
    if reason == "":
        Game.bye()
   
    Game.resetscreen()
    Game.clearscreen()
    
    # Display score
    score = Game.Turtle()
    score.hideturtle()
    score.color("black")
    score.penup()
    score.goto(-250, -150)
   
    userScore = int(len(rockets) * 1.5) + int((speed * 10) * 3)
   
    score.write("You died to: " + reason + "\n\nYou dealt with " + str(len(rockets)) + " rockets!\n\nScore: " + str(userScore) + "\n\nPress space to play again", font=("Arial", 30, "normal"))
   
    # Wait for user to press space to restart game
    wn.onkey(game, 'space')
   
    # Dont close window
    wn.mainloop()
   
   
game()