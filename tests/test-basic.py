from numpy import *
from matplotlib.pyplot import *
from lut4brian import *

lut4brian.Xmin = -10.
lut4brian.Xmax =  10.
lut4brian.dX   =   1.
x = linspace(lut4brian.Xmin,lut4brian.Xmax,int(round((lut4brian.Xmax-lut4brian.Xmin)/lut4brian.dX))+1 )
lut4brian.tbl=array([
    [ 1./(1.+exp(-_)) for _ in x ]
])
lutinit()
v = linspace(-20,20,201)
plot(v,lutinterpol(v,0))
plot(x,lut4brian.tbl[0,:],"ro")
show()

