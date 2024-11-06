from PyQt5 import QtWidgets, QtTest
from PyQt5.Qt import QGraphicsRectItem, QBrush, QColor

from vehiclegraphicsitem import VehicleGraphicsItem
from targetgraphicsitem import TargetGraphicsItem


class GUI(QtWidgets.QMainWindow):
    
    WIDTH = 1000
    HEIGHT = 600
    TURN_IN_SECONDS = 1 # how many seconds one turn lasts
    
    # this class draws the background (Simulation) and adds VehicleGraphicsItems to it
    def __init__(self, simulation):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)
        self.simulation = simulation
        self.graphics_items = []
        self.init_window()
        
        border = QGraphicsRectItem(0,0,GUI.WIDTH, GUI.HEIGHT)
        # color the background here if you want
        brush = QBrush(QColor(224,224,224),1)
        border.setBrush(brush)
        self.scene.addItem(border)
        
        self.add_graphics_items()
        QtTest.QTest.qWait(3000) #delay time as mseconds
        self.update_vehicles()
        
        while self.vehicles_moving():
            self.update_vehicles()

        
    def init_window(self):

        self.setGeometry(300, 150, 800, 550) # where on the screen the window opens
        self.setWindowTitle('Liikennesimulaatio')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, GUI.WIDTH, GUI.HEIGHT) # scene is WIDTHxHEIGHT pixels

        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)
        
        
    def add_graphics_items(self):
        # creates a VehicleGraphicsItem and a TargetGraphicsItem for every Vehicle added to the Simulation
        for vehicle in self.simulation.vehicles:
            target = TargetGraphicsItem(vehicle)
            self.scene.addItem(target)
        for vehicle in self.simulation.vehicles:
            item = VehicleGraphicsItem(vehicle)
            self.scene.addItem(item)
            self.graphics_items.append(item)
    
    
    def update_vehicles(self):
        # first calls the Simulation to move Vehicles, then draws the VehicleGraphicsItems
        self.simulation.next_turn()
        for graphics_item in self.graphics_items:
            # check if two vehiclegraphicsitems have collided
            for i in range(len(self.graphics_items)):
                if graphics_item.collidesWithItem(self.graphics_items[i]):
                    if graphics_item != self.graphics_items[i]:
                        graphics_item.vehicle.crashed = True
                        graphics_item.vehicle.velocity = [0,0]
        for graphics_item in self.graphics_items:
            graphics_item.update_position()
        QtTest.QTest.qWait(GUI.TURN_IN_SECONDS*1000) #delay time as mseconds

    
    def vehicles_moving(self):
        #check that the vehicles are still moving
        for vehicle in self.simulation.vehicles:
            if vehicle.velocity != [0,0]:
                return True
        return False
    
    
    