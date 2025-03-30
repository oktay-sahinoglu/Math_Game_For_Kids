#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from game import Game
from argparse import ArgumentParser

def main(bg_image_id):
    # Initialize all imported pygame modules
    pygame.init()
    # Get the width and height of the background
    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.image.load("background1.jpg" if bg_image_id == 1 else "background2.png").get_size()
    # Set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # Set the current window caption
    pygame.display.set_caption("Math Game for Kids")
    #Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Create game object
    game = Game(bg_image_id)
    # -------- Main Program Loop -----------
    while not done:
        # --- Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
        # --- Draw the current frame
        game.display_frame(screen)
        # --- Limit to 30 frames per second
        clock.tick(30)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-bg', '--background', help='Choose the background image alternavies. Possible values: [1,2].', type=int, choices=[1,2], default=1)
    opts = parser.parse_args()
    main(opts.background)
