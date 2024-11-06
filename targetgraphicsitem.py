from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QBrush, QColor, QPointF

import math

class TargetGraphicsItem(QtWidgets.QGraphicsEllipseItem):
    
    DIAMETER = 5
    
    def __init__(self, vehicle):
        super(TargetGraphicsItem, self).__init__()
        self.vehicle = vehicle
        self.rgb = self.vehicle.rgb
        self.create_circle()
        self.place_target()
        
        
    def create_circle(self):
        circle = QtCore.QRectF(0,0,TargetGraphicsItem.DIAMETER, TargetGraphicsItem.DIAMETER)
        self.setRect(circle)
        brush = QBrush(QColor(self.rgb[0], self.rgb[1], self.rgb[2]),1)
        self.setBrush(brush)
        self.setTransformOriginPoint(QPointF(TargetGraphicsItem.DIAMETER/2, TargetGraphicsItem.DIAMETER/2))
        
    
    
    def place_target(self):
        self.setPos(self.vehicle.target[0]+10, self.vehicle.target[1]+10)