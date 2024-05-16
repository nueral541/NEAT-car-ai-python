import pygame
import random
pygame.init()

clock = pygame.time.Clock()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

class Box:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, 500)
        self.rect = pygame.Rect(self.x, self.y, 1, 5)
        self.surf = pygame.Surface((self.rect.width, self.rect.height))
        self.surf.fill((255, 255, 255))
        self.angle = 0

    def draw(self, win):
        self.angle += 5
        self.surf = pygame.Surface(self.rect.size).convert_alpha()
        self.rot_surf = pygame.transform.rotate(self.surf, round(self.angle))
        self.rot_surf.fill((255, 255, 255))
        win.blit(self.rot_surf, (self.rect.x, self.rect.y))


boxes = []

for i in range(0, 10):
    boxes.append(Box())

running = True
while running:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    screen.fill((0, 0, 0))
    for i in boxes:
        i.draw(screen)

    pygame.display.flip()