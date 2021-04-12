import random
import easygopigo3 as easy
import threading
import time
from time import sleep
import math
from math import pi
import easysensors

        
class GoPiGo3WithKeyboard(object):

    KEY_DESCRIPTION = 0
    KEY_FUNC_SUFFIX = 1

    servo1_position = 0
    servo2_position = 0
    
    ###------- MAIN MENU -------###
    def __init__(self):
        self.gopigo3 = easy.EasyGoPiGo3()
        self.servo1 = self.gopigo3.init_servo("SERVO1")
        
        self.keybindings = {
		    "w" : ["Move the GoPiGo3 forward", "forward"],
            "<SPACE>" : ["Stop the GoPiGo3 from moving", "stop"],

            "<UP>" : ["Take a distance sensor reading then adjust motor speed", "read_respond_sensor"],
            "<DOWN>" : ["Take a distance sensor reading", "test_sensor"],
            
            "<ESC>" : ["Exit", "exit"],
        }
        self.order_of_keys = ["w", "<SPACE>", "<UP>", "<DOWN>", "<ESC>"]
  

    ###------- BUILT-IN FUNCTIONS (don't change any of these) -------###
    def executeKeyboardJob(self, argument):
        method_prefix = "_gopigo3_command_"
        try:
            method_suffix = str(self.keybindings[argument][self.KEY_FUNC_SUFFIX])
        except KeyError:
            method_suffix = ""
        method_name = method_prefix + method_suffix

        method = getattr(self, method_name, lambda : "nothing")

        return method()

    def drawLogo(self):
        """
        Draws the name of the GoPiGo3.
        """
        print("__________                     __________                             ")
        print("\______   \_____ _______   ____\______   \ ____   ____   ____   ______")
        print(" |    |  _/\__  \\_  __ \_/ __ \|    |  _//  _ \ /    \_/ __ \ /  ___/")
        print(" |    |   \ / __ \|  | \/\  ___/|    |   (  <_> )   |  \  ___/ \___ \ ")
        print(" |______  /(____  /__|    \___  >______  /\____/|___|  /\___  >____  >")
        print("        \/      \/            \/       \/            \/     \/     \/ ")

    def drawDescription(self):
        """
        Prints details related on how to operate the GoPiGo3.
        """
        print("\nPress the following keys to run the features of the GoPiGo3.")
        print("To move the motors, make sure you have a fresh set of batteries powering the GoPiGo3.\n")

    def drawMenu(self):
        """
        Prints all the key-bindings between the keys and the GoPiGo3's commands on the screen.
        """
        try:
            for key in self.order_of_keys:
                print("\r[key {:8}] :  {}".format(key, self.keybindings[key][self.KEY_DESCRIPTION]))
        except KeyError:
            print("Error: Keys found GoPiGo3WithKeyboard.order_of_keys don't match with those in GoPiGo3WithKeyboard.keybindings.")

 
 
    ###------- ROBOT FUNCTIONS (try these out) -------###
    def _gopigo3_command_forward(self):
        self.gopigo3.forward()

        return "moving"

    def _gopigo3_command_stop(self):
        self.gopigo3.stop()

        return "moving"

    def _gopigo3_command_test_sensor(self):
	    # initialize the sensor then print the current reading
        my_distance_sensor = self.gopigo3.init_distance_sensor()
        print("Distance Sensor Reading: {} mm ".format(my_distance_sensor.read_mm()))
		
    def _gopigo3_read_respond_sensor(self):
        # call the test_sensor function to get a reading and print to console
		# notice how you do NOT need the ".gopigo3" in the function call because you are NOT calling a function from the easygopigo3.py file
        self._gopigo3_command_test_sensor
        
        if (my_distance_sensor.read_mm() < 150):
            self.gopigo3.set_speed(1) #NOTE: Setting speed to '0' causes the robot to move at max speed backward then forward ???
            print("stopped")
        elif (my_distance_sensor.read_mm() < 750):
            self.gopigo3.set_speed(150)
        else:
            self.gopigo3.set_speed(300)
            
        # Directly print the values of the sensor.
        print("Current Speed: {} DPS".format(self.gopigo3.get_speed()))
       

    def _gopigo3_command_exit(self):
        return "exit"
