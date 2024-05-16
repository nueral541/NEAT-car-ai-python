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

    
    touching_color = car.is_touching_color(car.position, (255, 255, 255), screen)

    if touching_color:
            car.position = car.DEFAULT  # reset position
              # exit the update method early

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        car.on_left()
    if keys[pygame.K_LEFT]:
        car.on_right()
    if keys[pygame.K_UP]:
        car.accelerate()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    screen.blit(background, (0, 0))

    car.update(screen)

    # Create a new surface with the same size as the mask
    mask_surface = pygame.Surface(car.car_mask.get_size())

    # Fill the surface with a color
    mask_surface.fill((255, 0, 0))  # Red color

    # Set the color key of the surface to make the parts of the surface that are not in the mask transparent
    mask_surface.set_colorkey((0, 0, 0))

    # Get the size of the mask
    mask_width, mask_height = car.car_mask.get_size()

    # Iterate over each pixel in the mask
    for x in range(mask_width):
        for y in range(mask_height):
            # If the pixel is not in the mask, set it to the color key
            if not car.car_mask.get_at((x, y)):
                mask_surface.set_at((x, y), (0, 0, 0))

    # Blit the surface onto the screen at the car's position
    screen.blit(mask_surface, car.position)

    # flip() the display to put your work on screen
    pygame.display.flip()
    
    clock.tick(60)  # limits FPS to 60

pygame.quit()
