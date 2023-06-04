from random import randint

# Time variables
min_wait    = 0
max_wait    = 0
total_time  = 0
car_numbers = 1

directions = ['left', 'right']

class Cars:
  def __init__(self):
    self.direction        = directions[car_numbers%2]
    self.number           = car_numbers
    self.time_arrive      = randint(1, 3) # Time to car has comming
    self.time_start_wait  = 0
    self.time_leave_wait  = 0
    self.__increment_car_numbers() # Increment car number to continue correct counting
  
  def __increment_car_numbers(self):
    global car_numbers
    car_numbers += 1
  
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
  
def number_of_cars():
  car_numbers

def cars_statistics():
  print(f'Max time wait: {max_wait} seconds')
  print(f'Min time wait: {min_wait} seconds')
  print(f'Med time wait: {round(total_time/number_of_cars(), 2)} seconds')
  print(f'Total time of execution: {round(total_time, 2)} seconds')