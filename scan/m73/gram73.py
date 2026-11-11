# candidate tail family G for nos. 72/73/97 (level start (110)^n W, W as list of runs of ones):
#   W = X* Y,  X = [3,5] + [2]*j  or  [8] + [2]*j  (j >= 1),  Y = [3t] (t >= 1)  or  [3, 3t] (t >= 2)
import re
def parse(t):
    # returns list of blocks or None
    i=0; blocks=[]
    while True:
        if t[i:i+2]==[3,5] and i+2<len(t) and t[i+2]==2:
            j=i+2
            while j<len(t) and t[j]==2: j+=1
            blocks.append(('P',j-i-2)); i=j; continue
        if t[i:i+1]==[8] and i+1<len(t) and t[i+1]==2:
            j=i+1
            while j<len(t) and t[j]==2: j+=1
            blocks.append(('Q',j-i-1)); i=j; continue
        break
    rest=t[i:]
    if len(rest)==1 and rest[0]%3==0 and rest[0]>=3: blocks.append(('Y',rest[0])); return blocks
    if len(rest)==2 and rest[0]==3 and rest[1]%3==0 and rest[1]>=6: blocks.append(('Y3',rest[1])); return blocks
    return None
def runs(W): return [len(x) for x in W.split('0')] if W else []
def word(t): return '0'.join('1'*k for k in t)
