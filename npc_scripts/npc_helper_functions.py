""" NPC Helper Functions """
import os
import sys
import math

from	settings import *
import  ray_caster   

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir  = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def move(npc, dt, value=0):
	x, y = npc.path[-2]
	x += 0.5
	y += 0.5	
	
	if npc.pos_x - x < -NPC_RADIUS:
		npc.pos_x += npc.speed * dt
		
	elif npc.pos_x - x > NPC_RADIUS:
		npc.pos_x -= npc.speed * dt
		
	else:
		pass
	
	if npc.pos_y - y < -NPC_RADIUS:
		npc.pos_y += npc.speed * dt
		
	elif npc.pos_y - y > NPC_RADIUS:
		npc.pos_y -= npc.speed * dt
		
	else:
		pass
		
	return math.dist((x,y),(npc.pos_x, npc.pos_y)) 

	
def move_to_next_node(npc, dt):
	target_node = int(npc.game.player.pos_x),		 int(npc.game.player.pos_y)
	start_node  = int(npc.pos_x),					 int(npc.pos_y)			
	bfs_result  = npc.game.graph_mngr.bfs(start_node, target_node)

	npc.path.clear()
	
	if target_node in bfs_result:
		path 	   = []
		path.append(target_node)
		
		while target_node != start_node:
			target_node = bfs_result[target_node]
			path.append(target_node)
			
		if len(path)>1:
			x, y = path[-2]
			npc.path = path

			move(npc, dt)
			
def d_is_player_in_LoS(self):
	return ray_caster.LoS(npc.pos_x,npc.pos_y, npc.angle+math.pi, npc.game.player.pos_x,npc.game.player.pos_y)
	
def is_player_in_range(npc):
	return math.dist((npc.pos_x, npc.pos_y), (npc.game.player.pos_x, npc.game.player.pos_y)) <= npc.atk_range
