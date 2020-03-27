import random
import time
import arcade


# Set constants for the screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CIRCLE_PADDING = 0.8  # 1 is touching lines and 0 no balls at all

# name of the file to be processed
name = 'level.txt'

# 2d matrix with (0,0) at top left, currState[y][x]
currState = []

# x and y axis size
xLength = 0
yLength = 0

# number of tries
nTries = 0

# list of projectiles
balls = []

# projectiles count
ballCount = 0

# nodes count
nodeCount = 0



class Node(object):

    def __init__(self, parent, click, state, currentCost):
        global nodeCount

        self.parent = parent
        self.children = []
        self.click = click
        self.state = state
        self.balls = []
        nodeCount += 1
        self.id = nodeCount
        self.currentCost = currentCost
        self.estimatedCost = 0
        self.totalCost = 0


    def move_balls(self):
        for ball in self.balls:
            ball.move()

    
    def check_colisions(self):
        newBalls = []

        i = 0
        while i < len(self.balls):
            auxballs = self.balls[i].check_colision(self.state)
            if auxballs != "deleted":
                if (len(auxballs) > 0):
                    newBalls.extend(auxballs)
                else:
                    i=i+1
        
        self.balls.extend(newBalls)

    
    def process_click(self):
        self.state[self.click[0]][self.click[1]] = max(0, self.state[self.click[0]][self.click[1]] - 1)

        if not self.state[self.click[0]][self.click[1]]:
            self.balls.append(Projectile("up", click))
            self.balls.append(Projectile("down", click))
            self.balls.append(Projectile("right", click))
            self.balls.append(Projectile("left", click))

            while len(self.balls) > 0:
                self.move_balls()
                self.check_colisions()


    def get_children(self):
        global xLength, yLength

        i = 0
        while i < xLength:
            j = 0
            while j < yLength:
                if self.state[j][i] != 0:
                    child = Node(self, [j,i], self.state, self.currentCost+1)
                    child.process_click()
                j = j + 1
            x = x + 1


    def draw(self, sleep_duration):
        global SCREEN_HEIGHT, SCREEN_WIDTH, CIRCLE_PADDING, yLength, xLength

        radius = min(SCREEN_WIDTH / xLength, SCREEN_HEIGHT / yLength) * CIRCLE_PADDING / 2
        row_height = SCREEN_HEIGHT / yLength
        col_width = SCREEN_WIDTH / xLength

        arcade.start_render()

        # y axis "inverted" cuz origin is in oposite side in screen and currState array
        for y in range(yLength):
            for x in range(xLength):
                if currState[y][x] == 3:
                    arcade.draw_circle_filled((x + 0.5) * col_width, -((y + 0.5) * row_height) + SCREEN_HEIGHT, radius, arcade.color.GREEN)
                elif currState[y][x] == 2:
                    arcade.draw_circle_filled((x + 0.5) * col_width, -((y + 0.5) * row_height) + SCREEN_HEIGHT, radius, arcade.color.YELLOW)
                elif currState[y][x] == 1:
                    arcade.draw_circle_filled((x + 0.5) * col_width, -((y + 0.5) * row_height) + SCREEN_HEIGHT, radius, arcade.color.RED)
        
        arcade.finish_render()
        
        if sleep_duration == None:
            time.sleep(0.6)
        else:
            time.sleep(sleep_duration)


    def draw_results(self, sleep_duration):
        self.draw(sleep_duration)

        for child in children:
            child.draw_results(sleep_duration)



class Projectile(object):
    # pos is [y,x]
    def __init__(self, direction, pos):
        global ballCount

        ballCount += 1
        self.id = ballCount
        
        self.direction = direction
        self.pos = pos.copy()
    
    def __str__(self):
        return "id: %d || pos: (%d, %d) || direction: %s" % (self.id, self.pos[1], self.pos[0], self.direction)

    def move(self):
        # pos update
        if(self.direction == "up"):
            self.pos[0] -= 1
        elif(self.direction == "down"):
            self.pos[0] += 1
        elif(self.direction == "right"):
            self.pos[1] += 1
        elif(self.direction == "left"):
            self.pos[1] -= 1


    def check_colision(self, state):
        if not ((self.pos[0] >= 0 and self.pos[0] < yLength) and (self.pos[1] >= 0 and self.pos[1] < xLength)):
            self.delete()
            return "deleted"

        # blowup
        newBalls = []
        if state[self.pos[0]] [self.pos[1]] > 0:
            state[self.pos[0]] [self.pos[1]] -= 1
            if not state[self.pos[0]] [self.pos[1]]:
                newBalls.append(Projectile("up", self.pos))
                newBalls.append(Projectile("down", self.pos))
                newBalls.append(Projectile("right", self.pos))
                newBalls.append(Projectile("left", self.pos))
                self.delete()
                return newBalls
            else:
                self.delete()
                return "deleted"
        
        return newBalls

        
    def delete(self):
        global balls

        balls.remove(self)
        del self
        

class Game(object):

    def __init__(self, filename):
        global xLength, yLength
        global SCREEN_WIDTH, SCREEN_HEIGHT

        self.filename = filename
        self.get_level()
        
        arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Bubble blast but better")
        arcade.set_background_color(arcade.color.WHITE)

        self.radius = min(SCREEN_WIDTH / xLength, SCREEN_HEIGHT / yLength) * CIRCLE_PADDING / 2
        self.row_height = SCREEN_HEIGHT / yLength
        self.col_width = SCREEN_WIDTH / xLength
    
    def get_level(self):
        global currState, nTries
        global xLength, yLength

        path = '../' + self.filename

        with open(path, 'r') as f:
            [xLength, yLength, nTries] = [int(el) for el in f.readline().split()]
            
            for line in f:
                currState.append([int(el) for el in line.split()])
    
    def draw_screen(self, sleep_duration, log):
        global currState, SCREEN_HEIGHT

        if log:
            print("**************")
            print(currState)

        arcade.start_render()

        # y axis "inverted" cuz origin is in oposite side in screen and currState array
        for y in range(yLength):
            for x in range(xLength):
                if currState[y][x] == 3:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.GREEN)
                elif currState[y][x] == 2:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.YELLOW)
                elif currState[y][x] == 1:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.RED)
        
        arcade.finish_render()
        
        if sleep_duration == None:
            if log:
                print("sleeping 0.6s")
            time.sleep(0.6)
        else:
            if log:
                print("sleeping " + str(sleep_duration) + "s")
            time.sleep(sleep_duration)

    def get_input(self):
        global xLength, yLength, nTries

        nTries -= 1
        return [random.randint(0,yLength-1), random.randint(0, xLength-1)]


    def move_balls(self, log):
        global balls
        for ball in balls:
            ball.move()
            if log:
                print(ball)


    def check_colisions(self, log):
        global balls
        newBalls = []

        i = 0
        while i < len(balls):
            auxballs = balls[i].check_colision(currState)
            if auxballs != "deleted":
                if (len(auxballs) > 0):
                    newBalls.extend(auxballs)
                    self.draw_screen(0.05, log)
                else:
                    i=i+1
        
        balls.extend(newBalls)

        if log:
            for ball in balls:
                print(ball)


    def play(self, log):
        global nTries, balls, currState

        self.draw_screen(1, log)

        balls.clear()

        while nTries > 0:
            click = self.get_input()

            print("click: (" + str(click[1]) + "," + str(click[0]) + ")")
            currState[click[0]][click[1]] = max(0, currState[click[0]][click[1]] - 1)
            self.draw_screen(0.7, log)

            if not currState[click[0]] [click[1]]:
                balls.append(Projectile("up", click))
                balls.append(Projectile("down", click))
                balls.append(Projectile("right", click))
                balls.append(Projectile("left", click))

                while len(balls) > 0:
                    self.move_balls(log)
                    self.check_colisions(log)
                    time.sleep(0.2)


def get_level(name):
    global nTries
    global xLength, yLength

    state = []

    path = '../' + name
    
    with open(path, 'r') as f:
        [xLength, yLength, nTries] = [int(el) for el in f.readline().split()]
            
        for line in f:
            state.append([int(el) for el in line.split()])

    return state
    

def main():
    global nTries, name

    game = Game(name)

    game.play(log=False)

    print("Game Ended - %d tries left" % nTries)

    state = get_level(name)
    root = Node(None, None, state, 0)

    arcade.run()
    

if __name__ == '__main__':
    main()
