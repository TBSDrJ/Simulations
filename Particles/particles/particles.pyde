# Processing uses Python 2.7, this import the Python 3 print function
from __future__ import print_function
from random import randrange

SIZE = 840
PARTICLES = 8
# Both Edges and Particles will be in this list
# Notice that I created a .repel() method in both classes, so I can just call
#   obj.repel() whether the obj is an Edge or a Particle.
objs = []

def setup():
    # I need to declare the global variable in order to modify it
    global objs
    size(SIZE, SIZE)
    # print("Creating Edges")
    objs.append(Edge(x = 0))
    objs.append(Edge(x = SIZE))
    objs.append(Edge(y = 0))
    objs.append(Edge(y = SIZE))
    for i in range(PARTICLES):
        x = randrange(1, SIZE)
        y = randrange(1, SIZE)
        objs.append(Particle(x, y))
        # print("Creating particle", i, "at", x, ",", y)

def draw():
    # Wipe the window for the new frame
    background(0, 0, 0)
    # Draw the particles; the edges are the first 4 objects
    for particle in objs[4:]:
        circle(particle.x, particle.y, 50)
    i = 0
    part_str = ""
    # We only need to calculate new positions for particles
    for obj in objs[4:]:
        # Put each particle is repelled by all objects, including edges
        for other in objs:
            # Don't try to repel itself, that would divide by zero.
            if obj != other:
                i += 1
                repel = other.repel(obj)
                obj.x += repel[0]
                obj.y += repel[1]
        # If a particle goes off-screen, put it back on-screen
        if obj.x < 0:
            obj.x = 1
        if obj.y < 0:
            obj.y = 1
        if obj.x > SIZE:
            obj.x = SIZE - 1
        if obj.y > SIZE:
            obj.y = SIZE - 1
        # part_str += "(" + str(obj.x) + "," + str(obj.y) + ")"
    # print(part_str)
            
class Edge(object):
    # An Edge is literally the edge of the screen
    def __init__(self, x=None, y=None):
    # We expect to get x or y, but not both so we made x,y optional arguments
        # Crash the program if we got neither x,y or both
        if x is None and y is None:
            raise ValueError("Can't create Edge instance with no coordinate given.  Provide either an x or a y coordinate.")
        if x is not None and y is not None:
            raise ValueError("Can't create Edge instance with both coordinate given.  Provide either an x or a y coordinate.")
        # Whichever was not passed in will be None, that was the default value
        self.x = x
        self.y = y
        self.repel_const = 250
    

    def repel(self, other):
        # Apply the repelling force on a particle, perpendicular to the edge
        # Force is proportional to reciprocal of distance, so closer => stronger
        if self.x is not None:
            return (self.repel_const * other.repel_const / (other.x - self.x), 0)
        elif self.y is not None:
            return (0, self.repel_const * other.repel_const / (other.y - self.y))
        
class Particle(object):
    # A particle is a freely moving object that repels all other particles
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.repel_const = (20 + PARTICLES) / PARTICLES

    def repel(self, other):
        # Apply the repelling force of a particle, closer => stronger
        distance = dist(self, other)
        if distance > 0:
            x_repel = self.repel_const * (other.x - self.x) / distance
            y_repel = self.repel_const * (other.y - self.y) / distance
        else:
            # Really unlikely that distance == 0, but avoid a crash if so
            x_repel = randrange(1,10)
            y_repel = randrange(1,10)
        return (x_repel, y_repel)
    
def dist(obj1, obj2):
    # Just usual Pythagorean distance formula
    return sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) 
