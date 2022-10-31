"""
textures
"""
from kivy.core.image import Image
import os
from settings import *

""" image caches """
_controller_icons	 = None
_map_icons			= None
_wall_textures		= None
_sky_textures		 = None
_digit_textures	   = None
_menu_textures=None

_image_sequences 	 = {}

	
def init(game_ref):
	global _controller_icons, _map_icons, _wall_textures, _sky_textures, _digit_textures, _menu_textures
	global _image_sequences
	
	_controller_icons = get_textures(PATH_CONTROLLER_ICONS, True,  False)
	_map_icons		= get_textures(PATH_MAP_ICONS,		True,  False)
	_wall_textures    = get_textures(PATH_WALL_TEXTURES,	True,  False)
	_sky_textures	 = get_textures(PATH_SKY_TEXTURES,	 False, True)
	_digit_textures   = get_textures(DIGIT_TEXTURES,		True,  False)
	_menu_textures=get_textures(MENU_TEXTURES,True,False)
							   	  
	for key in SPRITE_ID_TO_IMAGES_PATH:
		_image_sequences[key] = tuple([get_images(path, True, False) 
									   for i, path in enumerate(SPRITE_ID_TO_IMAGES_PATH[key]) 
									   if path != EMPTY_PATH])
									   
def re_init():
	pass			

def get_filenames(path, tantrum='Invalid path!'):
	if os.path.isdir(path):	  pass
	elif os.path.isfile(path):   path = path.rsplit('/', 1)[0]
	else:						raise Exception(tantrum)
	return path, [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]	
			
def get_textures(path, mipmap=True, repeat=False, tantrum='Invalid path!'):
	path, file_names = get_filenames(path, tantrum)
	if repeat:
		set = {name: Image(os.path.join(path, name), mipmap=mipmap).texture for name in file_names}
		for key in set.keys():
			 set[key].wrap = 'repeat'
		return set
	 
	return {name: Image(os.path.join(path, name), mipmap=mipmap).texture for name in file_names}
	
def get_images(path, mipmap=True, repeat=False, tantrum='Invalid path!'):
	path, file_names = get_filenames(path, tantrum)
	
	if repeat:
		list = tuple(Image(os.path.join(path,file_name),mipmap=mipmap).texture for file_name in file_names)
		for image in list:
			image.wrap = 'repeat'
		return list
	
	return tuple(Image(os.path.join(path,file_name),mipmap=mipmap).texture for file_name in file_names)


###############[GETTERS]#####################
def get_controller_texture(str="dotted_circle"):
	return _controller_icons.get("{}{}".format(str, '.png'))

def get_wall_texture(str="1"):
	return _wall_textures.get("{}{}".format(str, '.png'), _wall_textures.get('1.png'))
	
def get_sky_texture(str="sky"):
	return _sky_textures.get("{}{}".format(str, '.png'))
	
def get_map_texture(str="brick_wall.png"):
	return _map_icons.get("{}{}".format(str, '.png'))
	
def get_digit_texture(str='0'):
	return _digit_textures.get("{}{}".format(str, '.png'))
	
def get_menu_texture(str='victory'):
	return _menu_textures.get('{}{}'.format(str, '.png'))
	
def get_image_sequence(id='npc', action_type='idle'):
	""" Returns a tuple of image texture sequences based on id and action type """
	if id in _image_sequences:
		if action_type == 'idle':
			return _image_sequences.get(id)[0]
			
		elif action_type == 'walk':
			try:
				return _image_sequences.get(id)[1]
			except:
				return _image_sequences.get(id)[0]
			
		elif action_type == 'hit':
			try:
				return _image_sequences.get(id)[2]
			except:
				return _image_sequences.get(id)[0]
							
		elif action_type == 'attack':
			try:
				return _image_sequences.get(id)[3]
			except:
				return _image_sequences.get(id)[0]
			
		elif action_type == 'death':
			try:
				return _image_sequences.get(id)[4]
			except:
				return _image_sequences.get(id)[0]
			
		else:
			raise Exception("Invalid action type {}. Must be type: idle, walk, hit, attack, death".format(action_type))
	else:
		raise Exception("Invalid id: {}".format(id))		

	
		
			
				
					
							