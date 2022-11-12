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
Ball and container ball going [-1, 0]
'''
b2 = bs.Ball(1, 1, [0, 0], [-1,0])

np.testing.assert_array_equal(b2.collide(c).vel(), [1,0])


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
Testing simulation
'''

ball7 = bs.Ball(1, 1, [-5, 0], [0,1])

#%%
'''
repeated next collisions lead to ball going through centre so only 2 velocities that alternate
'''
simul = bs.Simulation(c, ball7)
print(ball7.time_to_collision(c))
simul.next_collision()
print(ball7.vel(), ball7.time_to_collision(c))