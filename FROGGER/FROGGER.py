"""
Author: Matt Franchi
Summary: A rudimentary game of Frogger -- same rules apply:
    - move up one space = 10 points
    - reach a lilypad at top of map = 200 points
    - go down one space = -10 points
    - you lose if you go off the map in any direction (except the top)
"""

import pygame, random, sys # module imports
from pygame.locals import *

# Initiate Pygame
pygame.init()

# Color Definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Game Window Configuration

hSize = 900
vSize = 900
gameWindow = pygame.display.set_mode((hSize, vSize), 0, 32)
gameWindow.fill(BLACK)
pygame.display.set_caption('Frogger') # sets window caption
clock = pygame.time.Clock() # starts game Clock
titleFont = pygame.font.Font('ARCADECLASSIC.ttf', hSize // 15) # defines fonts
titleFont.set_underline(1)
headerFont = pygame.font.Font('ARCADECLASSIC.ttf', hSize // 20)
gameFont = pygame.font.Font('ARCADECLASSIC.ttf', hSize // 30)


# Spritesheet Function
class spriteSheet():
    """
    class Spritesheet():
    Input for constructor is:
        - fileName: the filename of the spritesheet
    Class variables are:
        - sheet: the converted image, ready to be accessed by pygame
    """
    def __init__(self, fileName):

        self.sheet = pygame.image.load(fileName).convert()

    def image_at(self, rectangle, colorkey=None):
        """
        class method image_at: gets a sprite at the specified coordinates
        :param rectangle: the coordinates of the sprite (xStart,yStart,width,height)
        :param colorkey: color to be rendered transparent on gameWindow
        :return:
        class method variables:
            - rect: a pygame.Rect object using rectangle from constructor
            - image: a Surface object with dimensions of rect
        """
        self.rectangle = rectangle
        self.rect = pygame.Rect(rectangle)
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.blit(self.sheet, (0, 0), self.rect)
        self.colorkey = colorkey
        if self.colorkey is not None:
            if self.colorkey is -1:
                self.colorkey = self.image.get_at((0, 0)) # creates colorkey, transparency for each sprite
            self.image.set_colorkey(self.colorkey, pygame.RLEACCEL)
        return self.image


class gameSprite(pygame.sprite.Sprite):
    def __init__(self, imgFile, xStart=0, yStart=0, speed=0, xSize=hSize // 60, ySize=hSize // 60):
        """
        class gamsSprite(pygame.sprite.Sprite)
        :param imgFile: the image for each sprite
        :param xStart:  the starting x-coordinate for each sprite
        :param yStart: the starting y-coordinate for each sprite
        :param speed: the speed for each sprite
        :param xSize: the width of each sprite
        :param ySize: the height of each sprite

        Class Variables are:
            - image: the scaled sprite image, as to ensure uniform sizing
            - rect: the corresponding rect for each self.image
            - animNum: the starting animation number, only necessary for frog sprite
            - time: gets the current time
        """

        super().__init__()
        self.imgFile = imgFile
        self.image = pygame.transform.scale(imgFile, (xSize, ySize))
        self.rect = self.image.get_rect(center=(xStart, yStart))
        self.xStart, self.yStart, self.speed = xStart, yStart, speed
        self.animNum = 0
        self.time = pygame.time.get_ticks()

    def moveSprite(self, isPressed):
        """
        function moveSprite: moves the sprite a distance speed after a specific arrow key is pressed
        :param isPressed: list of keys pressed
        :return:
        """
        if isPressed[pygame.K_UP]: # move up
            self.rect.y -= self.speed
            for n in range(0, len(frogIMGs)): # restore images to default orientation
                frogIMGs[n] = frogIMGsOriginal[n]
        if isPressed[pygame.K_DOWN]: # move down
            self.rect.y += self.speed
            for n in range(0, len(frogIMGs)):
                frogIMGs[n] = frogIMGsOriginal[n]
                frogIMGs[n] = pygame.transform.flip(frogIMGs[n], 0, 1) # flip images to face downwards
        if isPressed[pygame.K_LEFT]: # move left
            self.rect.x -= self.speed
            for n in range(0, len(frogIMGs)):
                frogIMGs[n] = frogIMGsOriginal[n]
                frogIMGs[n] = pygame.transform.rotate(frogIMGs[n], 90) # rotate images to face left
        if isPressed[pygame.K_RIGHT]: # move right
            self.rect.x += self.speed
            for n in range(0, len(frogIMGs)):
                frogIMGs[n] = frogIMGsOriginal[n]
                frogIMGs[n] = pygame.transform.rotate(frogIMGs[n], 270) # rotate images to face right

    def updateImg(self, images):
        """
        function updateImg: changes image after a time interval, effectively animating a sprite
        :param images: list of images to cycle through
        :return:
        """
        self.images = images
        self.now = pygame.time.get_ticks() # new time
        if abs(self.now - self.time) > 10: # elapsed time > 10; self.time gotten from sprite class
            self.animNum += 1 # go to next image
        if self.animNum >= len(self.images): #  restart cycle
            self.animNum = 0
        self.image = self.images[self.animNum] # update image
        self.time = pygame.time.get_ticks() # get elapsed time


def objectGen(objImgs, imgSizes, yStart, speed):
    """
    function objectGen: creates a sprite based on list of images, sizes, start coords, and speed
    :param objImgs: list of images to be used
    :param imgSizes: list of corresponding sizes, in same order as objImgs
    :param yStart: starting y coordinate
    :param speed: speed
    :return:
    """
    numImgs = len(objImgs) # gets number of images in objImgs
    imgNum = random.randint(0, numImgs - 1) # chooses image randomly
    xStart = random.randint(0, hSize) # generates random x-start coordinate between 0 and screen end
    object = gameSprite(objImgs[imgNum], xStart, yStart, speed, imgSizes[imgNum], hSize // 32) # creates the sprite
    return object


def addToASL(allSpritesList, objectList):
    """
    function addtoASL:
    :param allSpritesList: list of all used sprites in game
    :param objectList: list of sprites to be added to complete list
    :return:
    """
    for object in objectList:
        allSpritesList.add(object) # adds sprite to allSpritesList
    return allSpritesList


def menuScreen():
    """
    function menuScreen: VERY basic menu screen with game title and start button (was going to add options, ran out of
    time)
    Function Variables are:
    shouldStart: determines whether menu screen is sustained or game loop is started
    :return:
    """
    shouldStart = False # initial value
    gameWindow.fill(WHITE)
    title = titleFont.render('FROGGER', True, GREEN) # creates title text
    titleRect = title.get_rect(center=(hSize / 2, vSize // 30)) # creates corresponding rect
    gameWindow.blit(title, titleRect) # places text on gameWindow
    gameStart = headerFont.render(' START GAME ', True, GREEN)
    gameStartRect = gameStart.get_rect(center=(hSize / 2, vSize // 8))
    pygame.draw.rect(gameWindow, BLACK, gameStartRect)
    gameWindow.blit(gameStart, gameStartRect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # program exits if user clicks the x in top right corner
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN: # shouldStart is True is button is clicked
            mousePos = pygame.mouse.get_pos()
            if gameStartRect.collidepoint(mousePos):
                shouldStart = True
    return shouldStart


def getModifiedSprites(imgCoordList, scaleFactor):
    """
    function getModifiedSprites: flips and scales sprites from spritelist
    :param imgCoordList: list of coords to grab sprites from spritelist
    :param scaleFactor: factor to shrink/enlarge each image
    :return:
    """
    newImageList = [] # initial value
    for imgCoord in imgCoordList:
        newImage = pygame.transform.flip(gameSprites.image_at(imgCoord, BLACK), 0, 1) # flips each image vertically
        newImage = pygame.transform.scale(newImage, (scaleFactor, scaleFactor)) # scales each image
        newImageList.append(newImage)
    return newImageList # returns modified list


def getSprites(imgCoordList):
    """
    function getSprites: basic version of above function, just grabs sprite without modification
    :param imgCoordList: coord list to grab sprites
    :return:
    """
    newImageList = []
    for imgCoord in imgCoordList:
        newImage = gameSprites.image_at(imgCoord, BLACK) # grabs sprite from spritelist
        newImageList.append(newImage)
    return newImageList


gameSprites = spriteSheet('finalproject_gameSprites.png') # creates a spritesheet

frogImgCoords = ((0, 31, 52, 37), (54, 28, 58, 42), (113, 19, 58, 53), (173, 8, 54, 66), (230, 2, 56, 74),
                 (113, 19, 58, 53), (0, 31, 52, 37)) # coordinates of frog images

frogIMGs = getModifiedSprites(frogImgCoords, hSize // 30) # runs through modification function
frogIMGsOriginal = tuple(frogIMGs) # original images, tuple, for sprite rotation after key-press

deadFrogIMG = pygame.transform.scale(gameSprites.image_at((302, 333, 65, 50), BLACK), (hSize // 30, hSize // 30))
# image to be displayed upon loseFlag

vehicleImgCoords = ((12, 483, 127, 69), (155, 483, 135, 71), (305, 482, 134, 71), (9, 407, 178, 66),
                    (203, 406, 285, 66))
vehicleTypes = getSprites(vehicleImgCoords)
vehicleSizes = [hSize // 16, hSize // 16, hSize // 16, 3 * hSize // 32, hSize // 8]

grassIMG = gameSprites.image_at((135, 158, 82, 82)) # grabs singular image from spritesheet
waterIMG = gameSprites.image_at((226, 158, 82, 82))
roadIMG = gameSprites.image_at((316, 158, 82, 82))

logImgCoords = ((13, 258, 353, 59), (387, 258, 185, 59,), (14, 328, 273, 59))
logTypes = getSprites(logImgCoords)
logSizes = [7 * hSize // 48, 3 * hSize // 32, hSize // 8]

brushImgCoords = ((497, 158, 82, 82), (407, 158, 82, 82), (407, 158, 82, 82), (407, 158, 82, 82))
brushIMGs = getSprites(brushImgCoords)

pygame.display.set_icon(frogIMGs[0]) # sets window icon to image of frog

# MAP GENERATION VARIABLES
grassList = [] # initial values
waterList = []
roadList = []
vehicleList = []
vehicleRowList = []
brushList = []
logList = []
logRowList = []
numRows = vSize // (hSize // 30) # number of rows, changes with resolution

for n in range(0, numRows): # loop for map generation
    if n == 0: # first (bottom) row is always grass
        terrainType = 1
    elif n < .33 * numRows: # bottom third of map is roads + grass
        terrainType = random.randint(1, 2)
    elif n == numRows - 1: # top row is brush + lilypads
        terrainType = 4
    else: # rest of map is water + grass
        terrainType = random.randrange(1, 4, 2)
    if terrainType == 1: # grass row generation
        for num in range(1, 31):
            grassList.append(gameSprite(grassIMG, num * hSize // 30 - hSize // 60,  # 30 instances of grass sprite
                                        vSize - hSize // 60 - hSize // 30 * n, xSize=hSize // 30, ySize=hSize // 30))

    elif terrainType == 2: # road generation
        for num in range(1, 31): # 30 instances of road sprite
            roadList.append(
                gameSprite(roadIMG, num * hSize // 30 - hSize // 60, vSize - hSize // 60 - hSize // 30 * n,
                           xSize=hSize // 30, ySize=hSize // 30))

        vehicleCount = 1 # vehicle generation for each row of road
        while vehicleCount <= 4: # 4 vehicles per row
            collision = 0 # collision sequences, makes sure vehicles don't spawn on top of eachother
            vehicle = objectGen(vehicleTypes, vehicleSizes, vSize - hSize // 60 - hSize // 30 * n, 4)
            for goodVehicle in vehicleRowList:
                if vehicle.rect.colliderect(goodVehicle.rect):
                    collision = 1
                    break
            if collision == 1:
                continue
            vehicleRowList.append(vehicle) # optimized list, so for loop doesn't go through ALL cars each check
            vehicleList.append(vehicle)
            vehicleCount += 1
        else:
            vehicleRowList = [] # resets row list

    elif terrainType == 3: # water row generation
        for num in range(1, 31): # 30 instances of water sprite
            waterList.append(
                gameSprite(waterIMG, num * hSize // 30 - hSize // 60, vSize - hSize // 60 - hSize // 30 * n,
                           xSize=hSize // 30, ySize=hSize // 30))
        log = objectGen(logTypes, logSizes, vSize - hSize // 60 - hSize // 30 * n, 2) # log generation sequence
        logRowList.append(log)
        logList.append(log)
        logCount = 1
        while logCount <= 2:
            collision = 0 # collision check, same process as vehicles -- almost made function, but only two applications
            log = objectGen(logTypes, logSizes, vSize - hSize // 60 - hSize // 30 * n, random.randint(2,3))
            for goodLog in logRowList:
                if log.rect.colliderect(goodLog.rect):
                    collision = 1
                    break
            if collision == 1:
                continue
            logRowList.append(log)
            logList.append(log)
            logCount += 1
        else:
            logRowList = []

    if terrainType == 4: # brush row generation -- 1/4 lilypads, 3/4 brush
        for num in range(1, 31):
            brushList.append(gameSprite(brushIMGs[random.randint(0, 3)], num * hSize // 30 - hSize // 60,
                                        vSize - hSize // 60 - hSize // 30 * n, xSize=hSize // 30, ySize=hSize // 30))

# COMPILING SPRITES TO MASTER LIST
allSpritesList = pygame.sprite.Group() # adds all spritelists to master spritelist for drawing
allSpritesList = addToASL(allSpritesList, grassList)
allSpritesList = addToASL(allSpritesList, waterList)
allSpritesList = addToASL(allSpritesList, roadList)
allSpritesList = addToASL(allSpritesList, vehicleList)
allSpritesList = addToASL(allSpritesList, logList)
allSpritesList = addToASL(allSpritesList, brushList)
frog = gameSprite(frogIMGs[0], hSize // 2, vSize - hSize // 60, hSize // 30, hSize // 30, hSize // 30)
"""
creates frog Sprite, with adaptable size based on resolution
"""
allSpritesList.add(frog)

score = 10 # initial score, first row

winFlag = False # initial values
loseFlag = False
shouldAnimate = False
count = 0
shouldStart = False
while True: # outer program loop
    while shouldStart is False:  # menu screen loop
        shouldStart = menuScreen()
    while winFlag is False and loseFlag is False: # game loop
        clock.tick(60) # 60 FPS
        if shouldAnimate is True: # Ensures animation only runs once per key press
            count += 1
        if count == 7:
            count = 0
            shouldAnimate = False
        for event in pygame.event.get():
            if event.type == QUIT: # quit sequence
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == pygame.K_UP: # score increase when you move up
                score += 10
                shouldAnimate = True
            if event.type == KEYDOWN and event.key == pygame.K_DOWN: # score decrease when you move down
                score -= 10
                shouldAnimate = True
            if event.type == KEYDOWN and (event.key == pygame.K_LEFT or
                                          event.key == pygame.K_RIGHT):
                shouldAnimate = True # animate when move left or right

            isPressed = pygame.key.get_pressed() # gets keys pressed
            frog.moveSprite(isPressed) # moves frog based on key pressed

        for vehicle in vehicleList:
            vehicle.rect.x += vehicle.speed # makes vehicles move at speed each frame
            if vehicle.rect.left >= hSize:
                vehicle.rect.left = - hSize // 8 # restarts vehicles at x=0 if they move off screen
            if vehicle.rect.colliderect(frog.rect): # player loses if they hit a vehicle
                loseFlag = True

        for log in logList:
            log.rect.x += log.speed # same as vehicles
            if log.rect.left >= hSize:
                log.rect.left = -hSize // 8

        onLog = gameSprite(logTypes[0]) # player loses if they are in water but not on log
        for water in waterList:
            if frog.rect.colliderect(water.rect):
                for log in logList:
                    if frog.rect.colliderect(log.rect):
                        onLog = log
                        break
                else:
                    loseFlag = True

        if frog.rect.colliderect(onLog.rect): # if frog is on log, moves with speed of log
            frog.rect.x += onLog.speed

        for brush in brushList: # if frog is on a lilypad, game win, score += 200
            if frog.rect.colliderect(brush.rect) and brush.imgFile == brushIMGs[0]:
                score += 200
                winFlag = True

        if frog.rect.centerx >= hSize or frog.rect.centerx <= 0 or frog.rect.top == vSize \
                or frog.rect.bottom == 0: # game lose if frog goes off screen in any direction
            loseFlag = True

        pygame.draw.rect(gameWindow, BLACK, frog.rect, 0) # draws the frog on screen

        if shouldAnimate is True:
            frog.updateImg(frogIMGs) # animates frog

        allSpritesList.draw(gameWindow) # draws all sprites
        scoreText= gameFont.render('Score  ' + str(score), True, WHITE) # score, displaying in bottom-left corner
        gameWindow.blit(scoreText, (0, vSize - vSize // 30))
        pygame.display.update() # updates screen every frame

    else: # if you're here, frog either won or lost
        if loseFlag is True:
            frog.image = deadFrogIMG # skull (dead frog image)
            pygame.draw.rect(gameWindow, BLACK, frog.rect, 0)
            allSpritesList.draw(gameWindow) # draws the skull

            pygame.display.update() # update screen
            pygame.time.wait(500) # wait half a second before "you lost" screen
            gameWindow.fill(BLACK)
            gameOver = titleFont.render("You  Lose!", True, WHITE) # text generation
            gameOverRect = gameOver.get_rect(center=(hSize / 2, vSize / 4))
            gameWindow.blit(gameOver, gameOverRect)

            finalScore = titleFont.render("Your  final score is  " + str(score), True, WHITE)
            finalScoreRect = finalScore.get_rect(center=(hSize / 2, vSize / 2))
            gameWindow.blit(finalScore, finalScoreRect) # final score display
            pygame.display.update()
            pygame.time.wait(3000) # wait 3 seconds before closing out game
        if winFlag is True:
            gameWin = titleFont.render("You Win!", True, BLACK) # same process as losing screen, overlayed
            finalScore = titleFont.render("Your final score is " + str(score), True, BLACK)
            gameWindow.blit(gameWin, (hSize // 2 - hSize // 7, vSize // 30))
            gameWindow.blit(finalScore, (hSize // 7, vSize // 10))
            pygame.display.update()
            pygame.time.wait(3000)

    pygame.quit() # exit game
    sys.exit()
