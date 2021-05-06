import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, coord: tuple, size: tuple, text: str = None, color: tuple = None, img: str = None):
        super().__init__()

        self.coord = coord
        self.size = size

        if color:
            self.image = pygame.Surface(size)
            self.image.fill(color)
        elif img:
            self.image = pygame.transform.scale(pygame.image.load(img), size)
        else:
            raise TypeError("Нужно указать один из аргументор color | img")

        self.text = text
        if text:
            font = pygame.font.SysFont("Roboto", 80)
            self.label = font.render(text, True, (73, 168, 70))
            self.label_rect = self.label.get_rect()
            self.label_rect.center = (coord[0] + size[0] / 2, coord[1] + size[1] / 2)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        if self.text:
            screen.blit(self.label, self.label_rect)
