from __future__ import print_function
from random import randrange

SIZE = 840
PARTICLES = 8
objs = []

def setup():
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
    background(0, 0, 0)
    for particle in objs[4:]:
        circle(particle.x, particle.y, 50)
    i = 0
    part_str = ""
    for obj in objs[4:]:
        for other in objs:
            if obj != other:
                i += 1
                repel = other.repel(obj)
                obj.x += repel[0]
                obj.y += repel[1]
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
    def __init__(self, x=None, y=None):
    # We expect to get x or y, but not both
        if x is None and y is None:
            raise ValueError("Can't create Edge instance with no coordinate given.  Provide either an x or a y coordinate.")
        if x is not None and y is not None:
            raise ValueError("Can't create Edge instance with both coordinate given.  Provide either an x or a y coordinate.")
        self.x = x
        self.y = y
        self.repel_const = 250
    

    def repel(self, other):
        if self.x is not None:
            return (self.repel_const * other.repel_const / (other.x - self.x), 0)
        elif self.y is not None:
            return (0, self.repel_const * other.repel_const / (other.y - self.y))
        
class Particle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.repel_const = (20 + PARTICLES) / PARTICLES

    def repel(self, other):
        distance = dist(self, other)
        if distance > 0:
            x_repel = self.repel_const * (other.x - self.x) / distance
            y_repel = self.repel_const * (other.y - self.y) / distance
        else:
            x_repel = randrange(1,10)
            y_repel = randrange(1,10)
        return (x_repel, y_repel)
    
def dist(obj1, obj2):
    return sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) 
