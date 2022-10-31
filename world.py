"""
WorldRenderer
"""
from   kivy.graphics.context_instructions import Color
from   kivy.graphics.vertex_instructions  import Rectangle
from   kivy.graphics.instructions		 import InstructionGroup
from   kivy.core.image 				   import Image

from   settings                           import *  	# constant values
#import settings                           as     game   # dynamic values
from   textures						   import *
import player                             as     player

import math

class World:	
	def __init__(self, game):
		self.game = game
				
		with self.game.canvas:
			self.flr_colour = Color()
			self.flr_rect   = Rectangle()
			self.sky_colour = Color()
			self.sky_rect   = Rectangle()
			
			self.scr_rect_cols = [(Color(1,1,1,1), Rectangle()) for _ in range(NUMBER_OF_RAYS)]
								
	def re_init(self):		
		self.flr_rect.size    = scr_width(), scr_height() / 2
		self.sky_rect.size    = scr_width(), scr_height() / 2
		
		self.flr_rect.pos 	= self.game.pos
		self.sky_rect.pos 	= 0, scr_height() / 2
		
		self.sky_texture 	 = get_sky_texture()
		self.sky_rect.texture = self.sky_texture
		
		self.flr_colour.rgb   = WORLD_FLOOR_COLOUR
		self.flr_rect.texture = flr_texture()
				
	def update(self, idx, distance, P_x, P_y, angle, texture_idx, horizontal_scan=True):
		width, height = scr_rect_w(), 	  scr_distance() / distance
		Px,    Py     = idx * scr_rect_w(), half_scr_h()   - height / 2
		wall_texture  = get_wall_texture(texture_idx)

		# _ _ _ _ _ 
		#| #C#C#C  |
		#|#B     #A|
		#|#B     #A|
		#|#B     #A|
		#|_#D#D#D _|
		############

		if horizontal_scan:
			if math.cos(angle) >= 0:
				offset = 1 - (P_y % 1)
				c = 100_000 / (100_000 + 2 * distance ** 5) #A6				
			else:
				offset = (P_y % 1)
				c = 100_000 / (100_000 + 2 * distance ** 5) #B8			
		else:
			if math.sin(angle) >= 0:
				offset = (P_x % 1)
				c = 100_000 / (100_000 + 2 * distance ** 5) #C4
			else:
				offset = 1 - (P_x % 1)
				c = 100_000 / (100_000 + 2 * distance ** 5) #D10
				
		colour        	= self.scr_rect_cols[idx][0]
		rectangle    	 = self.scr_rect_cols[idx][1]
							
		colour.rgb        = c, c, c	
		rectangle.size    = width, height
		rectangle.pos     = Px, Py
		rectangle.texture = wall_texture.get_region((wall_texture.width - width) * offset , 0, width, wall_texture.height)
		
	def update_sky(self, dt):
		yaw = self.game.player.yaw
		
		if yaw == 0:
			return
			
		self.sky_texture.uvpos = (self.sky_texture.uvpos[0] + 1 * dt * yaw) % self.sky_texture.width, self.sky_texture.uvpos[1]
		self.sky_rect.texture  = self.sky_texture
											