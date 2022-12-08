'''
This file contains initial pressure, tempreture, kinetic energy and angular momentum evolution investigations and also investigates the velocity distribution for a simulation
'''
import numpy as np
import matplotlib.pyplot as plt
import balls as bs
import simulation as sm
import scipy.stats as stats
import time

#%%
'''
Getting a better plot for inter ball seperation at the end of 3000 collisions of 150 balls.
'''

sm.Simulation.impulse_tot = 0
sm.Simulation.t_container = 0
container = bs.Ball(np.inf, -20, [0,0], [0,0]) 
simul_sep = sm.Simulation(container, no_balls=150, ball_rad=1, v_max = 80)
simul_sep.run(num_frames=3000, animate = True, plots = False)
#%%
'''
Plotting the distance between pairs of balls and distance from balls to center of container as histograms
'''
simul_sep.plot_pair_distance()

simul_sep.plot_position()

#%%
'''
Initial simulation to get temp and press values
'''
sm.Simulation.impulse_tot = 0
sm.Simulation.t_container = 0
container = bs.Ball(np.inf, -20, [0,0], [0,0])
simul = sm.Simulation(container, no_balls=60)
simul.run(num_frames=3000, animate = False, plots = False)
 #%%
'''
As we're approximating an ideal gas the KE = 2(NkT)/2 = NkT  as our 2D system only has 2 degrees of freedom. Therefore T = KE/Nk where k is the boltzmann constant.
'''
#Finds tempreture and pressure for above simulation
temp = simul.calc_temp()
press = simul.calc_pressure(20)
print("Tempreture: ", temp)
print("Pressure: ", press)


#%%

'''
Investigating vel distibribution
'''
sm.Simulation.impulse_tot = 0
sm.Simulation.t_container = 0
container3 = bs.Ball(np.inf, -20, [0,0], [0,0])
simul3 = sm.Simulation(container3,no_balls = 100, ball_rad=0.5,  v_max = 100)
simul3.run(num_frames=1000, animate = False, plots= True)

#%%
'''
Plotting distribtution and fitting a normalised maxwell curve on it
'''
all_v, heights, edges = simul3.plot_v_dist()

widths = edges[1:]-edges[:-1]
area = 0
for i in range(len(widths)):
    area+= widths[i]*heights[i] # finding total area under histogram to normalise maxwell-boltzman distribution

x = np.linspace(0, 300, 300)
maxwell = stats.maxwell
params = maxwell.fit(all_v, floc=0)
plt.plot(x, area*maxwell.pdf(x, *params))
plt.legend(["Boltzman fit","Speed bins", "Errors"])
plt.show()
#%%
'''
Calculating the vrms of our system and the vrms we should have. Theoretical V_rms = sqrt(2*k*T/m), theoretical v_avg = sqrt(8*kT/pi*m), variance in v = <v**2> - <v>**2.
'''
T = simul3.calc_temp()
k = 1.38*10**-23
all_v_squares= []
for ball in simul3._balls:
    speed = np.dot(ball.vel(), ball.vel())
    all_v_squares.append(speed)

v_rms = np.sqrt(np.mean(all_v_squares))

pred_v_rms = np.sqrt(2*k*T)
print(f'''
      Predicted v_rms = {pred_v_rms}
      V_rms of our system = {v_rms}
      ''')

v_avg = np.mean(all_v)
pred_v_avg = np.sqrt(8*k*T/np.pi)

print(f'''
      Predicted v_avg = {pred_v_avg}
      V_avg of our system = {v_avg}
      ''')

v_var = v_rms**2 - v_avg**2
pred_v_var = np.std(all_v)**2

print(f'''
      Predicted variance in v = {pred_v_var}
      variance in v of our system = {v_var}
      ''')

#%%
