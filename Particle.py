import pygame

class Particle:
    # Initialize a particle with mass, position, and velocity
    def __init__(self, mass, pos, vel, rsize, csize, zones):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.radius = mass / 3
        self.rsize = rsize
        self.csize = csize
        self.zone = (int(pos.y() // rsize), int(pos.x() // csize))
        self.zones = zones
        self.zones[self.zone[0]][self.zone[1]].add(self)
    
    # Get the momentum of the particle based on its mass and velocity
    def mom(self):
        return self.vel.scale(self.mass)
    
    # Get the kinetic energy of the particle based on its mass and velocity
    def ke(self):
        return 0.5 * self.mass * (self.vel.mag() ** 2)
    
    # Update position based on velocity and velocity based on acceleration
    def update(self, maxX, maxY, damping=1):
        # Update position based on velocity
        self.pos = self.pos + self.vel

        # Handle wall collisions
        self.checkWalls(maxX, maxY, damping)

        # Determine new zone (row and column)
        row = int(self.pos.y() // self.rsize)
        col = int(self.pos.x() // self.csize)

        # Check if the zone has changed and update accordingly
        if self.zone != (row, col):
            self.zones[self.zone[0]][self.zone[1]].remove(self)
            self.zone = (row, col)
            self.zones[row][col].add(self)


    # Check for an handle an elastic collison between self and other with optional damping
    def collide(self, other, damping=1):
        # Check if the two particles are colliding
        if self.pos.dist(other.pos) < self.radius + other.radius:
            # Make overlapping particles just barely touch
            overlap = (other.pos - self.pos).mag() - (self.radius + other.radius)
            other.pos -= (other.pos - self.pos).norm().scale(0.5 * overlap)
            self.pos -= (self.pos - other.pos).norm().scale(0.5 * overlap)

            # Calculate relative position and velocity vectors
            self_diff = other.pos - self.pos
            other_diff = self.pos - other.pos
            self_vel_diff = other.vel - self.vel
            other_vel_diff = self.vel - other.vel

            # Adjust velocity of particle 1 based on conservation of momentum
            self_proj = self_vel_diff.proj(self_diff)
            self.vel += self_proj.scale(2 * other.mass / (self.mass + other.mass))

            # Adjust velocity of particle 2 based on conservation of momentum
            other_proj = other_vel_diff.proj(other_diff)
            other.vel += other_proj.scale(2 * self.mass / (self.mass + other.mass))

            # Dampen particle velocities to simulate friction
            self.vel = self.vel.scale(damping)
            other.vel = other.vel.scale(damping)
    
    # Checks for and handles elastic collision with a wall with otional damping
    def checkWalls(self, maxX, maxY, damping=1):
        # Check left wall collision
        if self.pos.x() - self.radius < 0:
            self.vel.setX(self.vel.x() * -1)
            self.pos.setX(self.radius)
            self.vel = self.vel.scale(damping)
        # Check right wall collision
        elif self.pos.x() + self.radius > maxX:
            self.vel.setX(self.vel.x() * -1)
            self.pos.setX(maxX - self.radius)
            self.vel = self.vel.scale(damping)
        # Check top wall collision
        if self.pos.y() - self.radius < 0:
            self.vel.setY(self.vel.y() * -1)
            self.pos.setY(self.radius)
            self.vel = self.vel.scale(damping)
        # Check bottom wall collision
        elif self.pos.y() + self.radius > maxY:
            self.vel.setY(self.vel.y() * -1)
            self.pos.setY(maxY - self.radius)
            self.vel = self.vel.scale(damping)
    
    def draw(self, screen):
        color = pygame.Color(255, 255, 255)

        # hue = 0 if self.ke() > 1000 else 220
        # dev = min(1, abs(self.ke() - 1000) / 1000)
        # lum = 50 + (50 * (1 - dev))
        lum = 50
        hue = max(0, 220 - (220 * self.ke() // 3000))

        color.hsla = (hue, 100, min(100, lum), 100)
        pygame.draw.circle(screen, color, (self.pos.x(), self.pos.y()), self.radius)








import pygame

class Particle3D:
    # Initialize a particle with mass, position, and velocity
    def __init__(self, mass, pos, vel, xsize, ysize, zsize, zones):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.radius = mass / 2
        self.xsize = xsize
        self.ysize = ysize
        self.zsize = zsize
        x = int(self.pos.x() // self.xsize)
        y = int(self.pos.y() // self.ysize)
        z = int(self.pos.z() // self.zsize)
        self.zone = (x, y, z)
        self.zones = zones
        self.zones[self.zone[0]][self.zone[1]][self.zone[2]].add(self)
    
    # Get the momentum of the particle based on its mass and velocity
    def mom(self):
        return self.vel.scale(self.mass)
    
    # Get the kinetic energy of the particle based on its mass and velocity
    def ke(self):
        return 0.5 * self.mass * (self.vel.mag() ** 2)
    
    # Update position based on velocity and velocity based on acceleration
    def update(self, maxX, maxY, maxZ, damping=1):
        # Update position based on velocity
        self.pos = self.pos + self.vel

        # Handle wall collisions
        self.checkWalls(maxX, maxY, maxZ, damping)

        # Determine new zone (row and column)
        x = int(self.pos.x() // self.xsize)
        y = int(self.pos.y() // self.ysize)
        z = int(self.pos.z() // self.zsize)

        # Check if the zone has changed and update accordingly
        if self.zone != (x, y, z):
            if self in self.zones[self.zone[0]][self.zone[1]][self.zone[2]]:
                self.zones[self.zone[0]][self.zone[1]][self.zone[2]].remove(self)
            self.zone = (x, y, z)
            self.zones[x][y][z].add(self)


    # Check for an handle an elastic collison between self and other with optional damping
    def collide(self, other, damping=1):
        # Check if the two particles are colliding
        if self.pos.dist(other.pos) < self.radius + other.radius:
            # Make overlapping particles just barely touch
            overlap = (other.pos - self.pos).mag() - (self.radius + other.radius)
            other.pos -= (other.pos - self.pos).norm().scale(0.5 * overlap)
            self.pos -= (self.pos - other.pos).norm().scale(0.5 * overlap)

            # Calculate relative position and velocity vectors
            self_diff = other.pos - self.pos
            other_diff = self.pos - other.pos
            self_vel_diff = other.vel - self.vel
            other_vel_diff = self.vel - other.vel

            # Adjust velocity of particle 1 based on conservation of momentum
            self_proj = self_vel_diff.proj(self_diff)
            self.vel += self_proj.scale(2 * other.mass / (self.mass + other.mass))

            # Adjust velocity of particle 2 based on conservation of momentum
            other_proj = other_vel_diff.proj(other_diff)
            other.vel += other_proj.scale(2 * self.mass / (self.mass + other.mass))

            # Dampen particle velocities to simulate friction
            self.vel = self.vel.scale(damping)
            other.vel = other.vel.scale(damping)
    
    # Checks for and handles elastic collision with a wall with otional damping
    def checkWalls(self, maxX, maxY, maxZ, damping=1):
        # Check left wall collision
        if self.pos.x() - self.radius < 0:
            self.vel.setX(self.vel.x() * -1)
            self.pos.setX(self.radius)
            self.vel = self.vel.scale(damping)
        # Check right wall collision
        elif self.pos.x() + self.radius > maxX:
            self.vel.setX(self.vel.x() * -1)
            self.pos.setX(maxX - self.radius)
            self.vel = self.vel.scale(damping)
        # Check top wall collision
        if self.pos.y() - self.radius < 0:
            self.vel.setY(self.vel.y() * -1)
            self.pos.setY(self.radius)
            self.vel = self.vel.scale(damping)
        # Check bottom wall collision
        elif self.pos.y() + self.radius > maxY:
            self.vel.setY(self.vel.y() * -1)
            self.pos.setY(maxY - self.radius)
            self.vel = self.vel.scale(damping)
        # Check back wall collision
        if self.pos.z() - self.radius < 0:
            self.vel.setZ(self.vel.z() * -1)
            self.pos.setZ(self.radius)
            self.vel = self.vel.scale(damping)
        # Check front wall collision
        elif self.pos.z() + self.radius > maxZ:
            self.vel.setZ(self.vel.z() * -1)
            self.pos.setZ(maxZ - self.radius)
            self.vel = self.vel.scale(damping)