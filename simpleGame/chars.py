import sys, pygame

class Player:

    def __init__(self, id, img, scale):
        self.id = id
        self.tail = 0
        self.previousPos = []
        self.alive = True
        self.onScreen = True
        self.speed = [0,0]
        self.size = [100 * scale ,100 * scale]
        self.imgName = img
        self.img = pygame.transform.scale(pygame.image.load(img),
        (int(100 * scale), int(100 * scale)))
        self.rect = self.img.get_rect()

    def scale(self,scale):
        old = self.rect
        self.img = pygame.transform.scale(pygame.image.load(self.imgName),
        (int(scale + self.size[0]), int(scale + self.size[1])))
        self.size[0] += scale
        self.size[1] += scale
        ## scale rect
        self.rect = self.img.get_rect()
        self.rect = self.rect.move([old[0],old[1]])
