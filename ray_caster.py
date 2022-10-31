"""
ray_caster
"""
import math
from   settings import *  # constant values
import settings as game   # dynamic values
#import map

game=None

def init(game_ref):
	global game
	
	game = game_ref
	
def re_init():
	pass
		
def cast_ray(pos_x, pos_y, reference_angle, angle=0.0):
	""" General form of casting ray """
	cosine_theta, sine_theta = math.cos(angle), math.sin(angle)		
	start_pos_x, start_pos_y = pos_x, 		  pos_y
	
	# horizontal_scan_h
	Px_h, Py_h = 0.0, 0.0
	total_distance_h, delta_distance_h = 0.0, 0.0
	wall_texture_h, wall_texture_v = '0', '0'
	next_vertical_line = 0
	
	if cosine_theta > 0:
		next_vertical_line = int(start_pos_x) + 1
		total_distance_h, delta_distance_h = (math.fabs((next_vertical_line - start_pos_x) / cosine_theta), 
		                                      math.fabs(RAY_STEPS / cosine_theta))
	elif cosine_theta < 0:
		next_vertical_line = int(start_pos_x)
		total_distance_h, delta_distance_h = (math.fabs((next_vertical_line - start_pos_x) / cosine_theta),
											  math.fabs(RAY_STEPS / cosine_theta))
	else:
		total_distance_h = MAX_NUMBER
	
	while total_distance_h < MAX_LINE_OF_SIGHT_DISTANCE:
		Px_h, Py_h = start_pos_x + total_distance_h * cosine_theta, start_pos_y + total_distance_h * sine_theta
		Py_h = max(0, min(Py_h, NUMBER_OF_BLOCKS_DOWN - 1))
			
		if cosine_theta >= 0:
			idx = int(Px_h + RAYCAST_COLLISION_PEAK_DISTANCE) + int(Py_h) * NUMBER_OF_BLOCKS_ACROSS
		else:
			idx = int(Px_h - RAYCAST_COLLISION_PEAK_DISTANCE) + int(Py_h) * NUMBER_OF_BLOCKS_ACROSS
		
		if game.graph_mngr.get_string(idx) != ".":
			wall_texture_h = game.graph_mngr.get_string(idx)
			break
		else:
			total_distance_h += delta_distance_h

	# vertical_scan_v
	Px_v, Py_v = 0.0, 0.0
	total_distance_v, delta_distance_v = 0.0, 0.0
	next_horizontal_line = 0.0
	
	if sine_theta > 0:
		next_horizontal_line = int(start_pos_y) + 1
		total_distance_v, delta_distance_v = (math.fabs((next_horizontal_line - start_pos_y) / sine_theta),
											  math.fabs(RAY_STEPS / sine_theta))
	elif sine_theta < 0:
		next_horizontal_line = int(start_pos_y) 
		total_distance_v, delta_distance_v = (math.fabs((next_horizontal_line - start_pos_y) / sine_theta),
											  math.fabs(RAY_STEPS / sine_theta))
	else:
		total_distance_v = MAX_NUMBER				 				

	while total_distance_v < MAX_LINE_OF_SIGHT_DISTANCE:
		Px_v, Py_v = start_pos_x + total_distance_v * cosine_theta, start_pos_y + total_distance_v * sine_theta
		Px_v = max(0, min(Px_v, NUMBER_OF_BLOCKS_ACROSS - 1))
		
		if sine_theta >= 0:
			idx = int(Px_v) + int(Py_v + RAYCAST_COLLISION_PEAK_DISTANCE) * NUMBER_OF_BLOCKS_ACROSS
		else:
			idx = int(Px_v) + int(Py_v - RAYCAST_COLLISION_PEAK_DISTANCE) * NUMBER_OF_BLOCKS_ACROSS
		
		if game.graph_mngr.get_string(idx) != ".":
			wall_texture_v = game.graph_mngr.get_string(idx)
			break
		else:
			total_distance_v += delta_distance_v
		
	if total_distance_h <= total_distance_v:
		return total_distance_h * math.cos(reference_angle - angle), Px_h, Py_h, wall_texture_h, True
	else:
		return total_distance_v * math.cos(reference_angle - angle), Px_v, Py_v, wall_texture_v, False
			
def cast_ray_f_player_POV(angle=0.0):
	""" Casting ray from player's POV """
	start_pos_x, start_pos_y = game.player.pos_x, game.player.pos_y
	cosine_theta, sine_theta = math.cos(angle),   math.sin(angle)		
	
	# horizontal_scan_h
	Px_h, Py_h = 0.0, 0.0
	total_distance_h, delta_distance_h = 0.0, 0.0
	wall_texture_h, wall_texture_v = '0', '0'
	next_vertical_line = 0
	
	if cosine_theta > 0:
		next_vertical_line = int(start_pos_x) + 1
		total_distance_h, delta_distance_h = (math.fabs((next_vertical_line - start_pos_x) / cosine_theta), 
		                                      math.fabs(RAY_STEPS / cosine_theta))
	elif cosine_theta < 0:
		next_vertical_line = int(start_pos_x)
		total_distance_h, delta_distance_h = (math.fabs((next_vertical_line - start_pos_x) / cosine_theta),
											  math.fabs(RAY_STEPS / cosine_theta))
	else:
		total_distance_h = MAX_NUMBER
	
	while total_distance_h < MAX_LINE_OF_SIGHT_DISTANCE:
		Px_h, Py_h = start_pos_x + total_distance_h * cosine_theta, start_pos_y + total_distance_h * sine_theta
		Py_h = max(0, min(Py_h, NUMBER_OF_BLOCKS_DOWN - 1))
			
		if cosine_theta >= 0:
			idx = int(Px_h + RAYCAST_COLLISION_PEAK_DISTANCE) + int(Py_h) * NUMBER_OF_BLOCKS_ACROSS
		else:
			idx = int(Px_h - RAYCAST_COLLISION_PEAK_DISTANCE) + int(Py_h) * NUMBER_OF_BLOCKS_ACROSS
		
		if game.graph_mngr.get_string(idx) != ".":
			wall_texture_h = game.graph_mngr.get_string(idx)
			break
		else:
			total_distance_h += delta_distance_h

	# vertical_scan_v
	Px_v, Py_v = 0.0, 0.0
	total_distance_v, delta_distance_v = 0.0, 0.0
	next_horizontal_line = 0.0
	
	if sine_theta > 0:
		next_horizontal_line = int(start_pos_y) + 1
		total_distance_v, delta_distance_v = (math.fabs((next_horizontal_line - start_pos_y) / sine_theta),
											  math.fabs(RAY_STEPS / sine_theta))
	elif sine_theta < 0:
		next_horizontal_line = int(start_pos_y) 
		total_distance_v, delta_distance_v = (math.fabs((next_horizontal_line - start_pos_y) / sine_theta),
											  math.fabs(RAY_STEPS / sine_theta))
	else:
		total_distance_v = MAX_NUMBER				 				

	while total_distance_v < MAX_LINE_OF_SIGHT_DISTANCE:
		Px_v, Py_v = start_pos_x + total_distance_v * cosine_theta, start_pos_y + total_distance_v * sine_theta
		Px_v = max(0, min(Px_v, NUMBER_OF_BLOCKS_ACROSS - 1))
		
		if sine_theta >= 0:
			idx = int(Px_v) + int(Py_v + RAYCAST_COLLISION_PEAK_DISTANCE) * NUMBER_OF_BLOCKS_ACROSS
		else:
			idx = int(Px_v) + int(Py_v - RAYCAST_COLLISION_PEAK_DISTANCE) * NUMBER_OF_BLOCKS_ACROSS
		
		if game.graph_mngr.get_string(idx) != ".":
			wall_texture_v = game.graph_mngr.get_string(idx)
			break
		else:
			total_distance_v += delta_distance_v
		
	if total_distance_h <= total_distance_v:
		return total_distance_h * math.cos(game.player.angle - angle), Px_h, Py_h, wall_texture_h, True
	else:
		return total_distance_v * math.cos(game.player.angle - angle), Px_v, Py_v, wall_texture_v, False

																		
def LoS(pos_x, pos_y, angle, target_x, target_y):
	""" Is there a line of sight given reference pos and angle, and target pos """
	cosine_theta, sine_theta = math.cos(angle), math.sin(angle)		
	start_pos_x, start_pos_y = pos_x, 		  pos_y	
	target_index = int(target_x) + int(target_y) * NUMBER_OF_BLOCKS_ACROSS
	b_has_hit_target_h = b_has_hit_target_v = False
	
	# horizontal_scan_h
	Px_h, Py_h = 0.0, 0.0
	total_distance_h, delta_distance_h = 0.0, 0.0
	wall_texture_h, wall_texture_v = '0', '0'
	next_vertical_line = 0
	
	if cosine_theta > 0:
		next_vertical_line = int(start_pos_x) + 1
		total_distance_h, delta_distance_h = (math.fabs((next_vertical_line - start_pos_x) / cosine_theta), 
		                                      math.fabs(RAY_STEPS / cosine_theta))
	elif cosine_theta < 0:
		next_vertical_line = int(start_pos_x)
		total_distance_h, delta_distance_h = (math.fabs((next_vertical_line - start_pos_x) / cosine_theta),
											  math.fabs(RAY_STEPS / cosine_theta))
	else:
		total_distance_h = MAX_NUMBER
	
	while total_distance_h < MAX_LINE_OF_SIGHT_DISTANCE:
		Px_h, Py_h = start_pos_x + total_distance_h * cosine_theta, start_pos_y + total_distance_h * sine_theta
		Py_h = max(0, min(Py_h, NUMBER_OF_BLOCKS_DOWN - 1))			
		if cosine_theta >= 0:
			idx = int(Px_h + RAYCAST_COLLISION_PEAK_DISTANCE) + int(Py_h) * NUMBER_OF_BLOCKS_ACROSS
		else:
			idx = int(Px_h - RAYCAST_COLLISION_PEAK_DISTANCE) + int(Py_h) * NUMBER_OF_BLOCKS_ACROSS
					
		if game.graph_mngr.get_string(idx) != ".":
			break			
		elif idx == target_index:
			b_has_hit_target_h = True
			break
		else:
			total_distance_h += delta_distance_h

	# vertical_scan_v
	Px_v, Py_v = 0.0, 0.0
	total_distance_v, delta_distance_v = 0.0, 0.0
	next_horizontal_line = 0.0
	
	if sine_theta > 0:
		next_horizontal_line = int(start_pos_y) + 1
		total_distance_v, delta_distance_v = (math.fabs((next_horizontal_line - start_pos_y) / sine_theta),
											  math.fabs(RAY_STEPS / sine_theta))
	elif sine_theta < 0:
		next_horizontal_line = int(start_pos_y) 
		total_distance_v, delta_distance_v = (math.fabs((next_horizontal_line - start_pos_y) / sine_theta),
											  math.fabs(RAY_STEPS / sine_theta))
	else:
		total_distance_v = MAX_NUMBER	
					 				
	while total_distance_v < MAX_LINE_OF_SIGHT_DISTANCE:
		Px_v, Py_v = start_pos_x + total_distance_v * cosine_theta, start_pos_y + total_distance_v * sine_theta
		Px_v = max(0, min(Px_v, NUMBER_OF_BLOCKS_ACROSS - 1))
		if sine_theta >= 0:
			idx = int(Px_v) + int(Py_v + RAYCAST_COLLISION_PEAK_DISTANCE) * NUMBER_OF_BLOCKS_ACROSS
		else:
			idx = int(Px_v) + int(Py_v - RAYCAST_COLLISION_PEAK_DISTANCE) * NUMBER_OF_BLOCKS_ACROSS
			
		if game.graph_mngr.get_string(idx) != ".":
			break			
		elif idx == target_index:
			b_has_hit_target_v = True
			break
		else:
			total_distance_v += delta_distance_v
			
	if total_distance_h <= total_distance_v:
		return b_has_hit_target_h
	else:
		return b_has_hit_target_v

def can_see_player(sprite):
	""" LOS but from sprites's POV """
	angle = sprite.angle + math.pi

	cosine_theta, sine_theta = math.cos(angle), math.sin(angle)		
	start_pos_x, start_pos_y = sprite.pos_x, 		  sprite.pos_y
		
	target_index = int(game.player.pos_x) + int(game.player.pos_y) * NUMBER_OF_BLOCKS_ACROSS
	b_has_hit_target_h = b_has_hit_target_v = False
	
	# horizontal_scan_h
	Px_h, Py_h = 0.0, 0.0
	total_distance_h, delta_distance_h = 0.0, 0.0
	wall_texture_h, wall_texture_v = '0', '0'
	next_vertical_line = 0
	
	if cosine_theta > 0:
		next_vertical_line = int(start_pos_x) + 1
		total_distance_h, delta_distance_h = (math.fabs((next_vertical_line - start_pos_x) / cosine_theta), 
		                                      math.fabs(RAY_STEPS / cosine_theta))
	elif cosine_theta < 0:
		next_vertical_line = int(start_pos_x)
		total_distance_h, delta_distance_h = (math.fabs((next_vertical_line - start_pos_x) / cosine_theta),
											  math.fabs(RAY_STEPS / cosine_theta))
	else:
		total_distance_h = MAX_NUMBER
	
	while total_distance_h < MAX_LINE_OF_SIGHT_DISTANCE:
		Px_h, Py_h = start_pos_x + total_distance_h * cosine_theta, start_pos_y + total_distance_h * sine_theta
		Py_h = max(0, min(Py_h, NUMBER_OF_BLOCKS_DOWN - 1))			
		if cosine_theta >= 0:
			idx = int(Px_h + RAYCAST_COLLISION_PEAK_DISTANCE) + int(Py_h) * NUMBER_OF_BLOCKS_ACROSS
		else:
			idx = int(Px_h - RAYCAST_COLLISION_PEAK_DISTANCE) + int(Py_h) * NUMBER_OF_BLOCKS_ACROSS
					
		if game.graph_mngr.get_string(idx) != ".":
			break			
		elif idx == target_index:
			b_has_hit_target_h = True
			break
		else:
			total_distance_h += delta_distance_h

	# vertical_scan_v
	Px_v, Py_v = 0.0, 0.0
	total_distance_v, delta_distance_v = 0.0, 0.0
	next_horizontal_line = 0.0
	
	if sine_theta > 0:
		next_horizontal_line = int(start_pos_y) + 1
		total_distance_v, delta_distance_v = (math.fabs((next_horizontal_line - start_pos_y) / sine_theta),
											  math.fabs(RAY_STEPS / sine_theta))
	elif sine_theta < 0:
		next_horizontal_line = int(start_pos_y) 
		total_distance_v, delta_distance_v = (math.fabs((next_horizontal_line - start_pos_y) / sine_theta),
											  math.fabs(RAY_STEPS / sine_theta))
	else:
		total_distance_v = MAX_NUMBER	
					 				
	while total_distance_v < MAX_LINE_OF_SIGHT_DISTANCE:
		Px_v, Py_v = start_pos_x + total_distance_v * cosine_theta, start_pos_y + total_distance_v * sine_theta
		Px_v = max(0, min(Px_v, NUMBER_OF_BLOCKS_ACROSS - 1))
		if sine_theta >= 0:
			idx = int(Px_v) + int(Py_v + RAYCAST_COLLISION_PEAK_DISTANCE) * NUMBER_OF_BLOCKS_ACROSS
		else:
			idx = int(Px_v) + int(Py_v - RAYCAST_COLLISION_PEAK_DISTANCE) * NUMBER_OF_BLOCKS_ACROSS
			
		if game.graph_mngr.get_string(idx) != ".":
			break			
		elif idx == target_index:
			b_has_hit_target_v = True
			break
		else:
			total_distance_v += delta_distance_v
			
	if total_distance_h <= total_distance_v:
		return b_has_hit_target_h
	else:
		return b_has_hit_target_v
						
			