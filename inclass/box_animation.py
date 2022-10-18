import sys
import time

import pygame


class Vector:
    def __init__(self, vx, vy):
        self.vx, self.vy = vx, vy

    def __repr__(self):
        return f"Vector({self.vx}, {self.vy})"

    def __add__(self, other):
        return Vector(self.vx + other.vx, self.vy + other.vy)

    def __sub__(self, other):
        return self + -other

    def __neg__(self):
        return Vector(-self.vx, -self.vy)

    def __mul__(self, k):
        return Vector(k * self.vx, k * self.vy)

    def __rmul__(self, k):
        return self.__mul__(k)

    def __eq__(self, other):
        return self.vx == other.vx and self.vy == other.vy

    @staticmethod
    def run_tests():
        v1 = Vector(vx=10, vy=0)
        v2 = Vector(vx=0, vy=5)

        vsum = v1 + v2
        vsub = v1 - v2
        vmul = v1 * 3
        vmulr = 3 * v1
        neg_v1 = -v1
        neg_v2 = -v2

        print(f"{v1} + {v2} = {vsum}")
        print(f"{v1} - {v2} = {vsub}")
        print(f"-{v1} = {neg_v1}")
        print(f"-{v2} = {neg_v2}")
        print(f"3 * {v1} = {vmulr}")
        print(f"{v1} * 3 = {vmul}")


MOVESPEED = 4

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def play():
    pygame.init()

    WINDOWWIDTH = 400
    WINDOWHEIGHT = 400
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption("Animation")

    b1 = {"rect": pygame.Rect(300, 80, 50, 100), "color": RED, "dir": Vector(1, -1)}
    b2 = {"rect": pygame.Rect(200, 200, 20, 20), "color": GREEN, "dir": Vector(-1, -1)}
    b3 = {"rect": pygame.Rect(100, 150, 60, 60), "color": BLUE, "dir": Vector(-1, 1)}
    boxes = [b1, b2, b3]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        windowSurface.fill(WHITE)

        for b in boxes:
            rect = b["rect"]
            vel = b["dir"]
            posn = Vector(rect.left, rect.top)
            posn = posn + MOVESPEED * vel

            b["rect"].left = posn.vx
            b["rect"].top = posn.vy

            if b["rect"].top < 0 or b["rect"].bottom > WINDOWHEIGHT:
                vel = Vector(vel.vx, -vel.vy)
            if b["rect"].left < 0 or b["rect"].right > WINDOWWIDTH:
                vel = Vector(-vel.vx, vel.vy)

            b["dir"] = vel

            pygame.draw.rect(windowSurface, b["color"], b["rect"])

        pygame.display.update()
        time.sleep(0.02)


def main():
    play()
    # Vector.run_tests()


if __name__ == "__main__":
    main()
