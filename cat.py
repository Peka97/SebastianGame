import pygame as pg
import pymunk as pm


class Cat(pg.sprite.Sprite):
	anim_move_left = []
	anim_move_right = []
	anim_sit_forward = []
	anim_sit_back = []
	anim_sit_and_breath = []
	anim_jump_ready_right = []
	anim_jump_ready_left = []
	anim_timer = 0
	counter = 0
	speed = 10
	gravity = 8
	prev_direction = None
	direction = None
	jump_power = 0
	jump_power_limit = 15
	is_falling = True
	is_jump = False
	is_prepared_to_jump = False

	def __init__(self):
		super().__init__()
		# Загружаем картинки
		img_sit_back_1 = pg.image.load('images/cat/sit_back_1.png').convert_alpha()
		img_sit_back_2 = pg.image.load('images/cat/sit_back_2.png').convert_alpha()
		img_sit_back_3 = pg.image.load('images/cat/sit_back_3.png').convert_alpha()

		img_sit_and_breath_1 = pg.image.load('images/cat/sit_back_and_breath_1.png').convert_alpha()
		img_sit_and_breath_2 = pg.image.load('images/cat/sit_back_and_breath_2.png').convert_alpha()

		img_move_left_1 = pg.image.load('images/cat/move_left_1.png').convert_alpha()
		img_move_left_2 = pg.image.load('images/cat/move_left_2.png').convert_alpha()
		img_move_left_3 = pg.image.load('images/cat/move_left_3.png').convert_alpha()

		img_move_right_1 = pg.image.load('images/cat/move_right_1.png').convert_alpha()
		img_move_right_2 = pg.image.load('images/cat/move_right_2.png').convert_alpha()
		img_move_right_3 = pg.image.load('images/cat/move_right_3.png').convert_alpha()

		img_jump_ready_right_1 = pg.image.load('images/cat/jump_ready_right_1.png').convert_alpha()
		img_jump_ready_right_2 = pg.image.load('images/cat/jump_ready_right_2.png').convert_alpha()
		img_jump_ready_right_3 = pg.image.load('images/cat/jump_ready_right_3.png').convert_alpha()

		img_jump_ready_left_1 = pg.image.load('images/cat/jump_ready_left_1.png').convert_alpha()
		img_jump_ready_left_2 = pg.image.load('images/cat/jump_ready_left_2.png').convert_alpha()
		img_jump_ready_left_3 = pg.image.load('images/cat/jump_ready_left_3.png').convert_alpha()

		# Формируем коллекции для анимации
		self.anim_sit_back.extend((
			img_sit_back_2,
			img_sit_back_3,
			img_sit_back_2,
			img_sit_back_1,
			img_sit_back_2
		))
		self.anim_sit_and_breath.extend((
			img_sit_back_2,
			img_sit_and_breath_1,
			img_sit_and_breath_2,
			img_sit_and_breath_1,
			img_sit_back_2,
		))
		self.anim_move_left.extend((
			img_move_left_1,
			img_move_left_2,
			img_move_left_3,
			img_move_left_2,
		))
		self.anim_move_right.extend((
			img_move_right_1,
			img_move_right_2,
			img_move_right_3,
			img_move_right_2
		))
		self.anim_jump_ready_right.extend((
			img_move_right_2,
			img_jump_ready_right_1,
			img_jump_ready_right_2,
			img_jump_ready_right_3
		))
		self.anim_jump_ready_left.extend((
			img_move_left_2,
			img_jump_ready_left_1,
			img_jump_ready_left_2,
			img_jump_ready_left_3
		))

		# Удаляем фон
		color_key = img_sit_back_1.get_at((0, 0))
		for img in self.anim_sit_back:
			img.set_colorkey(color_key)
		for img in self.anim_move_right:
			img.set_colorkey(color_key)
		for img in self.anim_move_left:
			img.set_colorkey(color_key)

		# Выставляем параметры спрайта
		self.image = self.anim_sit_back[0]
		self.rect = self.image.get_rect(topleft=(530, 400))

	def move(self, screen):
		screen_weight, screen_height = screen.get_size()
		cat_weight, _ = self.image.get_size()
		cat_weight += 18
		if self.direction:
			if self.direction == 'right' and self.rect.x + cat_weight < screen_weight:
				self.rect.x += self.speed
			elif self.direction == 'left' and self.rect.x - cat_weight // 2 > 0:
				self.rect.x -= self.speed

	def sit_back_animation(self):
		if self.anim_timer > 100:
			if self.anim_timer == 170:
				self.anim_timer = 0
				self.counter = 0
				return
			elif self.anim_timer % 5 == 0 and 125 <= self.anim_timer < 146:
				max_len = len(self.anim_sit_and_breath)
				if self.counter == max_len:
					self.counter = 0
				self.image = self.anim_sit_and_breath[self.counter]
				self.counter += 1
			self.anim_timer += 1
		elif self.anim_timer % 5 == 0 and (
				0 <= self.anim_timer < 21 or 40 <= self.anim_timer < 61 or 80 <= self.anim_timer < 101):
			max_len = len(self.anim_sit_back)
			if self.counter == max_len:
				self.counter = 0
			self.image = self.anim_sit_back[self.counter]
			self.anim_timer += 1
			self.counter += 1
		else:
			self.anim_timer += 1

	def move_animation(self):
		images = self.anim_move_right if self.direction == 'right' else self.anim_move_left
		if self.anim_timer % 5 == 0:
			max_len = len(self.anim_move_right)
			if self.counter == max_len:
				self.counter = 0
			try:
				self.image = images[self.counter]
			except IndexError:
				self.counter = 0
				self.image = images[self.counter]
			self.counter += 1
		self.anim_timer += 1

	def ready_to_jump_animation(self):
		if self.direction:
			animation = self.anim_jump_ready_left if self.direction == 'left' else self.anim_jump_ready_right
		else:
			animation = self.anim_jump_ready_left if self.prev_direction == 'left' else self.anim_jump_ready_right

		if self.jump_power * 100 % 30 == 0:
			max_len = len(animation) - 1
			self.image = animation[self.counter]
			if self.counter < max_len:
				self.counter += 1

	def fall(self, collide: list):
		if self.is_falling:
			self.rect.y += (self.gravity ** 2) / 2
			self.gravity += 1
		if collide and self.rect.y >= collide[0].rect.y - self.image.get_size()[1]:
			self.rect.y = collide[0].rect.y - self.image.get_size()[1]
			self.gravity = 8
			self.is_falling = False

	def jump(self):
		if self.is_jump is True:
			if self.jump_power > 0:
				self.rect.y -= (self.jump_power ** 2) / 2
				self.jump_power -= 1
			else:
				self.is_jump = False
				self.is_falling = True
				self.jump_power = 0
