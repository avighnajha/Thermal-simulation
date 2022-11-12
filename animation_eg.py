import numpy as np
import pylab as pl


#%%
f = pl.figure()
patch = pl.Circle([-4., -4.], 3, fc='r')
ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.add_patch(patch)

pl.pause(1)
patch.center = [4, 4]
pl.pause(1)
pl.show()
#%%

patch = pl.Circle([-10., -10.], 1, fc='r')
ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.add_patch(patch)

for i in range(-10, 10):
    patch.center = [i, i]
    pl.pause(0.07)
pl.show()