import os
from brian2 import *

set_device('cpp_standalone', directory='standalone-org')
#prefs.devices.cpp_standalone.openmp_threads = os.cpu_count()

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
dv/dt = (-gNa*m**3*h*(v-ENa)-gK*n**4*(v-EK)-gL*(v-EL)+I+b*gsyn*(Esyn-v))/Cm : volt
m       = alpha_m/(alpha_m+beta_m)          : 1
alpha_m = 0.1*10./exprel(-(v/mV+35.)/(10.)) : 1
beta_m  = 4*exp(-(v/mV+60.)/(18.))          : 1
dh/dt   = 5*(alpha_h*(1-h)-beta_h*h)/ms     : 1
alpha_h = 0.07*exp(-(v/mV+58.)/(20.))       : 1
beta_h  = 1./(exp(-0.1*(v/mV+28.))+1.)      : 1
dn/dt   = 5*(alpha_n*(1-n)-beta_n*n)/ms     : 1
alpha_n = 0.01*10/exprel(-(v/mV+34.)/(10.)) : 1
beta_n  = 0.125*exp(-(v/mV+44.)/(80.))      : 1
db/dt   = -b/taus                           : 1
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
run(10000*ms, report='text')
subplot(211)
plot(M.t/ms, M[0].v/mV)
subplot(212)
plot(S.t/ms,S.i,'k.')
show()

