import neat
import pygame
import pickle

class Car:
    MAX_ACCELERATION = 5
    MIN_ACCELERATION = 2
    ACCELERATION_STEP = 0.2
    DIRECTION_OFFSET = 5
    DEFAULT = (640, 640)

    def __init__(self, direction, img, screen):
        """Initialize the car with a given direction."""
        self.start_pos = (0, 0)
        self._acceleration = 5
        self.direction = direction
        self.direction_offset = 0
        self.img = img
        self.original_img = self.img
        self.turn_momentum = 0  # new attribute
        self.speed = 0  # new attribute
        self.position = self.DEFAULT  # new attribute
        self.width = img.get_width()  # new attribute
        self.height = img.get_height()  # new attribute

    def blit_car(self, screen, pos):
        """Draw the car on the screen at the given position."""
        # create a new surface with the same size as the original image and per-pixel alpha
        new_surface = pygame.Surface(self.original_img.get_size(), pygame.SRCALPHA)

        # fill the new surface with a transparent color
        new_surface.fill((0, 0, 0, 0))

        # blit the original image onto the new surface
        new_surface.blit(self.original_img, (0, 0))

        # rotate the new surface and get its rectangle
        rotated_image = pygame.transform.rotate(new_surface, self.direction)
        rotated_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=pos).center
        )

        # draw the rotated image at the adjusted position
        screen.blit(rotated_image, rotated_rect.topleft)

    @property
    def acceleration(self):
        """Get the current acceleration."""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        """Set the acceleration, ensuring it stays within the desired range."""
        if self.MIN_ACCELERATION <= value <= self.MAX_ACCELERATION:
            self._acceleration = value

    def on_right(self):
        """Turn the car to the right."""
        self.turn_momentum += 0.4

    def on_left(self):
        """Turn the car to the left."""
        self.turn_momentum -= 0.4

    def accelerate(self):
        if self.speed < self.MAX_ACCELERATION:
            self.speed += 1

    def get_vector(self, direction, value):
        """Get the x and y components of a vector given a direction and magnitude."""
        # convert the direction to radians
        direction_rad = math.radians(direction)

        # calculate the x and y components
        x = value * math.cos(direction_rad)
        y = -value * math.sin(
            direction_rad
        )  # negate y because Pygame's y axis points downwards

        return (x, y)

    def is_touching_color(self, pos, color, screen):
        # get the size of the car's image
        car_width, car_height = self.img.get_size()

        # calculate the car's bounding box
        left = max(int(pos[0]), 0)
        right = min(int(pos[0]) + car_width, screen.get_width())
        top = max(int(pos[1]), 0)
        bottom = min(int(pos[1]) + car_height, screen.get_height())

        # check the color of the pixels within the car's bounding box
        for x in range(left, right):
            for y in range(top, bottom):
                if screen.get_at((x, y)) == color:
                    return True

        return False

    def update(self, screen):
        """Update the car's position and direction."""
        # calculate the x and y components of the velocity
        velocity_x, velocity_y = self.get_vector(self.direction, self.speed)

        # update the position
        new_position = (self.position[0] + velocity_x, self.position[1] + velocity_y)

        if self.is_touching_color(self.position, (255, 255, 255), screen):
            self.position = (0, 0)  # reset position
            return  # exit the update method early

        # check if the new position is outside the screen boundaries
        screen_width, screen_height = screen.get_size()
        if new_position[0] < 0:
            new_position = (0, new_position[1])
        elif new_position[0] > screen_width - self.width:
            new_position = (screen_width - self.width, new_position[1])
        if new_position[1] < 0:
            new_position = (new_position[0], 0)
        elif new_position[1] > screen_height - self.height:
            new_position = (new_position[0], screen_height - self.height)

        self.position = new_position

        self.blit_car(screen, self.position)
        self.direction += (
            self.turn_momentum
        )  # update the direction based on the momentum
        self.turn_momentum *= 0.9  # decrease the momentum over time
        self.speed *= 0.9  # decrease the speed over time (simulate friction)
