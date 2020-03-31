import random
import time
import arcade
from copy import deepcopy


# Set constants for the screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CIRCLE_PADDING = 0.8  # 1 is touching lines and 0 no balls at all

# x and y axis size
xLength = 0
yLength = 0

# number of tries
nTries = 0

# projectiles count
ballCount = 0

# nodes count
nodeCount = 0

# algorithm used
algorithm = "A*"


# Node object, used to create the search tree
class Node(object):

    # Node object init
    def __init__(self, parent, click, state, currentCost):
        global nodeCount

        self.parent = parent
        self.children = []
        self.click = click
        self.operator = []
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


    # Calculates the estimated cost of a given line
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

        # There are bubbles that are not completely isolated, they might be hit by projectiles
        if cost < (len(bubbles1) + len(bubbles2)*2 + len(bubbles3)*3 + len(bubbles4)*4):
            only_isolated[0] = False

        return cost


    # Calculate the estimated cost (estimated moves necessary) from the node's state to the solution
    def calculate_estimated_cost(self):
        global yLength
        cost = 0
        only_isolated = [True]

        i = 0
        while i < yLength:
            cost = cost + self.line_estimated_cost(i, only_isolated)
            i = i + 1

        if not only_isolated[0]:
            cost = cost + 1     # At least one more move necessary to eliminate the non isolated bubbles
        
        self.estimatedCost = cost


    # Reset estimatedCost and totalCost
    def reset_costs(self):
        self.estimatedCost = None
        self.totalCost = None

    
    # Calculates next state after click
    def process_click(self):
        self.state[self.click[0]][self.click[1]] = max(0, self.state[self.click[0]][self.click[1]] - 1)

        # Bubble burst
        if not self.state[self.click[0]][self.click[1]]:
            self.operator = ["burst bubble", self.click[1], self.click[0]]
            self.balls.append(Projectile("up", self.click))
            self.balls.append(Projectile("down", self.click))
            self.balls.append(Projectile("right", self.click))
            self.balls.append(Projectile("left", self.click))

            while len(self.balls) > 0:
                move_balls(self.balls)
                check_collisions(self.balls, self.state)
        else:
            self.operator = ["attack bubble", self.click[1], self.click[0]]

        if algorithm == "A*":
            self.calculate_estimated_cost()
            self.totalCost = self.currentCost + self.estimatedCost
        elif algorithm == "Greedy number":
            self.totalCost = self.number_of_bubbles()
        elif algorithm == "Greedy lives":
            self.totalCost = self.number_of_lives()


    # Expands the node, getting all possible children, based on the node's state
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


    # Get best node to expand
    def get_best_node(self):
        best_node = None

        for child in self.children:
            if child.totalCost == None:
                current_node = child.get_best_node()
            else:
                current_node = child

            if current_node != None:
                if best_node == None:
                    best_node = current_node
                elif current_node.totalCost < best_node.totalCost:
                    best_node = current_node
                elif (current_node.totalCost == best_node.totalCost) & (current_node.estimatedCost < best_node.estimatedCost):
                    best_node = current_node

        return best_node


    # Get solution using A* algorithm
    def A_solution(self):
        global algorithm
        algorithm = "A*"
        solution_found = False
        operators = []

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
            operators.append(current_node.operator)
            current_node = current_node.parent

        operators.reverse()
        return operators


    # Objective Test - Check if node's state is empty
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


    # Expands all the nodes of the same level until it finds the solution
    def expand_level(self, nodes):
        tree_level = []

        for node in nodes:
            if node.empty():
                return node
            else:
                node.get_children()
                tree_level.extend(node.children)
        
        return self.expand_level(tree_level)

    
    # Get solution using breadth-first search
    def breadth_first_solution(self):
        global algorithm
        algorithm = "Breadth-first"
        current_node = self.expand_level([self])
        operators = []

        while current_node.id != 1:
            operators.append(current_node.operator)
            current_node = current_node.parent

        operators.reverse()
        return operators


    # Count number of bubbles left
    def number_of_bubbles(self):
        counter = 0
        
        i = 0
        while i < yLength:
            j = 0
            while j < xLength:
                if self.state[i][j]:
                    counter = counter + 1
                j = j + 1
            i = i + 1

        return counter


    # Count number of lives left
    def number_of_lives(self):
        counter = 0

        i = 0
        while i < yLength:
            j = 0
            while j < xLength:
                counter = counter + self.state[i][j]
                j = j + 1
            i = i + 1

        return counter


    # Get solution using greedy search
    def greedy_solution(self, heuristic):
        global algorithm, nTries
        algorithm = "Greedy " + heuristic
        solution_found = False
        operators = []

        self.get_children()
        best_node = None

        while not solution_found:
            best_node = self.get_best_node()
            if best_node.totalCost == 0:
                solution_found = True
            else:
                if best_node.currentCost < nTries:
                    best_node.get_children()
                best_node.reset_costs()

        current_node = best_node
        while current_node.id != 1:
            operators.append(current_node.operator)
            current_node = current_node.parent

        operators.reverse()
        return operators 



# Projectile object, which is sent when a bubble burst
class Projectile(object):

    # Projectile object init
    def __init__(self, direction, pos):
        global ballCount

        ballCount += 1
        self.id = ballCount
        
        self.direction = direction
        self.pos = pos.copy()


    # Update pos
    def move(self):
        if(self.direction == "up"):
            self.pos[0] -= 1
        elif(self.direction == "down"):
            self.pos[0] += 1
        elif(self.direction == "right"):
            self.pos[1] += 1
        elif(self.direction == "left"):
            self.pos[1] -= 1


    # Check collision between projectile and bubble
    def check_collision(self, balls, state):
        if not ((self.pos[0] >= 0 and self.pos[0] < yLength) and (self.pos[1] >= 0 and self.pos[1] < xLength)):
            self.delete(balls)
            return "deleted"

        newBalls = []
        if state[self.pos[0]] [self.pos[1]] > 0:
            state[self.pos[0]] [self.pos[1]] -= 1
            # Bubble burst
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


    # Delete projectile        
    def delete(self, balls):
        balls.remove(self)
        del self
        


# Game object, used to display the solution
class Game(object):

    # Game object init
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

    
    def draw_screen(self, sleep_duration):
        global SCREEN_HEIGHT

        arcade.start_render()

        # y axis "inverted" cuz origin is in oposite side in screen and self.state array
        for y in range(yLength):
            for x in range(xLength):
                if self.state[y][x] == 4:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.BLUE)
                elif self.state[y][x] == 3:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.YELLOW)
                elif self.state[y][x] == 2:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.GREEN)
                elif self.state[y][x] == 1:
                    arcade.draw_circle_filled((x + 0.5) * self.col_width, -((y + 0.5) * self.row_height) + SCREEN_HEIGHT, self.radius, arcade.color.RED)
        
        arcade.finish_render()
        
        if sleep_duration == None:
            time.sleep(0.6)
        else:
            time.sleep(sleep_duration)


    def play(self, operators):
        global nTries

        if nTries != 1 and nTries != 0:
                print(nTries, "tries left")
        elif nTries != 0:
            print("Last try")

        self.draw_screen(1.2)

        for operator in operators:
            nTries = nTries - 1
            click = [operator[2], operator[1]]
            print("click: (" + str(click[1]) + "," + str(click[0]) + ")")
            self.state[click[0]][click[1]] = max(0, self.state[click[0]][click[1]] - 1)
            self.draw_screen(0.7)

            if not self.state[click[0]][click[1]]:
                self.balls.append(Projectile("up", click))
                self.balls.append(Projectile("down", click))
                self.balls.append(Projectile("right", click))
                self.balls.append(Projectile("left", click))

                while len(self.balls) > 0:
                    move_balls(self.balls)
                    check_collisions(self.balls, self.state)
                    self.draw_screen(0.2)

            if nTries != 1 and nTries != 0:
                print(nTries, "tries left")
            elif nTries != 0:
                print("Last try")
            time.sleep(1.2)



def move_balls(balls):
        for ball in balls:
            ball.move()


def check_collisions(balls, state):
        newBalls = []

        i = 0
        while i < len(balls):
            auxballs = balls[i].check_collision(balls, state)
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
    for operator in solution:
        print("%s (%d, %d)" % (operator[0], operator[1], operator[2]))
    print("Time elapsed:", end-start, "seconds")


def main():
    global nTries, nodeCount

    print("\n\n")
    level = input("Introduce level file: ")

    state = get_level(level)

    root = Node(None, None, state, 0)

    print("\nCalculating solution using A* algorithm...")
    start = time.time()
    solution = root.A_solution()
    end = time.time()
    print_solution(solution, start, end)

    print("\nCalculating solution using breadth-first search...")
    nodeCount = 0
    root = Node(None, None, state, 0)
    start = time.time()
    solution2 = root.breadth_first_solution()
    end = time.time()
    print_solution(solution2, start, end)

    print("\nCalculating solution using greedy search with number of bubbles...")
    nodeCount = 0
    root = Node(None, None, state, 0)
    start = time.time()
    solution3 = root.greedy_solution("number")
    end = time.time()
    print_solution(solution3, start, end)

    print("\nCalculating solution using greedy search with total lives...")
    nodeCount = 0
    root = Node(None, None, state, 0)
    start = time.time()
    solution3 = root.greedy_solution("lives")
    end = time.time()
    print_solution(solution3, start, end)

    print("\n\nDisplaying A* algorithm solution...")
    game = Game(state)
    game.play(solution)
    print("Game Ended - %d tries left" % nTries)

    arcade.run()



if __name__ == '__main__':
    main()
