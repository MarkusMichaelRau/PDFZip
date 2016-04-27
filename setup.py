import numpy as np

#Tuning parameters for the spline compression
#please adapt this to your data
zmin = 0.0
zmax = 3.0
nnum = 30
zlim = np.linspace(start=zmin, stop=zmax, num=nnum)
thresh = 0.0001

