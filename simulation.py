import math
from vehiclegraphicsitem import VehicleGraphicsItem
from gui import GUI

class Simulation:
    
    WANTED_DISTANCE = 50 # how much distance we want between two vehicles
    LOW_BORDER = VehicleGraphicsItem.VEHICLE_HEIGHT
    HIGH_BORDER_X = GUI.WIDTH - VehicleGraphicsItem.VEHICLE_HEIGHT
    HIGH_BORDER_Y = GUI.HEIGHT - VehicleGraphicsItem.VEHICLE_HEIGHT
    
    def __init__(self):
        self.vehicles = []
        
        
    def add_vehicle(self, vehicle):
        # vehicle: Vehicle
        if vehicle not in self.vehicles:
            self.vehicles.append(vehicle)
        # check that the vehicles aren't too close to each other
        for other_vehicle in self.vehicles:
            if other_vehicle != vehicle:
                distance = math.sqrt((vehicle.position[0]-other_vehicle.position[0])**2+(vehicle.position[1]-other_vehicle.position[1])**2)
                if distance < Simulation.WANTED_DISTANCE:
                    raise ValueError("Two vehicles are too close to each other. Distance should be at least {:}.".format(Simulation.WANTED_DISTANCE))
               
                
    def next_turn(self):
        # moves every vehicle
        for i in range(len(self.vehicles)):
            self.vehicles[i].crashed_in_wall()
            self.vehicles[i].move(self.vehicles)
            
            
    def add_vehicles(self, file):
    #creates new Vehicles from the file and adds them to the Simulation
    #example of line: VEHICLE-MAS80-POS100:50-TAR450:60-ORI90-MXF100-MXS100
        from vehicle import Vehicle
        file = open(file, "r")
        for line in file:
            line = line.strip()
            parts = line.split("-")
            if parts[0] == "VEHICLE":
                mass = int(parts[1][3:])
                x1, y1 = parts[2][3:].split(":")
                x2, y2 = parts[3][3:].split(":")
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                orientation = math.radians(int(parts[4][3:]))
                max_force = int(parts[5][3:])
                max_speed = int(parts[6][3:])
                red, green, blue = parts[7][3:].split(":")
                red, green, blue = int(red), int(green), int(blue)
                rgb = [red, green, blue]
                # check that all values are within acceptable boundaries
                if orientation > math.radians(360) or x1 < Simulation.LOW_BORDER or x2 < Simulation.LOW_BORDER or y1 < Simulation.LOW_BORDER or y2 < Simulation.LOW_BORDER or x1 > Simulation.HIGH_BORDER_X or x2 > Simulation.HIGH_BORDER_X or y1 > Simulation.HIGH_BORDER_Y or y2 > Simulation.HIGH_BORDER_Y or red > 256 or green > 256 or blue > 256:
                    raise ValueError("Your file has an integer outside acceptable boundaries. Integers must be positive, x coordinates between {:.0f} and {:.0f} and y coordinates between {:.0f} and {:.0f}.".format(Simulation.LOW_BORDER, Simulation.HIGH_BORDER_X, Simulation.LOW_BORDER, Simulation.HIGH_BORDER_Y))
                vehicle = Vehicle(mass, x1, y1, x2, y2, orientation, max_force, max_speed, rgb)
                self.add_vehicle(vehicle)
        file.close()
        

            
            
            