""" sprite handler """
from kivy.uix.layout import Layout
from sprite import *
import random

#<----   'class',    'texture id', 'position',
LIST = [ 
		['animated', 'flame', 	 (7.5, 8.5)],
		['animated', 'flame', 	 (8.5, 5.5)],
		['animated', 'flame', 	 (6.5, 5.5)],
		['animated', 'flame', 	 (7.5, 5.5)],
		['animated', 'flame', 	 (8.5, 7.5)],
		['animated', 'flame', 	 (2.5, 8.5)],
		['animated', 'flame', 	 (2.5, 7.5)],
		['animated', 'flame', 	 (6.5, 7.5)],
		['animated', 'flame', 	 (3.5, 12.5)],
		['animated', 'flame', 	 (4.5, 11.5)],
		['animated', 'flame', 	 (10.5, 11.5)],
		['animated', 'flame', 	 (11.5, 12.5)],
		['animated', 'flame', 	 (12.5, 7.5)],
		['animated', 'flame', 	 (12.5, 8.5)],
		['npc', 	 'npc',		(8.5, 8.5)],
		['npc', 	 'npc',		(11.5, 2.5)],
		['npc', 	 'npc',		(3.5, 2.5)],
		['npc', 	 'npc',		(5.5, 3.5)],
		['npc', 	 'npc',		(7.5, 2.5)],
		['npc', 	 'npc',		(7.5, 7.5)],
		['npc', 	 'npc',		(3.5, 5.5)],
		['npc', 	 'npc',		(4.5, 6.5)],
		['npc', 	 'npc',		(10.5, 5.5)],
		['npc', 	 'npc',		(11.5, 6.5)],
		['npc', 	 'npc',		(6.5, 8.5)],
		['npc', 	 'npc',		(3.5, 11.5)],
		['npc', 	 'npc',		(9.5, 3.5)],
		['npc', 	 'npc',		(11.5, 11.5)],
		['npc', 	 'npc',		(5.5, 9.5)],
		['npc', 	 'npc',		(4.5, 8.5)],
		['sprite',   'candle_bra', (7.4, 8.4)],
		['npc', 	 'npc',		(10.5, 8.5)],
	   ]

class SpriteSpace(Layout):
	def __init__(self, game, **kwargs):	
		super().__init__(**kwargs)
		self.game		= game  					 
		
		self.c_t_s 	  = None		
		self.FOV_s 	  = []
		self.o_s   	  = []
		self.all_sprites = []
		self.load_list   = LIST
		
		self.game.add_widget(self)
		self.debug_int=0					   
	
	def re_init(self):
		self.c_t_s = None		
		self.FOV_s.clear() 	
		self.o_s.clear() 	
		self.delete_all_sprts()

		for entry in self.load_list:
			
			if   entry[0] == 'sprite':
				if self.game.graph_mngr.is_valid_position(*entry[2]):
					sprt = Sprite(self.game, sprite_id=entry[1], pos = entry[2])
					self.all_sprites.append(sprt)
					
				else:
					raise Exception('Conflict detected in sprite location {} {}'.format(entry[0], entry[2]))
						
			elif entry[0] == 'animated':
				if self.game.graph_mngr.is_valid_position(*entry[2]):
					sprt = AnimatedSprite(self.game, sprite_id=entry[1], pos = entry[2])
					self.all_sprites.append(sprt)
					
				else:
					raise Exception('Conflict detected in animated sprite location {} {}'.format(entry[0], entry[2]))
						
			elif entry[0] == 'npc':
				if self.game.graph_mngr.is_valid_position(*entry[2]):
					sprt = NPC(self.game, sprite_id=entry[1], pos = entry[2])
					self.all_sprites.append(sprt)
						
				else:
					raise Exception('Conflict detected in npc sprite location {} {}'.format(entry[0], entry[2]))
					
			else:
				raise Exception('Invalid sprite type!')
				
	def remaining_npcs(self):
		n = 0
		for i in self.all_sprites:
			if isinstance(i, NPC) and (i.current_action != 'die' and i.current_action != 'for delete'):
				n += 1		
		return n
	
	def delete_all_sprts(self):
		for sprt in list(self.all_sprites): #<---- Python Bug :)
			self.delete_sprt(sprt)						
												
	def delete_sprt(self, sprt):
		self.remove_from_sprt_cnvs(sprt)
		self.game.map.remove_from_mmp_cnvs(sprt)
		self.all_sprites.remove(sprt)

	def add_to_sprt_cnvs(self, sprt):
		if not sprt.in_sprt_cnvs:
			sprt.in_sprt_cnvs = True
			self.canvas.add(sprt.sprt_colour)
			self.canvas.add(sprt.sprt_rect)
			
	def remove_from_sprt_cnvs(self, sprt):
		if sprt.in_sprt_cnvs:
			sprt.in_sprt_cnvs = False
			self.canvas.remove(sprt.sprt_colour)
			self.canvas.remove(sprt.sprt_rect)

	def project_on_screen(self, sprt, idx):		
		proj_ratio      		= sprt.SCALE_FACTOR / sprt.d_f_player	
		proj_width, proj_height = sprt.IMAGE_RATIO * proj_ratio, proj_ratio
		
		sprt.sprt_rect.size     = proj_width, proj_height
		sprt.sprt_rect.pos      = idx * scr_rect_w() - proj_width // 2, half_scr_h() - proj_height
	
	def get_FOV_s(self):		
		self.c_t_s = None
		self.FOV_s.clear()
		self.o_s.clear()
		
		for i, s in enumerate(self.all_sprites):		
			if self.is_in_view(s):
				self.FOV_s.append((s.angle, s))

			self.remove_from_sprt_cnvs(s)	
				
		if self.FOV_s:
			self.FOV_s.sort(key=lambda d: d[0], reverse=True)
			self.c_t_s = self.FOV_s[0][-1]
			
	def next_c_t_s(self):		
		self.c_t_s = None	
		self.FOV_s.pop(0)
		if self.FOV_s:
			self.c_t_s = self.FOV_s[0][-1]
			
	def update_sprites(self, dt):
		for i, s in enumerate(self.all_sprites):
			if isinstance(s, AnimatedSprite):
				s.update(dt)		
			
	def update(self, idx, dist, r_a):		
		if self.c_t_s and r_a < self.c_t_s.angle:
			if dist > self.c_t_s.d_f_player:
				self.o_s.append((self.c_t_s.d_f_player, self.c_t_s))
				self.project_on_screen(self.c_t_s, idx)
			self.next_c_t_s()

		if idx == NUMBER_OF_RAYS - 1:
			self.o_s.sort(key=lambda data: data[0], reverse=True)
			for i, s in enumerate(self.o_s):
				self.add_to_sprt_cnvs(s[-1])
			
	def is_in_view(self, sprite):													
		p_angle     		 = self.game.player.angle									    		
		p_x				  = self.game.player.pos_x
		p_y				  = self.game.player.pos_y							   
		
		Dx, Dy      		 = sprite.pos_x - p_x, sprite.pos_y - p_y			
		max_angle, min_angle = p_angle + HALF_FOV, p_angle - HALF_FOV
		sprite.d_f_player    = math.dist((sprite.pos_x, sprite.pos_y),(p_x, p_y))			   			   
		
		in_view 			 = False
		if sprite.d_f_player < PLAYER_RADIUS:
			return in_view
						
		# Angle correction the hard way!
		if   Dx == 0 and Dy >= 0:
			sprite.angle = P_90_DEGREES
				
		elif Dx == 0 and Dy <  0:
			sprite.angle = P_270_DEGREES
			
		else:
			sprite.angle = math.atan(Dy/Dx)
			
			if   sprite.angle >= 0 and Dx > 0:
				pass
				
			elif sprite.angle >= 0 and Dx < 0:
				sprite.angle += P_180_DEGREES
				
			elif sprite.angle < 0  and Dx > 0:
				sprite.angle += P_360_DEGREES
				
			elif sprite.angle < 0 and Dx < 0:
				sprite.angle += P_180_DEGREES
				
			else:
				raise Exception('sprite_space.is_in_view() invalid angle!')
					
		# Check if within FOV
		if   P_90_DEGREES > p_angle >= ZERO_DEGREES and min_angle < 0:
			if   max_angle >= sprite.angle >= ZERO_DEGREES:
				in_view = True
				sprite.angle = sprite.angle
						
			elif P_360_DEGREES >= sprite.angle >= P_360_DEGREES + min_angle:
				in_view = True
				sprite.angle -= P_360_DEGREES
					
			else:
				in_view = False
		
		elif P_360_DEGREES >= p_angle > P_270_DEGREES and max_angle > P_360_DEGREES:
			if max_angle - P_360_DEGREES >= sprite.angle >= ZERO_DEGREES:
				in_view = True
				sprite.angle += P_360_DEGREES
							
			elif P_360_DEGREES >= sprite.angle >= min_angle:
				in_view = True
				sprite.angle = sprite.angle
						
			else:
				in_view = False
				
		else:
			 in_view = max_angle >= sprite.angle >= min_angle
			 			 	 
		return in_view
		
	def player_attack(self):
		max = self.game.player.angle + 0.1
		min = self.game.player.angle - 0.1
		
		for i, s in enumerate(self.o_s):			
			sprt = s[1]
			if isinstance(sprt, NPC) and max >= sprt.angle >= min:
				if sprt.d_f_player < sprt.atk_range + random.uniform(0,1):
					sprt.receive_damage()
	