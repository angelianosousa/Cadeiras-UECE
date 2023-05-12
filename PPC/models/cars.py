from random import randint

# Time variables
min_wait   = 0
max_wait   = 0
total_time = 0

directions = ['left', 'right']

class Cars:
  def __init__(self, number):
    self.direction        = directions[number%2]
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

def cars_statistics(cars_total_counter):
  print(f'Max time wait: {max_wait} seconds')
  print(f'Min time wait: {min_wait} seconds')
  print(f'Med time wait: {round(total_time/cars_total_counter, 2)} seconds')
  print(f'Total time of execution: {round(total_time, 2)} seconds')