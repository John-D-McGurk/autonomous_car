import pygame as pg

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pg.transform.scale(img, size)

def blit_rotate_center(disp, image, top_left, angle):
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
    disp.blit(rotated_image, new_rect.topleft)