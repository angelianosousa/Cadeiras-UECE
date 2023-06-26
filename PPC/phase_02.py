from threading import Thread, Condition
from time import sleep
from models.bridges import Bridges
from single_lane_bridge import leave_bridge, enter_bridge, print_results

if __name__ == '__main__':

  bridge    = Bridges()
  condition = Condition() # Lock variable
  BRIDGE_MECANISM = True

  cs1 = Thread(name='Leave bridge', target=leave_bridge, args=(condition, bridge))  # Start process to leave the bridge
  pr1 = Thread(name='will enter bridge', target=enter_bridge, args=(condition, bridge, BRIDGE_MECANISM))  # Start process to enter the bridge
  pr2 = Thread(name='will enter bridge', target=enter_bridge, args=(condition, bridge, BRIDGE_MECANISM))  # Start process to enter the bridge
  shr = Thread(name='Show results', target=print_results, args=(condition, bridge))

  cs1.start()
  sleep(2)

  pr1.start()
  pr1.join()
  sleep(2)

  pr2.start()
  pr2.join()
  sleep(2)
  cs1.join()

  shr.start()