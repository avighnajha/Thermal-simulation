import matplotlib.pyplot as plt
import numpy as np
import balls as bs
import simulation as sm
#%%
'''
Automating repeat simulations and collecting pressure vs Temp values for different radii of container.
'''
'''
Here for a specific radius of container, number of balls is fixed so we do 4 repeatitions for each container volume where in each repatition the velocity of the balls is doubled. So now we have 4 sets of P and T values for each volume. Now we have 3 changing varaibles, P, V and T so we could do a P/T vs 1/V plot as here V is the independent variable
'''
v_maxs = [10, 20, 40, 80]
#Going to try same exp but same v_max just 4 reps
def collect_r_data(v_maxs, r_con):
    '''

    Parameters
    ----------
        v_maxs : list
            a list of different maximum velocities that the investigation should be carried out for.
        r_con : float
            the radius of the container wanted for the investigation.

    Returns
    -------
    list
        a list containing a list of pressure and temperature values for the investigation carried out.

    '''
    pressures = []
    temps = []
    for i in v_maxs:
        sm.Simulation.impulse_tot = 0
        sm.Simulation.t_container = 0
        container = bs.Ball(np.inf, -r_con, [0,0], [0,0])
        simul = sm.Simulation(container, no_balls = 150, v_max = i, ball_rad=1)
        simul.run(num_frames=3000, animate = False, plots = False)
        fin_pressure = simul.calc_pressure(r_con)
        pressures.append(fin_pressure)
        temp = simul.calc_temp()
        temps.append(temp)
    return [pressures, temps]
rs = [20, 25, 30, 35]
all_data = []
for r in rs:
    data = collect_r_data(v_maxs, r)
    all_data.append(data)
    #temps = data[0]
    #pressures = data[1]
#%%    
'''
all_data contains the data for change in P-T for different container radii.
'''
for data in all_data:
    data[1].sort()
    data[0].sort()
    plt.plot(data[1], data[0], "x", linestyle = "-")
    plt.xlabel("Temperature")
    plt.ylabel("Pressure")

plt.title("Pressure vs Temperature graphs for different container radii")
plt.legend(["r = 10", "r = 15", "r = 20", "r = 25"])
plt.grid()
plt.show()
#%%
'''
Plotting P/T vs 1/V
'''
vols_inv = []
for r in rs:
    vol = np.pi*r**2
    vols_inv.append(1/vol)

PTs_vol = []


for data in all_data:
    press= data[0]
    temp =data[1]
    PT_vol_temp = []
    
    for i in range(len(temp)):
        PT_vol_temp.append(press[i]/temp[i])
    PTs_vol.append(np.mean(PT_vol_temp)) 
    
    
plt.plot(vols_inv, PTs_vol, "x", linestyle = "-", c = "r", markeredgecolor = "b", markerfacecolor = "b")
plt.ylim(0, 2e-26)
plt.xlim(0, 0.001)
plt.title("P/T vs 1/V")
plt.xlabel("1/V")
plt.ylabel("P/T")
plt.grid()
plt.show()

