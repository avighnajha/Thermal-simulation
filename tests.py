import numpy as np
import base as bs
import pylab as pl

#%%
'''
Testing time for collision
'''
# fig = pl.figure()
# ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
ball1 = bs.Ball(1, 1, [0,5], [0,-1])
ball2 = bs.Ball(1, 1,[0,0], [0,0])

ball3 = bs.Ball(1, 1, [0, 3])


pl.show()

assert ball1.time_to_collision(ball3) == 0
assert ball1.time_to_collision(ball2) == 3


#%%
'''
Testing collide feature
'''
np.testing.assert_array_equal(ball1.collide(ball2).vel(), [0,0])
np.testing.assert_array_equal(ball2.vel(), [0,-1])
#%%
'''
Time and collide with containers
'''
ball8 = bs.Ball(1, 1, [0, 0], [0,1])
c = bs.Ball(np.inf, -10, [0,0], [0,0])
assert ball8.time_to_collision(c) == 9
np.testing.assert_array_equal(ball8.collide(c).vel(), [0,-1])
np.testing.assert_array_equal(c.vel(), [0,0])
#%%
'''
Time to collide but ball already in contact and moving in other direction
'''
#This test is failing as app it isnt taking the velcoity being in the oposite direction into account
b10 = bs.Ball(1, 1, [-9,0], [1, 0])
print(b10.time_to_collision(c))
#%%
'''
Ball and container ball going [-1, 0]
'''
b2 = bs.Ball(1, 1, [0, 0], [-1,0])

np.testing.assert_array_equal(b2.collide(c).vel(), [1,0])


#%%
'''
Investigating error where ball aligned with x axis or y axis ends up not bouncing back and gives negative time
'''
ball100 = bs.Ball(1, 1, [0,0], [100, 2])
c100 = bs.Ball(np.inf, -10, [0,0], [0,0])
#%%
print(ball100.collide(c100).vel())

#%%
'''
Still collide feature but with 2 different masses
'''
ball4 = bs.Ball(2, 1, [0,5], [0,0])

ball5 = bs.Ball(1, 1, [0,0], [0, 1])

np.testing.assert_array_equal(ball4.collide(ball5).vel(), [0,0.6666667])
#%%
'''
Testing Move
'''
ball6 = bs.Ball(1, 1, [0,0], [7, 0])
np.testing.assert_array_equal(ball6.move(2).pos(), [14,0])
#%%
'''
Testing simulation - next collision
'''

ball7 = bs.Ball(1, 1, [-5, 0], [0, 1])
c2 = bs.Ball(np.inf, -10, [0,0], [0,0])
#%%
'''
repeated next collisions lead to ball going through centre so only 2 velocities that alternate
'''
simul = bs.Simulation(c2, ball7)
print(ball7.time_to_collision(c2))
#simul.next_collision().run(num_frames=1, animate = True)
#print(ball7.vel(), ball7.time_to_collision(c2))
#%%
'''
Testing run()
'''
simul.next_collision().run(num_frames=5, animate = True)
#%%
'''
Testing Pressure
'''
balls8 = [bs.Ball(1, 1, [0,0], [0,1])]
container = bs.Ball(np.inf, -10, [0,0], [0,0])
simul2 = bs.Simulation(container, 1)
simul2.next_collision().run(num_frames = 5, animate = False, plots = False)



#%%
'''
Several balls
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

#balls3 = bs.Simulation.generate_balls()
c4 = bs.Ball(np.inf, -10, [0,0], [0,0])

simul5 = bs.Simulation(c4)
simul5.run(num_frames=50, animate= True)    

