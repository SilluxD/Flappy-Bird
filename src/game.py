import random
import time

import pygame

from FlappyBird.src.main import SCREEN_HEIGHT, quit_game, get_highscore, set_highscore

# color declaration
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pipe dimensions
PIPE_WIDTH = 80
PIPE_GAP = 225
PIPE_IN_BETWEEN = 450


class Game:
    def __init__(self):
        """Constructor which initializes a Game. A Player and aLevel are created and the current score is set to 0.
        """
        self.player = Player()
        self.level = Level()
        self.finished = False
        self.score = 0

    def play(self, screen, clock):
        """Main loop of the game. The Game will continue until it is finished (the player collides with an obstacle).
         Changes are updated and drawn on the screen.
         """
        my_font = pygame.font.SysFont("monospace", 20)
        while not self.finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN \
                            or event.key == pygame.K_KP_ENTER:
                        self.player.jump()

            # update items in the level
            self.update()

            # draw elements on screen
            self.draw(screen)
            score_label = my_font.render("Score: " + str(self.score), 1, (255, 255, 0))
            screen.blit(score_label, (600, 30))

            # limit to 60 frames per second
            clock.tick(60)

            # update the screen
            pygame.display.flip()

        time.sleep(0.15)
        if self.score > get_highscore():
            set_highscore(self.score)

    def update(self):
        """Update positions of objects in this game. Also check for collision between the player and a pipe.
        The Game will end if the player collides with a pipe.
        """
        self.player.update()
        self.level.update()

        blocks_hit_list = pygame.sprite.spritecollide(self.player, self.level.pipe_list, False)
        if len(blocks_hit_list) != 0:
            self.finished = True

        if self.player.rect.x == self.level.pipe_list.sprites()[0].rect.x + PIPE_WIDTH:
            self.score += 1

    def draw(self, screen):
        """Draw all elements in the game. """
        self.level.draw(screen)
        self.player.draw(screen)


class Player(pygame.sprite.Sprite):
    """Class representing the player in the game. """

    def __init__(self):
        """ Constructor function """
        super().__init__()
        self.falling = 0

        # 60px x 40px
        self.image = pygame.image.load(
            "C:\\Users\\kirdn\\PycharmProjects\\Allerlei\\FlappyBird\\assets\\img\\player.png")
        self.rect = self.image.get_rect()

        self.rect.x = 340
        self.rect.y = 400 - self.rect.height

        # falling speed of the player
        self.change_y = 0

    def draw(self, screen):
        """Draw the player on the screen. """
        screen.blit(self.image, self.rect)

    def update(self):
        """ Move the player. """
        self.falling = self.falling + 1
        # Gravity
        self.calculate_gravity()

        self.rect.y += self.change_y

    def calculate_gravity(self):
        """ Calculate effect of gravity. Player will fall faster the longer he is falling.
        """

        self.change_y += 9 * self.falling / 150

        # Do not fall through the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

        # do not fly out of the top
        if self.rect.y < 0:
            self.rect.y = 0
            self.change_y = 0

    def jump(self):
        """ Called when user hits 'jump'-button. Resets the time falling and jump the player in the air.
        """
        self.falling = 0
        self.change_y = -10


class Pipe(pygame.sprite.Sprite):
    """ Obstacle the player has to avoid hitting."""

    def __init__(self, x, y):
        """ Platform constructor."""
        super().__init__()

        self.image = pygame.image.load(
            "C:\\Users\\kirdn\\PycharmProjects\\Allerlei\\FlappyBird\\assets\\img\\pipe.png")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Level:
    """ Level class which has pipes with varying heights as obstacles. Initially a few are created, and when
    needed new ones are created dynamically.
    """

    def __init__(self):
        """ Constructor which creates a list of pipe objects which are obstacles in the level.
        """
        self.pipe_list = pygame.sprite.Group()
        self.last_pipe = 300
        self.initiate_pipes()

    def initiate_pipes(self):
        """ Initially create some Pipes. """
        for _ in range(10):
            self.create_pipe()

    def create_pipe(self):
        """Create the upper and lower pipes at a fixed distance after the last one.
        Those pipes are then added to the pipe-list.
        """
        upper_pipe_end = random.randrange(50, SCREEN_HEIGHT - (PIPE_GAP + 100))
        bottom_pipe_start = -upper_pipe_end + 350 + PIPE_GAP
        self.last_pipe += PIPE_IN_BETWEEN

        # create Pipe objects and add them to platform list
        self.pipe_list.add(Pipe(self.last_pipe, -upper_pipe_end))
        self.pipe_list.add(Pipe(self.last_pipe, bottom_pipe_start))

    def update(self):
        """ Update everything in this level. """
        self.pipe_list.update()
        self.shift_world(-2)

    def draw(self, screen):
        """ Draw everything on this level. """
        # Draw the background
        screen.fill(BLUE)

        # Draw the pipes
        self.pipe_list.draw(screen)

    def shift_world(self, shift_x):
        """Shift all the pipes further to the left. """
        self.last_pipe += shift_x

        # Go through all the sprite lists and shift
        for pipe in self.pipe_list:
            pipe.rect.x += shift_x
            if pipe.rect.x < -100:
                self.pipe_list.remove(pipe)
                self.create_pipe()
