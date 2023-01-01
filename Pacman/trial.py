from math import sqrt
class TrialGrid():
    def __init__(self, map):
        self.grid = []
        self.paused = False
        x, y = self.create_grid(map)

        self.nodes_group = TrialNodeGroup()

        self.nodes_group.create_nodes(self.grid, x, y)
        self.nodes_group.connect_nodes_row_wise(x, y, self.grid)
        self.nodes_group.connect_nodes_col_wise(x, y, self.grid)
        self.ghost = TrialGhost((1,2), 13, 14)
        self.grid[13][14] = '@'
        self.display_grid()
        x, y = self.ghost.next_direction(self.nodes_group, self.ghost.target)
        self.grid[x][y] = '@'
    
    def create_grid(self, map):
        file = open(map)
        temp_grid = file.read().split('\n')
        for row in temp_grid:
            row = row.split()
            self.grid.append(row)
        file.close()

        return (len(self.grid), len(row))

    def check(self):
        for row in self.grid:
            for col in row:
                if type(col) is TrialNode:
                    # print(col.neighbours, col.position)
                    pass

    def display_grid(self):
        for row in self.grid:
            print(','.join(row))

class TrialNode():
    def __init__(self, x, y):
        self.position = x, y
        self.neighbours = {"UP": None, "DOWN": None, "LEFT": None, "RIGHT": None}
        pass

class TrialNodeGroup():
    def __init__(self):
        self.nodes = {}
        pass

    def create_nodes(self, grid, x, y):
        for row in range(x):
            for col in range(y):

                if grid[row][col] in "+nP":
                    node = TrialNode(row, col)
                    self.nodes[(row,col)] = node

    def connect_nodes_row_wise(self, x, y, grid):
        for row in range(x):
            previous_node = None

            for col in range(y):

                if grid[row][col] == 'X':
                    previous_node = None
                    
                elif (row, col) in self.nodes:
 
                    if previous_node is not None:
                        current_node = self.nodes[(row,col)]
                        current_node.neighbours["LEFT"] = previous_node
                        previous_node.neighbours["RIGHT"] = current_node

                    previous_node = self.nodes[(row,col)]

                    if col == 0:
                        self.nodes[(row, col)].neighbours["LEFT"] = self.nodes[(row, 27)]
                        self.nodes[(row, 27)].neighbours["RIGHT"] = self.nodes[(row, col)]

    def connect_nodes_col_wise(self, x, y, grid):
        for col in range(y):
            previous_node = None

            for row in range(x):

                if grid[row][col] == 'X':
                    previous_node = None

                elif (row, col) in self.nodes:

                    if previous_node is not None:
                        current_node = self.nodes[(row,col)]
                        current_node.neighbours["UP"] = previous_node
                        previous_node.neighbours["DOWN"] = current_node

                    previous_node = self.nodes[(row,col)]

class TrialGhost():
    def __init__(self, target, row, col):
        self.target = target
        # self.state = self.scatter(self.target)

        self.position = row, col
        self.row_pixel = self.position[0]*16
        self.col_pixel = self.position[1]*16

        self.directions = {"UP": -1, "LEFT": -2, "DOWN": 1, "RIGHT": 2}
        self.direction = self.directions["LEFT"]

    def scatter(self, target):
        self.time = 7
        pass

    def calculate_available_directions(self, direction, nodes_group):
        available_directions = []

        if self.position in nodes_group.nodes:
            neighbours = nodes_group.nodes[self.position].neighbours

            for neighbour in neighbours:
                if (neighbours[neighbour] is not None) and (self.directions[neighbour] != direction*-1):
                    available_directions.append(self.directions[neighbour])

        else: available_directions.append(direction)

        return list(set(available_directions))

    def calculate_target_distance(self, position, direction, target):
        x1, y1 = position
        if direction == -1:
            x1 -= 1
        elif direction == -2:
            y1 -= 1
        elif direction == 1:
            x1 += 1
        elif direction == 2:
            y1 += 1

        x2, y2 = target

        return sqrt((x1-x2)**2 + (y1-y2)**2)

    def next_direction(self, nodes_group, target):

        available_directions = self.calculate_available_directions(self.direction, nodes_group)

        distance = self.calculate_target_distance(self.position, available_directions[0], self.target)
        self.direction = available_directions[0]
        for direction in available_directions:
            temp_distance = self.calculate_target_distance(self.position, direction, self.target)
            if temp_distance < distance:
                distance = temp_distance
                self.direction = self.directions[direction]

        self.position = self.get_position(self.direction, self.position)
        print(self.direction)
        return self.position
    
    def get_position(self, direction, position):
        x, y = position
        if direction == -1:
            x -= 1
        elif direction == -2:
            y -= 1
        elif direction == 1:
            x += 1
        elif direction == 2:
            y += 1

        return x, y
b = TrialGrid("map.txt")
b.check()
print()
b.display_grid()