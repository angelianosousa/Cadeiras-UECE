from multiprocessing import Process
from time import sleep
from random import randint
from os import getpid

# Consts variables
N_CARS               = 100 # Number of cars
B_TIME_COMING        = 2   # Best time
L_TIME_COMING        = 6   # Worst time
P_THROUGH            = 10  # Time pass through the bridge
T_SPACE_BETWEEN_CARS = 2   # Time space between the cars

class SingleLaneBridge:
    def __init__(self):
        self.cars_list = []

class Car:
    def __init__(self, direction):
        self.p_through = P_THROUGH
        self.number = getpid()
        self.direction = direction
        self.time_for_comming = randint(B_TIME_COMING, L_TIME_COMING)

    def pass_in_the_bridge(self, bridge):
        sleep(2)

        print(f'Car {self.number} to come in {self.time_for_comming} seconds - direction {self.direction}')
        sleep(self.time_for_comming)
        bridge.cars_list.append(self.number)

        print(f'Car {self.number} to getout in {self.p_through} seconds - direction {self.direction}')
        sleep(self.p_through)
        bridge.cars_list.remove(self.number)
    

if __name__ == "__main__":
    bridge = SingleLaneBridge()
    directions = ['right', 'left']

    for i in range(1, 3):
        new_car = Car(directions[randint(0, 1)])
        car_run = Process(name='Get run', target=new_car.pass_in_the_bridge, args=(bridge, ))
        car_run.start()
        # car_run.join()
