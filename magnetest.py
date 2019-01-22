import pygame
import random
import time

magnet_random = random.randint(0,2)
_image_library = {}
pygame.init()
gameDisplay = pygame.display.set_mode((800,800))
screen_rect=gameDisplay.get_rect()
black = (0,0,0)
white = (255,255,255)
clock = pygame.time.Clock()
run = True
magnet = pygame.image.load("NSMagnet.png")
magnetNS = pygame.image.load("NSMagnet.png")
magnetSN = pygame.image.load("SNMagnet.png")
x = 360
y = 514
counter, text = 50, '50'.rjust(3) #change counter back to 50ish? when done
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Helvetica', 30)
stackheight = 1
x_change = 0

def NSMagnet(x,y):
    gameDisplay.blit(magnetNS, (x,y))
    
class fallingMagnet():
    def __init__(self, a, b, orientation, fall, stackheight_individual):
        self.a = a
        self.b = b
        self.orientation = orientation
        self.fall = fall
        self.stackheight_individual = stackheight_individual
        self.drawChar()
        self.fallConnect()

    def drawChar (self):
        gameDisplay.blit(self.orientation, (self.a,self.b))

    def reset_pos(self):
        self.b = 0
        self.a = random.randint(10,750)
        if random.randint(0,2) == 1:
            self.orientation = magnetSN
        else:
            self.orientation = magnetNS

    def fallConnect (self):
        if self.fall == False: 
            self.a = x
        else: 
            self.b += 2
            if self.b > 800:
                self.reset_pos()

            if self.b == (y-102*stackheight) and self.a >= (x-20) and self.a <= (x+20) and self.orientation == magnetNS:
                self.a = x
                self.fall = False
    
    def setStackheight (self):
        if self.b <= y+102*5:
            self.stackheight_individual = 5
        if self.b >= y-102*4:
            self.stackheight_individual = 4
        if self.b >= y-102*3:
            self.stackheight_individual = 3
        if self.b >= y-102*2:
            self.stackheight_individual = 2
        if self.b >= y-102*1:
            self.stackheight_individual = 1
        if self.b >= y-102*0:
            self.stackheight_individual = 0

def regenMagnet():
    global stackheight
    
    if random.randint(0,2) == 1:
            orientation = magnetSN
    else:
        orientation = magnetNS
    magnetList.append(fallingMagnet(random.randint(10,750), 0, orientation, True, 0))
    magnetList[i].setStackheight
    stackheight += 1

magnetList=[]
magnetList.append(fallingMagnet(random.randint(10,750), 0, magnetNS, True, 0))
magnetList[len(magnetList)-1].drawChar()
runCount = 0

while run:
    key = pygame.key.get_pressed()
    gameDisplay.fill(white)
    NSMagnet(x,y)

    for i in range(len(magnetList)):
        magnetList[i].drawChar()
        magnetList[i].fallConnect()
        magnetList[i].setStackheight()

        if (magnetList[i].fall == False and len(magnetList)-1 == i):
            regenMagnet()

        if magnetList[-1].fall == True and magnetList[-1].a >= (x-20) and magnetList[-1].a <= (x+20) and magnetList[-1] != magnetList[i] and magnetList[-1].stackheight_individual == magnetList[i].stackheight_individual:
            toDelete = []

            for j in range(len(magnetList)):
                if magnetList[-1].stackheight_individual <= magnetList[j].stackheight_individual:
                    toDelete.append(j)
                    stackheight -= 1

            for k in range(len(toDelete),0,-1):
                magnetList.pop(toDelete[k-1]) 
            regenMagnet()
            break

    for event in pygame.event.get():
        if event.type == pygame.USEREVENT: 
            counter -= 1
            text = str(counter).rjust(3) if counter > 0 else "sorry, you lose"
            if counter < -1:
                run = False
                        
    else:
        gameDisplay.blit(font.render(text, True, (0, 0, 0)), (32, 48))
        pygame.display.flip()
        clock.tick(60)

    if event.type == pygame.QUIT:
        run = False
    if key[pygame.K_LEFT]:
        x_change = -5
        if x < 10:
            x = 10
    elif key[pygame.K_RIGHT]:
        x_change = 5
        if x > 750:
            x = 750
    x += x_change

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            x_change = 0
    
    if stackheight == 5:
        text = "Congrats! You won!" ##I think this isn't working because the counter freezes
        
        gameDisplay.blit(font.render(text, True, (0, 0, 0)), (32, 48))

        pygame.time.delay(1000)
        run = False
        
pygame.quit()
exit()