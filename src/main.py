import random

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
    
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos

    def move(self):
        global currState

        # pos update
        if(self.direction == "up"):
            self.pos[1] -= 1
        elif(self.direction == "down"):
            self.pos[1] += 1
        elif(self.direction == "right"):
            self.pos[0] += 1
        elif(self.direction == "left"):
            self.pos[0] -= 1

        if not (self.pos[0] in range(xLength) and self.pos[1] in range(yLength)):
            self.delete()
            return

        # blowup
        if currState[self.pos[0]] [self.pos[1]] != 0:
            currState[self.pos[0]] [self.pos[1]] -= 1
            self.delete()
        
    def delete(self):
        balls.remove(self)
        del self
        

class Game(object):

    def __init__(self, filename):
        self.filename = filename
        self.get_level()

    def get_level(self):
        global currState, nTries
        global xLength, yLength

        path = '../' + self.filename

        with open(path, 'r') as f:
            [xLength, yLength, nTries] = [int(el) for el in f.readline().split()]
            
            for line in f:
                currState.append([int(el) for el in line.split()])
            
            print("Initial board")
            print(currState)
    
    def get_input(self):
        global xLength, yLength, nTries

        if nTries > 0:
            nTries -= 1
            return [random.randint(0,xLength-1), random.randint(0, yLength-1)]
        else:
            return "skip"

    def play(self):
        global nTries, balls, currState

        while nTries > 0 or len(balls) > 0:

            click = self.get_input()

            if click != "skip":
                currState[click[0]][click[1]] = max(0, currState[click[0]][click[1]] - 1)
                balls.append(Projectile("up", click))
                balls.append(Projectile("down", click))
                balls.append(Projectile("right", click))
                balls.append(Projectile("left", click))
            
            for ball in balls:
                ball.move()

            print("***********")
            print(currState)



def main():
    game = Game(name)

    game.play()


if __name__ == '__main__':
    main()
