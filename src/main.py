import sys
import threading

from FlappyBird.src.game import *
from FlappyBird.src.ui_elements import Button

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def initiate_view():
    """Initializes pygame and the screen. """
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    return screen


def get_highscore():
    """Read score from file. """
    try:
        infile = open("highscore.txt", "r+", encoding="utf8")
        highscore = str(infile.read())
        if highscore == "" or not highscore.isnumeric():
            infile.write("0")
            highscore = "0"

        return int(highscore)

    except IOError:
        print("An error was found. Either path is incorrect or file doesn't exist!")

    finally:
        infile.close()


def set_highscore(score):
    """Write score to file. """
    try:
        infile = open("highscore.txt", "w", encoding="utf8")
        infile.write(str(score))

    except IOError:
        print("Error when writing to file. Either path is incorrect or file doesn't exist!")

    finally:
        infile.close()


def play_music():
    """Load a sound file in order to play it as background music.
    """
    # not included in this version because I didn't want to deal with licenses or upload other peoples art
    pass  # playsound.playsound("possible path", True)


def main():
    """ Main Program. Initializes the screen and then starts the game.
    """
    screen = initiate_view()
    clock = pygame.time.Clock()

    music_thread = threading.Thread(target=play_music)
    music_thread.setDaemon(True)
    music_thread.start()

    # Create starting screen
    start_screen(screen, clock)


def start_screen(screen, clock):
    """Renders the start screen. The player has the option to start the game or to exit the game.
    """
    play_button = Button(GREEN, 100, 150, 300, 70, "Enter to start")
    exit_button = Button(RED, 450, 150, 250, 70, "Esc to Exit")
    my_font = pygame.font.SysFont("monospace", 20)

    buttons = [play_button, exit_button]

    done = False
    while not done:
        for button in buttons:
            button.draw(screen)
        highscore_label = my_font.render("Highscore: " + str(get_highscore()), 1, (255, 255, 0))
        screen.blit(highscore_label, (600, 50))
        clock.tick(30)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    game = Game()
                    game.play(screen, clock)

                if event.key == pygame.K_ESCAPE:
                    done = True
                    break

    quit_game()


def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
