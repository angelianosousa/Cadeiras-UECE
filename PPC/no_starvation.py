from threading import Thread, Condition, current_thread, enumerate
from time import sleep, time
from random import randint

# Consts variables
N_CARS               = 100 # Number of cars
P_THROUGH            = 5   # Time pass through the bridge
T_SPACE_BETWEEN_CARS = 1   # Time space between the cars

# Global variables
lock         = Condition()
directions   = ['right', 'left']
bridge       = []
cars         = []
passing_cars = 0

# Counter for process finished
cars_finished = 0

# Time variables
time_start = 0
time_end   = 0
total_time_left  = 0
total_time_right = 0

class Car:
  def __init__(self, direction):
    self.direction        = direction
    self.time_for_comming = randint(1, 3) # Time crossing

  def crossing_process(self):
    global total_time_left
    global total_time_right

    time_start = time()
    self.to_enter_the_bridge()
    self.to_out_the_bridge()
    time_end = time()

    if self.direction == 'left':
      total_time_left += time_end - time_start
    else:
      total_time_right += time_end - time_start
  
  # Function to start get in the bridge process
  def to_enter_the_bridge(self):

    with lock:
      lock.acquire()

      if len(bridge) == 0:
        self.speed_up()
      else:
        while bridge[-1].direction != self.direction:
          print(f'#== Car {self.direction} in opposite directions, putting on hold... ==#')
          lock.wait()

          self.speed_up()
  
  # Function to start get out the bridge process
  def to_out_the_bridge(self):
    global passing_cars

    with lock:
      lock.acquire()

      if passing_cars > 0:
        if passing_cars == 5:
          print('Five cars pass...')
          print('Changing the direction of the bridge...')
          passing_cars = 0
          lock.wait()
        else:
          lock.notify_all()

      sleep(self.time_for_comming)
      bridge.pop(0)
      cars_finished += 1
      print(f'{current_thread().name} took {self.time_for_comming} seconds to exit')
      lock.notify_all()
      lock.release()
  
  def speed_up(self):
    global passing_cars

    print(f'{current_thread().name} can speed up on the {self.direction}')
    sleep(1)                                                                            # Time for waiting comming a new car
    bridge.append(self)                                                                 # Car get in
    passing_cars += 1
    lock.notify_all()
    lock.release()

def creating_cars():
  for i in range(0, N_CARS):
    new_car_thread = Thread(name=f'Car {i}', target=Car(directions[i%2]).crossing_process, args=())
    cars.append(new_car_thread)
  
def starting_cars():
  for i in range(0, N_CARS):
    sleep(T_SPACE_BETWEEN_CARS)
    cars[i].start()
  
  for i in range(0, N_CARS):
    cars[i].join()

def printing_results():
  print(f'Total time for left cars: {total_time_left}')
  print(f'Total time for right cars: {total_time_right}')
  print(f'Media time left: {total_time_left/N_CARS}')
  print(f'Media time right: {total_time_right/N_CARS}')

if __name__ == "__main__":

  creating_cars()
  starting_cars()
  printing_results()
