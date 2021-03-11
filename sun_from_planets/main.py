import pygame

pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 30)

size = width, height = 1000, 1000
win = pygame.display.set_mode(size)

scale = 40
scaleEarth = 149_600_000

distanceMercury = scale * (scaleEarth/57_909_000)
distanceVenus = scale * (scaleEarth/108_160_000)
distanceEarth = scale * (scaleEarth/149_600_000)
distanceMars = scale * (scaleEarth/227_990_000)
distanceJupiter = scale * (scaleEarth/778_360_000)
distanceSaturn = scale * (scaleEarth/1_433_500_000)
distanceUranus = scale * (scaleEarth/2_872_400_000)
distanceNeptune = scale * (scaleEarth/4_498_400_000)
distancePluto = scale * (scaleEarth/5_906_380_000)

print(distanceEarth)
print(distanceMars)

def gradient(win, x, y, width, height, startColor, endColor):
    for row in range(y, height):
        r = row / (height-1) * endColor[0]
        g = row / (height-1) * endColor[1]
        b = row / (height-1) * endColor[2]

        pygame.draw.rect(win, (r, g, b), (0, row, width, row))


def draw_horizon(win):
    hh = int(0.5*height)
    gradient(win, 0, 0, width, hh, (0,0,0), (135, 206, 235))
    gradient(win, 0, hh, width, height, (0,0,0), (148,62,15))
    #pygame.draw.rect(win, (135, 206, 235), (0, 0, hw, hh))

class Sun:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self, win):
        pygame.draw.circle(win, (239, 142, 56), (self.x, self.y), int(self.r))


planets = [
    Sun(300, 300, distanceMercury),
    Sun(300, 300, distanceVenus),
    Sun(300, 300, distanceEarth),
    Sun(300, 300, distanceMars),
    Sun(300, 300, distanceJupiter),
    Sun(300, 300, distanceSaturn),
    Sun(300, 300, distanceUranus),
    Sun(300, 300, distanceNeptune),
    Sun(300, 300, distancePluto),
]
planet = 2
planetName = "Earth"
run = True
while run:
    win.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP1:
                planet = 0
                planetName = "Mercury"
            if event.key == pygame.K_KP2:
                planet = 1
                planetName = "Venus"
            if event.key == pygame.K_KP3:
                planet = 2
                planetName = "Earth"
            if event.key == pygame.K_KP4:
                planet = 3
                planetName = "Mars"
            if event.key == pygame.K_KP5:
                planet = 4
                planetName = "Jupiter"
            if event.key == pygame.K_KP6:
                planet = 5
                planetName = "Saturn"
            if event.key == pygame.K_KP7:
                planet = 6
                planetName = "Uranus"
            if event.key == pygame.K_KP8:
                planet = 7
                planetName = "Neptun"
            if event.key == pygame.K_KP9:
                planet = 8
                planetName = "Pluto"

        
    draw_horizon(win)
    planets[planet].draw(win)
    textSurface = myFont.render(planetName, True, (0, 0, 0))
    win.blit(textSurface, (0.5*width, 10))
    
    pygame.display.update()
  
