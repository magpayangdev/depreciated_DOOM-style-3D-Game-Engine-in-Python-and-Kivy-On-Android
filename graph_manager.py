"""
graph manager - creates a dict of tiles and their neighbors
"""

import math
from   settings    import *
from   collections import deque

from textures import *


class Graph:
	MAP_STRING=["777777777777777" +
				"7.............7" +
				"7.7.7777777.7.7" +
				"7.7.........7.7" +
				"7.777.....777.7" +
				"7.....222.....7" +
				"7..3.......3..7" +
				"7..33.....33..7" +
				"7.....555.....7" +
				"7.............7" +
				"4.447.....744.4" +
				"4.4...434...4.4" +
				"4.4.4.4.4.4.4.4" +
				"4.............4" +
				"444444444444444"][0]
					
	def __init__(self, game):
		self.graph = {}
		self.npc_locs = [(9, 8)]
		
		self.create_graph()
		
	def re_init():
		pass
		
	def update(self, dt):
		self.npc_locs.clear()
	
	def add_npc_location(self, in_loc):
		self.npc_locs.append(in_loc)

	def flip_vertically(self, idx):
		row = NUMBER_OF_BLOCKS_DOWN - 1 - (idx // NUMBER_OF_BLOCKS_DOWN)
		col = idx % NUMBER_OF_BLOCKS_ACROSS
		return col + row * NUMBER_OF_BLOCKS_ACROSS									
																
	def get_string(self, idx):
		return self.MAP_STRING[self.flip_vertically(idx)]
				
	def is_valid_position(self, Px, Py):	
		if self.get_string(int(Px) + int(Py) * NUMBER_OF_BLOCKS_ACROSS) is not ".":
			return False
		return True

	def get_adjacent_cells(self, x, y):
		valid_directions = [-1, 0], [0, -1], [1, 0], [0, 1] #[1,1], [1,-1], [-1,1], [-1,-1]
		return [(x + dx, y + dy) for dx, dy in valid_directions if self.is_valid_position(x + dx, y + dy)]
					
	def create_graph(self):	
		self.graph.clear()
		
		for i in range(TOTAL_NUMBER_OF_MAP_BLOCKS):
			x, y = i %  NUMBER_OF_BLOCKS_ACROSS, i // NUMBER_OF_BLOCKS_DOWN
			
			if self.is_valid_position(x, y):
				self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_adjacent_cells(x, y)

	def bfs(self, start, goal):	
		start   = tuple(int(i) for i in start)
		goal	= tuple(int(i) for i in goal)
		queue   = deque([start])
		visited = {start: None}	
				
		while queue:
			cur_node   = queue.popleft()
			next_nodes = self.graph[cur_node]
				
			for next_node in next_nodes:
				if next_node not in visited and next_node not in self.npc_locs:
					queue.append(next_node)
					visited[next_node] = cur_node
							
				if next_node == goal:
					break
									
		return visited
				
		
				
					
	