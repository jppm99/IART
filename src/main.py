import random
import time
import arcade


# Set constants for the screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CIRCLE_PADDING = 0.8  # 1 is touching lines and 0 no balls at all

# name of the file to be processed
name = 'level.txt'

# 2d matrix with 0,0 at top left
currState = []

# x and y axis size
xLength = 0
yLength = 0

# number of tries
nTries = 0

# list of projectiles
balls = []


class Projectile(object):
    # pos is [y,x]
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos

    def move(self):
        global currState, balls

        # pos update
        if(self.direction == "up"):
            self.pos[0] -= 1
        elif(self.direction == "down"):
            self.pos[0] += 1
        elif(self.direction == "right"):
            self.pos[1] += 1
        elif(self.direction == "left"):
            self.pos[1] -= 1

        if not (self.pos[0] in range(yLength) and self.pos[1] in range(xLength)):
            self.delete()
            return

        # blowup
        if currState[self.pos[0]] [self.pos[1]] > 0:
            currState[self.pos[0]] [self.pos[1]] -= 1
            if not currState[self.pos[0]] [self.pos[1]]:
                balls.append(Projectile("up", self.pos))
                balls.append(Projectile("down", self.pos))
                balls.append(Projectile("right", self.pos))
                balls.append(Projectile("left", self.pos))
            self.delete()
        
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
    
    def draw_screen(self):
        global currState, SCREEN_HEIGHT

        arcade.start_render()

        for y in range(yLength):
            for x in range(xLength):
                if currState[y][x] == 3:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.GREEN)
                elif currState[y][x] == 2:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.YELLOW)
                elif currState[y][x] == 1:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.RED)
        
        arcade.finish_render()
        time.sleep(0.5)
        

    def get_input(self):
        global xLength, yLength, nTries

        if nTries > 0:
            nTries -= 1
            return [random.randint(0,yLength-1), random.randint(0, xLength-1)]
        else:
            return "skip"

    def play(self):
        global nTries, balls, currState

        print("Initial board")
        print(currState)
        self.draw_screen()

        while nTries > 0 or len(balls) > 0:

            click = self.get_input()

            if click != "skip":
                print("click: (" + str(click[1]) + "," + str(click[0]) + ")")
                currState[click[0]][click[1]] = max(0, currState[click[0]][click[1]] - 1)
                balls.append(Projectile("up", click))
                balls.append(Projectile("down", click))
                balls.append(Projectile("right", click))
                balls.append(Projectile("left", click))
            
            self.draw_screen()
            print("***********")
            print(currState)
            
            for ball in balls:
                ball.move()

            print("***********")
            print(currState)
            self.draw_screen()



def main():
    game = Game(name)

    game.play()
    arcade.run()

    print("Game Ended")


if __name__ == '__main__':
    main()
