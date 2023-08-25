from random import randrange

# Following distance of one car to another.  1 car length = 80 pixels
NEAR_TEST = 240
# Width of the window showing the road.  Height depends on # of lanes
WIDTH = 1200

# Number of lanes in my road
lanes = 3
# Counting frames drawn so we can generate new traffic on a schedule
frames = 0
# List of all cars on the road, excluding me
cars = []

def setup():
    # Create the window, leave room for edge lines
    size(WIDTH, 100*lanes + 30)
    # Any global variables to be modified have to be declared here
    global me, cars
    me = MyCar(0)
    for i in range(randrange(2, 5*lanes)):
        cars.append(generate_new_car())

def draw():
    global frames, cars
    # Set background to dark gray
    background(60, 60, 60)
    # Count frames
    frames += 1
    road = Road()
    road.draw_road()
    # Draw my car, adjust as needed
    me.draw_car()
    me.check_near()
    me.check_speeds()
    # Draw and adjust other cars
    for car in cars:
        car.draw_car()
        car.check_near()
    # Check who's far enough off-screen that they're not coming on-screen
    purge_cars()
    # Every once in a while, add a new car
    if frames % 160 == 0:
        cars.append(generate_new_car())
        # If needed, print car stats
        my_str = str(len(cars))
        for car in cars:
            my_str += "\t" + str(car.lane) + "," + str(int(car.x))
        # print(my_str)

class Road:
    # This draws the road
    def __init__(self):
        self.line_color = color(195, 195, 195)
        self.left_edge_color = color(255, 195, 60)
        
    def draw_road(self):
        '''
        "with pushMatrix" allows you to do a temporary movement to draw some
        stuff, and then when you exit the "with" block, the location of the 
        cursor resets back to (0, 0).
        '''  
        with pushMatrix():
            self.draw_edge_lines()
        with pushMatrix():
            self.draw_lane_lines()
    
    def draw_edge_lines(self):
        with pushMatrix():
            translate(0, 10)
            fill(self.line_color)
            rect(0, 0, WIDTH, 10)
            translate(0, lanes*100)
            fill(self.left_edge_color)
            rect(0, 0, WIDTH, 10)
    
    def draw_lane_lines(self):
            translate((frames % 60)*5 - 150, 10)
            for i in range(lanes - 1):
                translate(0, 100)
                with pushMatrix():            
                    for j in range(5):
                        fill(self.line_color)
                        rect(0, 0, 125, 10)
                        translate(300, 0)
    
class Car(object):
    # Not intended to be called directly, use the classes that inherit from it 
    def __init__(self, lane):
        # Used when changing lanes
        self.changing_lanes = False
        # Which direction we're changing: left (-1) or right (+1)
        self.changing_lanes_dir = 0
        # Number: 0 -> lane - 1
        self.lane = lane
        # If you have to slow down because someone is in front of you, keep
        # track of how fast you were going
        self.previous_speed = self.speed
        # Which frame number the car finished changing lanes.
        self.changed_lanes_frame = 0

    def draw_car(self):
        # Find the new correct location, both forward/back (x), and lane (y)
        self.x += self.speed * 10
        with pushMatrix():
            translate(self.x, 100*self.lane + 40)
            fill(self.color)
            rect(0, 0, 80, 50)
        if self.changing_lanes:
            self.lane += self.changing_lanes_dir * 0.05
            if abs(self.lane - round(self.lane)) < 0.01:
                self.changing_lanes = False
                self.changing_lanes_dir = 0
                self.lane = int(round(self.lane))
                self.speed = self.previous_speed
                self.changed_lanes_frame = frames
                # print("Done changing lanes")
        
    def change_lanes(self, dir):
        # To change lanes, just change the attributes, draw_car does the rest
        self.changing_lanes = True
        self.changing_lanes_dir = dir
    
    def check_near(self):
        # To see if another car is near enough to change this car's behavior
        near = False
        for i, car in enumerate(cars):
            # Avoid checking self, you're always near yourself
            if self != car:
                if self.lane == car.lane and self.x - car.x < NEAR_TEST and self.x - car.x > 0:
                    near = True
                    near_car_index = i
        if self != me:
            if self.lane == me.lane and self.x - me.x < NEAR_TEST and self.x - me.x > 0:
                near = True
                near_car_index = -1
        if not self.changing_lanes:
            # Any time a car is not in the right lane, and it can go right, it
            # should go right.
            blocked_right = False
            # Include me in cars that might need to get right
            cars.append(me)
            for car in cars:
                if car != self:
                    if car.lane == self.lane - 1 and abs(car.x - self.x) < NEAR_TEST:
                        blocked_right = True
                    if car.changing_lanes and abs(car.x - self.x) < NEAR_TEST:
                        blocked_right = True
            if not blocked_right and self.lane > 0 and not self.changing_lanes:
                if frames > self.changed_lanes_frame + 20:
                    self.change_lanes(-1)
            # But don't leave me in the list of cars
            cars.pop(-1)
        # If any car had to slow down, turn it red.
        if near:
            self.color = color(195, 45, 45)
            self.adjust(near_car_index)
        # Turn back to the original color, blue or green
        elif self != me:
            self.color = color(80, 80, 120)
        else:
            self.color = color(45, 195, 45)
            self.speed = self.previous_speed
        return near
    
    def adjust(self, near_car_index):
        # If one car is overtaking another, and can move left, move left,
        #   otherwise slow down.
        cars.append(me)
        blocked_left = False
        for car in cars:
            if car != self:
                if car.lane == self.lane + 1 and abs(car.x - self.x) < NEAR_TEST:
                    blocked_left = True
                if car.changing_lanes and abs(car.x - self.x) < NEAR_TEST:
                    blocked_left = True                    
        if not blocked_left and self.lane < lanes - 1 and not self.changing_lanes:
            if frames > self.changed_lanes_frame + 20:
                self.change_lanes(1)
        if near_car_index == -1:
            self.speed = me.speed
        else:
            self.speed = cars[near_car_index].speed
        cars.pop(-1)
    
class MyCar(Car):
    # This car is me, the speed of the simulation always matches my speed.
    # Expects only one instance of this class
    def __init__(self, lane):
        # Set the constants for me.
        self.color = color(45, 195, 45)
        self.x = 450
        self.speed = 0
        self.subtracted = 0
        # At the end, also run the __init__ method from the Car parent class
        super(MyCar, self).__init__(lane)
        
    def check_speeds(self):
        # If my speed goes down, slow down the entire simulator by speeding 
        #   up all the other cars.
        if self.speed > 0:
            self.subtracted = self.speed
            for car in cars:
                if car != self:
                    car.speed -= self.subtracted
            self.speed = 0
        elif self.subtracted > 0 and not self.changing_lanes and not self.check_near():
            for car in cars:
                if car != self:
                    car.speed += self.subtracted
            self.subtracted = 0

class OtherCar(Car):
    # For all the other cars.
    def __init__(self, lane, x, speed):
        self.color = color(80, 80, 120)
        self.x = x
        self.speed = speed
        # Run the parent Car class __init__ method.
        super(OtherCar, self).__init__(lane)
        
def generate_new_car():
    # Algorithm for making additional cars.
    speed = randrange(-6, 7) * 0.05
    # They can go anywhere if the simulation hasn't started running yet.
    if frames == 0:
        x = randrange(-2, WIDTH / 50 + 2) * 50
    else:
        # But if it has started running, try to generate them off-screen.  If
        #   they are faster, start them behind, if slower start them ahead.
        if speed == 0:
            adj = randrange(0,2)
            if adj == 0:
                speed = -0.05
            else:
                speed = 0.05
        if speed > 0:
            x = -100
        elif speed < 0:
            x = WIDTH + 100
    if speed < 0:
        # Make it more likely that slower cars are to the right
        lane_tmp = randrange(0, lanes * lanes)
        lane = lanes - 1
        diff = 1
        lane_tmp -= diff
        while lane_tmp >= 0:
            diff += 2
            lane_tmp -= diff
            lane -= 1
    elif speed > 0:
        # Make it more likely that faster cars are to the left
        lane_tmp = randrange(0, lanes * lanes)
        lane = 0
        diff = 1
        lane_tmp -= diff
        while lane_tmp >= 0:
            diff += 2
            lane_tmp -= diff
            lane += 1
    else:
        lane = randrange(0, lanes)
    # Collision is not an actual collision, but if the location where the car
    #   is about to generate is occupied, move it around until it can find an
    #   unoccupied location.
    collision = True
    while collision:
        # Keep trying to find an open spot for this car to spawn.
        collision = False
        cars.append(me)
        for car in cars:
            if lane == car.lane and abs(x - car.x) < NEAR_TEST:
                collision = True
                # print(lane, x, car.x)
        if collision:
            n = randrange(0,4)
            if n == 0 and lane < lanes - 1:
                lane += 1
            elif n == 1 and lane > 0:
                lane -= 1
            elif n == 2:
                x += NEAR_TEST
            else:
                x -= NEAR_TEST
        cars.pop(-1)
    return OtherCar(lane, x, speed)
        
def purge_cars():
    # If cars get far enough off-screen, drop them out of the list.
    global cars
    to_purge = []
    for i, car in enumerate(cars):
        if car.x > WIDTH + 1000 or car.x < -1000:
            to_purge.append(i)
    for i in to_purge:
        cars.pop(i)
