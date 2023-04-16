'''
  # Próximos passos:
  OK - Separar uma função só para a travessia dos carros na ponte dentro da classe Car
  OK - Definir ponto de trava
  OK - Definir ponto de liberação
  
  # Fluxo:
    - Carro chega até o inicio da ponte
    - Checa se a ponte está vazia
      + caso sim acelera e lock.release() e bridge.pop()
      + caso não
      + Confere se o último carro tem a mesma direção que ele
        ** caso sim carro acelera e lock.release() e libera bridge.pop()
        ** caso não carro espera lock.wait()
'''

from threading import Thread, Condition, current_thread, enumerate
from time import sleep, time
from random import randint

# Consts variables
N_CARS               = 100 # Number of cars
P_THROUGH            = 5   # Time pass through the bridge
T_SPACE_BETWEEN_CARS = 2   # Time space between the cars

# Global variables
lock       = Condition()
directions = ['right', 'left']
bridge     = []
cars       = []

# Time variables
time_start = 0
time_end   = 0
total_time_left  = 0
total_time_right = 0

class Car:
  def __init__(self, direction):
    self.direction        = direction
    self.time_for_comming = randint(1, 3) # Tempo de travessia do carro

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

    with lock:
      lock.acquire()

      sleep(self.time_for_comming)
      bridge.pop(0)                                                                     # Car finally out
      print(f'{current_thread().name} took {self.time_for_comming} seconds to exit')
      lock.notify_all()
      lock.release()
  
  def speed_up(self):
    print(f'{current_thread().name} can speed up on the {self.direction}')
    sleep(1)                                                                            # Time for waiting comming a new car
    bridge.append(self)                                                                 # Car get in
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

  # print(len(enumerate()))
  # while len(enumerate()) > 0:
    # printing_results()
    # print(f'Total time for left cars: {total_time_left}')
    # print(f'Total time for right cars: {total_time_right}')
    # print(f'Media time left: {total_time_left/N_CARS}')
    # print(f'Media time right: {total_time_right/N_CARS}')
