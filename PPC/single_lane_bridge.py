from models.vehicles import *
from models.bridges import bridge_statistics
from time import time

def creating_vehicles(bridge, create_truck=False):
  if create_truck == True and (bridge.vehicles_enter % 10 == 0 and bridge.vehicles_enter > 1):
    return Trucks()
  else:
    return Cars()

def enter_bridge(condition, bridge, bridge_mecanims=False, create_truck=False):

  while bridge.let_vehicles_enter():

    vehicle = creating_vehicles(bridge, create_truck)

    with condition:
      condition.acquire()

      # Time to wait start before the car enter in the bridge
      vehicle.time_start_wait = time()

      # Trucks check if bridge has cars
      bridge.truck_check_cars(condition, vehicle)

      # Car check if there's a truck in the bridge
      bridge.cars_check_trucks(condition, vehicle)
      
      # Check if the cars are in opposite sides
      bridge.check_opposite_cars(condition, vehicle)

      # Check if pass five cars
      # Check if a truck pass
      if bridge_mecanims == True:
        bridge.mecanism_for_five_cars(vehicle)

      # if vehicle.__type__() == 'Truck':
      #   bridge.vehicle_pass_in(vehicle)
      #   condition.wait()
      # else:
      bridge.vehicle_pass_in(vehicle)

      vehicle.time_leave_wait = time()
      condition.notify_all()
      condition.release()

def leave_bridge(condition, bridge):

  while bridge.let_vehicles_leave():

    with condition:
      condition.acquire()

      while len(bridge.lane) == 0:
        print(f'Bridge empty, stay on hold...')
        print(20*'-=-')
        condition.wait()

      bridge.vehicle_pass_out()
      condition.notify_all()
      condition.release()

def print_results(condition, bridge):

  with condition:

    while bridge.let_vehicles_leave():
      condition.wait()

    print(20*'-=-')
    bridge_statistics()
    vehicle_statistics()
