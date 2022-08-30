import pygame
import sys

# Set up the colors.
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
LIME = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


def play():
    # Set up pygame.
    pygame.init()

    # Set up the window.
    windowSurface = pygame.display.set_mode((500, 400), 0, 32)
    pygame.display.set_caption("Hello world!")

    # Set up the fonts.
    basicFont = pygame.font.SysFont(None, 48)

    # Set up the text.
    text = basicFont.render("Hello world!", True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery

    # Draw the white background onto the surface.
    windowSurface.fill(WHITE)

    # Draw a green polygon onto the surface.
    pygame.draw.polygon(
        windowSurface, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106))
    )

    # Draw some blue lines onto the surface.
    pygame.draw.line(windowSurface, BLUE, (60, 60), (120, 60), 4)
    pygame.draw.line(windowSurface, BLUE, (120, 60), (60, 120))
    pygame.draw.line(windowSurface, BLUE, (60, 120), (120, 120), 4)

    # Draw a blue circle onto the surface.
    pygame.draw.circle(windowSurface, BLUE, (300, 50), 20, 0)

    # Draw a red ellipse onto the surface.
    pygame.draw.ellipse(windowSurface, RED, (300, 250, 40, 80), 1)

    # Draw the text's background rectangle onto the surface.
    pygame.draw.rect(
        windowSurface,
        RED,
        (
            textRect.left - 20,
            textRect.top - 20,
            textRect.width + 40,
            textRect.height + 40,
        ),
    )
    # Get a pixel array of the surface.
    pixArray = pygame.PixelArray(windowSurface)
    pixArray[480][380] = BLACK
    del pixArray

    # Draw the text onto the surface.
    windowSurface.blit(text, textRect)

    # Draw the window onto the screen.
    pygame.display.update()

    # Run the game loop.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def main():
    play()


if __name__ == "__main__":
    main()
