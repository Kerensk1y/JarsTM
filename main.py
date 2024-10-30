"""
Расхардкодить координаты банок;
Добавить потери энергии и ускорить падение;
Добавить изменение цвета шарика в банке;
Стикер с текстом на банке;
Класс Button;
Добавить кнопку создания JAR`ов;
Схема добавления новых банок;
Функция выбора банки;
"""

import pygame
import sys
import math
import numpy as np

pygame.init()
screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("JarsTM")
# g = 9.81
g = 500
energy_loss = math.sqrt(0.5)
pygame.font.init() # you have to call this at the start,

class Objects:
    jar_color = (128, 128, 128, 25)  # Серый с альфа-каналом для прозрачности
    jar_outline_color = (50, 50, 50, 145)  # Цвет линии края
    ball_color = (255, 228, 26)  # Цвет шара
    ball_outline_color = (0, 0, 0)  # Контур шара

class Ball(Objects):
    "Класс для создания шариков"
    def __init__(self, x, y, bottom, surface: screen):
        self.x = x
        self.y = y
        self.surface = surface
        self.radius = 10
        self.vy = 0
        self.bottom = bottom - 2
        self.color = Objects.ball_color
        self.outline_color = Objects.ball_outline_color
        self.ball_radius = 10  # радиус шара в пикселях

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, self.outline_color, (self.x, self.y), self.radius, 1)

    @staticmethod
    def get_energy_loss():
        # Функция вычисляет рандомом потери энергии шара при падении
        numbers = np.arange(30.0, 60.1, 0.1)
        mean = np.mean(numbers)
        std_dev = np.std(numbers)
        energy_loss = np.random.normal(loc=mean, scale=std_dev)
        print(energy_loss)
        if energy_loss < 30.0:
            energy_loss = 30.0
        elif energy_loss > 60.0:
            energy_loss = 60.0

        return energy_loss

    def update(self, dt):
        # Обновляем скорость и позицию
        self.vy += g * dt  # обновляем скорость
        self.y += self.vy * dt  # обновляем позицию

        # Проверяем столкновение с землей
        if self.y >= self.bottom - self.radius:
            self.y = self.bottom - self.radius
            energy_loss = 1 - self.get_energy_loss()/100
            self.vy = -self.vy * energy_loss # меняем направление скорости (отскок) и вычитаем потерю энергии


class Jar(Objects):
    "Класс для создания банок"
    def __init__(self, name, ltx, lty, surface: screen):
        self.ltx = ltx
        self.lty = lty
        self.name = name
        self.surface = surface
        self.color = Objects.jar_color
        self.outline_color = Objects.jar_outline_color
        self.rect = pygame.Rect(ltx, lty, 120, 150)
        self.rect_n = pygame.Rect(ltx + 5, lty - 15, 110, 20)

    def draw(self):
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 20)
        # основание банки
        jar_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(jar_surface, self.color, (0, 0, self.rect.width, self.rect.height), border_radius=30)
        pygame.draw.rect(jar_surface, self.outline_color, (0, 0, self.rect.width, self.rect.height), width=2, border_radius=30)
        text_surface = my_font.render(self.name, False, (0, 0, 0))
        # горлышко
        neck_surface = pygame.Surface((self.rect_n.width, self.rect_n.height), pygame.SRCALPHA)
        pygame.draw.rect(neck_surface, self.color, (0, 0, self.rect_n.width, self.rect_n.height), border_radius=20)
        pygame.draw.rect(neck_surface, self.outline_color, (0, 0, self.rect_n.width, self.rect_n.height), width=2, border_radius=20)

        self.surface.blit(jar_surface, self.rect.topleft)
        self.surface.blit(neck_surface, self.rect_n.topleft)
        self.surface.blit(text_surface, (0,0))


pygame.init()
clock = pygame.time.Clock()

running = True
j = Jar('xxx', 100, 100, screen)
b = Ball(160, 50, 250, screen)  # создайте шарик вне цикла, чтобы постоянно обновлять его
start_motion = True  # для запуска движения

while running:
    dt = clock.tick(60) / 1000.0  # длительность кадра в секундах (60 FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отрисовка
    screen.fill('white')

    if start_motion:
        # j.draw()
        b.update(dt)  # обновляем координаты и скорость шарика
        b.draw()  # отрисовываем шарик
        j.draw()

    pygame.display.flip()

pygame.quit()

pygame.quit()
sys.exit()
