import pygame

from car import Car

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

background = pygame.image.load("track.png")

car_img = pygame.transform.scale(pygame.image.load("car.png"), (30, 15))
car = Car(90, car_img, screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        car.on_right()
    if keys[pygame.K_LEFT]:
        car.on_left()
    if keys[pygame.K_UP]:
        car.accelerate()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    screen.blit(background, (0, 0))

    car.update(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
