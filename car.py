import neat
import pygame
import pickle
import math


class Car:
    MAX_ACCELERATION = 5
    MIN_ACCELERATION = 2
    ACCELERATION_STEP = 0.2
    DIRECTION_OFFSET = 5
    DEFAULT = (640, 640)

    def __init__(self, direction, img, screen):
        """Initialize the car with a given direction."""
        self.direction = direction
        self.img = img
        self.speed = 0
        self.original_img = self.img
        self.position = self.DEFAULT  # new attribute
        self.turn_momentum = 0  # new line
        self.width = self.img.get_width()  # new line
        self.height = self.img.get_height() # new line
        

    def on_right(self):
        """Turn the car to the right."""
        self.direction += 3
        self.turn_momentum *= 0.9

    def decelerate(self):
        self.speed -= 0.2  # adjust as needed
        if self.speed < 0:
            self.speed = 0

    def on_left(self):
        """Turn the car to the left."""
        self.direction -= 3
        self.turn_momentum *= 0.9

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

        # calculate the relative positions of the corners of the bounding box
        corners = [(x - car_width / 2, y - car_height / 2) for x in (0, car_width) for y in (0, car_height)]

        # calculate the positions of the corners after rotation and translation
        corners = [self.rotate_point((corner[0] + pos[0], corner[1] + pos[1]), pos, self.direction) for corner in corners]

        # draw a small blue circle at each corner
        for corner in corners:
            pygame.draw.circle(screen, (0, 0, 255), (int(corner[0]), int(corner[1])), 5)

        # check the color of the pixels at the corners
        for corner in corners:
            if screen.get_at((int(corner[0]), int(corner[1]))) == color:
                return True

        return False
    
    def rotate_point(self, point, origin, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in degrees.
        """
        angle = math.radians(angle)
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

        return qx, qy
    
    def is_touching_white(self, screen):
        """Check if any of the car's corners is touching a white pixel."""
        corners = [(0, 0), (self.width, 0), (0, self.height), (self.width, self.height)]
        corners = [self.rotate_point((corner[0] + self.position[0], corner[1] + self.position[1]), self.position, self.direction) for corner in corners]

        for corner in corners:
            x, y = int(corner[0]), int(corner[1])
            if screen.get_at((x, y)) == (255, 255, 255, 255):  # Check if the pixel is white
                return True

        return False
    
    def blit_car(self, screen, position):
        """Draw the car on the screen at the given position."""
        # Rotate the image
        rotated_img = pygame.transform.rotate(self.img, self.direction)

        new_surface = pygame.Surface(rotated_img.get_size(), pygame.SRCALPHA)
        new_surface.fill((0, 0, 0, 0))
        new_surface.blit(rotated_img, (0, 0))
        new_pos = (
            position[0] - new_surface.get_width() / 2,
            position[1] - new_surface.get_height() / 2,
        )
        screen.blit(new_surface, new_pos)

    def update(self, screen):
        # calculate the x and y components of the velocity
        velocity_x, velocity_y = self.get_vector(self.direction, self.speed)

        new_position = (self.position[0] + velocity_x, self.position[1] + velocity_y)

        if self.is_touching_white(screen):
            self.position = self.DEFAULT

        if self.is_touching_color(self.position, (255, 255, 255), screen):
            self.position = self.DEFAULT  # reset position
            return  # exit the update method early

        # calculate the starting position of the ray
        ray_start = (
            self.position[0] + self.width / 2 + velocity_x,
            self.position[1] + self.height / 2 + velocity_y,
        )

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
