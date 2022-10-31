""" game mode - defines what happens when an event is called """

from kivy.clock import Clock
from settings import *

class GameMode:
	def __init__(self, game):
		self.game = game
		
	def pause_game(self):
		self.game.paused = True
		self.game.hud.debug_text = 'Paused!'
		self.game.hud.debug_label.color = RED
		self.game.audio.pause_game()
		self.game.audio.stop_theme()
				
	def unpause_game(self):
		self.game.paused = False
		self.game.hud.debug_label.color = GREEN
		self.game.audio.play_theme()
	
	def sprite_hit(self, damage_amount=1):
		self.game.audio.hit()

	def sprite_attack(self):
		self.game.audio.attack()
		self.player_hit()		

	def player_hit(self, damage_amount=7):
		self.game.player.hit(damage_amount)
		if PLAYER_CAN_DIE and self.game.player.health == 0:
			self.player_has_died()
		else:
			self.game.hud.player_is_hit()
		
	def player_attack(self):
		self.game.sprite_space.player_attack()
		self.game.audio.player_attack()

	def player_has_died(self):
		self.game.audio.theme.stop()
		self.game.hud.game_over()
		
		Clock.unschedule(self.game.tick)
		self.game.accum_time=0
		self.game.tick = Clock.schedule_interval(self.game.secondary_loop, 0)
		
	def sprite_has_died(self, sprt):
		if self.game.sprite_space.remaining_npcs() == 0:
			self.game.hud.victory()
			
			Clock.unschedule(self.game.tick)
			self.accum_time = 0
			self.game.tick  = Clock.schedule_interval(self.game.secondary_loop, 0)
		
	def sprite_for_delete(self, sprt):
		self.game.sprite_space.delete_sprt(sprt)	