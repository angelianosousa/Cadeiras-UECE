from models.cars import Cars, cars_statistics
from models.bridges import bridges_statistics

car_counter = 1

def enter_bridge(condition, bridge, change_direction_with_five_cars = False):
  global car_counter  
    
  while bridge.let_cars_enter():
    car = Cars(car_counter)
    car_counter += 1

    with condition:
      condition.acquire()

      # Check if pass five cars     
      if change_direction_with_five_cars == True:
        bridge.mecanism_for_five_cars(car)
        car_counter += 1 # Increment car number to continue correct counting

      # Check if the cars are in opposite sides
      bridge.check_opposite_cars(condition, car)

      bridge.car_pass_in(car)
      condition.notify_all()
      condition.release()

def leave_bridge(condition, bridge):

  while bridge.let_cars_leave():

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

  with condition:

    while bridge.let_cars_leave():
      condition.wait()

    print(20*'-=-')
    bridges_statistics()
    cars_statistics(car_counter)
