"""
player
"""

import math
import random
from   settings import *

class Player:
	def __init__(self, game, pos_x=1.5, pos_y=1.5, angle=math.pi/2, radius=PLAYER_RADIUS):
		self.game 	   	  = game
		self.accum_time		= 0
		self.pos_x, self.pos_y = pos_x, pos_y
		self.angle 	  	  = angle
		self.radius 	 	  = radius
		self.health			= 789
		self.forward_dir 	  = 0
		self.right_dir   	  = 0
		self.yaw		 	  = 0
		self.speed			 = 2
		self.turn_speed		= 2
		
		self.in_mmp_cnvs	   = False
		self.mmp_colour		= None
		self.mmp_rect		  = None
		self.mmp_line		  = None

	def re_init(self):
		self.pos_x, self.pos_y = 1.5, 1.5
		self.angle 	  	  = math.pi/2
		self.health			= 789
		
	def hit(self, damage_amount=10):
		self.health = max(0, min(MAX_PLAYER_HEALTH, self.health - damage_amount))
		return self.health
		
	def update(self, dt):
		self.move_forward(dt)
		self.move_right(dt)
		self.look_right(dt)
		
		self.accum_time += dt
		if self.accum_time > 2: #<---- Regen
			self.accum_time = 0
			self.health = max(0, min(MAX_PLAYER_HEALTH, self.health + 1))
			self.game.hud.player_health.flip()	
	
	def move_forward(self, dt):
		dx, dy, tx, ty = Player.move(dt, self.forward_dir, self.pos_x, self.pos_y, self.radius, self.angle, False)
			
		if self.game.graph_mngr.is_valid_position(tx, self.pos_y):
			self.pos_x += dx * self.speed
		
		if self.game.graph_mngr.is_valid_position(self.pos_x, ty):
			self.pos_y += dy * self.speed
		
	def move_right(self, dt):	
		dx, dy, tx, ty = Player.move(dt, self.right_dir, self.pos_x, self.pos_y, self.radius, self.angle, True)
												 			
		if self.game.graph_mngr.is_valid_position(tx, self.pos_y):
			self.pos_x += dx * self.speed
		
		if self.game.graph_mngr.is_valid_position(self.pos_x, ty):
			self.pos_y += dy * self.speed	
	
	def look_right(self, dt):
		self.angle -= dt * self.yaw * self.turn_speed
		
		if self.angle < 0:
			self.angle += 2 * math.pi 
		
		if self.angle > 2 * math.pi:
			self.angle -= 2 * math.pi
	
	@staticmethod
	def move(dt, value, pos_x, pos_y, radius, angle , strafe=False):
		if value == 0:
			return 0, 0, 0, 0 
			
		if strafe:
			cosine_theta, sine_theta =  math.sin(angle), -math.cos(angle)
		else:
			cosine_theta, sine_theta = math.cos(angle), math.sin(angle)
		
		dx, dy = cosine_theta * dt * value, sine_theta * dt * value
			
		if value > 0:		
			if cosine_theta > 0 and sine_theta > 0:
				tx = pos_x + radius + dx
				ty = pos_y + radius + dy
			
			elif cosine_theta < 0 and sine_theta > 0:
				tx = pos_x - radius + dx
				ty = pos_y + radius + dy
				
			elif cosine_theta < 0 and sine_theta < 0:
				tx = pos_x - radius + dx
				ty = pos_y - radius + dy
				
			elif cosine_theta > 0 and sine_theta < 0: 
				tx = pos_x + radius + dx
				ty = pos_y - radius + dy
			
			elif cosine_theta == 0:
				tx = pos_x + radius
				if sine_theta >= 0:
					ty = pos_y + radius + dy
				else:
					ty = pos_y - radius + dy 
			
			elif sine_theta == 0:
				ty = pos_y + radius
				if cosine_theta >= 0:
					tx = pos_x + radius + dx
				else:
					tx = pos_x - radius + dx
	
		elif value < 0:
			if cosine_theta > 0 and sine_theta > 0:
				tx = pos_x - radius + dx
				ty = pos_y - radius + dy
				
			elif cosine_theta < 0 and sine_theta > 0:
				tx = pos_x + radius + dx
				ty = pos_y - radius + dy
				
			elif cosine_theta < 0 and sine_theta < 0:
				tx = pos_x + radius + dx
				ty = pos_y + radius + dy
				
			elif cosine_theta > 0 and sine_theta < 0:
				tx = pos_x - radius + dx
				ty = pos_y + radius + dy
				
			elif cosine_theta == 0:
				tx = pos_x + radius
				if sine_theta >= 0:
					ty = pos_y - radius + dy
				else:
					ty = pos_y + radius + dy 
			
			elif sine_theta == 0:
				ty = pos_y + radius
				if cosine_theta >= 0:
					tx = pos_x - radius + dx
				else:
					tx = pos_x + radius + dx
				
		else:
			return 0, 0, 0, 0
			
		return dx, dy, tx, ty