##### IMPORTS #####
import pygame, sys, random, math
from pygame.locals import *
from Vector import Vector
from Particle import Particle






##### INITIALIZATION #####
# Global simulation constants
width = 800
height = 800
rows = 100
cols = 100
friction = 0.995
mass = 20

# PyGame Initialization
pygame.init()
screen = pygame.display.set_mode((width + 650, height))
clock = pygame.time.Clock()

# Simulation variables
particles = []
zones = [[set() for _ in range(cols)] for _ in range(rows)]
clicking = False
space_pressed = False
click_opacity = 0
click_size = 0

# Create particles
for i in range(1000):
    pos = Vector([random.randint(mass, width - mass), random.randint(mass, height - mass)])
    vel = Vector([random.uniform(-10, 10), random.uniform(-10, 10)])
    p = Particle(mass, pos, vel, height // rows, width // cols, zones)
    particles.append(p)

# Graph variables
total_ke = sum([p.ke() for p in particles])
ke_graph = [total_ke for _ in range(141)]






##### FUNCTIONS #####
# Increases the velocity of all particles within a certain radius of the click
def handleClick(particles, pos):
    vec = Vector([pos[0], pos[1]])
    for p in particles:
        if p.pos.dist(vec) < 70:
            p.vel += p.vel.norm().scale(6)

def handleSpace(particles, pos):
    vec = Vector([pos[0], pos[1]])
    for p in particles:
        scalar = (80 / (p.pos - vec).mag())
        p.vel -= (p.pos - vec).norm().scale(min(300, scalar))

# Draws a graph of the total kinetic energy of the system over time
def drawGraph(screen, ke_graph, startX, width, height):
    drawText(screen, "KINETIC ENERGY OVER TIME", startX + width - 25, height // 2, (200, 200, 200), 16, -90)

    # Find the current maximum value of the kinetic energy graph
    m = max(ke_graph)
    # Draw the grid lines and scale values
    for i in range(11):
        y = (height - 25) - ((height - 50) * i // 10)
        val = m * i / 10
        drawText(screen, getExpText(int(val)), startX + 20, y, "white")
        x1 = startX + 40
        x2 = startX + width - 50
        pygame.draw.line(screen, (42, 42, 42), (x1, y), (x2, y), 1)

    # Set the previous point to start drawing line segments
    y = (height - 25) - ((height - 50) * ke_graph[0] / m)
    x = startX + 40
    prev = (x, y)
    # Create a graph by drawing lines between points in the kinetic energy graph
    for i, ke in enumerate(ke_graph):
        y = (height - 25) - ((height - 50) * ke / m)
        x = startX + 40 + (i * 4)
        pygame.draw.line(screen, "purple", prev, (x, y), 2)
        prev = (x, y)

def drawDist(screen, particles, startX, startY, width, height):
    drawText(screen, "MAXWELL-BOLTZMANN DISTRIBUTION", startX + width - 25, startY + height // 2, (200, 200, 200), 16, -90)

    hist_size = ((width // 1) - 1)
    hist = [0 for _ in range(10000)]
    for p in particles:
        i = int(hist_size * p.vel.mag() // 39)
        hist[i] += 1
    max_h = 50 * ((height - 50) * max(hist) / len(particles))
    scale = 1 if max_h < (height - 50) else (height - 50) / max_h

    for i in range(11):
        y =  startY + (height - 25) - ((height - 50) * i // 10)
        val = 2 * i / (10 * scale)
        drawText(screen, str(round(val, 1)) + "%", startX + 20, y, "white")
        x1 = startX + 40
        x2 = startX + width - 50
        pygame.draw.line(screen, (42, 42, 42), (x1, y), (x2, y), 1)
    
    for i, h in enumerate(hist):
        x = startX + 50 + (i*1)
        val = scale * 50 * ((height - 50) * h / len(particles))
        y = startY + height - 20 - val
        color = pygame.Color(255, 255, 255)
        lum = 50
        hue = max(0, 220 - (scale * 220 * i // 350))
        color.hsla = (hue, 100, min(100, lum), 100)
        pygame.draw.rect(screen, color, (x, y, 1, val))

# Returns a string of the value in exponential form (1230 --> 1.2e3, 627 --> 627)
def getExpText(val):
    text = str((val))
    if val > 999:
        exp = 0
        while val >= 10:
            val /= 10
            exp += 1
        val = round(val, 1)
        text = f"{val}e{exp}"
    return text

# Draws text to the screen at a certain location
def drawText(screen, text, x, y, color, size=11, angle=0):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    text_surface =  pygame.transform.rotate(text_surface, angle)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def drawClick(screen, opacity, size):
    color = pygame.Color(150, 150, 150)
    h, s, l, a = color.hsla
    color.hsla = (h, s, max(opacity, 0), max(opacity, 0))
    pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, color, pos, size)






##### MAIN LOOP #####
while True:
    click_opacity -= 10
    if click_opacity < 0:
        click_opacity = 0
        click_size = 0
    ke_graph.pop(0)
    ke_graph.append(sum([p.ke() for p in particles]))
    # Event handler loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            clicking = True
        if event.type == MOUSEBUTTONUP:
            clicking = False
            # click_size = 0
        if event.type == KEYDOWN and event.key == K_SPACE:
            space_pressed = True
        if event.type == KEYUP and event.key == K_SPACE:
            space_pressed = False
    if clicking and space_pressed:
        handleSpace(particles, pygame.mouse.get_pos())
        click_opacity = 50
        click_size = min(click_size + 20, 70)
    elif clicking:
        handleClick(particles, pygame.mouse.get_pos())
        click_opacity = 50
        click_size = min(click_size + 20, 70)
    
    # Fills the background with black
    screen.fill((0, 0, 0))
    drawClick(screen, click_opacity, click_size)
    drawGraph(screen, ke_graph, width, 650, height // 2)
    drawDist(screen, particles, width, 400, 650, height // 2)
    pygame.draw.line(screen, (150, 150, 150), (width, height // 2), (width + 650, height // 2), 2)
    pygame.draw.line(screen, (150, 150, 150), (width, 0), (width, height), 2)
    pygame.draw.rect(screen, (150, 150, 150), (0, 0, width + 650, height), 2)

    # Update and draw particles and handle collisions and wall collisions
    for i in range(len(particles)):
        # Update the current particle
        particles[i].update(width, height, friction)
        # Current particle's zone
        zone = particles[i].zone
        # Set of already done collisions to avoid duplicates
        collisions = set()
        # Check collisions with other particles in nearby zones
        for zrow in range(zone[0] - 1, zone[0] + 2):
            for zcol in range(zone[1] - 1, zone[1] + 2):
                if 0 <= zrow < rows and 0 <= zcol < cols:
                    for p in zones[zrow][zcol]:
                        # Check that this collision has not already been done and
                        # that we are not colliding with ourself
                        if particles[i] != p and (p, particles[i]) not in collisions:
                            particles[i].collide(p, friction)
                            collisions.add((particles[i], p))
        # Draw the particle
        particles[i].draw(screen)
    
    # Update the display and set the caption to the total kinetic energy of the system
    pygame.display.update()
    pygame.display.set_caption(f"Total Kinetic Energy: {getExpText(int(sum([p.ke() for p in particles])))}    |    FPS: {int(clock.get_fps())}")
    clock.tick(500)
