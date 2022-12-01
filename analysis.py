import numpy as np
import matplotlib.pyplot as plt
import base as bs

bs.Simulation.impulse_tot = 0
bs.Simulation.t_container = 0
container = bs.Ball(np.inf, -10, [0,0], [0,0])
simul = bs.Simulation(container, 2)
simul.run(num_frames=3, animate = True, plots = False)
#%%
simul.plot_pressure_evol()
#%%
'''
As we're approximating an ideal gas the KE = 3(kT)/2 therefore T = 2KE/3k where k is the boltzmann constant.
'''

temp = simul.calc_temp(1)
press = simul.calc_pressure(2*np.pi*10)
print("Tempreture: ", temp)
print("Pressure: ", press)

#Ball at [-8.57311761 -2.73891482], with speed [29.28886384 70.45786628]

'''
Error:
    Time to collision goes negatice when ball collides with container and keeps flipping between the same value negaitve and positive. Happens whenevr both times to collision are negative meaning that -b is very negaitve. So b is a big postitive number. b is v.p so happne swhen position vector and vel vector aligned .
    From rechecking always happens qwhen ball aligned with x axis and b is very large.
FIX: added check for negative time in next collision but not sure if fixed yet
'''

'''
Balls now leaving the ball when they collide around the edge - Only happens if I start ignoring t negative
'''

'''
Need to change back pause to 0.001 and change back ball generation 
'''
'''

Error causing time to be 0 was that i was moving balls and then calling collide so the balls would be at 0 time to collision when collide called. So now passing min time as an argument 
'''

'''
Now time isnt going 0 anymore but very very small and i think thois is because the velocity isnt actually changing so it seems lioke ball gonna collide with the container again. so this keeps happeneing. Sam collision over and over
'''