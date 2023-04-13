'''
  # Próximos passos:
  - Separar uma função só para a travessia dos carros na ponte dentro da classe Car
  - Definir ponto de trava
  - Definir ponto de liberação
  
  # Fluxo:
    - Carro chega até o inicio da ponte
    - Checa se a ponte está vazia
      + caso sim acelera e lock.release() e bridge.pop()
      + caso não
      + Confere se o último carro tem a mesma direção que ele
        ** caso sim carro acelera e lock.release() e libera bridge.pop()
        ** caso não carro espera lock.wait()
'''

from threading import Thread, Condition, current_thread
from time import sleep
from random import randint, choice

# Consts variables
N_CARS               = 100 # Number of cars
P_THROUGH            = 10  # Time pass through the bridge
T_SPACE_BETWEEN_CARS = 2   # Time space between the cars

class Car:
  def __init__(self):
    self.number           = current_thread()
    self.direction        = choice(['right', 'left'])
    self.time_for_comming = randint(2, 6) # Tempo de travessia do carro
  
  def enter_the_bridge(self, lock):
    global sigle_lane_bridge

    with lock:
      lock.acquire()

      while sigle_lane_bridge[-1].direction != self.direction:
        lock.wait()
      
      print(f'Car {self.number} enter in the bridge on the {self.direction}')
      sigle_lane_bridge.append(self)
      sleep(self.time_for_comming)
      sigle_lane_bridge.pop()

if __name__ == "__main__":
  lock = Condition()
  sigle_lane_bridge = []

  for i in range(0, 2):
    new_car = Car()
    new_car_thread = Thread(name=f'Car {i}', target=new_car.enter_the_bridge, args=(lock, ))
    sleep(T_SPACE_BETWEEN_CARS)
    new_car_thread.start()
