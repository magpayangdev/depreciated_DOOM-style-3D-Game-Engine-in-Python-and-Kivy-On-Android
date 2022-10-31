""" Custom button """

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions  import Rectangle
from kivy.uix.button					import Button

from settings import *
from textures import * 

class BasicButton(Button):
	def __init__(self, game, pos_x=0, pos_y=0, texture_id='gun', **kwargs):
		super(Button, self).__init__(**kwargs)
		self.game = game
		self.pos_x, self.pos_y = pos_x, pos_y
		
		self.texture = get_controller_texture(texture_id)
		
		self.game.add_widget(self)
			
	def re_init(self):
		self.size = 10,10
		
	def on_touch_down(self):
		pass
		
	def on_touch_move(self):
		pass
		
	def on_touch_up(self):
		pass
		
