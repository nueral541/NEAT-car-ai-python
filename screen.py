import pygame
from car import Car
import math


def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.SRCALPHA)
    clock = pygame.time.Clock()
    return screen, clock


def load_assets():
    background = pygame.image.load("track.png")
    car_img = pygame.transform.scale(pygame.image.load("car.png"), (30, 15))
    return background, car_img


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            return False
    return True


def handle_keys(car):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        car.on_left()
    if keys[pygame.K_LEFT]:
        car.on_right()
    if keys[pygame.K_UP]:
        car.accelerate()
        
def draw_car(screen, car, car_img):
    # Rotate the image
    rotated_img = pygame.transform.rotate(car_img, car.direction)

    new_surface = pygame.Surface(rotated_img.get_size(), pygame.SRCALPHA)
    new_surface.fill((0, 0, 0, 0))
    new_surface.blit(rotated_img, (0, 0))
    new_pos = (
        car.position[0] - new_surface.get_width() / 2,
        car.position[1] - new_surface.get_height() / 2,
    )
    screen.blit(new_surface, new_pos)

def main():
    screen, clock = init_pygame()
    background, car_img = load_assets()
    car = Car(90, car_img, screen)
    
    running = True
    while running:
        running = handle_events()
        handle_keys(car)
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        draw_car(screen, car, car_img)
        car.update(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
