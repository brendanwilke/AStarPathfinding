import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH)) # width x2 because it will be a square
pygame.display.set_caption("A* Pathfinding")

# Assign color values
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Node is a single square on the graph
class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE # all white cubes to start
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	# Return x, y position
	def get_pos(self):
		return self.row, self.col 

	# Barriers do not allow for traversal
	def is_barrier(self):
		return self.color == BLACK

	def reset(self):
		self.color == WHITE

	# All make methods actually change the colors of the nodes
	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	# Method to draw the nodes on the screen
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	# Checks to see which adjacent nodes are traversable and which are barriers
	def update_neighbors(self, grid):
		self.neighbors = []

		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # down
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # up
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # right
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # left
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

# Finds total distance in nodes between 2 points
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# Draws path from start node to end node once a path has been found
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

# Finds the shortest path from start node to end node using A* pathfinding
def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue() # priority queue is similar to regular queue but certain elements have priority over others
	open_set.put((0, count, start)) # add the starting node to the set
	came_from = {} # keeps track if which node another node came from
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = h(start.get_pos(), end.get_pos()) # distance from start to end node

	open_set_hash = {start} # keeps track of items in priority queue

	while not open_set.empty(): # if open_set is empty, all paths have been exhausted
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] 
		open_set_hash.remove(current)

		if current == end: # the end node has been found
			reconstruct_path(came_from, end, draw) # form the shortest path
			start.make_start()
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1 # g score of neighbors is 1 more than current node

			if temp_g_score < g_score[neighbor]: # if a better path has been found
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

# Stores the nodes into a list of lists
def make_grid(rows, width):
	grid = []
	gap = width // rows # gives width of a cube
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid

# Draws the grid lines
def draw_grid(win, rows, width):
	gap = width // rows
	# draw horizontal lines
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		# draw vertical lines
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	win.fill(WHITE) # fills the window with white every frame

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width) # grid lines drawn here
	pygame.display.update()

# Returns the position of a mouse click
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap
	return row, col

def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # user clicks the x button at the top right corner
				run = False

			# if LMB has been pressed
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				if not start and node != end:
					start = node
					start.make_start()

				elif not end and node != start:
					end = node
					end.make_end()

				elif node != end and node != start:
					node.make_barrier()

			# if RMB has been pressed
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)	

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)