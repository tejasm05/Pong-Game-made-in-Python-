import pygame, sys
import math
import os
from pygame.time import Clock
import random
import numpy

q = 1

pygame.init()
from pygame import mixer

screen = pygame.display.set_mode((1360, 720))
pygame.display.set_caption("Glitch")
pygame.display.set_icon(pygame.image.load("snake-512.png"))
playerblock = pygame.image.load("launchpad.png")
ball = pygame.image.load("pixil-frame-0(1).png")
ball = pygame.transform.scale(ball, (30, 30))
compball = pygame.image.load("compblock.png")
three = pygame.image.load("3.png")
two = pygame.image.load("2.png")
one = pygame.image.load("1.png")
go = pygame.image.load("Go!.png")
blurimage = pygame.image.load("blurredimage.jpg")
bigfont = pygame.font.Font("Luna-2geX.ttf", 30)
headerfont = pygame.font.Font("Luna-2geX.ttf", 30)
smallfont = pygame.font.Font("Luna-2geX.ttf", 22)
pausescreenfont = pygame.font.Font("Luna-2geX.ttf", 70)
collision = pygame.mixer.Sound("bell-one-shot.wav")


def drawplayerblock(pblockx, mousey):
    if mousey <= 1:
        screen.blit(playerblock, (pblockx, 1))
    elif mousey >= 519:
        screen.blit(playerblock, (pblockx, 535))
        # check out the above value later
    else:
        screen.blit(playerblock, (pblockx, mousey))


def drawball(x, y):
    screen.blit(ball, (x, y))


running = True


def drawcompblock(x, y):
    screen.blit(compball, (x, y))


def homescreenfont():
    global smallfont, bigfont, headerfont
    showfont = bigfont.render("press any key to start", True, (255, 255, 255))
    screen.blit(showfont, (565, 640))
    showfont = smallfont.render("<< SinglePlayer >>", True, (255, 255, 255))
    screen.blit(showfont, (30, 30))
    showfont = smallfont.render("<< Music >>", True, (128, 128, 128))
    screen.blit(showfont, (30, 80))


def drawconfirmexit():
    print("are you suer yo uwanna quit?")
    pygame.quit()
    sys.exit()


startedgame = False
ballx, bally = 1288, 370
blockcollision = False
collision_count = 0
mass = 4  # ball mass
blockmass = 20
initvel = 44
finalvel = 4
massval = 0.002
firstsmash = True
imgnum = 0
calculate = 0
x = 1
iforchangevel = 1
collisionmade = False
compblockcollision = False
anglerange = range(-15, 16)
chosenangle = random.choice(anglerange)
print(chosenangle)
prob1, prob2, prob3 = 0.65, 0.30, 0.05
normalcollisionpblock = 0
# angles made values
startfromhomescreen = False
musicplaying = False


def homescreen():
    global startfromhomescreen
    while True:
        Clock().tick(120)
        screen.fill((255, 0, 0))
        # print(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drawconfirmexit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                global startedgame
                startedgame = True
                startfromhomescreen = True

                gameloop()
        homescreenfont()
        pygame.display.update()


def retry():
    global collision_count, collisionmade, ballx, bally, blockcollision, mass, blockmass, initvel, finalvel, firstsmash, imgnum, calculate, x, bigfont
    onceagain = False
    while onceagain == False:
        screen.fill((255, 255, 255))
        print("in retry screen")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                onceagain = True
                break

        screen.blit(blurimage, (0, 0))
        showfont = bigfont.render("press any key to retry", True, (255, 255, 255))
        screen.blit(showfont, (565, 640))
        global startfromhomescreen
        startfromhomescreen = False
        pygame.display.update()
    collision_count = 0
    collisionmade = False
    iforchangevel = 1
    ballx, bally = 1288, 370
    blockcollision = False
    collision_count = 0
    mass = 4  # ball mass
    blockmass = 20
    initvel = 38
    finalvel = 4

    firstsmash = True
    imgnum = 0
    calculate = 0
    x = 1

    gameloop()


def drawpausescreenfont():
    global pausescreenfont, blurimage
    screen.blit(blurimage, (0, 0))
    # print("drawing")
    showfont = pausescreenfont.render("Retry", True, (255, 255, 255))
    screen.blit(showfont, (589, 177))
    showfont = pausescreenfont.render("Quit", True, (255, 255, 255))
    screen.blit(showfont, (614, 540))


def gameloop():
    global startfromhomescreen, compblockcollision

    def pausescreen(x_mouse, y_mouse):
        while True:
            # print(pygame.mouse.get_pos())
            pygame.event.set_grab(False)
            mx, my = pygame.mouse.get_pos()
            mxrange = range(583, 756)
            myrange = range(176, 287)
            # pygame.mouse.set_pos((550, 427))
            drawpausescreenfont()
            pygame.event.set_grab(False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print(x_mouse, y_mouse)
                        pygame.mouse.set_pos((x_mouse, y_mouse))
                        gameloop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mx in mxrange and my in myrange:
                        print("in range!")
                        # screen.fill((143, 0, 0))
                        retry()
                    else:
                        pass
            updatedisplay()
            screen.fill((143, 0, 0))
        # retry()

    def aftercollide():
        global mass, initvel
        # we cwanna reverse vel
        # for that we calculate momentum!
        if collision_count <= 40:
            global q, massval, compblockcollision, collisionmade
            chngvar = 10 * q
            chng_var = 5 * (2 * q)
            changespeed = [1, 3, 15, 45, 75, 120]
            if q % 2 == 0 and collision_count == chng_var or chngvar:
                print("Changing speed")

                print(f"collisioncount is {collision_count}")
                lostmass = collision_count * massval
                newmass = mass - lostmass
                # calculating my momentum formula:
                # mass*initvel = newmass * initvel

                initvel = mass * initvel / newmass
                # now we get the new velocity
                round(initvel)
                # initvel = int(initvel)
                initvel = -(initvel)
                # initvel = (70/100) * initvel
                print(f"speed is {initvel} ")
                # chnge the angle here
                compblockcollision = False
                collisionmade = False
                q += 1
            else:
                initvel = -(initvel)
                round(initvel)
                initvel = int(initvel)
                print(f"speed is {initvel}")
                q += 1

        elif collision_count > 40 and collision_count <= 85:
            if collision_count % 5 == 0:
                # initvel = (initvel - 0.1)
                #
                # q += 1
                # print(initvel)
                initvel = -(initvel - 1)
                round(initvel)
                initvel = int(initvel)
                print(f"zeee vel in the first iterate isssss{initvel}")
                # pygame.time.wait(200000)
                print(initvel)
                compblockcollision = False
                collisionmade = False
                q += 1
                print(f"collisioncount is {collision_count}")
            else:
                print(f"collisioncount is {collision_count} in the second iterate brooooooo")
                initvel = -(initvel)
                print(initvel)
                q += 1
        elif collision_count > 85:
            if collision_count % 12 == 0:
                # initvel = (initvel - 0.1)
                #
                # q += 1
                # print(initvel)
                initvel = -(initvel - 1)
                round(initvel)
                initvel = int(initvel)
                print(f"zeee vel in the first iterate isssss{initvel}")
                # pygame.time.wait(200000)
                print(initvel)
                compblockcollision = False
                collisionmade = False
                q += 1
                print(f"collisioncount is {collision_count}")
            else:
                print(f"collisioncount is {collision_count} in the second iterate brooooooo")
                initvel = -(initvel)
                print(initvel)
                q += 1

    def normchngangle():
        global normalcollisionpblock

        def selfnormchngangle(coordinate):
            global bally, chosenangle, changeanglerange, ballx
            choose = [1, 2, 3]
            choice = numpy.random.choice(choose, 1, p=[0.5, 0.3, 0.2])
            if choice == 1:
                ballx = coordinate
                chosenangle = -(chosenangle)
            elif choice == 3:
                ballx = coordinate
                changeangle = random.randrange(chosenangle - 10, chosenangle + 10)
                chosenangle = -(changeangle)
            elif choice == 2:
                ballx = coordinate
                littlechange = random.randrange(-4, 5)
                chosenangle = -(chosenangle + littlechange)

        if normalcollisionpblock == True:
            selfnormchngangle(38)
        if normalcollisionpblock == False:
            selfnormchngangle(705)

    def reverseangle(topcollision):
        def chngangle(coordinate):
            global bally, chosenangle, changeanglerange
            choose = [1, 2, 3]
            choice = numpy.random.choice(choose, 1, p=[prob1, prob2, prob3])
            if choice == 1:
                bally = coordinate
                chosenangle = -(chosenangle)
            elif choice == 3:
                bally = coordinate
                changeangle = random.randrange(chosenangle - 10, chosenangle + 10)
                chosenangle = -(changeangle)
            elif choice == 2:
                bally = coordinate
                littlechange = random.randrange(-4, 5)
                chosenangle = -(chosenangle + littlechange)

        if topcollision == True:
            global collision_count
            chngangle(-5)
            if collision_count % 7:
                global prob1, prob2, prob3
                prob1 = prob1 - 0.02
                prob2 = prob2 + 0.01
                prob3 = prob3 + 0.01
            if collision_count >= 35:
                prob1 = 0.25
                prob2 = 0.25
                prob3 = 0.5
            if collision_count == 45:
                prob1 = 0.45
                prob2 = 0.25
                prob3 = 0.3
            # global topcollision
            # topcollision = False

        if topcollision == False:
            chngangle(700)
            if collision_count % 7:
                # global prob1, prob2, prob3
                prob1 = prob1 - 0.02
                prob2 = prob2 + 0.01
                prob3 = prob3 + 0.01
            if collision_count >= 35:
                prob1 = 0.25
                prob2 = 0.25
                prob3 = 0.5
            if collision_count == 45:
                prob1 = 0.45
                prob2 = 0.25
                prob3 = 0.3

            # global bottomcollision
            # bottomcollision = False

    def updatedisplay():
        pygame.display.update()

    while running == True:

        global imgnum, calculate, x, musicplaying

        def playmusic():
            global musicplaying
            if musicplaying == False:
                pygame.mixer.music.load("imsomnia.mp3")
                pygame.mixer.music.play(-1)
                musicplaying = True

        playmusic()
        Clock().tick(120)

        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        pygame.event.set_grab(True)

        # mousex is not necessary simply storing it cus can't get mouse y separately

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # this always should be the last event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    x_mouse, y_mouse = pygame.mouse.get_pos()
                    # print(x_mouse, y_mouse)
                    pausescreen(x_mouse, y_mouse)

            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = pygame.mouse.get_pos()
                pygame.mouse.set_pos(30, mousey)

        if imgnum == 70:
            imgnum = 0
            imgfile = f"{imgnum}.jpg"
        else:
            imgfile = f"{imgnum}.jpg"

        backgroundfolder = r"Background 22"
        file = os.path.join(backgroundfolder, imgfile)
        # print(file)
        background = pygame.image.load(file)

        def drawbackground():
            screen.blit(background, (0, 0))

        drawbackground()
        mousex, mousey = pygame.mouse.get_pos()
        pblockx = 30
        drawplayerblock(pblockx, mousey - 84)

        global startedgame

        def countdown():

            while True:
                global blurimage
                screen.fill((244, 244, 244))

                iteratinglist = [three, two, one, go]
                iterate = 0
                for i in range(271):
                    Clock().tick(90)
                    screen.fill((244, 244, 244))

                    num = iteratinglist[iterate]
                    if i == 90:

                        iterate += 1
                    elif i == 180:
                        iterate += 1
                    elif i == 270:
                        iterate += 1
                    screen.blit(blurimage, (0, 0))
                    screen.blit(num, (600, 500))
                    updatedisplay()
                break

        def startgame():

            global blockcollision, vel
            if blockcollision == False:
                global ballx, bally
            # print(ballx,bally)
            drawball(int(ballx), int(bally))

            # distance = math.sqrt((math.pow((ballx-pblockx),2)) + math.pow((bally-mousey),2))
            # print(distance)
            def changevel():
                # needs change
                global initvel, finalvel, ballx, iforchangevel, bally, chosenangle

                # if ballx <= 400 and collision_count % 2 ==0:
                #     print("triggering shit")
                #     changevel = initvel - finalvel
                #     changevel = changevel / 200
                #     initballvel = initvel - (changevel * iforchangevel)
                #     if initballvel < 0:
                #         initballvel = -(initballvel)
                #         iforchangevel = 1
                #     ballx -= initballvel
                #     iforchangevel += 1
                #     return initballvel
                #
                # else:
                ballx -= initvel

                if bally <= -5:
                    topcollision = True
                    bottomcollision = False
                    reverseangle(topcollision)
                    topcollision = False

                if bally >= 700:
                    bottomcollision = True
                    topcollision = False
                    reverseangle(topcollision)
                    bottomcollision = False
                bally -= chosenangle

            changevel()

            vsqr = math.pow(initvel, 2)
            KE = 1 / 2 * mass * vsqr
            # print(KE)

            # m1v1 = m2v2

            collisionrange = range(mousey - 100, mousey + 100)
            # print(collisionrange)
            global compblockcollision, collision
            global collision_count, collisionmade, normalcollisionpblock
            if bally in collisionrange and ballx <= 40:
                print("Collision detected")
                collision_count += 1
                if collisionmade == False:
                    # pygame.mixer.music.load("bell-one-shot.wav")
                    # pygame.mixer.music.play(1)
                    pygame.mixer.Sound.play(collision)
                    aftercollide()
                    normalcollisionpblock = True
                    normchngangle()
                    normalcollisionpblock = 0
                    collisionmade = True

            elif compblockcollision == True and collision_count % 2 != 0:
                print("collision detected")
                print(collision_count)
                compblockcollision = False
                collision_count += 1
                if collisionmade == False:
                    # pygame.mixer.music.load("bell-one-shot.wav")
                    # pygame.mixer.music.play(1)
                    pygame.mixer.Sound.play(collision)
                    aftercollide()
                    normalcollisionpblock = False
                    normchngangle()
                    normalcollisionpblock = 0
                    collisionmade = True

            collisionmade = False

            if ballx <= 20 and bally not in collisionrange:
                print("you lose")
                retry()

        if ballx >= 1320 and collision_count % 2 != 0:
            print("turning compblockcollision to true")
            compblockcollision = True

        drawcompblock(1320, bally - 84)

        if startfromhomescreen == True:
            # 270 frames here

            countdown()
            startfromhomescreen = False
            startgame()
        else:
            startgame()

        calculate = imgnum + x
        x += 1
        if calculate % 5 == 0:
            imgnum += 1

        # pygame.mixer.music.load("imsomnia.mp3")
        # pygame.mixer.music.play(-1)

        updatedisplay()


homescreen()
