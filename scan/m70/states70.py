import sys,pickle
sys.set_int_max_str_digits(0)
from macro70 import step,RULES
import os
if os.path.exists('rules70.pkl'): RULES.update(pickle.load(open('rules70.pkl','rb')))
x,S=30,[11,18,4]; out=[]
for lev in range(1,40001):
    x,S,_=step(x,S)
    if lev%2000==0: out.append((lev,x,S[:]))
pickle.dump(out,open('states70.pkl','wb')); pickle.dump(dict(RULES),open('rules70.pkl','wb')); print(len(out))
