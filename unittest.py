import unittest

from liikennesimu.vehicle import Vehicle
from liikennesimu.simulation import Simulation

class Test(unittest.TestCase):
    
    def test_vehicle_reached_target(self):
        #mass, x1, y1, x2, y2, orientation, max_force, max_speed
        vehicle = Vehicle(5000,100,100,100,100,0,5000,25, [0,0,0])
        list = []
        vehicle.move(list)
        self.assertEqual(vehicle.reached_target, True, "The vehicle doesn't seem to have reached its target.")
        
    
    def test_two_vehicles_in_same_coordinates(self):
        
        file = "tiedostot/vehicles_test1.txt"
        simulation = Simulation()
        
        try:
            simulation.add_vehicles(file)
        except ValueError:
            pass
        else:
            self.fail("Two vehicles too close to each other didn't cause an error.")
            
    def test_with_unacceptable_orientation(self):
        
        file = "tiedostot/vehicles_test2.txt"
        simulation = Simulation()
        
        try:
            simulation.add_vehicles(file)
        except ValueError:
            pass
        else:
            self.fail("Unacceptable integers didn't cause an error.")
            
    def test_with_unacceptable_coordinates(self):
        
        file = "tiedostot/vehicles_test3.txt"
        simulation = Simulation()
        
        try:
            simulation.add_vehicles(file)
        except ValueError:
            pass
        else:
            self.fail("Unacceptable integers didn't cause an error.")
    
    
    def test_return_empty_list_with_one_vehicle(self):
        
        file = "tiedostot/vehicles_test4.txt"
        simulation = Simulation()
        simulation.add_vehicles(file)
        list = simulation.vehicles
        vehicle = simulation.vehicles[0]
        self.assertEqual(vehicle.check_vehicles(list), [], "Simulation with only one vehicle didn't return an empty list of other vehicles")
    
    
    def test_with_unacceptable_rgb_values(self):
        
        file = "tiedostot/vehicles_test5.txt"
        simulation = Simulation()
        
        try:
            simulation.add_vehicles(file)
        except ValueError:
            pass
        else:
            self.fail("Unacceptable integers didn't cause an error.")
    
    
    
    
    
    
    