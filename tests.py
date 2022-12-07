'''
Below are tests carried out to check for functionality regarding the balls and the simulations. In some cases "assert" statements are used in which case if running the cell returns nothing the tests have passed. For tests of the simulation most tests are visual and looking at the simulation allows user to know if tests have passed.
'''
#%%
import numpy as np
import base as bs
import pylab as pl

#%%
'''
Testing time for collision
'''

ball1 = bs.Ball(1, 1, [0,5], [0,-1])
ball2 = bs.Ball(1, 1,[0,0], [0,0])

ball3 = bs.Ball(1, 1, [0, 7], [0,0])
ball4 = bs.Ball(1, 1, [0, -2], [0, 1])

pl.show()

assert ball1.time_to_collision(ball3) == None # No possible collision
assert ball1.time_to_collision(ball2) == 3
assert ball1.time_to_collision(ball4) == 2.5
#%%
'''
Testing move
'''
ball5 = bs.Ball(1, 1, [0, -2], [0, 1])
np.testing.assert_array_equal(ball5.move(5).pos(), [0,3])

#%%
'''
Testing error for negative time to move
'''
ball5.move(-3)

#%%
'''
Testing collide feature
'''
ball6 = bs.Ball(1, 1, [0,5], [0,-1])
ball7 = bs.Ball(1, 1,[0,0], [0,0]) 
time_to_collision = ball6.time_to_collision(ball7)
ball6.move(time_to_collision)
np.testing.assert_array_equal(ball6.collide(ball7, time_to_collision).vel(), [0,0])
np.testing.assert_array_equal(ball7.vel(), [0,-1])
#%%
'''
Testing error message for negative time to collision - Expecting an "Exception: Time to collision cannot be negative"
'''
ball5 = bs.Ball(1, 1, [0,0], [0,-1])
time1_3 = ball1.time_to_collision(ball3)
ball1.collide(ball3, time1_3).vel()
                              
#%%
'''
Time and collide with containers
'''
ball8 = bs.Ball(1, 1, [0, 0], [0,1])
c = bs.Ball(np.inf, -10, [0,0], [0,0])
assert ball8.time_to_collision(c) == 9
t_b_c = ball8.time_to_collision(c)
ball8.move(t_b_c)
np.testing.assert_array_equal(ball8.collide(c, t_b_c).vel(), [0,-1])
np.testing.assert_array_equal(c.vel(), [0,0])
#%%
'''
Time to collide with container but ball already in contact and moving in other direction
'''
ball9 = bs.Ball(1, 1, [-9,0], [1, 0])
assert ball9.time_to_collision(c) == 18

ball10 = bs.Ball(1, 1, [-9,0], [-1, 0])
assert ball10.time_to_collision(c) == 0 #Ball and container already in contact


#%%
'''
Collide feature but with 2 different masses
'''
ball11 = bs.Ball(2, 1, [0,5], [0,0])
ball12 = bs.Ball(1, 1, [0,0], [0, 1])
t_min = ball11.time_to_collision(ball12)

np.testing.assert_array_equal(ball11.collide(ball12, t_min).vel(), [0,2/3])

#%%
'''
Testing simulation - next collision 
!! Was used to test simulation when balls were generated externally. Now balls are generated in simulation hence tests are no more functional !!
'''

ball13 = bs.Ball(1, 1, [-5, 0], [0, 1])
c2 = bs.Ball(np.inf, -10, [0,0], [0,0])
simul = bs.Simulation(c2, ball13)
simul.next_collision()
#%%
'''
Repeatedly applying next collisions leads to ball going through centre so only 2 alternating velocities expected. 
!! Was used to test simulation when balls were generated externally. Now balls are generated in simulation hence tests are no more functional !!
'''
simul2 = bs.Simulation(c2, ball13)
print(ball13.time_to_collision(c2))
simul2.next_collision().run(num_frames=1, animate = True)
print(ball13.vel(), ball13.time_to_collision(c2))
#%%
'''
Testing run()
!! Was used to test simulation when balls were generated externally. Now balls are generated in simulation hence tests are no more functional !!
'''
simul.next_collision().run(num_frames=5, animate = True)
#%%
'''
Testing Pressure
!! Was used to test simulation when balls were generated externally. Now balls are generated in simulation hence tests are no more functional !!
'''
balls8 = [bs.Ball(1, 1, [0,0], [0,1])]
container = bs.Ball(np.inf, -10, [0,0], [0,0])
simul2 = bs.Simulation(container, 1)
simul2.next_collision().run(num_frames = 5, animate = False, plots = False)



#%%
'''
Several balls in the same simulation.
!! Was used to test simulation when balls were generated externally. Now balls are generated in simulation hence tests are no more functional !!
'''
c3 = bs.Ball(np.inf, -10, [0,0], [0,0])
bb1 = bs.Ball(1, 1, [0,0], [0,1])
bb2 = bs.Ball(1, 1, [0,9], [0,-1])
bb3 = bs.Ball(1, 1, [5, 0], [1, 0])
bb4 = bs.Ball(1, 1, [4, 0], [2, 0])

balls=[bb1, bb2, bb3]
simul3 = bs.Simulation(c3, balls)

simul3.next_collision().run(num_frames=50, animate = True)
#%%
c3 = bs.Ball(np.inf, -10, [0,0], [0,0])
bb5 = bs.Ball(1, 1, [0,0.5], [0,1])
bb6 = bs.Ball(1, 1, [0,-1], [0,-1])
balls2 = [bb5, bb6]
simul4 = bs.Simulation(c3, balls2)

simul4.next_collision().run(num_frames=7, animate = True)
#%%

#balls3 = bs.Simulation.generate_balls() #Was used to test a generate_balls() functions trialed earlier.
c4 = bs.Ball(np.inf, -10, [0,0], [0,0])

simul5 = bs.Simulation(c4)
simul5.run(num_frames=50, animate= True)    

#%%
'''
Testing ball generation - Console should show the number of balls generated. Only the balls that'll fit are generated.
'''
bs.Simulation.impulse_tot = 0
bs.Simulation.t_container = 0
container= bs.Ball(np.inf, -20, [0,0], [0,0]) 
simul_sep = bs.Simulation(container, no_balls=100, ball_rad=1, v_max = 800)
simul_sep.run(num_frames=1, animate = True, plots = False)
#%%
'''
Testing different number of balls that can fit in a container for different ball radii
'''
bs.Simulation.impulse_tot = 0
bs.Simulation.t_container = 0
container = bs.Ball(np.inf, -20, [0,0], [0,0]) 
simul_sep2 = bs.Simulation(container, no_balls=150, ball_rad=1.5, v_max = 800)
simul_sep2.run(num_frames=1, animate = True, plots = False)
#%%
'''
Also used to test different ball generation methods to see which was most durable.
'''
bs.Simulation.impulse_tot = 0
bs.Simulation.t_container = 0
container3 = bs.Ball(np.inf, -20, [0,0], [0,0]) 
simul_sep3 = bs.Simulation(container3, no_balls=150, ball_rad=2, v_max = 800)
simul_sep3.run(num_frames=1, animate = True, plots = False)
#%%
'''
Testing animation
'''
bs.Simulation.impulse_tot = 0
bs.Simulation.t_container = 0
container4= bs.Ball(np.inf, -20, [0,0], [0,0]) 
simul_sep4 = bs.Simulation(container4, no_balls=100, ball_rad=1, v_max = 800)
simul_sep4.run(num_frames=1000, animate = True, plots = False)
#%%
