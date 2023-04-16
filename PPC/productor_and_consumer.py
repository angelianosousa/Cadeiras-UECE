from threading import Thread, Condition, current_thread
import time
import random

queue = []
MAX_NUM = 2
condition = Condition()

def consumer(condition):
    global queue

    print('Consumidor iniciado')
    time.sleep(random.random())

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
   time.sleep(random.random())
   
   with condition:
    condition.acquire()
    
    while len(queue) == MAX_NUM:
      print(f'Fila cheia, {current_thread().name} fica em espera')
      condition.wait()
      print(f'Tem espaço na fila, {current_thread().name} pode continuar')
      product = random.randint(0, 10)
      queue.append(product)
      print(f'{current_thread().name}, produziu: {product}')
      condition.notify_all()
      condition.release()