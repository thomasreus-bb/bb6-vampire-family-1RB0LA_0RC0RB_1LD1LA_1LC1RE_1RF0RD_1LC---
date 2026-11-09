from pm import pm,fmt
import sys
res={}
for n in range(1,61):
    row=''
    for k in range(0,121):
        tail='' if k==0 else '0'+'1'*k
        st,out=pm(n,tail)
        row+= 'H' if st=='HALT' else ('.' if out is not None else '?')
    print('%3d %s'%(n,row))
