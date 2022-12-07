import matplotlib.pyplot as plt
import numpy as np
import base as bs
from no_balls import collect_data_no_balls
from scipy.optimize import curve_fit
#%%
'''
Investigate Ideal gas law - Basically just runing 1 cycle of collect_data_no_balls-2000 collisions- with all the different v_maxs. Going to plot P/T against v_maxs to show it is constant.
'''
v_maxs =  [10, 20,30, 40, 80]
press_ideal, temp_ideal = collect_data_no_balls(v_maxs, no_balls = 150, ball_rad = 0.5)
PT_ideal = []
for i in range(len(press_ideal)):
    pt = press_ideal[i]/temp_ideal[i]
    PT_ideal.append(pt)

#%%
plt.plot(v_maxs, PT_ideal, "x", linestyle = "-", c = "r",markerfacecolor = "b", markeredgecolor = "b")
plt.title("P/T for different max speeds")
plt.ylim(0, 5e-24)
plt.xlim(0, 90)
plt.xlabel("Maximum velocity")
plt.ylabel("P/T")
plt.grid()
#%%
plt.plot(temp_ideal,press_ideal,  "x", linestyle = "-", c = "r", markerfacecolor = "b", markeredgecolor = "b")
plt.title("P vs T for Different Maximum Speeds")
plt.xlabel("Temperature")
plt.ylabel("Pressure")
plt.grid()

#%%
'''
Functions defined for later fits
'''

def waals(T, b):
    N = 30
    k = 1.38e-23
    V = np.pi*20**2
    return N*k*T/(V-(N*b))
                  
def line(x, m, c):
    return m*x + c

def ideal(T, N):
    k = 1.38e-23
    V = np.pi*20*82
    return N*k*T/V
#%%
params, cov = curve_fit(line, temp_ideal, press_ideal)

fit_y = []
for i in temp_ideal:
    fit_y.append(line(i, params[0],params[1]))
plt.plot(temp_ideal, press_ideal, "x")
plt.plot(temp_ideal, fit_y)
plt.ylabel("Pressure")
plt.xlabel("Temperature")
plt.title("Pressure vs Temperature")
plt.grid()

#%%
m = params[0]
V = np.pi*20**2
k = 1.38e-23
N = 150

b = ((m*V) - (N*k))/(m*N)

err = (cov[0][0]/m)*b
print(f"b = {b} +/- {err}")
#%%
'''
Investigating ideal gas law for different ball radii. Runs 4 repeatitions with different v_maxs for each ball repeatition.
'''

v_maxs_2 = [100, 200, 300, 400]
v_maxs_3 = [300, 300, 300, 300] # To collect data for single max vel
ball_rads = [0.5, 1, 2, 2.5]
data_ball_rads = []
for rad in ball_rads:
    print(f"Ball radius: {rad} ...")
    data = collect_data_no_balls(v_maxs_3, no_balls=30, ball_rad = rad)
    data_ball_rads.append(data)

#%%
b_vals = []
b_errs = []
fig, ax = plt.subplots(1, 2, figsize = (10, 5))

for data in data_ball_rads:
    temps = data[1]
    press = data[0]
    temps.sort()
    press.sort()

    ax[0].plot(temps, press, "x")
    ax[0].set_xlabel("Temperature")
    ax[0].set_ylabel("Pressure")
    
    params, cov = curve_fit(line, temps, press)

    m = params[0]
    V = np.pi*20**2
    k = 1.38e-23
    N = 30
    
    params_b_full, cov_b_full = curve_fit(waals, temps, press, p0 = [1])
    b_full = params_b_full[0]
    b_full_err = cov_b_full[0][0]
    b_vals.append(b_full)
    b_errs.append(b_full_err)
    
    y_max = []
    for x in temps:
        y_max.append(waals(x, b_full))
    ax[0].plot(temps, y_max)
    print(f"b using maxwell = {b_full} +/-{b_full_err}")
    
t_ideal = np.arange(0, 8e27, 1e27)
p_ideal = []
for t in t_ideal:
    p_ideal.append(ideal(t, 30))
ax[1].plot(ball_rads,b_vals, "x", linestyle = "-")
ax[1].errorbar(ball_rads, b_vals, yerr = b_errs)

ax[0].plot(t_ideal, p_ideal, linestyle = "--")
ax[0].set_title("Pressure vs Temperature graphs for different ball radii")
ax[0].legend(["r = 0.5", "vdW fit","r = 1", "vdW fit", "r = 2", "vdW fit","r = 2.5", "vdW fit", "Ideal gas line"])
ax[0].set_xlim(0,8e27)
ax[0].grid()
ax[1].set_title("b values against ball radius")
ax[1].set_xlabel("Ball radii")
ax[1].set_ylabel("b")
ax[1].set_xlim(0, 2.7)
plt.grid()
plt.show()


#%%
'''
Plotting P/T against r
'''
PT = []
errs = []
for data in data_ball_rads:
    temps = data[1]
    press = data[0]
    temps.sort()
    press.sort()
    T = np.mean(temps)
    T_unc = np.std(temps)/T
    P = np.mean(press)
    P_unc = np.std(press)/P
    PT_unc = T_unc+P_unc
    PT.append(P/T)
    errs = PT_unc

plt.plot(ball_rads, PT, "x", c = "r", markerfacecolor = "b", markeredgecolor = "b", linestyle = "-")
#plt.errorbar(ball_rads, PT, yerr = PT_unc, fmt = "none")
plt.grid()
plt.ylabel("P/T")
plt.xlabel("Ball radius")
plt.title("P/T plotted against different ball radii")


#%%





