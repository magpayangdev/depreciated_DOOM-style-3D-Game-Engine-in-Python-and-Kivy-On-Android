""" Sprite Behaviour """
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir  = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import ray_caster
from   npc_scripts.npc_helper_functions import *

def persistent_follow(npc, dt, debug=False):
		""" Starts at idle. When sees player, consistenly follows until conditions meet, then attack """
		npc.sees_target=ray_caster.can_see_player(npc)
		
		if debug:
			npc.game.map.x, npc.game.map.y = npc.pos_x, npc.pos_y
		
		if npc.current_action == 'die':								#<---- Death
			return
		
		elif npc.current_action == 'hurt':							 #<---- Hurt
			npc.game.graph_mngr.add_npc_location((int(npc.pos_x), int(npc.pos_y)))
			return
			
		elif npc.current_action == 'idle':							 #<---- Idle
			npc.game.graph_mngr.add_npc_location((int(npc.pos_x), int(npc.pos_y)))
			 
			if npc.sees_target:
				if debug:
					npc.game.map.draw_line = True
				
				if is_player_in_range(npc):
					npc.current_action = 'attack'
					
				else:
					npc.current_action = 'walking'			
			
		elif npc.current_action == 'walking':						  #<---- Walking
			npc.game.graph_mngr.add_npc_location((int(npc.pos_x), int(npc.pos_y)))

			move_to_next_node(npc, dt)
			
			if is_player_in_range(npc):
				if npc.sees_target:
					npc.current_action = 'attack'
					npc.path.clear()
						
				else:
					pass	#<---- Keep Moving
						
			else:
				pass		#<---- Keep Moving
			
		elif npc.current_action == 'attack':							#<---- Attacking
			npc.game.graph_mngr.add_npc_location((int(npc.pos_x), int(npc.pos_y)))
			
			if not npc.sees_target:
				if debug:
					npc.game.map.draw_line = False
					
				npc.current_action = 'walking'
				
			else:
				if is_player_in_range(npc):
					pass
				else:
					npc.current_action = 'walking'
					
		elif npc.current_action == 'for delete':
			npc.for_del_cntr += dt
			
			if npc.for_del_cntr > npc.f_del_dur:
				npc.for_del_cntr = 0
				npc.game_mode.sprite_for_delete(npc)
			
		else:
			raise Exception('Invalid current action string value!')