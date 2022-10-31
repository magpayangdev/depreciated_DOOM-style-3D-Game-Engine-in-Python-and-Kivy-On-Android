"""
"""

from kivy.core.audio import SoundLoader

class Audio:
	def __init__(self, game):
		self.game = game
		self.gun_fire = SoundLoader.load('resources/sound/shotgun.wav')
		self.gun_fire.volume = 0.5
		
		self.npc_atk = SoundLoader.load('resources/sound/npc_attack.wav')
		self.npc_atk.volume = 0.2
		
		self.player_hit = SoundLoader.load("resources/sound/player_pain.wav")
		self.player_hit.volume = 1
		
		self.npc_hit = SoundLoader.load('resources/sound/npc_pain.wav')
		self.npc_hit.volume = 0.2

		self.theme = SoundLoader.load('resources/sound/theme.mp3')
		self.theme.volume = 0.2
		self.theme.loop = True
		
		self.pause_start = SoundLoader.load('resources/sound/pause_start.wav')

	def re_init(self):
		self.theme.play()
	
	def update(self, dt):
		pass
		
	def player_attack(self):
		self.gun_fire.play()
		
	def hit(self, id='npc'):
		if id is 'player':
			self.player_hit.play()
			
		elif id is 'npc':
			self.npc_hit.play()
		
	def attack(self, id='npc'):
		if id is 'player':
			self.gun_fire.play()
			
		elif id is 'npc':
			self.npc_atk.play()
			
	def pause_game(self):
		self.pause_start.play()
		
	def play_theme(self):
		self.theme.play()
		
	def stop_theme(self):
		self.theme.stop()