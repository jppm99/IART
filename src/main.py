import random
import time
import arcade
from copy import deepcopy


# Set constants for the screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CIRCLE_PADDING = 0.8  # 1 is touching lines and 0 no balls at all

# name of the file to be processed
name = 'level.txt'

# x and y axis size
xLength = 0
yLength = 0

# number of tries
nTries = 0

# projectiles count
ballCount = 0

# nodes count
nodeCount = 0


# Node object, used to create the search tree
class Node(object):

    # Node object init
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
        if self.id == 1:    # root
            self.reset_costs()
        else:
            self.estimatedCost = 0
            self.totalCost = 0


    # Calculates and returns the number of hits absolutely necessary to eliminate a given bubble
    def bubble_cost(self, bubble, remaining_health):
        global yLength

        # Check if there are bubbles on the same column as the given bubble, if there are, it might not be absolutely necessary to hit the bubble
        i = 0
        while i < yLength:
            if i != bubble[0]:
                if self.state[i][bubble[1]]:
                    remaining_health = remaining_health - 1
                    if remaining_health < 1:
                        break
            i = i + 1
        
        return remaining_health


    # Calculates the cost of a given group of bubbles
    def isolation_cost(self, bubbles, remaining_health):
        if remaining_health < 1:
            return 0
        
        cost = 0
        for bubble in bubbles:
            cost = cost + self.bubble_cost(bubble, remaining_health)

        return cost


    def line_estimated_cost(self, y, only_isolated):
        global xLength

        bubbles1 = []
        bubbles2 = []
        bubbles3 = []
        bubbles4 = []
        cost = 0

        i = 0
        while i < xLength:
            bubble = self.state[y][i]
            if (bubble == 1):
                bubbles1.append([y,i])
            elif (bubble == 2):
                bubbles2.append([y,i])
            elif (bubble == 3):
                bubbles3.append([y,i])
            elif (bubble == 4):
                bubbles4.append([y,i])
            i = i + 1

        total_bubbles = len(bubbles1) + len(bubbles2) + len(bubbles3) + len(bubbles4)
        cost = cost + self.isolation_cost(bubbles1, 2-total_bubbles)
        cost = cost + self.isolation_cost(bubbles2, 3-total_bubbles)
        cost = cost + self.isolation_cost(bubbles3, 4-total_bubbles)
        cost = cost + self.isolation_cost(bubbles4, 5-total_bubbles)

        if cost < (len(bubbles1) + len(bubbles2)*2 + len(bubbles3)*3 + len(bubbles4)*4):
            only_isolated[0] = False

        return cost


    def calculate_estimated_cost(self):
        global yLength
        cost = 0
        only_isolated = [True]

        i = 0
        while i < yLength:
            cost = cost + self.line_estimated_cost(i, only_isolated)
            i = i + 1

        if not only_isolated[0]:
            cost = cost + 1
        
        self.estimatedCost = cost


    def reset_costs(self):
        self.estimatedCost = None
        self.totalCost = None

    
    def process_click(self):
        self.state[self.click[0]][self.click[1]] = max(0, self.state[self.click[0]][self.click[1]] - 1)

        if not self.state[self.click[0]][self.click[1]]:
            self.balls.append(Projectile("up", self.click))
            self.balls.append(Projectile("down", self.click))
            self.balls.append(Projectile("right", self.click))
            self.balls.append(Projectile("left", self.click))

            while len(self.balls) > 0:
                move_balls(self.balls)
                check_colisions(self.balls, self.state)

        self.calculate_estimated_cost()
        self.totalCost = self.currentCost + self.estimatedCost


    def get_children(self):
        global xLength, yLength

        i = 0
        while i < yLength:
            j = 0
            while j < xLength:
                if self.state[i][j] != 0:
                    new_state = deepcopy(self.state)
                    child = Node(self, [i,j], new_state, self.currentCost+1)
                    child.process_click()
                    self.children.append(child)
                j = j + 1
            i = i + 1


    def get_best_node(self):
        best_node = None

        for child in self.children:
            if child.totalCost == None:
                current_node = child.get_best_node()
            else:
                current_node = child

            if best_node == None:
                best_node = current_node
            elif current_node.totalCost < best_node.totalCost:
                best_node = current_node
            elif (current_node.totalCost == best_node.totalCost) & (current_node.estimatedCost < best_node.estimatedCost):
                best_node = current_node

        return best_node


    def get_solution(self):
        solution_found = False
        clicks = []

        self.get_children()
        best_node = None

        while not solution_found:
            best_node = self.get_best_node()
            if best_node.estimatedCost == 0:
                solution_found = True
            else:
                best_node.get_children()
                best_node.reset_costs()

        current_node = best_node
        while current_node.id != 1:
            clicks.append(current_node.click)
            current_node = current_node.parent

        clicks.reverse()
        return clicks


    def empty(self):
        i = 0
        while i < yLength:
            j = 0
            while j < xLength:
                if self.state[i][j]:
                    return False
                j = j + 1
            i = i + 1

        return True


    def expand(self, nodes):
        tree_level = []

        for node in nodes:
            if node.empty():
                return node
            else:
                node.get_children()
                tree_level.extend(node.children)
        
        return self.expand(tree_level)

    
    def brute_force_solution(self):
        current_node = self.expand([self])
        clicks = []

        while current_node.id != 1:
            clicks.append(current_node.click)
            current_node = current_node.parent

        clicks.reverse()
        return clicks



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


    def check_colision(self, balls, state):
        if not ((self.pos[0] >= 0 and self.pos[0] < yLength) and (self.pos[1] >= 0 and self.pos[1] < xLength)):
            self.delete(balls)
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
                self.delete(balls)
                return newBalls
            else:
                self.delete(balls)
                return "deleted"
        
        return newBalls

        
    def delete(self, balls):
        balls.remove(self)
        del self
        


class Game(object):

    def __init__(self, state):
        global xLength, yLength
        global SCREEN_WIDTH, SCREEN_HEIGHT

        self.state = state
        self.balls = []
        
        arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Bubble blast but better")
        arcade.set_background_color(arcade.color.WHITE)

        self.radius = min(SCREEN_WIDTH / xLength, SCREEN_HEIGHT / yLength) * CIRCLE_PADDING / 2
        self.row_height = SCREEN_HEIGHT / yLength
        self.col_width = SCREEN_WIDTH / xLength

    
    def draw_screen(self, sleep_duration, log):
        global SCREEN_HEIGHT

        if log:
            print("**************")
            print(self.state)

        arcade.start_render()

        # y axis "inverted" cuz origin is in oposite side in screen and self.state array
        for y in range(yLength):
            for x in range(xLength):
                if self.state[y][x] == 4:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.BLUE)
                elif self.state[y][x] == 3:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.GREEN)
                elif self.state[y][x] == 2:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.YELLOW)
                elif self.state[y][x] == 1:
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


    def play(self, clicks, log):
        global nTries

        self.draw_screen(1, log)

        for click in clicks:
            nTries = nTries - 1
            print("click: (" + str(click[1]) + "," + str(click[0]) + ")")
            self.state[click[0]][click[1]] = max(0, self.state[click[0]][click[1]] - 1)
            self.draw_screen(0.7, log)

            if not self.state[click[0]][click[1]]:
                self.balls.append(Projectile("up", click))
                self.balls.append(Projectile("down", click))
                self.balls.append(Projectile("right", click))
                self.balls.append(Projectile("left", click))

                while len(self.balls) > 0:
                    move_balls(self.balls)
                    check_colisions(self.balls, self.state)
                    self.draw_screen(0.2, log)
            time.sleep(1.2)



def move_balls(balls):
        for ball in balls:
            ball.move()


def check_colisions(balls, state):
        newBalls = []

        i = 0
        while i < len(balls):
            auxballs = balls[i].check_colision(balls, state)
            if auxballs != "deleted":
                if (len(auxballs) > 0):
                    newBalls.extend(auxballs)
                else:
                    i=i+1
        
        balls.extend(newBalls)



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
    


def print_solution(solution, start, end):
    print("Solution:")
    for click in solution:
        print("(%d, %d)" % (click[1], click[0]))
    print("Time elapsed:", end-start, "\n")


def main():
    global nTries, name

    state = get_level(name)

    root = Node(None, None, state, 0)

    print("\n\n")
    print("Calculating solution using A* algorithm...")
    start = time.time()
    solution = root.get_solution()
    end = time.time()
    print_solution(solution, start, end)

    print("Calculating solution using brute-force algorithm...")
    start = time.time()
    solution2 = root.brute_force_solution()
    end = time.time()
    print_solution(solution2, start, end)

    print("Displaying A* algorithm solution...")
    game = Game(state)
    game.play(solution, log=False)
    print("Game Ended - %d tries left" % nTries)

    arcade.run()



if __name__ == '__main__':
    main()
