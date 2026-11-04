#!/bin/sh
# check the macro rules of nos. 44 and 51 with nxt for many x (and y up to 12)
M44=1RB0RE_1LC0RA_0LD1LB_1LA1LE_0LB0LF_1LD---; M51=1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---
python3 - "$M44" "$M51" <<'PY'
import subprocess,sys
M44,M51=sys.argv[1],sys.argv[2]
def nxt(M,pre,x,y,sf): 
    o=subprocess.run(['./nxt',M,pre,str(x),str(y),sf,'4000000000'],capture_output=True,text=True).stdout.split()
    return tuple([o[0]]+[int(v) for v in o[1:-1]])
bad=0
for x in range(1,200):
    e44={0:('B',x),1:('B',x+1),3:('A',x+4,1)}; e51={0:('B',x),1:('B',x+1),3:('A',x+3,1)}
    for y in range(0,13):
        if y!=2:
            ex=e44[y] if y in e44 else ('A',x+5,y-3)
            if nxt(M44,'',x,y,'A')!=ex: bad+=1; print('44',x,y,nxt(M44,'',x,y,'A'),ex)
            ex=e51[y] if y in e51 else ('A',x+4,y-3)
            if nxt(M51,'1',x,y,'A')!=ex: bad+=1; print('51',x,y,nxt(M51,'1',x,y,'A'),ex)
    if x>=6 and x%3==0 and nxt(M44,'',x,2,'A')!=('A',10*x//3-12,4): bad+=1; print('44 y2',x)
    if x%9==7 and nxt(M44,'',x,2,'A')!=('A',100*(x-7)//9+32,4): bad+=1; print('44 y2 x7',x)
    if x%3==0 and nxt(M51,'1',x,2,'A')!=('A',3,16*x//3+5): bad+=1; print('51 y2 x0',x)
    if x%3==2 and nxt(M51,'1',x,2,'A')!=('A',8*(x-2)//3+4,6): bad+=1; print('51 y2 x2',x)
    if x%9==7 and nxt(M51,'1',x,2,'A')!=('A',64*(x-7)//9+46,3): bad+=1; print('51 y2 x7',x)
for n in range(0,200):
    if nxt(M44,'',n,0,'B')!=('A',1,2*n+3): bad+=1; print('44 bell',n)
    if nxt(M51,'1',n,0,'B')!=('A',3,2*n+1): bad+=1; print('51 bell',n)
print('mismatches:',bad)
PY
