from random import randint
import csv

# Time variables
min_wait    = 0
max_wait    = 0
total_time  = 0
car_counter = 1
time_cars_dict = {}

truck_counter = 1

directions = ['left', 'right']

class Vehicles:
  def __init__(self):
    self.direction        = directions[car_counter%2]
    self.number           = car_counter
    self.time_arrive      = randint(1, 3) # Time to car has comming
    self.time_start_wait  = 0
    self.time_leave_wait  = 0
    self.time_pass        = 5 # Time for a car pass thought bridge
    self.__increment_vehicle_counter() # Increment car number to continue correct counting
  
  def __increment_vehicle_counter(self):
    global car_counter
    car_counter += 1
  
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

    time_cars_dict[self.number] = self.__time__()
    write_car_statistics_csv('../PPC/cars_times_wait.csv', time_cars_dict)

    if self.number == 1:
      min_wait = time
      max_wait = time
    else:
      if time < min_wait:
        min_wait = time
      else:
        max_wait = time


class Cars(Vehicles):
  pass

def vehicle_statistics():
  time_statistics = {
    'max_time_wait': max_wait,
    'min_time_wait': min_wait,
    'med_time_wait': round(total_time/car_counter, 2),
    'total_time': round(total_time, 2)
  }
  
  print(f'Max time wait: {time_statistics["max_time_wait"]} seconds')
  print(f'Min time wait: {time_statistics["min_time_wait"]} seconds')
  print(f'Med time wait: {time_statistics["med_time_wait"]} seconds')
  print(f'Total time of execution: {time_statistics["total_time"]} seconds')

  write_bridge_statistics_csv('../PPC/cars_times_wait.csv', time_statistics)

# For write our csv with times of execution for every counting
def write_car_statistics_csv(filename, infos):
  with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['Car Nº', 'Time wait']
    writer     = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in infos:
      writer.writerow({'Car Nº': data, 'Time wait': infos[data]})

def write_bridge_statistics_csv(filename, infos):
  with open(filename, 'a', newline='') as csvfile:
    fieldnames = ['Max time', 'Min time', 'Med time', 'Total time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({
      'Max time': infos['max_time_wait'], 
      'Min time': infos['min_time_wait'], 
      'Med time': infos['med_time_wait'],
      'Total time': infos['total_time']
    })

