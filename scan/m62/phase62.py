# iterate the macro map of no. 62 through a whole phase with exact big integers
import sys,time
from macro62 import cycle
sys.set_int_max_str_digits(0)
s=(227098,0,0)
t0=time.time()
while s[0]>0:
    s=cycle(*s)
c,b,t=s
print('phase 3 ends: c=0, b has',b.bit_length(),'bits, b odd:',b%2==1,'t=',t, 'time',round(time.time()-t0,1),'s')
print('log10 b =', len(str(b)))
r=cycle(*s); print('next:', 'HALT' if r=='HALT' else ('reset, new c has %d digits'%len(str(r[0]))))
