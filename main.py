import sys
from PyQt5.QtWidgets import QApplication

from simulation import Simulation
from gui import GUI
    
def main():
    no_file = True
    while no_file:
        try:
            file = input("Give the name of the file: ")
            file2 = open(file, "r") # a try to open the file to cause FileNotFoundError
            file2.close()
            no_file = False
        except FileNotFoundError:
            print("File not found.")
    simulation = Simulation()
    simulation.add_vehicles(file)
    global app
    app = QApplication(sys.argv)
    gui = GUI(simulation)
    sys.exit(app.exec_())
    
    
main()