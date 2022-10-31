"""
three digit register
"""
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions  import Rectangle
from kivy.core.image 				   import Image

from textures import *
from settings import *

class DigitalRegister:
	def __init__(self, game, number_of_digits=3):
		self.game = game
		self.pos_x, self.pos_y = 0, 0
		
		self.num_digits = number_of_digits
		self.digits = None
		
		with self.game.canvas:
			self.digits = tuple((Color(), Rectangle()) for _ in range(self.num_digits))
			
	def re_init(self):
		self.pos_x = 0
		self.pos_y = scr_height() - 100
		for idx, entry in enumerate(self.digits):
			entry[1].size = 100, 100
			entry[1].pos  = self.pos_x + 101 * idx, self.pos_y
			
		self.flip()
		
	def update(self, dt):
		pass							#<---- Use flip instead. wastefull of resources
		
	def flip(self):
		a = self.game.player.health
		for idx, entry in enumerate(self.digits):
			num = a // (100 // (10 ** idx))
			entry[1].texture = get_digit_texture(str(num))
			a = a % (100 // (10 ** idx))
				
			