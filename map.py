"""
map
"""

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions  import Rectangle
from kivy.graphics.vertex_instructions  import Point
from kivy.graphics.vertex_instructions  import Line

import math
from   settings    import *     # constant values
from   collections import deque

from textures import *
import sprite
												
class MiniMap:
	def __init__(self, game):
		self.is_visible 			 = False
		self.game 				   = game
		self.offset_x, self.offset_y = 0.0, 0.0
		self.map_element 			= []

		with self.game.canvas:			
			self.bg_colour 	= Color()		
			self.bg_rectangle  = Rectangle()
			
			for i in range(TOTAL_NUMBER_OF_MAP_BLOCKS):
				self.map_element.append((Color(), Rectangle()))

			self.game.player.mmp_colour  = Color(1,1,1)
			self.game.player.mmp_rect	= Rectangle()
			self.game.player.mmp_line	= Line(width=2)
			self.game.player.in_mmp_cnvs = True
			
			self.is_visible = True
																
	def re_init(self):			
		# sets map position and textures
		self.draw_map(b_init=True)
		self.update_character_positions()

		# what ever it is, just clear the map
		if self.is_visible:
			self.set_map_to_invisible()
		else:
			for entry in self.game.sprite_space.all_sprites:
				self.remove_from_mmp_cnvs(entry)			

	def update(self):
		if self.is_visible:
			self.draw_map(b_init=False)							# redraw map on first ray
			self.update_character_positions()
		
	def show_map(self):
		if self.is_visible:
			self.is_visible = False			
			self.set_map_to_invisible()
			self.game.gm.unpause_game()
	
		else:
			self.is_visible = True			
			self.set_map_to_visible()
			self.game.gm.pause_game()
			
	def set_map_to_visible(self):
		self.game.canvas.add(self.bg_colour)
		self.game.canvas.add(self.bg_rectangle)

		for idx, entry in enumerate(self.map_element):
			for inst in entry:
				self.game.canvas.add(inst)
				
		for entry in self.game.sprite_space.all_sprites:
			self.add_to_mmp_cnvs(entry)
			
		self.game.canvas.add(self.game.player.mmp_colour)
		self.game.canvas.add(self.game.player.mmp_rect)
		self.game.canvas.add(self.game.player.mmp_line)
		
		self.update()
		
		self.is_visible = True
	
	def set_map_to_invisible(self):		
		self.game.canvas.remove(self.bg_colour)
		self.game.canvas.remove(self.bg_rectangle)

		for entry in self.map_element:
			for inst in entry:
				self.game.canvas.remove(inst)
				
		for entry in self.game.sprite_space.all_sprites:
			self.remove_from_mmp_cnvs(entry)
				
		self.game.canvas.remove(self.game.player.mmp_colour)
		self.game.canvas.remove(self.game.player.mmp_rect)
		self.game.canvas.remove(self.game.player.mmp_line)
		
		self.is_visible = False

	def add_to_mmp_cnvs(self, sprt):
		if self.is_visible and not sprt.in_mmp_cnvs:
			sprt.in_mmp_cnvs = True
			self.game.canvas.add(sprt.mmp_colour)
			self.game.canvas.add(sprt.mmp_rect)
			self.game.canvas.add(sprt.mmp_line) 
		
	def remove_from_mmp_cnvs(self, sprt):
		if sprt.in_mmp_cnvs:
			sprt.in_mmp_cnvs = False
			self.game.canvas.remove(sprt.mmp_colour)
			self.game.canvas.remove(sprt.mmp_rect)
			self.game.canvas.remove(sprt.mmp_line)
							
	def draw_map(self, b_init=False):
		if b_init:
			self.game.player.mmp_rect.size = (c_block_size(), c_block_size())
			self.game.player.mmp_rect.texture = get_map_texture('rockman')
				
			self.bg_colour.rgb     = MAP_BACKGROUND_COLOUR
			self.bg_rectangle.size = map_size()
			self.bg_rectangle.pos  = self.offset_x, self.offset_y   = map_centre_o()
			
			for idx, rect in enumerate(self.map_element):
				wall = self.game.graph_mngr.get_string(idx)
						          
				if wall in '1234567890' : 
					rect[1].texture=get_map_texture('brick_wall')
					
				elif wall == ".": 
					rect[0].rgb = MAP_FLOOR_COLOUR
					
				else: 
					rect[0].rgb = MAP_INVALID_COLOUR
				
				Px = idx % NUMBER_OF_BLOCKS_ACROSS * g_block_size()[0]
				Py = idx // NUMBER_OF_BLOCKS_DOWN  * g_block_size()[1]	
				rect[1].size = n_block_size()
				rect[1].pos  = Px + self.offset_x, Py + self.offset_y + 1					
		else:
			for idx, rect in enumerate(self.map_element):
				wall = self.game.graph_mngr.get_string(idx)	
				if wall == ".": 
					rect[0].rgb = MAP_FLOOR_COLOUR
		
	def update_character_positions(self):
		b_x, b_y = g_block_size()
		
		Ax = self.game.player.pos_x * b_x + self.offset_x
		Ay = self.game.player.pos_y * b_y + self.offset_y
		self.game.player.mmp_rect.pos = Ax - hc_block_size(), Ay - hc_block_size()
		
		for idx, entry in enumerate(self.game.sprite_space.all_sprites):
			if True or entry.in_sprt_cnvs:
				if not entry.in_mmp_cnvs:
					self.add_to_mmp_cnvs(entry)
					
				Bx = entry.pos_x * b_x + self.offset_x
				By = entry.pos_y * b_y + self.offset_y

				entry.mmp_rect.pos = Bx - hc_block_size(), By - hc_block_size()
			
				if SPRITE_DEBUG:
					if entry.sees_target:					
						entry.mmp_line.points = Ax, Ay, Bx, By
					else:
						entry.mmp_line.points = Ax, Ay, Bx, By					
		
				if isinstance(entry, sprite.NPC) and entry.path:
					for path in entry.path:
						idx = path[0] + path[1] * NUMBER_OF_BLOCKS_ACROSS
						self.map_element[idx][0].rgb = entry.path_colour
						
			else:
				self.remove_from_mmp_cnvs(entry)
					

				
					
	