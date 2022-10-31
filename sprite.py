"""
sprite
"""
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions  import Rectangle
from kivy.graphics.vertex_instructions  import Line
from kivy.core.image 				   import Image

import os
import math
import random
from   collections 					 import deque

from   settings 						import * 
from   textures 						import * 
import ray_caster   

import map
from   npc_scripts 					 import npc_behavior
from   npc_scripts 					 import npc_animation		

class Sprite:
	""" Static sprtes. Projection constants are calculated """
	def __init__(self, game, sprite_id="candle_bra", pos=(0,0), radius=0.1, angle=0, scale=0.5, icon='cherry'):			
		self.game				  = game										     # game window instance
		self.game_mode			 = self.game.gm
		self.sprite_id			 = sprite_id										# used as key to texture paths
				
		self.pos_x, self.pos_y	 = pos[0], pos[1]	  		 				    # sprite position
		self.angle				 = 0.0											  # angle relative to player
		self.radius				= radius			 							  # sprite radius
		self.d_f_player			= 0.0											  # distance from player
		
		self.img_texture		   = get_image_sequence(self.sprite_id)[0]			# default idle image
		self.IMAGE_RATIO		   = self.img_texture.width / self.img_texture.height # image ratio
		self.SCALE_FACTOR		  = scale * screen_distance()					    # image scale factor
								
		with self.game.sprite_space.canvas:
			self.sprt_colour	   = Color()								   
			self.sprt_rect		 = Rectangle()
										   
			self.sprt_rect.texture = self.img_texture			
			self.in_sprt_cnvs	  = True
			
		with self.game.canvas:
			self.mmp_colour		 = Color(1,1,1)
			self.mmp_rect		  = Rectangle(size=(c_block_size(),c_block_size()), texture=get_map_texture(icon))
			self.mmp_line		  = Line(width=2)
			self.in_mmp_cnvs	   = True
			
		if not render_map():
			self.game.map.remove_from_mmp_cnvs(self)
	
class AnimatedSprite(Sprite):
	""" Handles idle image transistions """
	def __init__(self, game, sprite_id="flame", pos=(0,0), radius=0.1, angle=0, scale=0.5, icon='fire', anim_interval=0.1, del_dur = 3):
		super().__init__(game, sprite_id, pos, radius, angle, scale, icon)
		self.acc_time     = 0.0		
		self.for_del_cntr = 0.0	
		self.f_del_dur	= del_dur									  
		self.anim_int     = anim_interval										
		self.idle_i_seq   = (image for image in get_image_sequence(self.sprite_id))
		
	def update(self, dt):
		self.acc_time += dt
		self.fbf_update(dt)
				
		if self.acc_time > self.anim_int:
			self.acc_time = 0.0
			self.timed_update()
			
	def fbf_update(self,dt):
		pass
		
	def timed_update(self):
		npc_animation.idle_animation(self)	

	def receive_damage(self, damage_amount=1):
		pass

class NPC(AnimatedSprite):
	""" Has additional actions and animation sequences other than idle """
	def __init__(self, game, sprite_id='npc', pos=(0,0), radius=0.2, angle=0, scale=0.5, icon='monster', anim_interval=0.5, del_dur=3, atk_range=3):
		super().__init__(game, sprite_id, pos, radius, angle, scale, icon, anim_interval, del_dur)
		self.health		 = 3
		self.speed          = 0.30
		self.atk_range	  = atk_range
		self.path_colour	= 1, random.uniform(0, 1), random.uniform(0, 1)
				
		self.next_node	  = 0,0
		self.sees_target	= False
		self.current_action = 'idle'
		self.path 	      = []
			
		self.walk_i_seq = (image for image in get_image_sequence(self.sprite_id, 'walk'))
		self.hit_i_seq  = (image for image in get_image_sequence(self.sprite_id, 'hit'))
		self.die_i_seq  = (image for image in get_image_sequence(self.sprite_id, 'death'))
		self.atk_i_seq  = (image for image in get_image_sequence(self.sprite_id, 'attack'))
		
		self.atk_duration = 0.1
				
	def update(self, dt):
		super().update(dt)
									
	def fbf_update(self,dt):
		npc_behavior.persistent_follow(self, dt, debug=False)
		
	def timed_update(self):
		npc_animation.default_state_machine(self)
					
	def receive_damage(self, damage_amount=1):
		if self.current_action != 'die' and self.current_action != 'for delete':
			super().receive_damage(damage_amount)
			self.health -= damage_amount
			self.current_action = 'hurt'
			
			
			
			
			
			
			
			
			


		
			
					