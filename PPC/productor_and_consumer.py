from threading import Thread, Condition, current_thread
import time
from random import random, randint

queue = []
MAX_NUM = 2
condition = Condition()

def consumer(condition):
  global queue

  print('Consumidor iniciado')
  time.sleep(random())

  with condition:
    condition.acquire()

    while len(queue) == 0:
      print(f'Fila vazia, {current_thread().name} fica em espera')
      condition.wait()
      print(f'Produtor incluiu algo na fila, {current_thread().name} pode continuar')

    num = queue.pop(0)
    print(f'{current_thread().name} consumiu: {num}')
    condition.notify_all()
    condition.release()

def producer(condition):
   global queue

   print('Produtor iniciado...')
   time.sleep(random())
   
   with condition:
    condition.acquire()
    
    while len(queue) == MAX_NUM:
      print(f'Fila cheia, {current_thread().name} fica em espera')
      condition.wait()

      print(f'Tem espaço na fila, {current_thread().name} pode continuar')
    product = randint(0, 10)
    queue.append(product)

    print(f'{current_thread().name}, produziu: {product}')
    condition.notify_all()
    condition.release()


cs1 = Thread(name='Consumidor 1', target=consumer, args=(condition, ))
cs2 = Thread(name='Consumidor 2', target=consumer, args=(condition, ))
cs3 = Thread(name='Consumidor 3', target=consumer, args=(condition, ))

pr1 = Thread(name='Produtor 1', target=producer, args=(condition, ))
pr2 = Thread(name='Produtor 2', target=producer, args=(condition, ))
pr3 = Thread(name='Produtor 3', target=producer, args=(condition, ))

cs1.start()
time.sleep(2)
cs2.start()
time.sleep(2)
cs3.start()
time.sleep(2)

pr1.start()
time.sleep(2)
pr2.start()
time.sleep(2)
pr3.start()
time.sleep(5)