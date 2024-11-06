from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QBrush, QColor, QPointF

import math

class VehicleGraphicsItem(QtWidgets.QGraphicsRectItem):
    
    VEHICLE_WIDTH = 10
    VEHICLE_HEIGHT = 20
    
    def __init__(self, vehicle):
        super(VehicleGraphicsItem, self).__init__()
        self.vehicle = vehicle
        self.rgb = self.vehicle.rgb
        self.create_rectangle()
        self.update_position()
        
        
    def create_rectangle(self):
        #create rectangle and set it to be the shape of the object
        rect = QtCore.QRectF(0,0,VehicleGraphicsItem.VEHICLE_WIDTH, VehicleGraphicsItem.VEHICLE_HEIGHT)
        self.setRect(rect)
        brush = QBrush(QColor(self.rgb[0], self.rgb[1], self.rgb[2]),1)
        self.setBrush(brush)
        self.setTransformOriginPoint(QPointF(VehicleGraphicsItem.VEHICLE_WIDTH/2, VehicleGraphicsItem.VEHICLE_HEIGHT/2))
        
        
    def update_position(self):
        # update the vehicle's position and orientation
        self.setPos(self.vehicle.position[0], self.vehicle.position[1])
        self.setRotation(math.degrees(self.vehicle.orientation)) # angle in degrees
        