"""
controls
"""
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions  import Rectangle

from settings import *
from textures import * 

class XYPad:
	def __init__(self, game, orientation='left'):		
		self.game		= game
		self.orientation = orientation.lower()
		self.is_active   = False
		self.debug_int   = 0
		self.size        = 0
		self.stick_size  = 0
		
		with self.game.canvas:
			self.bg_colour	= Color()
			self.bg_rect	  = Rectangle()
			self.stick_colour = Color()
			self.stick_rect   = Rectangle()
																
	def re_init(self):
		center_left  = controller_center_left()
		center_right = controller_center_right()

		self.size		 	  = controller_size()
		self.stick_size   	  = controller_stick_size()
		
		self.bg_colour.rgba 	= CONTROLLER_BACKGROUND_COLOUR
		self.bg_rect.texture	= get_controller_texture("dotted_circle")		
		self.bg_rect.size       = self.size

		self.stick_colour.rgba  = CONTROLLER_STICK_COLOUR
		self.stick_rect.texture = get_controller_texture("skull")		
		self.stick_rect.size    = self.stick_size
		
		if self.orientation == 'left':						
			self.bg_rect.pos      = center_left[0] - self.size[0] / 2, 	  center_left[1] - self.size[0] / 2
			self.stick_rect.pos   = center_left[0] - self.stick_size[0] / 2, center_left[1] - self.stick_size[0] / 2
									
		elif self.orientation == 'right':
			self.bg_rect.pos      = center_right[0] - self.size[0] / 2, 	  center_right[1] - self.size[0] / 2
			self.stick_rect.pos   = center_right[0] - self.stick_size[0] / 2, center_right[1] - self.stick_size[0] / 2			
	
	def move_stick(self, Px, Py):
		if self.orientation == 'left':
			distance = math.dist((Px, Py),controller_center_left())
			
			if distance > 250:
				x = 250 * (Px - controller_center_left()[0]) / distance + controller_center_left()[0]
				y = 250 * (Py - controller_center_left()[1]) / distance + controller_center_left()[1]
			else:
				x, y = Px, Py
				
		else:
			distance = math.dist((Px, Py),controller_center_right())
			
			if distance > 250:
				x = 250 * (Px - controller_center_right()[0]) / distance + controller_center_right()[0]
				y = 250 * (Py - controller_center_right()[1]) / distance + controller_center_right()[1]
			else:
				x, y = Px, Py
			
		self.stick_rect.pos = x - self.stick_size[0] / 2, y - self.stick_size[1] / 2
		
	def reset_stick(self):
		center_left  = controller_center_left()
		center_right = controller_center_right()
		
		if self.orientation == 'left':						
			self.stick_rect.pos   = center_left[0] - self.stick_size[0] / 2, center_left[1] - self.stick_size[0] / 2
									
		elif self.orientation == 'right':
			self.stick_rect.pos   = center_right[0] - self.stick_size[0] / 2, center_right[1] - self.stick_size[0] / 2			
			


