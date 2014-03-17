#geometricforms is a program that rotates some geometric shapes

#####INITIALIZATION
###################
import pygame, sys
from pygame.locals import *
import math, cmath
pygame.init()

W = 640                                     #Screen Width
H = 480                                     #Screen Height
Cen = (W/2,H/2)                             #Screen Center
R = 150                                     #Radius
phi = 2                                     #Angle of rotation
screenColor = (255,0,0)                     #Background color
screenColorTemp = [255,0,0]                 #Temp to hold background color, since tuples are immutable in Python
colorUp = True                              #Boolean to hold whether color is moving up in value
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption('Geometric Forms')

#####FUNCTIONS
##############
#cartcen is a function that takes a pair of screen coordinates and center, returns a pair of cartesian coordinates relative to that center
def cartcen(point, c):
    point = list(point)
    c = list(c)
    z = [0,0]

    if point[0] <= c[0]:
        z[0] = -(c[0] - point[0])
    else:
        z[0] = point[0] - c[0]
    if point[1] <= c[1]:
        z[1] = c[1] - point[1]
    else:
        z[1] = -(point[1] - c[1])
    return tuple(z)

#cartscreen is a function that takes a pair of cartesian coordinates relative to a given center and returns a pair of screen coordinates
def cartscreen(point, c):
    point = list(point)
    c = list(c)
    a = [0,0]

    if point[0] <= 0:
        a[0] = c[0] - math.fabs(point[0])
    else:
        a[0] = c[0] + point[0]
    if point[1] <= 0:
        a[1] = c[1] + math.fabs(point[1])
    else:
        a[1] = c[1] - point[1]
    return tuple(a)

#ripple is a function that takes a color, center point, radius 
#thickness and spacing distance and draws a circular ripple
def ripple(col, cen, rad, thick, dist):
    pygame.draw.circle(screen, col, cen, rad, thick)
    d = (rad - dist)
    while 0 < d:
        pygame.draw.circle(screen, col, cen, d, thick)
        d = (d - dist)


#rotate takes a set of points and rotates them phi angles relative to a given center
def rotate(points, c, phi):
    points = list(points)   #original screencoordinate points
    cartpoints = []         #original catesian points, with c as center
    compoints = []          #original cartesian points in complex form
    polarpoints = []        #original cartesian points in polar form
    newpolarpoints = []     #rotated cartesian points in polar form
    newcompoints = []       #rotated cartesian points in complex form
    screenpoints = []       #rotated screencoordinate points
    for p in points:
        cartpoints.append(cartcen(p, c))
    for p in cartpoints:
        compoints.append(complex(p[0], p[1]))
    for p in compoints:
        polarpoints.append(cmath.polar(p))
    for p in polarpoints:
        newpolarpoints.append((p[0], p[1] + phi))
    for p in newpolarpoints:
        newcompoints.append(cmath.rect(p[0], p[1]))
    for p in newcompoints:
        screenpoints.append(cartscreen((p.real, p.imag), c))
    return tuple(screenpoints)

#####OTHER STUFF
################
#Triangles
#Initial Triangle, points relative to Cen, screen coordinates
T = ((Cen[0] - R*(math.sqrt(3)/2), Cen[1] - math.sqrt(R**2 - (R*(math.sqrt(3)/2))**2)),
     (Cen[0] + R*(math.sqrt(3)/2), Cen[1] - math.sqrt(R**2 - (R*(math.sqrt(3)/2))**2)), 
     (Cen[0], Cen[1] + R))
#Bigger triangle
Tbig = ((Cen[0] - (R+75)*(math.sqrt(3)/2), Cen[1] - math.sqrt((R+75)**2 - ((R+75)*(math.sqrt(3)/2))**2)),
     (Cen[0] + (R+75)*(math.sqrt(3)/2), Cen[1] - math.sqrt((R+75)**2 - ((R+75)*(math.sqrt(3)/2))**2)), 
     (Cen[0], Cen[1] + (R+75)))
#Smaller triangle
Tsmall = ((Cen[0] - (R-75)*(math.sqrt(3)/2), Cen[1] - math.sqrt((R-75)**2 - ((R-75)*(math.sqrt(3)/2))**2)),
     (Cen[0] + (R-75)*(math.sqrt(3)/2), Cen[1] - math.sqrt((R-75)**2 - ((R-75)*(math.sqrt(3)/2))**2)), 
     (Cen[0], Cen[1] + (R-75)))
#A square, points relative to Cen
S = ((Cen[0] - R, Cen[1] - R), (Cen[0] + R, Cen[1] - R), (Cen[0] + R, Cen[1] + R), (Cen[0] - R, Cen[1] + R))
#A polygon
P = ((300, 100), (325, 150), (400, 150), (325, 200), (350, 300), (300, 250), (250, 300), (275, 200), (200, 150), (275, 150))

#------------------------------RUN TIME---------------------------------------#
while True:
    screen.fill(screenColor)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.draw.polygon(screen, (0,0,0), T, 3)              #triangle
    pygame.draw.polygon(screen, (0,0,0), Tbig, 3)           #bigger triangle
    pygame.draw.polygon(screen, (0,0,0), Tsmall, 3)         #smaller triangle
    pygame.draw.circle(screen, (0,0,0), Cen, 2, 0)          #center point
    ripple((0,0,0), Cen, R/2, 2, 10)                        #circles
    pygame.display.update()
    clock.tick(30)
                 
    #update background color
    if colorUp:
        if screenColorTemp[0] < 255:
            screenColorTemp[0] += 1
        elif screenColorTemp[1] < 255:
            screenColorTemp[1] +=1
        elif screenColorTemp[2] < 155:
            screenColorTemp[2] += 1
        else:
            colorUp = False
    else:
        if screenColorTemp[0] > 0:
            screenColorTemp[0] -= 1
        elif screenColorTemp[1] > 0:
            screenColorTemp[1] -=1
        elif screenColorTemp[2] > 100:
            screenColorTemp[2] -= 1
        else:
            colorUp = True
    screenColor = tuple(screenColorTemp)

    T = rotate(T, Cen, phi)         #rotate T
    Tbig = rotate(Tbig, Cen, phi)   #rotate Tbig
    Tsmall = rotate(Tsmall, Cen, phi)   #rotate Tsmall
