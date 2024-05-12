import neat
import pygame
import pickle

class Car:
    def __init__(self, direction):
        self.start_pos = (0, 0)
        self.acceleration = 5
        self.direction = direction
        self.direction_offset = 0

    def on_right(self):
        self.direction_offset = 3

    def on_left(self):
        self.direction_offset = -3

    def accelerate(self):
        if self.acceleration < 10
            self.acceleration = self.acceleration + 0.2

    def deccelerate(self):
        if self.acceleration > 2:
            self.acceleration = self.acceleration - 0.2