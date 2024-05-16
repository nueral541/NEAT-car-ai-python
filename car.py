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
        corners = [
            (x, y)
            for x in (-car_width / 2, car_width / 2)
            for y in (-car_height / 2, car_height / 2)
        ]

        # calculate the positions of the corners after rotation and translation
        corners = [
            (
                self.position[0] + self.rotate_point(corner, (0, 0), self.direction)[0],
                self.position[1] + self.rotate_point(corner, (0, 0), self.direction)[1],
            )
            for corner in corners
        ]

        # check the color of the pixels within the car's bounding box
        for x in range(
            int(min(corners, key=lambda x: x[0])[0]),
            int(max(corners, key=lambda x: x[0])[0]),
        ):
            for y in range(
                int(min(corners, key=lambda x: x[1])[1]),
                int(max(corners, key=lambda x: x[1])[1]),
            ):
                if screen.get_at((x, y)) == color:
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

    def update(self, screen):
        velocity_x, velocity_y = self.get_vector(self.direction, self.speed)

        new_position = (self.position[0] + velocity_x, self.position[1] + velocity_y)

        self.position = new_position

        self.direction += self.turn_momentum
        self.turn_momentum *= 0.9  # apply some friction to the turn momentum
