import pygame
from src.boss import Boss

class Explosion:
    """
    Trida pro explozi
    """
    # nacteni raw obrazku bez scalingu
    _raw_frames = [pygame.image.load(f"assets/img/explosion/exp_{i}.png") for i in range(8)]

    def __init__(self, start_x, start_y, *, is_boss: bool = False) -> None:
        # tady je scaling
        if is_boss:
            self.frames = [pygame.transform.scale(img, (120, 120)) for img in Explosion._raw_frames]
        else:
            self.frames = [pygame.transform.scale(img, (50, 50)) for img in Explosion._raw_frames]

        self.index = 0
        self.timer = 0.0
        if is_boss:
            self.frame_rate = 0.20
        else: 
            self.frame_rate = 0.08
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(start_x, start_y))

        self.finished = False

    def update(self, dt):
        """
        animovani vybuchu
        """
        self.timer += dt
        if self.timer >= self.frame_rate:
            self.timer = 0
            self.index += 1

            if self.index >= len(self.frames):
                self.finished = True
            else:
                self.image = self.frames[self.index]

    def draw(self, surface):
        """
        vykresleni vybuchu
        """
        surface.blit(self.image, self.rect)