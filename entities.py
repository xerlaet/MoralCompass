import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, path, size, x, y, question):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(path),size)
        # self.image = pygame.Surface([width, height])
        # self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if question != "":
            self.question = Dilemma(question[0],question[1])
        else:
            self.question = ""
    def update(self):
        if self.question != "":
            self.question.updatePos(self.rect)
    def moveLeft(self, pixels):
        self.rect.x -= pixels
    def moveRight(self, pixels):
        self.rect.x += pixels
    def moveUp(self, pixels):
        self.rect.y -= pixels
    def moveDown(self, pixels):
        self.rect.y += pixels
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(pygame.sprite.Sprite):
    def __init__(self, pathL, pathR, size, x, y):
        super().__init__()
        image = (pygame.transform.scale(pygame.image.load(pathL),size),
                pygame.transform.scale(pygame.image.load(pathR),size))
        self.imageleft = image[0]
        self.imageright = image[1]
        self.image = self.imageright
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.questionrect = pygame.Rect(self.rect.x-50,self.rect.y-50,self.rect.width+100,self.rect.height+100)
    def changeLeft(self):
        self.image = self.imageleft
    def changeRight(self):
        self.image = self.imageright
    def update(self):
        pass
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Text:
    def __init__(self, center, text, font, size, color):
        self.message = text
        self.center = center
        self.color = color
        self.font = pygame.font.Font(font, size)
        self.text_obj = self.font.render(text, False, color)
        self.text_rect = self.text_obj.get_rect()
        self.text_rect.center = center
        self.image = pygame.Surface([self.text_rect.width, self.text_rect.height])
        self.image.fill((222, 200, 120))
    def update(self, text):
        self.message = text
        self.text_obj = self.font.render(text, False, self.color)
        self.text_rect = self.text_obj.get_rect()
        self.text_rect.center = self.center
    def blit(self, screen):
        # screen.blit(self.image, self.text_rect)
        screen.blit(self.text_obj, self.text_rect)
    def blitbackground(self, screen):
        screen.blit(self.image, self.text_rect)

class Button:
    def __init__(self, center, w, h, text,result):
        self.hover = False
        self.clicked = False
        self.top = center[1]-h/2
        self.bottom = center[1]+h/2
        self.left = center[0]-w/2
        self.right = center[0]+w/2
        self.message = text
        self.text = Text(center,text,'freesansbold.ttf',20,(0,0,0))
        self.image = pygame.Surface([w,h])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(center=center)
        self.result = result
    def update(self):
        if self.hover:
            self.image.fill((219, 188, 75))
        else:
            self.image.fill((222, 200, 120))
        self.top = self.rect.top
        self.bottom = self.rect.bottom
        self.left = self.rect.left
        self.right = self.rect.right
        self.text = Text(self.rect.center,self.message,'freesansbold.ttf',20,(0,0,0))
    def blit(self, screen):
        mousepos = pygame.mouse.get_pos()
        if self.left <= mousepos[0] <= self.right and self.top <= mousepos[1] <= self.bottom:
            self.hover = True
        else:
            self.hover = False
        screen.blit(self.image,self.rect)
        self.text.blit(screen)

class Dilemma:
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers
        self.buttons = []
        self.text = Text([100,100],question,'freesansbold.ttf',20,(0,0,0))
        for i in range(len(answers)):
            button = Button([0,0+75*i],100,50,answers[i][0],answers[i][1])
            self.buttons.append(button)
    def update(self):
        for button in self.buttons:
            button.update()
    def updatePos(self, pos):
        self.text.text_rect.center = pos.center
        self.text.text_rect = self.text.text_rect.move(0,-200)
        for i in range(len(self.buttons)):
            self.buttons[i].rect.center = pos.center
            self.buttons[i].rect.y -= 150
            self.buttons[i].rect.x -= (75 - 150*i)
            self.buttons[i].text.center = self.buttons[i].rect.center
    def draw(self, screen):
        self.text.blitbackground(screen)
        self.text.blit(screen)

        for button in self.buttons:
            button.blit(screen)