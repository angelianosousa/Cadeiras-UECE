from threading import Thread, Condition, current_thread, get_native_id
from time import time, sleep
from random import randint, choice

class Cars:
  def __init__(self, direction, number):
    self.direction   = direction
    self.number      = number
    self.time_arrive = randint(1, 3)

class Bridges:
  def __init__(self):
    self.lane       = []
    self.cars_enter = 0
    self.cars_out   = 0

def leave_bridge(condition):
  global bridge

  while bridge.cars_out < N_CARS:

    with condition:
      condition.acquire()

      while len(bridge.lane) == 0:
        print(f'Bridge empty, stay on hold...')
        condition.wait()

      car = bridge.lane[0]

      sleep(TIME_PASS)
      bridge.lane.pop(0)
      bridge.cars_out += 1

      print(f'{current_thread().name} take off: Car {car.number} on #{car.direction}')
      print(20*'-=-')
      condition.notify_all()
      condition.release()

def enter_bridge(condition):
  global bridge

  car_number = 1
    
  while bridge.cars_out < N_CARS:
    car = Cars(choice(['left', 'right']), car_number)
    car_number += 1

    with condition:
      condition.acquire()

      # Check if the cars are in opposite sides
      if len(bridge.lane) > 0 and bridge.lane[0].direction == car.direction:
        print(f'Car {bridge.lane[0].number} has the same direction than Car {car.number}')
        print('Putting on hold...')
        condition.wait()

      sleep(car.time_arrive)
      bridge.lane.append(car)
      bridge.cars_enter += 1

      print(20*'-=-')
      print(f'{current_thread().name} put Car: {car.number} on #{car.direction} - {car.time_arrive} seconds to arrive')
      condition.notify_all()
      condition.release()

if __name__ == '__main__':
  # Const variables
  N_CARS = 100  # Cars numbers
  TIME_PASS = 5 # Time for a car pass thought bridge

  bridge = Bridges()
  condition = Condition() # Lock variable

  cs1 = Thread(name='Leave bridge', target=leave_bridge, args=(condition, ))  # Start process to leave the bridge
  pr1 = Thread(name='Enter bridge', target=enter_bridge, args=(condition, ))  # Start process to enter the bridge

  cs1.start()
  sleep(2)

  pr1.start()
  sleep(2)
