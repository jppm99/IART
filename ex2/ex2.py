
def main():
    puzzle = [1,2,3,4,5,6,7,8,0]
    
    howBadItIsRn = number_of_misplaced_pieces(puzzle) * avg_misplacing_distance(puzzle)


def number_of_misplaced_pieces(puzzle):
    n = 0

    for i in range(len(puzzle)):
        if puzzle[i] != i:
            n += 1

    return n

def avg_misplacing_distance(puzzle):
    n = 0

    for i in range(len(puzzle)):
        if puzzle[i] != i:
            n += distance(i, puzzle[i], len(puzzle))

    return n

def distance(n1, n2, side):
    c1 = n1 % side
    r1 = n1 / side

    c2 = n2 % side
    r2 = n2 / side

    return module(c2 - c1) + module(r2 - r1)

if __name__ == '__main__':
    main()
