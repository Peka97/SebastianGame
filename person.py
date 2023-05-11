import pygame as pg


class PersonLiza(pg.sprite.Sprite):
	anim_meditation = []
	anim_timer = 0
	counter = 0
	counter_direction = 1
	anim_speed = 6

	def __init__(self):
		super().__init__()
		img_1 = pg.image.load('images/lobby/persons/liza/pixel_liza_meditation_1.png').convert_alpha()
		img_2 = pg.image.load('images/lobby/persons/liza/pixel_liza_meditation_2.png').convert_alpha()
		img_3 = pg.image.load('images/lobby/persons/liza/pixel_liza_meditation_3.png').convert_alpha()
		img_4 = pg.image.load('images/lobby/persons/liza/pixel_liza_meditation_4.png').convert_alpha()
		self.anim_meditation.extend((
			img_1,
			img_2,
			img_3,
			img_4
		))

		self.image = self.anim_meditation[0]
		self.rect = self.image.get_rect(topleft=(890, 447))

	def meditation_animation(self):
		max_counter = len(self.anim_meditation) - 1
		if self.anim_timer % self.anim_speed == 0:
			if self.counter == max_counter:
				self.counter_direction = -1
			elif self.counter == 0:
				self.counter_direction = 1
			self.image = self.anim_meditation[self.counter]
			self.counter += self.counter_direction
		self.anim_timer += 1
		print(self.counter, self.anim_timer, -max_counter)
