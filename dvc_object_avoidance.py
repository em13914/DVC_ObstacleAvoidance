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
            "w" : ["Drive the GoPiGo along the delivery route", "delivery"],
            "1" : ["BRONZE Tier Challenge Function", "bronze"],
            "2" : ["SILVER Tier Challenge Function", "silver"],
            "3" : ["GOLD Tier Challenge Function", "gold"],
            "<SPACE>" : ["Stop the GoPiGo3 from moving", "stop"],

            "<LEFT>" : ["Turn servo completely to 0 degrees", "servo_total_left"],
            "<UP>" : ["Turn servo to 90 degrees (centered)", "servo_total_center"],
            "<RIGHT>" : ["Turn servo completely to 180 degrees", "servo_total_right"],
            "<DOWN>" : ["Take a distance sensor reading", "test_sensor"],
            

            "<ESC>" : ["Exit", "exit"],
        }
        self.order_of_keys = ["w", "1", "2", "3", "<SPACE>", "<LEFT>", "<UP>", "<RIGHT>", "<DOWN>", "<ESC>"]
  

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

            
    ###------- ROBOT FUNCTIONS (customize as you please) -------###
    def _gopigo3_command_delivery(self):
        # your delivery route here!
        self.dvc_drive_in(107)
        self.gopigo3.turn_degrees(-90)
        self.dvc_drive_in(84)
        self.gopigo3.turn_degrees(90)
        self.dvc_drive_in(46)

        return "moving"

    def _gopigo3_command_bronze(self):
        print("Your Code Here")
        return "moving"

    def _gopigo3_command_silver(self):
        print("Your Code Here")
        return "moving"

    def _gopigo3_command_gold(self):
        print("Your Code Here")
        return "moving"

    def _gopigo3_command_stop(self):
        self.gopigo3.stop()
        return "moving"


    ###------- DISTANCE SENSOR FUNCTIONS (exactly the same as in the simplified file you saw previously) -------###
    def _gopigo3_command_test_sensor(self):
        # initialize the sensor then print the current reading
        my_distance_sensor = self.gopigo3.init_distance_sensor()
        print("Distance Sensor Reading: {} mm ".format(my_distance_sensor.read_mm()))

    def _gopigo3_command_read_respond_sensor(self):
	# initialize the sensor then print the current reading
        my_distance_sensor = self.gopigo3.init_distance_sensor()
        print("Distance Sensor Reading: {} mm ".format(my_distance_sensor.read_mm()))
        
        if (my_distance_sensor.read_mm() < 150):
            self.gopigo3.set_speed(1) #NOTE: Setting speed to '0' causes the robot to move at max speed backward then forward ???
            print("obstacle detected!")
        elif (my_distance_sensor.read_mm() < 750):
            self.gopigo3.set_speed(150)
            print("obstacle approaching...")
        else:
            self.gopigo3.set_speed(300)
            print("coast is clear!")
   

    ###------- CUSTOMIZED FUNCTIONS (modified from the drive_in function in easygopigo3.py) -------###
    def dvc_drive_in(self, dist, blocking=True):      
        # convert inches to mm
        dist_cm = dist * 2.54
        dist_mm = dist_cm * 10
        wheel_circumference = math.pi * 66.5
        
        # the number of degrees each wheel needs to turn
        WheelTurnDegrees = ((dist_mm / wheel_circumference) * 360)

        # get the starting position of each motor
        StartPositionLeft = self.gopigo3.get_motor_encoder(self.gopigo3.MOTOR_LEFT)
        StartPositionRight = self.gopigo3.get_motor_encoder(self.gopigo3.MOTOR_RIGHT)
        
        # add the degrees it must turn to the starting position
        self.gopigo3.set_motor_position(self.gopigo3.MOTOR_LEFT,
                                (StartPositionLeft + WheelTurnDegrees))
        self.gopigo3.set_motor_position(self.gopigo3.MOTOR_RIGHT,
                                (StartPositionRight + WheelTurnDegrees))
        
        # print the total degrees to the terminal
        print(WheelTurnDegrees)
        
        # move forward, checking every 0.1 seconds to see if the target has been reached
        if blocking:
            while self.gopigo3.target_reached(
                    StartPositionLeft + WheelTurnDegrees,
                    StartPositionRight + WheelTurnDegrees) is False:
                
                # inside the WHILE loop we make a call to the 'test_distance_sensor' function
                # notice how since the function we are using is defined HERE in this file we do not need the '.gopigo3'
                self._gopigo3_command_test_sensor()
                time.sleep(0.1)
    
    
    ###------- SERVO FUNCTIONS (copied over from ServoControl example) -------###
    def _gopigo3_command_servo_total_left(self):
        self.servo1_position = 0
        self.servo1.rotate_servo(self.servo1_position)
        return "complete_turn_servo1"

    def _gopigo3_command_servo_total_center(self):
        self.servo1_position = 90
        self.servo1.rotate_servo(self.servo1_position)
        return "complete_turn_servo1"
    
    def _gopigo3_command_servo_total_right(self):
        self.servo1_position = 180
        self.servo1.rotate_servo(self.servo1_position)
        return "complete_turn_servo1"
   

    def _gopigo3_command_exit(self):
        return "exit"
