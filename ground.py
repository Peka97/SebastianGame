import pygame as pg


class Ground(pg.sprite.Sprite):
	def __init__(self, screen):
		super().__init__()
<<<<<<< HEAD
		self.image = pg.image.load('images/lobby/floor.png').convert_alpha()
=======
		self.image = pg.image.load('images/grounds/debug_ground.png')
>>>>>>> dev
		screen_weight, screen_height = screen.get_size()
		image_weight, image_height = self.image.get_size()
		self.rect = self.image.get_rect(topleft=(0, screen_height - image_height / 2))
