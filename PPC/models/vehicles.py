from random import randint, choice
import csv
import numpy as np

# Time variables
car_times            = []
total_time_wait      = 0
total_time_in_bridge = 0
vehicle_counter      = 1
truck_counter        = 1

directions = ['left', 'right']

class Vehicles:
  def __init__(self, direction=''):
    self.direction       = direction if direction != '' else directions[vehicle_counter%2]
    self.number          = vehicle_counter
    self.time_arrive     = randint(1, 3) # Time to car has comming
    self.time_start_wait = 0
    self.time_leave_wait = 0
    self.time_in_bridge  = 0
    self.time_pass       = 5             # Time for a car pass thought bridge
    self.__increment_vehicle_counter__() # Increment car number to continue correct counting
  
  def __type__(self):
    return 'Car'
  
  def __increment_vehicle_counter__(self):
    global vehicle_counter
    vehicle_counter += 1
  
  def __time_wait__(self):
    return round(self.time_leave_wait - self.time_start_wait, 2)

  def __total_time_in_bridge__(self):
    global total_time_in_bridge

    total_time_in_bridge += self.__get_time_in_bridge__()

  def __get_time_in_bridge__(self):
    return round(self.time_in_bridge, 2)

  def count_time_metrics(self):
    global total_time_wait

    car_times.append(self.__time_wait__())
    total_time_wait += self.__time_wait__()
    self.__total_time_in_bridge__()

class Cars(Vehicles):
  pass

class Trucks(Vehicles):
  def __init__(self):
    self.direction       = directions[truck_counter%2]
    self.number          = truck_counter
    self.time_arrive     = randint(1, 3) # Time to car has comming
    self.time_start_wait = 0
    self.time_leave_wait = 0
    self.time_in_bridge  = 0
    self.time_pass       = 10            # Time for a car pass thought bridge
    self.__increment_vehicle_counter__() # Increment car number to continue correct counting
  
  def __type__(self):
    return 'Truck'
  
  def __increment_vehicle_counter__(self):
    global truck_counter
    truck_counter += 1

def filter_array(times):
  # using numpy to filter the zeros
  new_arr = np.array(times, dtype=int)
  filter_arr = new_arr > 0

  return new_arr[filter_arr]

def vehicle_statistics():

  filtered_car_times = filter_array(car_times)
  filtered_car_times.sort()

  time_statistics = {
    'max_time_wait': filtered_car_times[-1],
    'min_time_wait': filtered_car_times[0],
    'med_time_wait': round(total_time_wait/len(car_times), 2),
    'total_time_in_bridge': round(total_time_wait, 2)
  }
  
  print(f'Max time wait: {time_statistics["max_time_wait"]} seconds')
  print(f'Min time wait: {time_statistics["min_time_wait"]} seconds')
  print(f'Med time wait: {time_statistics["med_time_wait"]} seconds')
  print(f'Time total in bridge: {time_statistics["total_time_in_bridge"]} seconds')

  write_car_statistics_csv('./PPC/cars_times_wait.csv', car_times)
  write_bridge_statistics_csv('./PPC/cars_times_wait.csv', time_statistics)

# For write our csv with times of execution for every counting
def write_car_statistics_csv(filename, infos):
  with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['Car Nº', 'Time wait']
    writer     = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for index in range(len(infos)):
      writer.writerow({
        'Car Nº': index,
        'Time wait': infos[index]
      })

def write_bridge_statistics_csv(filename, infos):
  with open(filename, 'a', newline='') as csvfile:
    fieldnames = ['Max time', 'Min time', 'Med time', 'Total time in bridge']
    writer     = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({
      'Max time': infos['max_time_wait'], 
      'Min time': infos['min_time_wait'], 
      'Med time': infos['med_time_wait'],
      'Total time in bridge': infos['total_time_in_bridge']
    })
