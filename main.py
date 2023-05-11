from ctypes import windll
import os

import pygame
import pygame as pg


from cat import Cat
from person import PersonLiza
from ground import Ground


class Game:
	def __init__(self):
		# Base
		pg.init()
		os.environ['SDL_VIDEO_CENTERED'] = '1'

		self.WINDOW_WEIGHT = windll.user32.GetSystemMetrics(0)
		self.WINDOW_HEIGHT = windll.user32.GetSystemMetrics(1)
		self.is_running = True
		self.display = pg.display
		self.fullscreen = False
		self.screen = self.display.set_mode((self.WINDOW_WEIGHT, self.WINDOW_HEIGHT))
		self.display.set_caption('The Adventures of Sebastian')

		self.bg = pg.image.load('images/lobby/pixel-room.jpg').convert_alpha()
		self.bg = pg.transform.scale(self.bg, (self.screen.get_size()))
		self.clock = pg.time.Clock()
		self.FPS = 30

		# Colors
		self.menu_color = (224, 255, 255)
		self.bg_color = (100, 100, 100)

		# Objects
		self.cat = Cat()
		self.liza = PersonLiza()

		self.ground = Ground(self.screen)

		# Groups
		self.all_sprites = pg.sprite.Group(self.cat, self.ground)
		self.sprites_for_drawing = pg.sprite.Group(self.liza, self.cat)
		self.grounds = pg.sprite.Group(self.ground)

	def main_loop(self):
		while self.is_running:

			# Filling background
			self.screen.blit(self.bg, (0, 0))
			keys = pg.key.get_pressed()

			# Handler for hold keys
			if keys[pg.K_SPACE]:
				self.cat.is_prepared_to_jump = True
				if self.cat.jump_power < self.cat.jump_power_limit:
					self.cat.jump_power += 0.7
					if self.cat.jump_power < 1:
						self.cat.counter = 0
					if round(self.cat.jump_power) % 5 == 0 and self.cat.counter < 3:
						self.cat.counter += 1
				else:
					self.cat.jump_power = 15
			if keys[pg.K_LSHIFT]:
				self.cat.speed = 20

			# Handlers
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.is_running = False

				if event.type == pg.KEYDOWN:
					if event.key in [pg.K_d, pg.K_a]:
						self.cat.prev_direction = self.cat.direction
						if event.key == pg.K_d:
							self.cat.direction = 'right'
						elif event.key == pg.K_a:
							self.cat.direction = 'left'

						self.cat.anim_timer = 0
						self.cat.counter = 0

					if event.key == pg.K_F1:
						self.switch_fullscreen_mode()

				if event.type == pg.KEYUP:
					if event.key in (pg.K_a, pg.K_d):
						self.cat.prev_direction = self.cat.direction
						self.cat.direction = None
					if event.key == pg.K_SPACE:
						self.cat.is_jump = True
						self.cat.is_prepared_to_jump = False

					self.cat.anim_timer = 0
					self.cat.counter = 0

					if event.key == pg.K_LSHIFT:
						self.cat.speed = 10

			# Animation and move of objects
			collide = pg.sprite.spritecollide(self.cat, self.grounds, False)
			if collide:
				self.cat.is_falling = False

			if self.cat.direction is None and self.cat.jump_power == 0:
				self.cat.sit_back_animation()
			elif self.cat.jump_power > 0 and not self.cat.is_jump and self.cat.is_prepared_to_jump:
				self.cat.ready_to_jump_animation()
			else:
				self.cat.move(self.screen)
				self.cat.move_animation()

			self.cat.fall(collide)
			self.cat.jump()

			self.liza.meditation_animation()

			# PyGame Draw
			self.all_sprites.update()
			self.sprites_for_drawing.draw(self.screen)

			self.clock.tick(self.FPS)
			pg.display.update()

	def switch_fullscreen_mode(self):
		if self.fullscreen:
			os.environ['SDL_VIDEO_CENTERED'] = '1'
			self.WINDOW_WEIGHT = windll.user32.GetSystemMetrics(0) * 2 / 3
			self.WINDOW_HEIGHT = windll.user32.GetSystemMetrics(1) * 2 / 3
			self.fullscreen = False
			self.screen = self.display.set_mode((self.WINDOW_WEIGHT, self.WINDOW_HEIGHT))
			self.ground = Ground(self.screen)

		else:
			os.environ['SDL_VIDEO_CENTERED'] = '1'
			self.WINDOW_WEIGHT = windll.user32.GetSystemMetrics(0)
			self.WINDOW_HEIGHT = windll.user32.GetSystemMetrics(1)
			self.fullscreen = True
			self.screen = self.display.set_mode((0, 0), pygame.FULLSCREEN)
			self.ground = Ground(self.screen)


if __name__ == '__main__':
	game = Game()
	game.main_loop()
