import pygame
import os

def main_menu_music():
    pygame.mixer.music.load(os.path.join("..\data\music", "Hollow Knight.mp3"))

def first_loc_music():
    pygame.mixer.music.load(os.path.join("..\data\music", "Crossroads.mp3"))