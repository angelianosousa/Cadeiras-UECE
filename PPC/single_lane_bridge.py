from time import time, sleep
from random import randint

# Const variables
N_CARS    = 100 # Cars numbers
TIME_PASS = 5   # Time for a car pass thought bridge

# Count variables
cars_right = 0
cars_left  = 0

# Time variables
min_wait   = 0
max_wait   = 0
total_time = 0
directions = ['left', 'right']

class Cars:
  def __init__(self, direction, number):
    self.direction        = direction
    self.number           = number
    self.time_arrive      = randint(1, 3)
    self.time_start_wait  = 0
    self.time_leave_wait  = 0
  
  def __time__(self):
    time = self.time_leave_wait - self.time_start_wait
    return round(time, 2)

  def __total_time__(self):
    global total_time

    total_time += self.__time__()

  def count_time_metrics(self):
    global min_wait
    global max_wait

    time = self.__time__()
    self.__total_time__()

    if self.number == 1:
      min_wait = time
      max_wait = time
    else:
      if time < min_wait:
        min_wait = time
      else:
        max_wait = time

class Bridges:
  def __init__(self):
    self.lane       = []
    self.cars_enter = 0
    self.cars_out   = 0

  def count_cars(self):
    global cars_left
    global cars_right

    if self.lane[0].direction == 'left':
      cars_left += 1
    else:
      cars_right += 1
  
  def check_opposite_cars(self, condition, car):
    if len(self.lane) > 0 and self.lane[0].direction == car.direction and self.lane[0].time_arrive > car.time_arrive:
      print(f'Next car {car.number} has the same direction than Car {self.lane[0].number}')
      print('Putting on hold...')
      condition.wait()

  def car_pass_in(self, car):
    car.time_start_wait = time()
    sleep(car.time_arrive)
    self.lane.append(car)
    self.cars_enter += 1

    print(f'Car {car.number} enter bridge on #{car.direction} with {car.time_arrive} seconds to arrive')
  
  def car_pass_out(self):
    car = self.lane[0]

    self.count_cars() # Just count cars

    sleep(TIME_PASS)
    self.lane.pop(0)
    self.cars_out += 1            # Count cars out
    car.time_leave_wait = time()  # Count time leave the bridge
    car.count_time_metrics()      # Build statistics

    print(f'Car {car.number} leave bridge on #{car.direction}')
    print(f'Car {car.number} time wait: {round(car.time_leave_wait - car.time_start_wait, 2)} seconds')
  
  def mecanism_for_five_cars(self, car):
    if self.cars_enter > 0 and self.cars_enter % 5 == 0:
      print('Five cars have pass..')
      print(f'Car {car.number} #{car.direction} was stopped...')
      print('Change the direction of the bridge...')
      sleep(1)
      new_car_direction = 'right' if car.direction == 'left' else 'left'

      new_car = Cars(new_car_direction, car.number+1)
      print(f'Car {new_car.number} is the next...')
      sleep(1)
      self.car_pass_in(new_car)

def enter_bridge(condition, bridge, change_direction_with_five_cars = False):

  car_number = 1
    
  while bridge.cars_enter < N_CARS:
    car = Cars(directions[car_number%2], car_number)
    car_number += 1

    with condition:
      condition.acquire()

      # Check if pass five cars
      bridge.mecanism_for_five_cars(car) if change_direction_with_five_cars == True else ''

      # Check if the cars are in opposite sides
      bridge.check_opposite_cars(condition, car)

      bridge.car_pass_in(car)
      condition.notify_all()
      condition.release()

def leave_bridge(condition, bridge):

  while bridge.cars_out < N_CARS:

    with condition:
      condition.acquire()

      while len(bridge.lane) == 0:
        print(f'Bridge empty, stay on hold...')
        print(20*'-=-')
        condition.wait()

      bridge.car_pass_out()
      condition.notify_all()
      condition.release()

def print_results(condition, bridge):
  global cars_left
  global cars_right
  global min_wait

  with condition:

    while bridge.cars_out < N_CARS:
      condition.wait()

    print(20*'-=-')
    print(f'Nº Cars right: {cars_right}')
    print(f'Nº Cars left: {cars_left}')
    print(f'Min time wait: {min_wait} seconds')
    print(f'Max time wait: {max_wait} seconds')
    print(f'Med time wait: {round(total_time/N_CARS, 2)} seconds')
    print(f'Total time of execution: {round(total_time, 2)} seconds')
