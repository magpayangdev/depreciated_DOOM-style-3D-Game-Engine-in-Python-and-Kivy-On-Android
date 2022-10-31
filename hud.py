"""
hud
"""

from kivy.uix.button					import Button
from kivy.uix.label       			  import Label

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions  import Rectangle
from kivy.core.image 				   import Image	   

from settings 						  import *  		 # constant values
from textures 					  	import * 

from hud_scripts.controller			 import XYPad	   # controls
from hud_scripts.player_sprite		  import PlayerSprite
from hud_scripts.digital_register	   import DigitalRegister
from hud_scripts.buttons				import BasicButton 


class Hud:
	def __init__(self, game):
		self.game		  = game
		
		self.accum_time	= 0.0
		self.rst_hit_rect  = False
		
		self.player_sprt   = PlayerSprite(self.game)
		self.left_xypad    = XYPad(self.game, orientation='left')
		self.right_xypad   = XYPad(self.game, orientation='right')
		self.player_health = DigitalRegister(self.game)
		
		self.debug_label=Label(text="Debug Text",color=DEBUG_TEXT_COLOR,size_hint=(1,1), pos_hint={'x':-0.45, 'y':0.35})
		self.game.add_widget(self.debug_label)
				
		self.exit_button   = None
		self.left_button   = None
		self.right_button  = None
		self.map_button    = None
		
		with self.game.canvas:
			self.hit_colour = Color()
			self.hit_rect = Rectangle()
			
	def re_init(self):
		if self.exit_button:
			self.game.remove_widget(self.exit_button)
		self.exit_button = self.create_button('resources/textures/controller/x.png', 
												'resources/textures/controller/x.png',
												(100/scr_width(), 100/scr_height()), 
												{'right':0.99,'top':0.99}, self.e_b_callback)			
		
		if self.left_button:			
			self.game.remove_widget(self.left_button)
		self.left_button = self.create_button('resources/textures/controller/gun_r.png',
												'resources/textures/controller/gun_firing_r.png',
												(250/scr_width(), 250/scr_height()),
												{'right':0.99,'center_y':0.4}, self.l_b_callback)				
			
		if self.right_button:
			self.game.remove_widget(self.right_button)
		self.right_button = self.create_button('resources/textures/controller/gun.png',
												'resources/textures/controller/gun_firing.png',
												(250/scr_width(), 250/scr_height()),
												{'left':0.945,'center_y':0.4}, self.r_b_callback)
												
		if self.map_button:
			self.game.remove_widget(self.map_button)
		self.map_button = self.create_button('resources/textures/controller/map_icon.png', 
											 'resources/textures/controller/map_icon.png', 
											 (200/scr_width(), 200/scr_height()), 
											 {'left':0.945, 'center_y':0.55}, self.map_button_callback)
		
		self.player_sprt.re_init()
		self.left_xypad.re_init()
		self.right_xypad.re_init()
		self.player_health.re_init()
		
		self.hit_colour.rgba = 1,0,0,0
		self.hit_rect.size = self.game.size
		self.hit_rect.texture = None
		
	def create_button(self, bg_normal='path', bg_down='path', size_hint=(1,1), pos_hint={}, callback=None):
		button = Button(background_normal=bg_normal, background_down=bg_down, size_hint=size_hint, pos_hint=pos_hint)
		button.bind(state=callback)
		self.game.add_widget(button)
		
		return button
		
	def update(self, dt):
		self.accum_time += dt
		self.player_sprt.update(dt)
		
		if self.accum_time > 0.3:
			self.accum_time = 0.0
			
			if self.rst_hit_rect:
				self.rst_hit_rect = False
				self.hit_colour.rgba = 0,0,0,0
	
	def game_over(self):
		self.hit_colour.rgba = 1,1,1,1
		self.hit_rect.texture = get_menu_texture('game_over')
		
	def victory(self):
		self.hit_colour.rgba = 1,1,1,1
		self.hit_rect.texture = get_menu_texture('victory')

	def player_is_hit(self):			
		self.accum_time = 0.0
		self.rst_hit_rect = True
		self.hit_colour.rgba = 1,0,0,0.5
		
		self.player_health.flip()
		
	def e_b_callback(self, *args):
		if self.exit_button.state == 'down':
			self.game.quit_game()
			
	def map_button_callback(self, *args):
		if self.map_button.state == 'down':
			self.game.map.show_map()
			
	def l_b_callback(self, *args):
		if self.left_button.state == 'down':
			self.player_sprt.attack()
		else:
			pass
			
	def r_b_callback(self, *args):
		if self.right_button.state == 'down':
			self.player_sprt.attack()
				
	@property
	def debug_text(self):
		return self.debug_label.text
	
	@debug_text.setter
	def debug_text(self, str):
		self.debug_label.text = str
		
	@debug_text.deleter
	def debug_text(self):
		self.debug_label.text = ''	
	
	@property
	def left_xypad_active(self):
		return self.left_xypad.is_active
		
	@left_xypad_active.setter
	def left_xypad_active(self, bool):
		self.left_xypad.is_active = bool
		
	@property
	def right_xypad_active(self):
		return self.right_xypad.is_active
		
	@right_xypad_active.setter
	def right_xypad_active(self, bool):
		self.right_xypad.is_active = bool
	
	def on_touch_down(self, touch):

		if self.exit_button.collide_point(*touch.pos):
			self.exit_button.state = 'down'
			return True

		if self.left_button.collide_point(*touch.pos):
			self.left_button.state = 'down'
			return True
			
		if self.right_button.collide_point(*touch.pos):
			self.right_button.state = 'down'
			return True
			
		if self.map_button.collide_point(*touch.pos):
			self.map_button.state = 'down'
			return True

		if   touch.x <= self.game.center_x and touch.y <= self.game.center_y:  	# if touch_down in Q1:
			if math.dist(touch.pos, controller_center_left()) < 250:
				self.left_xypad_active = True
			else:
				self.left_xypad_active = False

		elif touch.x <= self.game.center_x and touch.y > self.game.center_y:   	# if touch_down in Q2:
			pass

		elif touch.x >  self.game.center_y and touch.y <= self.game.center_y:  	# if touch_down in Q3: 
			if math.dist(touch.pos, controller_center_right()) < 250:
				self.right_xypad_active = True
			else:
				self.right_xypad_active = False

		else:																	  # if touch_down in Q4:
			pass
		
	def on_touch_move(self, touch):
	
		if self.left_button.collide_point(*touch.pos) or self.right_button.collide_point(*touch.pos) or self.map_button.collide_point(*touch.pos):
			return True

		# if touch_move in Q1:
		if   touch.x<=self.game.center_x and touch.y<=self.game.center_y:				
			if self.left_xypad_active:		
				self.left_xypad.move_stick(*touch.pos)
				self.game.player.right_dir	  = max(-1, min(1, (touch.x - controller_center_left()[0]) / 250))
				self.game.player.forward_dir    = max(-1, min(1, (touch.y - controller_center_left()[1]) / 250))
				
			else:
				self.left_xypad.reset_stick()
				self.game.player.forward_dir	= 0
				self.game.player.right_dir	  = 0
									
		elif touch.x <= self.game.center_x and touch.y > self.game.center_y:   	# if touch_move in Q2:
			pass
			
		# if touch_move in Q3: 
		elif touch.x>self.game.center_y and touch.y<=self.game.center_y:
			if self.right_xypad_active:
				self.right_xypad.move_stick(*touch.pos)
				self.game.player.yaw			= max(-1, min(1, (touch.x - controller_center_right()[0]) / 250))	
			else:
				self.right_xypad.reset_stick()
				self.game.player.yaw			= 0

		else:																	  # if touch_move in Q4:
			pass
		
	def on_touch_up(self, touch):
	
		if self.left_button.collide_point(*touch.pos):
			self.left_button.state = 'normal'
			return True
			
		if self.right_button.collide_point(*touch.pos):
			self.right_button.state = 'normal'
			return True
		
		if self.map_button.collide_point(*touch.pos):
			self.map_button.state = 'normal'
			return True
			
		if   touch.x <= self.game.center_x and touch.y <= self.game.center_y:  	# if touch_up in Q1:
			self.left_xypad.reset_stick()
			self.game.player.forward_dir = 0
			self.game.player.right_dir   = 0
									
		elif touch.x <= self.game.center_x and touch.y > self.game.center_y:   	# if touch_up in Q2:
			self.left_xypad.reset_stick()
			self.game.player.forward_dir = 0
			self.game.player.right_dir   = 0
								
		elif touch.x >  self.game.center_y and touch.y <= self.game.center_y:  	# if touch_up in Q3:
			self.right_xypad.reset_stick()
			self.game.player.yaw = 0
				
		else:						   						 				  # if touch_up in Q4:
			self.right_xypad.reset_stick()
			self.game.player.yaw = 0		



			











