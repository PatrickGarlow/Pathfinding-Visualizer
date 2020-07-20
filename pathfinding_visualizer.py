import pygame
import math
from queue import PriorityQueue
import queue
pygame.init()

WIDTH = 700
HEIGHT = 800

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

class Node:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    def get_pos(self):
        return self.row,self.col

    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUOISE
    def is_path(self):
        return self.color == PURPLE


    def reset(self):
        self.color = WHITE
    def make_closed(self):
        self.color = RED
    def make_open(self):
        self.color = GREEN
    def make_barrier(self):
        self.color = BLACK
    def make_start(self):
        self.color = ORANGE
    def make_end(self):
        self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE



    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        return False

def manhattan_distance(cube1pos,cube2pos):
    x1, y1 = cube1pos
    x2, y2 = cube2pos
    return abs(y2-y1) + abs(x2-x1)
def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
def a_star_algorithm(draw,grid,start_pos,end_pos):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start_pos))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start_pos] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start_pos] = manhattan_distance(start_pos.get_pos(),end_pos.get_pos())
    open_set_hash = {start_pos}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end_pos:
            reconstruct_path(came_from,end_pos,draw)
            end_pos.make_end()
            return True
        for neighbour in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + manhattan_distance(neighbour.get_pos(),end_pos.get_pos())
                if neighbour not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbour],count,neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()
        if current != start_pos:
            current.make_closed()
    return False
def dijkstra_algorithm(draw,grid,start_pos,end_pos):
    distance = {node: float(99999) for row in grid for node in row}
    distance[start_pos] = 0
    q = PriorityQueue()
    visited = []
    came_from  = {}
    q.put((distance[start_pos],start_pos))
    while not q.empty():
        node = q.get()[1]
        node.make_closed()
        if node == end_pos:
            reconstruct_path(came_from, end_pos, draw)
            end_pos.make_end()
            return True
        for neighbour in node.neighbors:
            if neighbour not in visited:
                visited.append(neighbour)
                q.put((distance[neighbour], neighbour))
                came_from[neighbour] = node
                neighbour.make_open()
                temp = distance[node] + 1
                if temp < distance[neighbour]:
                    distance[neighbour] = temp
        draw()

    return False

def bfs_algorithm(draw,grid,start_pos,end_pos):
    visited = []  # List to keep track of visited nodes.
    queue = []  # Initialize a queue
    visited.append(start_pos)
    queue.append(start_pos)
    came_from = {}

    while queue:
        current = queue.pop(0)
        current.make_closed()
        if current == end_pos:
            reconstruct_path(came_from,end_pos,draw)
            end_pos.make_end()
            return True

        for neighbour in current.neighbors:

            if neighbour not in visited:
                came_from[neighbour] = current
                visited.append(neighbour)
                neighbour.make_open()
                queue.append(neighbour)
        draw()
        if current != start_pos:
            current.make_closed()
    return False
dfs_visited = []
def dfs_algorithm(draw,current,end_pos):
    if current == end_pos:
        #reconstruct_path(came_from, end_pos, draw)
        end_pos.make_end()
        return True
    if current not in dfs_visited:
        dfs_visited.append(current)
        for neighbour in current.neighbors:
            neighbour.make_open()
            dfs_algorithm(draw,neighbour,end_pos)
            draw()
    return False

def create_grid(rows_num,col_num,width):
    grid = []
    gap = width // rows_num
    for x in range(rows_num):
        grid.append([])
        for y in range(col_num):
            node = Node(x,y,gap,rows_num)
            grid[x].append(node)
    return grid

def draw_grid(win,rows,cols,width):
    GAP = width // rows
    for x in range(rows+1):
        pygame.draw.line(win,GREY,(0,x*GAP),(width,x*GAP))
        for y in range(cols):
            pygame.draw.line(win, GREY, (y * GAP, 0), (y * GAP, width))

def draw(win,grid,rows,cols,width):
    win.fill(WHITE)
    textFont = pygame.font.SysFont("Arial", 14)
    titleFont = pygame.font.SysFont("Arial", 20)

    d_label = titleFont.render("Dijkstra's", 1, BLACK)
    d_instructions = textFont.render("Press D", 1, BLACK)
    b_label = titleFont.render("Breadth First Search", 1, BLACK)
    b_instructions = textFont.render("Press B", 1, BLACK)
    a_label = titleFont.render("A Star", 1, BLACK)
    a_instructions = textFont.render("Press A", 1, BLACK)
    r_label = titleFont.render("To Reset the Grid", 1, BLACK)
    r_instructions = textFont.render("Press R", 1, BLACK)
    instructions1 = textFont.render("The first two right clicks will be for start (Orange) and end (Turquoise).", 1, BLACK)
    instructions2 = textFont.render("After they are placed left click to add a wall, right click to erase.", 1, BLACK)

    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win,rows,cols,width)
    win.blit(d_label,(10,710))
    win.blit(d_instructions, (10, 735))
    win.blit(b_label, (140, 710))
    win.blit(b_instructions, (140, 735))
    win.blit(a_label, (370, 710))
    win.blit(a_instructions, (370, 735))
    win.blit(r_label, (500, 710))
    win.blit(r_instructions, (500, 735))
    win.blit(instructions1, (10, 755))
    win.blit(instructions2, (10, 775))


    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row,col

def main(win,width):
    ROWS = 50
    COLS = 50
    grid = create_grid(ROWS,COLS,width)
    start_pos = None
    end_pos = None
    run = True

    while run:
        draw(win,grid,ROWS,COLS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: #gets the left click
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]
                if not start_pos and node != end_pos:
                    start_pos = node
                    start_pos.make_start()
                elif not end_pos and node != start_pos:
                    end_pos = node
                    end_pos.make_end()
                elif node != end_pos and node != start_pos:
                    node.make_barrier();

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start_pos:
                    start_pos = None
                elif node == end_pos:
                    end_pos = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start_pos and end_pos:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star_algorithm(lambda:draw(win,grid,ROWS,COLS,width),grid,start_pos,end_pos)
                if event.key == pygame.K_d and start_pos and end_pos:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    dijkstra_algorithm(lambda:draw(win,grid,ROWS,COLS,width),grid,start_pos,end_pos)
                if event.key == pygame.K_b and start_pos and end_pos:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    bfs_algorithm(lambda:draw(win,grid,ROWS,COLS,width),grid,start_pos,end_pos)
                if event.key == pygame.K_r:
                    for row in grid:
                        for node in row:
                            node.reset()
                    start_pos = None
                    end_pos = None
    pygame.quit()

main(WIN,WIDTH)