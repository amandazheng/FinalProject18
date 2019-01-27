#Import statements 
import pygame
import random
import time

#To set up pygame
_image_library = {}
pygame.init()
gameDisplay = pygame.display.set_mode((800,800))
screen_rect=gameDisplay.get_rect()
black = (0,0,0)
white = (255,255,255)

#To set up the timer
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Helvetica', 30)
counter, text = 50, '50'.rjust(3) 
clock = pygame.time.Clock()

#To load the magnet images
magnetNS = pygame.image.load("NSMagnet.png")
magnetSN = pygame.image.load("SNMagnet.png")
homePic = pygame.image.load("MagneTrisHome.png")
homePic = pygame.transform.scale(homePic, (800, 800))
lostPic = pygame.image.load("MagneTrisLost.png")
lostPic = pygame.transform.scale(lostPic, (800, 800))
wonPic = pygame.image.load("MagneTrisWon.png")
wonPic = pygame.transform.scale(wonPic, (800, 800))

#Sets starting position for movingMagnet
x = 360
y = 514

#Sets initial values for important variables (run, stackheight, and x_change)
run = True
stackheight = 1
x_change = 0

def movingMagnet(x,y):
    '''to update the position of the movingMagnet'''
    gameDisplay.blit(magnetNS, (x,y))
    
class fallingMagnet():
    '''class for all fallingMagnets'''
    def __init__(self, a, b, orientation, fall, stackheight_individual):
        self.a = a
        self.b = b
        self.orientation = orientation
        self.fall = fall
        self.stackheight_individual = stackheight_individual
        self.drawChar()
        self.reset_pos()
        self.fallConnect()

    def drawChar (self):
        '''updates the fallingMagnet's position on the screen'''
        gameDisplay.blit(self.orientation, (self.a,self.b))

    def reset_pos(self):
        '''regenerates the fallingMagnet to the top of the screen for when it falls off the bottom of the screen'''
        #sets y at top of screen and randomized x position
        self.b = 0
        self.a = random.randint(10,750)

        #randomizes NS or SN magnet
        if random.randint(0,2) == 1:
            self.orientation = magnetSN
        else:
            self.orientation = magnetNS

    def fallConnect (self):
        '''connects the fallingMagnet to the movingMagnet (base) when it hits it from the top'''
        #if it is not falling (already connected), it continues to set the x coordinate = to the one of the base magnet
        if self.fall == False: 
            self.a = x
        #if it is falling, it continues to fall unless it fell of the screen (it is reset), or fits the conditions to connect (connects it and stops it from falling)
        else: 
            self.b += 2
            if self.b > 800:
                self.reset_pos()
            if self.b == (y-102*stackheight) and self.a >= (x-20) and self.a <= (x+20) and self.orientation == magnetNS:
                self.a = x
                self.fall = False
    
    def setStackheight (self):
        '''updates the stackheight of the magnet'''
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
    '''creates a new fallingMagnet and adds it to the magnetList of existing fallingMagnets'''
    global stackheight

    #randomizes orientation of magnet 
    if random.randint(0,2) == 1:
        orientation = magnetSN
    else:
        orientation = magnetNS
    
    #creates a new fallingMagnet, adds it to the list, and sets its stackheight
    magnetList.append(fallingMagnet(random.randint(10,750), 0, orientation, True, 0))
    magnetList[i].setStackheight
    stackheight += 1

#initializes necessary things (creates magnetList, first fallingMagnet...)
magnetList=[]
magnetList.append(fallingMagnet(random.randint(10,750), 0, magnetNS, True, 0))
magnetList[len(magnetList)-1].drawChar()
runCount = 0
startGame = False
finishGame = False


#Displays homescreen
while startGame == False:
    #prints homescreen
    gameDisplay.blit(homePic, (0,0))
    pygame.display.update()

    #breaks the loop if the space bar is pressed
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            startGame = True

#begins game loop
while run:
    #to be done every loop (check for key press, display background, update movingMagent)
    key = pygame.key.get_pressed()  
    gameDisplay.fill(white)
    movingMagnet(x,y)

    #loops through each fallingMagnet in magnetList
    for i in range(len(magnetList)):
        #draws, updates position, and sets stackheight for each 
        magnetList[i].drawChar()
        magnetList[i].fallConnect()
        magnetList[i].setStackheight()

        #if the last magnet is not falling (is connected), generates a new fallingMagnet
        if (magnetList[i].fall == False and len(magnetList)-1 == i):
            regenMagnet()

        #if the last magnet is falling and hits the stack of magnets from the side, it creates a list of stacked magnets it needs to delete
        if magnetList[-1].fall == True and magnetList[-1].a >= (x-20) and magnetList[-1].a <= (x+20) and magnetList[-1] != magnetList[i] and magnetList[-1].stackheight_individual == magnetList[i].stackheight_individual:
            toDelete = []

            #determines which magnets to delete
            for j in range(len(magnetList)):
                if magnetList[-1].stackheight_individual <= magnetList[j].stackheight_individual:
                    toDelete.append(j)
                    stackheight -= 1

            #deletes the necessary fallingMagnets (the list was necessary to insure they would be deleted in the same order to stay in the exisiting list range)
            for k in range(len(toDelete),0,-1):
                magnetList.pop(toDelete[k-1]) 

            #generates a new fallingMagnet
            regenMagnet()
            break

    #updates the count for the clock
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT: 
            counter -= 1
            if counter > 0: 
                text = str(counter).rjust(3) 
            else:
                while finishGame == False:
                    #prints lose screen
                    gameDisplay.blit(lostPic, (0,0))
                    pygame.display.update()

                    #breaks the loop if the space bar is pressed
                    for event in pygame.event.get():
                        if pygame.key.get_pressed()[pygame.K_SPACE]:
                            finishGame = True

                run = False

    #updates the display of the clock                  
    else:
        gameDisplay.blit(font.render(text, True, (0, 0, 0)), (32, 48))
        pygame.display.flip()
        clock.tick(60)

    #quits pygame when necessary 
    if event.type == pygame.QUIT:
        run = False

    #moves base magnet to the left when left arrow is pressed
    if key[pygame.K_LEFT]:
        x_change = -5
        if x < 10:
            x = 10

    #moves base magnet to the right when right arrow is pressed
    elif key[pygame.K_RIGHT]:
        x_change = 5
        if x > 750:
            x = 750
    x += x_change

    #does not move the magnet if no keys are pressed
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            x_change = 0
    
    #congradulates and exits the game when the player has stacked the magnets to the top of the screen 
    if stackheight == 5:

        while finishGame == False:
            #prints win screen
            gameDisplay.blit(wonPic, (0,0))
            pygame.display.update()

            #breaks the loop if the space bar is pressed
            for event in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    finishGame = True
        run = False

#quits the game when done      
pygame.quit()
exit()