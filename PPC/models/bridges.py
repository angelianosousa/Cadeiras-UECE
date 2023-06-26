from time import time, sleep
from models.vehicles import Cars

# Const variables
N_CARS   = 100 # Cars counter
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
    # self.vehicles_stopped    = []

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

  def count_vehicles_sides(self):
    global cars_left
    global cars_right
    global trucks_right
    global trucks_left

    vehicle = self.__current_vehicle__()

    if vehicle.__type__() == 'Car':
      if vehicle.direction == 'left':
        cars_left += 1
      else:
        cars_right += 1
    else:
      if vehicle.direction == 'left':
        trucks_right += 1
      else:
        trucks_left += 1
  
  # Mecanism methods
  def check_opposite_cars(self, condition, current_vehicle):
    if len(self.lane) > 0 and self.__last_vehicle__().direction != current_vehicle.direction:
      print(f'{current_vehicle.__type__()} {current_vehicle.number} and {self.__last_vehicle__().__type__()} {self.__last_vehicle__().number} has opposite sides...')
      print(f'{current_vehicle.__type__()} {current_vehicle.number} have to wait...')
      condition.wait()
  
  def mecanism_for_five_cars(self, car):
    if (self.vehicles_enter > 0 and self.vehicles_enter % 5 == 0) and car.__type__() == 'Car':
      print('Five cars was enter..')
      print(f'{car.__type__()} {car.number} #{car.direction} was stopped...')
      print('Change the direction of the bridge...')
      sleep(1)                                        # Time to change the bridge direction

      new_direction = 'right' if car.direction == 'left' else 'left'
      new_car = Cars(new_direction)
      
      print(f'{new_car.__type__()} {new_car.number} enter bridge on #{new_car.direction} -> {new_car.time_arrive} seconds to arrive')
      sleep(1)
      # self.vehicles_stopped.append(new_car)
      # self.lane.insert(0, new_car)
      self.lane.insert(0, new_car)
      self.vehicles_enter += 1
    
  def truck_check_cars(self, condition, next_vehicle):
    if next_vehicle.__type__() == 'Truck' and self.__has_vehicle__():
      print(f"Stopping Truck {next_vehicle.number}, bridge has cars, he'll wait...")
      condition.wait()
  
  def cars_check_trucks(self, condition, next_vehicle):
    if self.__has_vehicle__():
      if next_vehicle.__type__() == 'Car' and self.__last_vehicle__().__type__() == 'Truck':
        print(f'Only Truck {self.__last_vehicle__().number} can pass now...')
        condition.wait()
        print('Trucks pass, bridge free...')

  def vehicle_pass_in(self, vehicle):
    sleep(vehicle.time_arrive)
    sleep(1)                                         # Time space between cars

    self.lane.append(vehicle)
    self.vehicles_enter += 1

    vehicle.time_in_bridge = time()

    print(f'{vehicle.__type__()} {vehicle.number} enter bridge on #{vehicle.direction} -> {vehicle.time_arrive} seconds to arrive')
  
  def vehicle_pass_out(self):

    # if len(self.vehicles_stopped) > 0:
    #   vehicle = self.vehicles_stopped.pop(0)
    # else:
    vehicle = self.lane[0]

    self.count_vehicles_sides()                      # Just count cars

    sleep(vehicle.time_pass)
    self.lane.pop(0)                                 # Take of a vehicle

    self.vehicles_out += 1

    vehicle.time_in_bridge = time() - vehicle.time_in_bridge # Time total in bridge
    vehicle.count_time_metrics()                             # Build statistics

    print(f'{vehicle.__type__()} {vehicle.number} leave bridge on #{vehicle.direction} -> time wait: {round(vehicle.__time_wait__(), 2)} seconds')

  def let_vehicles_enter(self):
    return self.vehicles_enter <= M_TRUCKS + N_CARS
  
  def let_vehicles_leave(self):
    return self.vehicles_out <= M_TRUCKS + N_CARS

def bridge_statistics():
  print(f'Nº Cars right: {cars_right}')
  print(f'Nº Cars left: {cars_left}')
  print(f'Nº Trucks left: {trucks_right}')
  print(f'Nº Trucks left: {trucks_left}')
