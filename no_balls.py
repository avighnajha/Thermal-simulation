import matplotlib.pyplot as plt
import numpy as np
import base as bs
#%%
'''
Change in P-T for different number of balls
'''
'''
Here for a speciric number of balls I do 4 reps with different max velocities and return the pressure and temp data for each velocity
Then repeat this for all the different number of balls. eg: for 4 different numbers of balls, for each number of balls I get 4 sets of data corresponding to 4 dif v_maxs. Now I can plot these 4 sets of data for P and T for each number of balls.
'''

pos_balls = [15, 39, 63, 150, 288]
v_maxs = [10, 20, 40, 80]
def collect_data_no_balls(v_maxs, no_balls = 100, ball_rad = 0.5):
    '''
    For a specific number of balls, several repeatitions dependiing on the length of "v_maxs" are carried out. For each repeatition, values for pressure and temperature are appended to a list and returned at the end.

    Parameters
    ----------
    v_maxs : list
        a list of different maximum velocities that the investigation should be carried out for.
    no_balls : int, optional
        The number of balls to be used in the analysis. The default is 100.
    ball_rad : float, optional
        The radius of the balls inside the container. The default is 0.5.

    Returns
    -------
    list
        a list containing a list of pressure and temperature values for the investigation carried out.

    '''
    pressures_balls = [] # The pressures of the different number of balls
    temps_balls = [] #The temnpretures of the different number of balls
    final_pres = []
    final_temps = []
    for j in v_maxs:
        print(f"Current v_max = {j}")
        bs.Simulation.impulse_tot = 0
        bs.Simulation.t_container = 0
        container2 = bs.Ball(np.inf, -20, [0,0], [0,0])
        simul2 = bs.Simulation(container2, no_balls = no_balls,v_max = j, ball_rad=ball_rad)
        simul2.run(num_frames=3000, animate = False, plots= False)
        fin_pressure = simul2.calc_pressure(rad_con=20)
        pressures_balls.append(fin_pressure)
        temp = simul2.calc_temp()
        temps_balls.append(temp)
    final_pres.append(simul2.calc_pressure(20))
    final_temps.append(simul2.calc_temp())
    return [pressures_balls, temps_balls]

all_data_no_balls = []
for k in pos_balls: #Carries out simulation at certain number of balls 5 times and adds to all data
    data = collect_data_no_balls(v_maxs, k)
    all_data_no_balls.append(data)
#%%
'''
Plotting P vs T data for different number of balls
'''
for data in all_data_no_balls:
    data[1].sort()
    data[0].sort()
    plt.plot(data[1], data[0], "x", linestyle = "-")
    plt.xlabel("Temperature")
    plt.ylabel("Pressure")

plt.title("Pressure vs Temperature graphs for different number of balls")
plt.legend(["Balls = 15", "Balls = 39", "Balls = 63", "Balls = 150","Balls = 288"])
plt.grid()
plt.show()
#%%
'''
Plotting P/T vs N data - expect straight line
'''
'''
Here "data in all_data_no_balls" takes each set of data, where data has 2 arrays 1 with 4 values of pressure and the other with 4 values of temperature where each value is for a specific v_max. I then find P/T for each v_max and add to a list and then get the mean of this as we should get constant P/T for the same number of balls. Now I plot this mean value of P/T against the number of balls
'''

PTs = []

for data in all_data_no_balls:
    press= data[0]
    temp =data[1]
    PT_temp = []
    
    for i in range(len(temp)):
        PT_temp.append(press[i]/temp[i])
    PTs.append(np.mean(PT_temp)) 
    
    
plt.plot(pos_balls, PTs, "x", linestyle = "-")
plt.ylim(0,2e-26) #vary depending on data and parameters to make data visible
plt.title("P/T vs N")
plt.xlabel("Number of balls")
plt.ylabel("P/T")
plt.grid()
plt.show()

