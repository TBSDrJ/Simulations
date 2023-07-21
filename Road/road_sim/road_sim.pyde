from random import randrange

NEAR_TEST = 160
WIDTH = 1200

lanes = 3
frames = 0
dir = 0
cars = []


def setup():
    size(WIDTH, 100*lanes + 30)
    global me, cars
    me = MyCar(0)
    for i in range(randrange(2, 5*lanes)):
        cars.append(generate_new_car())

def draw():
    global frames, dir, cars
    background(60, 60, 60)
    frames += 1
    road = Road()
    road.draw_road()
    me.draw_car()
    me.check_near()
    for car in cars:
        car.draw_car()
        car.check_near()
    purge_cars()
    if frames % 80 == 0:
        cars.append(generate_new_car())
        my_str = str(len(cars))
        for car in cars:
            my_str += "\t" + str(car.lane) + "," + str(int(car.x))
        # print(my_str)

class Road:
    def __init__(self):
        self.line_color = color(195, 195, 195)
        self.left_edge_color = color(255, 195, 60)
        
    def draw_road(self):
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
    def __init__(self, lane):
        self.changing_lanes = False
        self.changing_lanes_dir = 0
        self.lane = lane
        self.previous_speed = self.speed

    def draw_car(self):
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
                print("Done changing lanes")
        
    def change_lanes(self, dir):
        self.changing_lanes = True
        self.changing_lanes_dir = dir
    
    def check_near(self):
        near = False
        for i, car in enumerate(cars):
            if self != car:
                if self.lane == car.lane and self.x - car.x < NEAR_TEST and self.x - car.x > 0:
                    near = True
                    near_car_index = i
        if self != me:
            if self.lane == me.lane and self.x - me.x < NEAR_TEST and self.x - me.x > 0:
                near = True
                near_car_index = -1
        if near:
            self.color = color(195, 45, 45)
            self.adjust(near_car_index)
        elif self != me:
            self.color = color(80, 80, 120)
        else:
            self.color = color(45, 195, 45)
            self.speed = self.previous_speed
        return near
    
    def adjust(self, near_car_index):
        if near_car_index == -1:
            self.speed = me.speed
        else:
            self.speed = cars[near_car_index].speed
    
class MyCar(Car):
    def __init__(self, lane):
        self.color = color(45, 195, 45)
        self.x = 450
        self.speed = 0
        super(MyCar, self).__init__(lane)

class OtherCar(Car):
    def __init__(self, lane, x, speed):
        self.color = color(80, 80, 120)
        self.x = x
        self.speed = speed
        super(OtherCar, self).__init__(lane)
        
def generate_new_car():
    speed = randrange(-6, 7) * 0.05
    if frames == 0:
        x = randrange(-2, WIDTH / 50 + 2) * 50
    else:
        if speed == 0:
            adj = randrange(0,2)
            if adj == 0:
                speed = 0.95
            else:
                speed = 1.05
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
    collision = True
    while collision:
        collision = False
        cars.append(me)
        for car in cars:
            if lane == car.lane and abs(x - car.x) < NEAR_TEST:
                collision = True
                print(lane, x, car.x)
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
    global cars
    to_purge = []
    for i, car in enumerate(cars):
        if car.x > WIDTH + 150 or car.x < -150:
            to_purge.append(i)
    for i in to_purge:
        cars.pop(i)
