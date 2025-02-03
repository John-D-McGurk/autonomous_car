import pygame as pg
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import sys

import util

def get_track(path):
    # Consider adding other options to convert non black-white tracks. See track_convert.py
    image = cv2.imread('tracks/track1.png')  # Replace with your track image path

    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    image = cv2.flip(image, 1)

    return image

def draw_track(track_image):
    track_surface = pg.surfarray.make_surface(track_image)
    
    return track_surface

TRACK = get_track('tracks/track1.png')
TRACK_SURF = draw_track(TRACK)

CAR = util.scale_image(pg.image.load('cars/car.png'), 0.1)

DISP = pg.display.set_mode((TRACK.shape[0], TRACK.shape[1]))
FPS = 60


class AbstractCar:
    def __init__(self, angle=0, max_vel=10, rotation_vel=3, length=30, max_accel = 0.2, max_decel = 0.5):
        self.img = self.IMG
        # CENTER IS CURRENTLY TOP LEFT
        self.center = self.START_POS
        self.length = length
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.angle=angle
        self.vel = 0
        self.max_accel = max_accel
        self.max_decel = max_decel
        
    def rotate(self, left=0, right=0):
        if left:
            self.angle -= self.rotation_vel * left
        elif right:
            self.angle += self.rotation_vel * right

    def accelerate(self, forward=0, backward=0):
        if forward:
            if self.vel < self.max_vel:
                self.vel += forward * self.max_accel
            else:
                self.vel = self.max_vel
        if backward:
            if self.vel > 0:
                self.vel -= backward * self.max_decel
            else:
                self.vel = 0
                
    def draw(self, disp):        
        self.center += pg.Vector2.from_polar((self.vel, self.angle))
        util.blit_rotate_center(disp, self.img, self.center, -self.angle - 90)

class PlayerCar(AbstractCar):
    IMG = CAR
    START_POS = pg.Vector2(0,0)


def draw(disp):
    player_car.draw(disp)

pg.init()
player_car = PlayerCar(angle=90)

run = True
clock = pg.time.Clock()

joystick = None
if pg.joystick.get_count() > 0:
    joystick = pg.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick found!")

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run= False

    keys = pg.key.get_pressed()

    if keys[pg.K_a]:
        player_car.rotate(left=1)
    elif keys[pg.K_d]:
        player_car.rotate(right=1)
    elif keys[pg.K_w]:
        player_car.accelerate(forward=1)
    elif keys[pg.K_s]:
        player_car.accelerate(backward=1)
    if joystick:
        # Get joystick axis values (continuous reading)
        steer = joystick.get_axis(3)  # Right stick X-axis
        throttle = joystick.get_axis(5)  # R2 Trigger
        brake = joystick.get_axis(2)  # L2 Trigger

        # **Steering**
        if abs(steer) > 0.1:  # Dead zone filtering
            if steer > 0:
                player_car.rotate(right=steer)
            else:
                player_car.rotate(left=-steer)

        # **Acceleration & Braking**
        if throttle > -1:
            player_car.accelerate(forward=(throttle + 1) / 2)  # Normalize to 0-1
        if brake > -1:
            player_car.accelerate(backward=(brake + 1) / 2)  # Normalize to 0-1





    # Draw the track image as the background
    DISP.blit(TRACK_SURF, (0, 0))

    draw(DISP)

    # Update the display
    pg.display.update()    
    clock.tick(FPS)

pg.quit()
sys.exit()