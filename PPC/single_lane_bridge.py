from models.vehicles import *#Cars, Trucks, vehicle_statistics
from models.bridges import *#bridge_statistics
from time import time

def creating_vehicles(bridge, create_truck=False):
  if create_truck == True and bridge.vehicles_enter % 10 == 0 and bridge.vehicles_enter > 1:
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

      # Check if pass five cars
      # Check if a truck pass
      if bridge_mecanims == True:
        bridge.mecanism_for_five_cars(vehicle)

      # Trucks check if bridge has cars
      if vehicle.__type_vehicle__() == 'Truck' and bridge.__has_vehicle__():
        print(f"Stopping Truck {vehicle.number}, bridge has cars, he'll wait...")
        condition.wait()

      # Car check if there's a truck in the bridge
      if bridge.__has_vehicle__():
        if vehicle.__type_vehicle__() == 'Car' and bridge.__last_vehicle__().__type_vehicle__() == 'Truck':
          print(f'Only Truck {bridge.__last_vehicle__().number} can pass now...')
          condition.wait()
          print('Trucks pass, bridge free...')

      # Check if the cars are in opposite sides
      bridge.check_opposite_cars(condition, vehicle)

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
