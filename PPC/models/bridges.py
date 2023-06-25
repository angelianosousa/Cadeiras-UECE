from time import time, sleep
from models.vehicles import Cars

# Const variables
N_CARS   = 50 # Cars counter
M_TRUCKS = N_CARS/10 # For each 10 cars we want 1 truck

# Count variables
cars_right   = 0
cars_left    = 0
trucks_right = 0
trucks_left  = 0

class Bridges:
  def __init__(self):
    self.lane           = []
    self.vehicles_enter = 0
    self.vehicles_out   = 0

  def __current_vehicle__(self):
    if len(self.lane) == 0:
      return 'Bridge empty'

    return self.lane[0]
  
  def __last_vehicle__(self):
    if len(self.lane) == 0:
      return 'Bridge empty'

    return self.lane[-1]
  
  def __has_vehicle__(self):
    return len(self.lane) > 0
  
  # def vehicles_count(self):
  #   return { 'cars': cars_right + cars_left, 'trucks': trucks_right + trucks_left}

  def count_vehicles_sides(self):
    global cars_left
    global cars_right
    global trucks_right
    global trucks_left

    vehicle = self.__current_vehicle__()

    if vehicle.__type_vehicle__() == 'Car':
      if vehicle.direction == 'left':
        cars_left += 1
      else:
        cars_right += 1
    else:
      if vehicle.direction == 'left':
        trucks_right += 1
      else:
        trucks_left += 1
  
  def check_opposite_cars(self, condition, current_vehicle):
    if len(self.lane) > 0 and self.__last_vehicle__().direction != current_vehicle.direction:
      print(f'{current_vehicle.__type_vehicle__()} {current_vehicle.number} and {self.__last_vehicle__().__type_vehicle__()} {self.__last_vehicle__().number} has opposite sides...')
      print(f'{current_vehicle.__type_vehicle__()} {current_vehicle.number} have to wait...')
      condition.wait()
  
  def mecanism_for_five_cars(self, car):
    if self.vehicles_enter > 0 and self.vehicles_enter % 5 == 0:
      print('Five cars was enter..')
      print(f'{car.__type_vehicle__()} {car.number} #{car.direction} was stopped...')
      print('Change the direction of the bridge...')
      sleep(1)                                        # Time to change the bridge direction

      new_car = Cars()
      print(f'Car {new_car.number} is the next...')
      sleep(1)
      self.vehicle_pass_in(new_car)

  def vehicle_pass_in(self, vehicle):
    sleep(vehicle.time_arrive)
    sleep(1)                                         # Time space between cars

    self.lane.append(vehicle)
    self.vehicles_enter += 1
    vehicle.time_in_bridge  = time()

    print(f'{vehicle.__type_vehicle__()} {vehicle.number} enter bridge on #{vehicle.direction} -> {vehicle.time_arrive} seconds to arrive')
  
  def vehicle_pass_out(self):
    vehicle = self.lane[0]

    self.count_vehicles_sides()                          # Just count cars

    sleep(vehicle.time_pass)
    self.lane.pop(0)                                 # Take of a vehicle
    self.vehicles_out += 1                           # Count cars out

    vehicle.time_in_bridge = time() - vehicle.time_in_bridge # Time total in bridge
    vehicle.count_time_metrics()                         # Build statistics

    print(f'{vehicle.__type_vehicle__()} {vehicle.number} leave bridge on #{vehicle.direction} -> time wait: {round(vehicle.__time__(), 2)} seconds')

  def let_vehicles_enter(self):
    return self.vehicles_enter < N_CARS + M_TRUCKS
  
  def let_vehicles_leave(self):
    return self.vehicles_out < N_CARS + M_TRUCKS

def bridge_statistics():
  print(f'Nº Cars right: {cars_right}')
  print(f'Nº Cars left: {cars_left}')
  print(f'Nº Trucks left: {trucks_right}')
  print(f'Nº Trucks left: {trucks_left}')
