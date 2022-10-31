"""
"""
from kivy.app import App

from   kivy.uix.floatlayout import FloatLayout # MainWidget
from   kivy.clock           import Clock	   # Schedules
from   kivy.core.window     import Window	  # Keyboard and touch events

from   settings             import *  		 # constant values
import settings             as     settings    # see re_init(). MF should have made a class
import textures			 as 	textures
import ray_caster		   as     ray_caster  # eyes/world probe

from   game_mode			import GameMode
from   graph_manager		import Graph 
from   player               import Player	  # player params
from   world      		  import World	   # walls
from   sprite_space 		import SpriteSpace # sprite manager package
  
from   hud				  import Hud    	 # includes arms, score 
from   map                  import MiniMap	 # map
from   audio				import Audio

import time
#import concurrent.futures not available on android				

class MainWindow(FloatLayout):
	def __init__(self, **kwargs):
		super(MainWindow, self).__init__(**kwargs)
		
		settings.init(self)
		textures.init(self)
		ray_caster.init(self)		
		
		self.gm		   = GameMode(self)
		self.audio		= Audio(self)
		self.graph_mngr   = Graph(self)
		self.player 	  = Player(self)		
		self.world 	   = World(self)
		self.sprite_space = SpriteSpace(self)		
		self.map 		 = MiniMap(self)
		self.hud		  = Hud(self)
		
		self.accum_time   = 0.0	
		self.paused	   = False			
		self.tick	     = Clock.schedule_interval(self.primary_loop, 0)						
		self.bind(size=self.re_init, pos=self.re_init)
					
	def re_init(self, instance, *args): 						
		settings.re_init() 

		self.hud.re_init()		
		self.audio.re_init()
		self.player.re_init()
		self.world.re_init()
		self.sprite_space.re_init()
		self.map.re_init()
						
	def primary_loop(self, dt):
		if self.paused:
			return
					
		self.accum_time += dt
		
		self.hud.update(dt)
		self.player.update(dt)
		self.graph_mngr.update(dt)	
		self.world.update_sky(dt)
		self.sprite_space.update_sprites(dt)

		i_a_d = self.pre_run_prep(dt)
		while True:
			try:
				self.run(next(i_a_d))
			except StopIteration:
				break
		
		""" On PC, use multiprocess! Don't forget to comment out the while loop
		with concurrent.futures.ProcessPoolExecutor() as executor:
			executor.map(self.run, i_a_d)
		"""

		if self.accum_time > DEBUG_TEXT_REFRESH_RATE:
			self.accum_time = 0.0
			self.hud.debug_text = "FPS: {0:.2f}".format(1/dt)
			
	def secondary_loop(self, dt):
		if self.paused:
			return

		self.accum_time += dt

		if self.accum_time >= 1:
			self.clean_up()
	
		if self.accum_time >= 5:
			self.re_init(self)
			
			self.accum_time = 0.0
			self.loop_num   = 1
			self.tick	   = Clock.schedule_interval(self.primary_loop, 0)
	
	def pre_run_prep(self, dt):
		self.sprite_space.get_FOV_s()	
		
		angle_0 = self.player.angle + HALF_FOV	
		return ((idx, angle_0 - DELTA_ANGLE * idx, dt) for idx in range(NUMBER_OF_RAYS))	
			
	def run(self, idx_angle_dt):
		idx, angle, dt = idx_angle_dt
		
		dist, Px, Py, wall, hor = ray_caster.cast_ray_f_player_POV(angle)
		
		self.world.update(	   idx, dist, Px, Py, angle, wall, hor)
		self.sprite_space.update(idx, dist, 		angle)
		
	def clean_up(self):
		self.sprite_space.delete_all_sprts()	

	def quit_game(self):
		App.get_running_app().stop()
						
	def on_touch_down(self, touch):
		self.hud.on_touch_down(touch)
						
	def on_touch_move(self, touch):
		self.hud.on_touch_move(touch)
							
	def on_touch_up(self, touch):
		self.hud.on_touch_up(touch)

class MainApp(App):
	def build(self):
		root = MainWindow()
		root.bind(size=root.re_init,pos=root.re_init)
		return root
		
if __name__ == "__main__":
	MainApp().run()		
		