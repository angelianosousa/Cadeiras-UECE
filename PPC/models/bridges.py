from time import time, sleep
from .cars import Cars

# Const variables
N_CARS    = 100 # Cars numbers
TIME_PASS = 5   # Time for a car pass thought bridge

# Count variables
cars_right  = 0
cars_left   = 0

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
  
  def check_opposite_cars(self, condition, current_car):
    if len(self.lane) > 0 and self.lane[-1].direction != current_car.direction and self.lane[-1].time_arrive > current_car.time_arrive:
      print(f'Next car {current_car.number} has opposite direction than Car {self.lane[-1].number} with {current_car.time_arrive} seconds to arrive...')
      print('Putting on wait...')
      condition.wait()

  def car_pass_in(self, car):
    sleep(car.time_arrive)
    sleep(1) # Time space between cars
    self.lane.append(car)
    self.cars_enter += 1
    car.time_start_wait = time()

    print(f'Car {car.number} enter bridge on #{car.direction} with {car.time_arrive} seconds to arrive')
  
  def car_pass_out(self):
    car = self.lane[0]

    self.count_cars() # Just count cars

    sleep(TIME_PASS)
    self.lane.pop(0)              # Take of a car
    self.cars_out += 1            # Count cars out
    car.time_leave_wait = time()  # Count time leave the bridge
    car.count_time_metrics()      # Build statistics

    print(f'Car {car.number} leave bridge on #{car.direction}\ntime wait: {round(car.time_leave_wait - car.time_start_wait, 2)} seconds')
  
  def mecanism_for_five_cars(self, car):
    if self.cars_enter > 0 and self.cars_enter % 5 == 0:
      print('Five cars was enter..')
      print(f'Car {car.number} #{car.direction} was stopped...')
      print('Change the direction of the bridge...')
      sleep(2) # Time to change the bridge direction

      new_car = Cars()
      print(f'Car {new_car.number} is the next...')
      sleep(1)
      self.car_pass_in(new_car)
  
  def let_cars_enter(self):
    return self.cars_enter < N_CARS
  
  def let_cars_leave(self):
    return self.cars_out < N_CARS

def bridges_statistics():
  print(f'Nº Cars right: {cars_right}')
  print(f'Nº Cars left: {cars_left}')