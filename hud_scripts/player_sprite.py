""" player sprite. no relation to sprite.py """
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions  import Rectangle
from kivy.core.image 				   import Image

from settings 						  import *  		 # constant values
from textures						   import *
from collections 					   import deque
import os

class PlayerSprite:
	def __init__(self, game, path=PLAYER_SPRITE_PATH, colour=(1,1,1,1)):
		self.game 			 = game
		self.game_mode		 = self.game.gm
		self.pos_x, self.pos_y = 0,0
		self.accum_time 	   = 0.0
		self.animate_fire 	 = False
		self.do_once		   = True
		
		self.texture_gen = (image for image in get_image_sequence('player'))
									
		with self.game.canvas:
			self.sprt_colour = Color(colour)
			self.sprt_rect = Rectangle(texture = next(self.texture_gen))
		
	def re_init(self):
		self.pos_x, self.pos_y = scr_width() / 2, 0
		self.sprt_rect.size = controller_size()
		self.sprt_rect.pos = (self.pos_x - controller_size()[0] / 2, self.pos_y)
		
	def update(self, dt):
		self.accum_time += dt

		if self.accum_time > GUN_ANIMATION_DURATION:
			self.accum_time = 0
			
			if self.animate_fire:
				if self.do_once:
					self.game_mode.player_attack()
					self.do_once = False
					
				try: 
					texture = next(self.texture_gen)
					self.sprt_rect.texture = texture
									
				except StopIteration:
					self.do_once = True
					self.animate_fire = True if self.game.hud.left_button.state == 'down' else False
					
					self.texture_gen = (image for image in get_image_sequence('player'))
					self.sprt_rect.texture = next(self.texture_gen)

	def attack(self):
		self.animate_fire = True
		
		
		
		
		
		
		
		
		
		
		