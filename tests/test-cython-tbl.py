
from brian2 import *
from lut4brian import *

x=linspace(-100,50,151)

lut4brian.Xmin = -100.
lut4brian.Xmax =   50.
lut4brian.dX   =    1.


alpha_m = 0.1*10./exprel(-(x+35.)/(10.))
beta_m  = 4*exp(-(x+60.)/(18.))
minf    = alpha_m/(alpha_m+beta_m)

alpha_h = 0.07*exp(-(x+58.)/(20.))
beta_h  = 1./(exp(-0.1*(x+28.))+1.)
htau    = 1./(alpha_h+beta_h)
hinf    = alpha_h*htau

alpha_n = 0.01*10/exprel(-(x+34.)/(10.))
beta_n  = 0.125*exp(-(x+44.)/(80.))
ntau    = 1./(alpha_n+beta_n)
ninf    = alpha_n*ntau

lut4brian.tbl = array([minf,hinf,htau,ninf,ntau])
lutinit()


defaultclock.dt = 0.01*ms

Cm   = 1.*uF # /cm**2
Iapp = 2.*uA
gL   = 0.1*msiemens
EL   = -65.*mV
ENa  = 55.*mV
EK   = -90.*mV
gNa  = 35.*msiemens
gK   = 9.*msiemens
taus = 5*ms
gsyn = 1.*usiemens
Esyn = 0*mV

eqs = '''
dv/dt = (-gNa*minf**3*h*(v-ENa)-gK*n**4*(v-EK)-gL*(v-EL)+I+b*gsyn*(Esyn-v))/Cm : volt
minf    = lutinterpol(v/mV,0) : 1
hinf    = lutinterpol(v/mV,1) : 1
htau    = lutinterpol(v/mV,2) : 1
ninf    = lutinterpol(v/mV,3) : 1
ntau    = lutinterpol(v/mV,4) : 1
dh/dt   = 5*(hinf-h)/htau/ms  : 1
dn/dt   = 5*(ninf-n)/ntau/ms  : 1
db/dt   = -b/taus             : 1
I : amp
'''

neurons = NeuronGroup(1000, eqs, threshold="v>0.*mV", refractory="v>0.*mV", method='euler')
neurons.v = "(-70+rand()*15)*mV"
neurons.h = 1
neurons.I = 0*amp
M = StateMonitor(neurons, 'v', record=0)
S = SpikeMonitor(neurons)
s = Synapses(neurons,neurons,on_pre="b_post += 1")
s.connect(p=0.1)
s.delay = "(3+rand()*2)*ms"
run(2000*ms, report='text')
subplot(211)
plot(M.t/ms, M[0].v/mV)
subplot(212)
plot(S.t/ms,S.i,'k.')
show()

