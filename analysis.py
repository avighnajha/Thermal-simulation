'''
This file contains initial pressure, tempreture, kinetic energy and angular momentum evolution investigations and also investigates the velocity distribution for a simulation
'''
import numpy as np
import matplotlib.pyplot as plt
import base as bs
import scipy.stats as stats
#%%
'''
Getting a better plot for inter ball seperation at the end of 3000 collisions of 150 balls.
'''

bs.Simulation.impulse_tot = 0
bs.Simulation.t_container = 0
container = bs.Ball(np.inf, -20, [0,0], [0,0]) 
simul_sep = bs.Simulation(container, no_balls=150, ball_rad=1, v_max = 80)
simul_sep.run(num_frames=100, animate = True, plots = False)
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
bs.Simulation.impulse_tot = 0
bs.Simulation.t_container = 0
container = bs.Ball(np.inf, -20, [0,0], [0,0])
simul = bs.Simulation(container, no_balls=60)
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
Temp evol, press evol, angular momentum evol and KE evol calc for different vel factor
'''
ang_evols = []
pres_evols = []
temp_evols = []
v_maxs = [20, 40, 80]
for i in v_maxs: # Different vel factors
    print(f'''
          VELOCITY = {i}
          ''')
    bs.Simulation.impulse_tot = 0
    bs.Simulation.t_container = 0
    container = bs.Ball(np.inf, -20, [0,0], [0,0]) 
    simul = bs.Simulation(container, no_balls=63, v_max = i)
    simul.run(num_frames=3000, animate = False, plots = False)
    temp = simul.calc_temp()
    press = simul.calc_pressure(20)
    print("Tempreture: ", temp)
    print("Pressure: ", press)
    ang_evols.append(simul._ang_mom_evol)
    pres_evols.append(simul._press_evol)
    temp_evols.append(simul._temp_evol)
#%%
'''
Plotting evolution of pressure, KE and ang mom plots
'''
simul.plot_pressure_evol()
simul.plot_ang_mom()
simul.plot_ke_evol()
simul.plot_mom_evol()
#%%
'''
Attempt to plot varying T, KE, P and L evol for different vel factors in the same plot as a 3x3 set of subplots.
'''
times = simul._col_times
fig, ax = plt.subplots(3, 3, figsize = (10, 10))
idx_vel_factor = {0: 1,
 1: 2,
 2: 4}
for i in range(0, 3):
    for j in range(0, 3):
        if i == 0:
            if j ==0:
                ax[i][j].set_ylabel("Angular momentum")
                
            ax[i][j].plot(times,ang_evols[j])
            ax[i][j].set_ylim([0, 1000])
            ax[i][j].set_xlabel("Time")
            ax[i][j].set_ylabel("Angular momentum")
            ax[i][j].set_title(f"Angular momentum for velocity factor: {idx_vel_factor[j]}")
            plt.grid()
        elif i == 1:
            if j ==0:
                ax[i][j].set_ylabel("Pressure")
            ax[i][j].plot(times,pres_evols[j])
            plt.ylabel("Pressure")
            plt.xlabel("Time")
            ax[i][j].set_title(f"Pressure for velocity factor: {idx_vel_factor[j]}")
            plt.grid()
        elif i == 2:
            if j ==0:
                ax[i][j].set_ylabel("Tempreture")
            ax[i][j].plot(times,temp_evols[j])
            ax[i][j].set_xlabel("Time")
            plt.ylabel("Tempreture")
            ax[i][j].set_title(f"Tempreture for velocity factor: {idx_vel_factor[j]}")
            plt.grid()

plt.grid()
plt.show()


#%%

'''
Investigating vel distibribution
'''
bs.Simulation.impulse_tot = 0
bs.Simulation.t_container = 0
container3 = bs.Ball(np.inf, -20, [0,0], [0,0])
simul3 = bs.Simulation(container3,no_balls = 100, ball_rad=0.5,  v_max = 100)
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

