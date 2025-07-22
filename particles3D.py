# Imports
import pygame, math, random
from Vector import Vector, Matrix, Quaternion
from Particle import Particle3D




# Initialize PyGame
pygame.init()
pygame.display.set_mode((1450, 800))
screen = pygame.display.get_surface()
clock = pygame.time.Clock()




# Generates a rotation matrix for angle a about the x axis
def rotX(a):
    c1 = Vector([1, 0, 0])
    c2 = Vector([0, math.cos(a), math.sin(a)])
    c3 = Vector([0, -math.sin(a), math.cos(a)])
    return Matrix([c1, c2, c3])

# Generates a rotation matrix for angle a about the y axis
def rotY(a):
    c1 = Vector([math.cos(a), 0, -math.sin(a)])
    c2 = Vector([0, 1, 0])
    c3 = Vector([math.sin(a), 0, math.cos(a)])
    return Matrix([c1, c2, c3])

# Generates a rotation matrix for angle a about the z axis
def rotZ(a):
    c1 = Vector([math.cos(a), math.sin(a), 0])
    c2 = Vector([-math.sin(a), math.cos(a), 0])
    c3 = Vector([0, 0, 1])
    return Matrix([c1, c2, c3])

# Alternative rotation method using Rodrigues rotations.
# Quaternions can also be used but not necessary.
def rodriguesRotation(ax, ay):
    cx = math.cos(ax)
    sx = math.sin(ax)
    cy = math.cos(ay)
    sy = math.sin(ay)

    c1 = Vector([cy, 0, sy])
    c2 = Vector([sx*sy, cx, -sx*cy])
    c3 = Vector([-cx*sy, sx, cx*cy])

    return Matrix([c1, c2, c3])

# Draw the cube by checking distances between pairs of points to see if they are adjacent
def drawCube(screen, cube, pcube, color):
    for i in range(len(cube)):
        for j in range(i + 1, len(cube)):
            dist = cube[i].dist(cube[j])
            if round(dist, 5) == 400 or round(dist, 5) == 600:
                start = (0.9 * pcube[i].x() + 400, 0.9 * pcube[i].y() + 400)
                end = (0.9 * pcube[j].x() + 400, 0.9 * pcube[j].y() + 400)
                avg_z = (cube[i].z() + cube[j].z()) / 400
                lum = (avg_z + 1) * 30
                color = pygame.Color(255, 255, 255)
                color.hsla = (0, 0, max(30, min(100, lum)), 100)
                pygame.draw.line(screen, color, start, end, 2)

# Update the cube by applying a matrix transformation to each of its vectors
def updatedCube(cube, matrix):
    new_cube = []
    for v in cube:
        new_cube.append(matrix.mult(v))
    return new_cube

# Generate and apply stereographic projection matrices for each vector in the cube
def getProjCube(cube):
    proj_cube = []
    for v in cube:
        proj_mat = getProjMatrix(v)
        proj_cube.append(proj_mat.mult(v))
    return proj_cube

# Generate the stereographic projection matrix for vector v
def getProjMatrix(v):
    distance = 800
    proj_factor = distance / (distance - v.z())
    c1 = Vector([proj_factor, 0])
    c2 = Vector([0, proj_factor])
    c3 = Vector([0, 0])
    proj_mat = Matrix([c1, c2, c3])
    return proj_mat

# Returns the the new radius of a particle accounting for projection
def getProjSize(v, r):
    distance = 800
    proj_factor = distance / (distance - v.z())
    return r * proj_factor

# Draws a particle to the screen accounting for rotations and projections
def drawParticle(screen, p, rot):
    # Determine the color of the particle from its kinetic energy
    color = pygame.Color(255, 255, 255)
    lum = 50
    hue = max(0, 220 - (220 * p.ke() // 800))
    color.hsla = (hue, 100, min(100, lum), 100)
    # Calculate the x y position of the particle after rotation and projection
    centered_pos = Vector([p.pos.x() - 300, p.pos.y() - 200, p.pos.z() - 200])
    rotated_p = rot.mult(centered_pos)
    proj_mat = getProjMatrix(rotated_p)
    projected_p = proj_mat.mult(rotated_p)
    # Offset the particle and calculate the projected radius
    x = 0.9 * projected_p.x() + 400
    y = 0.9 * projected_p.y() + 400
    r = getProjSize(rotated_p, p.radius)
    # Draw the particle
    pygame.draw.circle(screen, color, (x, y), r)

# Slowly increases the velocity of all particles by scaling by a constant factor
def heat(particles):
    for p in particles:
        p.vel = p.vel.scale(1.02)

# Draws a graph of the total kinetic energy of the system over time
def drawGraph(screen, ke_graph, startX, width, height):
    # Draw text to indicate what is being graphed
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
        x = startX + 40 + (i * 2)
        pygame.draw.line(screen, "purple", prev, (x, y), 2)
        prev = (x, y)

# Draws a Maxwell-Boltzmann distribution representing the energies of all particles
def drawDist(screen, particles, startX, startY, width, height):
    # Draw text to indicate what is being graphed
    drawText(screen, "MAXWELL-BOLTZMANN DISTRIBUTION", startX + width - 25, startY + height // 2, (200, 200, 200), 16, -90)

    # Calculate the histogram size and create the histrogram
    hist_size = ((width // 1) - 1)
    hist = [0 for _ in range(10000)]
    # Determine which velocity bin each particle falls into and fill the histogram accordingly
    for p in particles:
        i = int(hist_size * p.vel.mag() // 29)
        hist[i] += 1
    # Calculate the maximum height for the histogram and scale values accordingly
    max_h = 30 * ((height - 50) * max(hist) / len(particles))
    scale = 1 if max_h < (height - 50) else (height - 50) / max_h

    # Draw the grid lines and scale values
    for i in range(11):
        y =  startY + (height - 25) - ((height - 50) * i // 10)
        val = 3.333 * i / (10 * scale)
        drawText(screen, str(round(val, 1)) + "%", startX + 20, y, "white")
        x1 = startX + 40
        x2 = startX + width - 50
        pygame.draw.line(screen, (42, 42, 42), (x1, y), (x2, y), 1)
    
    # Draw the histogram bars
    for i, h in enumerate(hist):
        x = startX + 50 + (i*1)
        val = scale * 30 * ((height - 50) * h / len(particles))
        y = startY + height - 20 - val
        color = pygame.Color(255, 255, 255)
        hue = max(0, 250 - (scale * 250 * i // 230))
        color.hsla = (hue, 100, 50, 100)
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











# Create a rectangular prism (called cube) centered at the origin
cube = [
    Vector([-300, -200, -200]), Vector([-300, -200, 200]),
    Vector([-300, 200, -200]), Vector([-300, 200, 200]),
    Vector([300, -200, -200]), Vector([300, -200, 200]),
    Vector([300, 200, -200]), Vector([300, 200, 200]),
]

# State variables
start_click = pygame.mouse.get_pos()
clicking = False
heating = False
base_x_angle = 0
base_y_angle = 0
space_anim = False

# Initializing the particles in their zones and set friction value
friction = 0.98
zones = [[[set() for _ in range(40)] for _ in range(40)] for _ in range(60)]
particles = []
for _ in range(500):
    mass = 20
    x = random.randint(10, 590)
    y = random.randint(10, 390)
    z = random.randint(10, 390)
    pos = Vector([x, y, z])
    vx = random.uniform(-10, 10)
    vy = random.uniform(-10, 10)
    vz = random.uniform(-10, 10)
    vel = Vector([vx, vy, vz])
    p = Particle3D(mass, pos, vel, 20, 20, 20, zones)
    particles.append(p)

# Initializing kinetic energy variables to make the graphs
total_ke = sum([p.ke() for p in particles])
ke_graph = [total_ke for _ in range(282)]




##### MAIN LOOP #####
while True:
    # Fill the screen with a background color
    screen.fill((0, 0, 0))

    # Event loop
    for event in pygame.event.get():

        # Handle quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Handle mouse click and movement by checking for mouse down and mouse up
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True
            space_anim = False
            start_click = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            clicking = False
            base_x_angle = x_angle
            base_y_angle = y_angle
        
        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            # Start animation to go back to the original view when space is pressed
            if event.key == pygame.K_SPACE:
                space_anim = True
                base_x_angle %= math.pi * 2
                base_y_angle %= math.pi * 2
                if base_x_angle > math.pi:
                    base_x_angle -= math.pi * 2
                if base_y_angle > math.pi:
                    base_y_angle -= math.pi * 2
            if event.key == pygame.K_UP:
                heating = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                heating = False
    
    # Slowly reduce angles back to zero if reset animation is active
    if round(base_x_angle, 5) == 0 and round(base_y_angle, 5) == 0:
        space_anim = False
    if space_anim:
        base_x_angle *= 0.8
        base_y_angle *= 0.8

    # Determine rotation angles based on where the mouse left off after the last click
    x_angle = base_x_angle
    y_angle = base_y_angle

    # Adjust the rotation angles if the mouse is currently moving
    if clicking:
        mouse_pos = pygame.mouse.get_pos()
        x_angle += (0.004 * (start_click[1] - mouse_pos[1]))
        y_angle += (0.004 * (mouse_pos[0] - start_click[0]))
        if x_angle > math.pi / 2.0:
            x_angle = math.pi / 2.0
        elif x_angle < -math.pi / 2.0:
            x_angle = -math.pi / 2.0

    if heating:
        heat(particles)
    
    # Generate the rotation matrices and compose them then apply to the cube
    x_rot = rotX(x_angle)
    y_rot = rotY(y_angle)
    rot = x_rot * y_rot
    rotated = updatedCube(cube, rot)

    for i in range(len(particles)):
        # Update the current particle
        particles[i].update(600, 400, 400, friction)
        # Current particle's zone
        zone = particles[i].zone
        # Set of already done collisions to avoid duplicates
        collisions = set()
        # Check collisions with other particles in nearby zones
        for xzone in range(zone[0] - 1, zone[0] + 2):
            for yzone in range(zone[1] - 1, zone[1] + 2):
                for zzone in range(zone[2] - 1, zone[2] + 2):
                    if 0 <= xzone < 60 and 0 <= yzone < 40 and 0 <= zzone < 40:
                        for p in zones[xzone][yzone][zzone]:
                            # Check that this collision has not already been done and
                            # that we are not colliding with ourself
                            if particles[i] != p and (p, particles[i]) not in collisions:
                                particles[i].collide(p, friction)
                                collisions.add((particles[i], p))
        # Draw the particle keeping in mind the rotations
        drawParticle(screen, particles[i], rot)


    # Draw the cube projected into the xy plane and update the display
    drawCube(screen, rotated, getProjCube(rotated), "white")

    # Draw the kinetic energy graph and the Maxwell-Boltzmann distributions
    ke_graph.pop(0)
    ke_graph.append(sum([p.ke() for p in particles]))
    pygame.draw.rect(screen, "black", (800, 0, 650, 800))
    drawGraph(screen, ke_graph, 800, 650, 400)
    drawDist(screen, particles, 800, 400, 650, 400)
    pygame.draw.line(screen, (150, 150, 150), (800, 400), (1450, 400), 2)
    pygame.draw.line(screen, (150, 150, 150), (800, 0), (800, 800), 2)
    pygame.draw.rect(screen, (150, 150, 150), (0, 0, 1450, 800), 2)


    # Update the display, set caption to show the kinetic energy, and tick the clock at a maximum of 500 fps
    pygame.display.update()
    pygame.display.set_caption(f"Total Kinetic Energy: {getExpText(int(sum([p.ke() for p in particles])))}    |    FPS: {int(clock.get_fps())}")
    clock.tick(500)
