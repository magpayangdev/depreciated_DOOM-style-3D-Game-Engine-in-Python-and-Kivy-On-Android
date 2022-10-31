""" npc animations """
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir  = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import sprite as sprt
from   textures import *

def idle_animation(npc):
	try:
		npc.sprt_rect.texture = next(npc.idle_i_seq)

	except StopIteration:
		npc.idle_i_seq = (image for image in get_image_sequence(npc.sprite_id))
		npc.sprt_rect.texture = next(npc.idle_i_seq)

def default_state_machine(npc):
	""" Default npc animation routine """
	if npc.current_action == 'die':						#<---- Death Anim
		npc.anim_int = 0.08
		try:
			npc.sprt_rect.texture = next(npc.die_i_seq)

		except StopIteration:
			npc.path.clear()
			npc.game_mode.sprite_has_died(npc)
			npc.current_action = 'for delete'
					
	elif npc.current_action == 'hurt':					 #<---- Hurt Anim
		npc.anim_int = 0.2
		try:
			npc.sprt_rect.texture = next(npc.hit_i_seq)
			
		except StopIteration:				
			npc.game_mode.sprite_hit()
			
			npc.hit_i_seq = (image for image in get_image_sequence(npc.sprite_id, 'hit'))
			npc.sprt_rect.texture = next(npc.hit_i_seq)
			npc.current_action = 'walking'

		if npc.health <= 0:
			npc.current_action = 'die'
			
			
	elif npc.current_action == 'idle':					 #<---- Idle Anim
		super(sprt.NPC, npc).timed_update()
			
	elif npc.current_action == 'walking':				  #<---- Death Anim
		npc.anim_int = 0.4
		try:
			npc.sprt_rect.texture = next(npc.walk_i_seq)
			
		except StopIteration:
			npc.walk_i_seq = (image for image in get_image_sequence(npc.sprite_id, 'walk'))
			npc.sprt_rect.texture = next(npc.walk_i_seq)
			
	elif npc.current_action == 'attack':				   #<---- Attack Anim
		npc.anim_int = npc.atk_duration
		try:
			npc.sprt_rect.texture = next(npc.atk_i_seq)
				
		except StopIteration:
			npc.game_mode.sprite_attack()				

			npc.atk_i_seq  = (image for image in get_image_sequence(npc.sprite_id, 'attack'))
			npc.sprt_rect.texture = next(npc.atk_i_seq)
			
	elif npc.current_action == 'for delete':
		pass
		
	else:
		raise Exception('Invalid current action string value!')