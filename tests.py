import numpy as np
import base as bs
import pylab as pl
#%%
'''
Testing time for collision
'''
fig = pl.figure()
ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
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
b = bs.Ball(1, 1, [0, 0], [0,1])
c = bs.Ball(9e999, -10, [0,0], [0,0])
assert b.time_to_collision(c) == 9
np.testing.assert_array_equal(b.collide(c).vel(), [0,-1])
np.testing.assert_array_equal(c.vel(), [0,0])

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

ball7 = bs.Ball(1, 1, [0,0], [0,1])
container1 = bs.Ball(np.inf, -10, [0,0], [0,0]) 

print(ball7.time_to_collision(container1))
simul = Simulation(container1, ball7 )
simul.next_collision().run(5, animate = True)