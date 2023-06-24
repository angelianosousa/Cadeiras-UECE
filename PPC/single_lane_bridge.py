from models.cars import Cars, vehicle_statistics
from models.bridges import bridge_statistics
from time import time
from threading import current_thread

# def starting_vehicle(create_truck):
#   if create_truck == True:
#     Trucks()
#   else:
#     Cars()

def enter_bridge(condition, bridge, bridge_mecanims = False):
    
  while bridge.let_cars_enter():
    vehicle = Cars()

    with condition:
      condition.acquire()

      # Time to wait start before the car enter in the bridge
      vehicle.time_start_wait = time()

      # Check if pass five cars     
      if bridge_mecanims == True:
        bridge.mecanism_for_five_cars(vehicle)

      # Check if the cars are in opposite sides
      bridge.check_opposite_cars(condition, vehicle)
      vehicle.time_leave_wait = time()

      bridge.car_pass_in(vehicle)
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
    bridge_statistics()
    vehicle_statistics()
