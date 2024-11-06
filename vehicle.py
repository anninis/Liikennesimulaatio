import math

from simulation import Simulation
from gui import GUI

class Vehicle:
    
    TIME_FORWARD = 4 # how many moves forward the program looks to see if there's a wall in front of a vehicle
    SIMILAR_ORIENTATION = math.radians(5)
    BRAKING_FORCE = -10000
    DISTANCE_TO_TARGET = 100 # at what distance to the target the vehicle starts braking
    CLOSE_ENOUGH = 0.1 # how close the vehicle must be to the target so that the vehicle stops completely
    STEERING_FORCE = 5000
    MAX_ANGLE = math.radians(20) # how many radians a vehicle can turn in one move
    
    def __init__(self, mass, x1, y1, x2, y2, orientation, max_force, max_speed, rgb):
        self.mass = mass # [m] = kg
        self.velocity = [0,0] # vector, x and y
        self.position = [x1, y1] # vector, x and y
        self.target = [x2, y2] # vector, x and y
        self.orientation = orientation # angle in radians
        self.max_force = max_force
        self.max_speed = max_speed
        self.rgb = rgb # list of three numbers between 0 and 256
        self.reached_target = False
        self.crashed = False
                
    def move(self, list_of_vehicles):
        # this method decides whether the vehicle should seek its target or avoid another vehicled
        if not self.reached_target and not self.crashed:
            # check if there are walls or other vehicles in the way
            walls = self.check_walls()
            wall_force = self.create_wall_force(walls)
            vehicles = self.check_vehicles(list_of_vehicles)
            if walls != []:
                self.containment(wall_force)
            elif vehicles != []:
                if len(vehicles) == 1 and abs(vehicles[0].orientation - self.orientation) < Vehicle.SIMILAR_ORIENTATION and vehicles[0].get_speed() > 10:
                    if self.get_speed() > vehicles[0].get_speed():
                        self.brake()
                    else:
                        self.accelerate()
                else:
                    self.separate(vehicles)
            else:
                # the car either slows down or continues normally towards its target    
                if self.vehicle_close_to_target():
                    self.arrive()
                else:
                    # there is nothing in front of the vehicle, vehicle seeks its target
                    # s=vt, t=1 second
                    self.seek()
            # check that the new velocity isn't bigger than max_speed
            if self.get_speed() > self.max_speed:
                self.velocity = [self.max_speed*math.sin(self.orientation), -(self.max_speed*math.cos(self.orientation))]
            self.position = [self.position[0]+self.velocity[0], self.position[1]+self.velocity[1]]
            
            
    def crashed_in_wall(self):
        if self.position[0] < Simulation.LOW_BORDER/4 or self.position[0] > Simulation.HIGH_BORDER_X + 5 or self.position[1] < Simulation.LOW_BORDER/4 or self.position[1] > Simulation.HIGH_BORDER_Y + 5:
            self.crashed = True
            self.velocity = [0,0]
        
        
    def check_vehicles(self, list_of_vehicles):
        # goes through all the vehicles of the scene
        # checks whether there are vehicles to close to the vehicle
        # returns list of vehicles that are too close
        vehicles = []
        for vehicle in list_of_vehicles:
            if vehicle != self:
                distance = math.sqrt((self.position[0]-vehicle.position[0])**2 + (self.position[1]-vehicle.position[1])**2)
                if distance < 4 * self.get_speed():
                    vehicles.append(vehicle)
        return vehicles
    
    
    def check_walls(self):
        # check if there are walls in front of the vehicle
        # returns list of walls
        # possible list components: up, down, left, right
        walls = []
        future_position = [self.position[0]+self.velocity[0]*Vehicle.TIME_FORWARD, self.position[1]+self.velocity[1]*Vehicle.TIME_FORWARD]
        if future_position[0] <= Simulation.LOW_BORDER:
            walls.append("left")
        if future_position[0] >= Simulation.HIGH_BORDER_X:
            walls.append("right")
        if future_position[1] <= Simulation.LOW_BORDER:
            walls.append("up")
        if future_position[1] >= Simulation.HIGH_BORDER_Y:
            walls.append("down")
        return walls


    def create_wall_force(self, walls):
        # create a repulsion force away from the walls too close
        wall_force_x = 0
        wall_force_y = 0
        for wall in walls:
            if wall == "left":
                distance = self.position[0]
                wall_force_x = distance
            if wall == "right":
                distance = GUI.WIDTH - self.position[0]
                wall_force_x = -distance
            if wall == "up":
                distance = self.position[1]
                wall_force_y = distance
            if wall == "down":
                distance = GUI.HEIGHT - self.position[1]
                wall_force_y = distance
        wall_force = [wall_force_x, wall_force_y]
        return wall_force
            
    
    def brake(self):
        acceleration = Vehicle.BRAKING_FORCE / self.mass
        self.velocity = [self.velocity[0]+acceleration*math.sin(self.orientation), self.velocity[1]-acceleration*math.cos(self.orientation)]
    
    
    def accelerate(self):
        if Vehicle.STEERING_FORCE < self.max_force:
            acceleration = Vehicle.STEERING_FORCE / self.mass
        else:
            acceleration = self.max_force / self.mass
        self.velocity = [self.velocity[0]+acceleration*math.sin(self.orientation), self.velocity[1]-acceleration*math.cos(self.orientation)]
        
    
    def containment(self, wall_force):
        # this behaviour is a combination of separate and seek
        seek_vector = [self.target[0]-self.position[0], self.target[1]-self.position[1]]
        middle_vector = [(wall_force[0]+seek_vector[0])/2,(wall_force[1]+seek_vector[1])/2]
        target = [self.position[0]+middle_vector[0], self.position[1]+middle_vector[1]]
        self.orientation = self.get_angle(target)
        force = math.sqrt(wall_force[0]**2 + wall_force[1]**2) * Vehicle.STEERING_FORCE
        if force < self.max_force:
            acceleration = force / self.mass
        else:
            acceleration = self.max_force / self.mass
        self.velocity = [self.velocity[0]+acceleration*math.sin(self.orientation), self.velocity[1]-acceleration*math.cos(self.orientation)]
    
        
    def separate(self, vehicles):
        # creates a repulsion force from the vehicles that are too close
        force_vectors = []
        for vehicle in vehicles:
            distance = math.sqrt((self.position[0]-vehicle.position[0])**2 + (self.position[1]-vehicle.position[1])**2)
            force_vector = [(self.position[0]-vehicle.position[0])/distance, (self.position[1]-vehicle.position[1])/distance]
            force_vectors.append(force_vector)
        forces_x = 0
        forces_y = 0
        for i in range(len(force_vectors)):
            forces_x += force_vectors[i][0]
            forces_y += force_vectors[i][1]
        total_force = [forces_x, forces_y]
        # this force accelerates the vehicle
        force = math.sqrt(total_force[0]**2 + total_force[1]**2) * Vehicle.STEERING_FORCE
        if force < self.max_force:
            acceleration = force / self.mass
        else:
            acceleration = self.max_force / self.mass
        # we add the forces to vehicle's position to get the right orientation
        target = [self.position[0]+total_force[0], self.position[1]+total_force[1]]
        self.orientation = self.get_angle(target)
        self.velocity = [self.velocity[0]+acceleration*math.sin(self.orientation), self.velocity[1]-acceleration*math.cos(self.orientation)]
        

    def vehicle_close_to_target(self):
        # return True/False
        distance = math.sqrt((self.position[0]-self.target[0])**2 + (self.position[1]-self.target[1])**2)
        if distance < Vehicle.DISTANCE_TO_TARGET:
            return True
        return False
    
    
    def arrive(self):
        # vehicle is getting closer to its target, this method slows it down
        distance = math.sqrt((self.position[0]-self.target[0])**2 + (self.position[1]-self.target[1])**2)
        if distance < Vehicle.CLOSE_ENOUGH:
            # there's no point in giving the vehicle minimal velocity anymore, the vehicle stops
            self.velocity = [0,0]
            self.position = self.target
            self.reached_target = True
        else:
            wanted_speed = self.max_speed * (distance / Vehicle.DISTANCE_TO_TARGET)
            self.orientation = self.get_angle(self.target)
            self.velocity = [wanted_speed*math.sin(self.orientation), -(wanted_speed*math.cos(self.orientation))]


    def seek(self):
        # this method gives the vehicle a new velocity towards its target
        # F=ma --> a=F/m
        # SEEK
        if Vehicle.STEERING_FORCE < self.max_force:
            acceleration = Vehicle.STEERING_FORCE / self.mass # int
        else:
            acceleration = self.max_force / self.mass # int
        # add the acceleration to the old velocity, v=at, t=1 second
        self.orientation = self.get_angle(self.target)
        self.velocity = [self.velocity[0]+acceleration*math.sin(self.orientation), self.velocity[1]-acceleration*math.cos(self.orientation)]
        

    def get_angle(self, target):
        # creates a vector that starts from the vehicle's position and ends in the target
        # y is negative because y axis is inverted here
        vector = [target[0]-self.position[0], -(target[1]-self.position[1])]
        # angle between this vector and unit vector j using dot product
        angle = math.acos(vector[1]/math.sqrt(vector[0]**2 + vector[1]**2))
        # if x component of the vector is negative, we need the bigger angle
        if vector[0] < 0:
            angle = math.radians(360) - angle
        # check that the vehicle only turns for max MAX_ANGLE radians
        if abs(angle - self.orientation) > Vehicle.MAX_ANGLE:
            if abs(angle - self.orientation) > math.radians(180):
                if angle > self.orientation:
                    angle = self.orientation - Vehicle.MAX_ANGLE
                else:
                    angle = self.orientation + Vehicle.MAX_ANGLE
            else:
                if angle > self.orientation:
                    angle = self.orientation + Vehicle.MAX_ANGLE
                else:
                    angle = self.orientation - Vehicle.MAX_ANGLE
        # we want an angle between 0 and 360 degrees!
        if angle > math.radians(360):
            angle -= math.radians(360)
        if angle < 0:
            angle += math.radians(360)
        return angle
        
        
    def get_speed(self):
        # returns the speed of the vehicle
        return math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        
        
        
        
        
    