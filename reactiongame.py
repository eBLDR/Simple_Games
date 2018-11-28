# REACTION GAME
import random
from time import sleep, perf_counter as my_timer

wait_time = random.randint(1, 5)
input('REACTION GAME!\n<enter> when you are ready... ')

sleep(wait_time)

start_time = my_timer()
input('ENTER! ')
end_time = my_timer()

print('Your reaction time was {:6.4} seconds'.format(end_time - start_time))

