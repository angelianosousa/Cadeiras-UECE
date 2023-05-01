'''  
  # Fluxo:
    - Carro chega até o inicio da ponte
    - Checa se a ponte está vazia
      + caso sim acelera e lock.release() e bridge.pop()
      + caso não
      + Confere se o último carro tem a mesma direção que ele
        ** caso sim carro acelera e lock.release() e libera bridge.pop()
        ** caso não carro espera lock.wait()
'''

# TODO | Adicionar uma metodo a classe Bridges para adicionar e remover carros de forma atômica

from threading import Thread, Condition, get_native_id
from time import sleep, time
from random import randint

# Consts variables
N_CARS               = 100 # Number of cars
P_THROUGH            = 5   # Time pass through the bridge
T_SPACE_BETWEEN_CARS = 1   # Time space between the cars

class Bridges():
  def __init__(self):
    self.lane = []

class Cars:
  def __init__(self, direction):
    self.direction        = direction
    self.time_for_comming = randint(1, 3) # Tempo de travessia do carro

  def crossing_process(self):
    global cars_left
    global cars_right

    self.to_enter_the_bridge()
    self.to_out_the_bridge()

    if self.direction == 'left':
      cars_left += 1
    else:
      cars_right += 1
  
  # Function to start get in the bridge process - Productor
  def to_enter_the_bridge(self):

    with lock:
      lock.acquire()

      if len(bridge.lane) == 0:
        self.speed_up()
      else:
        if bridge.lane[-1].direction != self.direction and bridge.lane[-1].time_for_comming > self.time_for_comming:
          print(f'# Car {get_native_id()} on {self.direction} putting on hold...')
          print(f'Car {get_native_id()} need {self.time_for_comming} seconds to across...')
          lock.wait()

        sleep(1)
        self.speed_up()
  
  # Function to start get out the bridge process - Consumer
  def to_out_the_bridge(self):

    with lock:
      lock.acquire()

      sleep(self.time_for_comming)
      bridge.lane.pop(0) # Car finally out

      print(f'Car {get_native_id()} was left now...')
  
  def speed_up(self):
    global cars_count

    cars_count += 1
    sleep(1)
    print(f'================================= {cars_count} ==============================')

    print(f'Car {get_native_id()} on the bridge, can leave in *{self.time_for_comming} seconds* on the #{self.direction}')
    bridge.lane.append(self) # Car get in
    lock.notify()
    lock.release()

def creating_cars():
  for i in range(0, N_CARS):
    new_car = Thread(name=f'Car {i}', target=Cars(directions[i%2]).crossing_process, args=())
    cars.append(new_car)
  
def starting_cars():
  for i in range(0, N_CARS):
    sleep(T_SPACE_BETWEEN_CARS)
    cars[i].start()
  
  for i in range(0, N_CARS):
    cars[i].join()

def priting_results():
  print(f'Nº cars left: {cars_left}')
  print(f'Nº cars right: {cars_right}')
  # print(f'Minimal time for wait: {min_wait}')

if __name__ == "__main__":
  # Count cars variables
  cars_left  = 0
  cars_right = 0

  # Time variables
  min_wait = 0
  max_wait = 0
  # max_time_on_bridge = 0

  # Global variables
  lock       = Condition()
  bridge     = Bridges()
  directions = ['right', 'left']
  cars       = []
  cars_count = 0

  creating_cars()
  starting_cars()
  priting_results()
