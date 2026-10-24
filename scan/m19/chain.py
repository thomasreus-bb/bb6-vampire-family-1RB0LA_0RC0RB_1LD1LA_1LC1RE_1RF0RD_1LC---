import subprocess,itertools,sys
TM='1RB0LC_1LA1RE_1LD1RE_1RE0LA_0RA1RF_0RB---'
def rle(s): return '/'.join(k+str(len(list(g))) for k,g in itertools.groupby(s)) or 'e'
def step(L,T,n):
    o=subprocess.run(['./bstep',TM,'R','E','1',L or '-',T or '-',str(n),'1.3',str(4*len(L)+400),'4000000000000'],capture_output=True,text=True).stdout.split()
    return o
L='';T='0'
for k in range(1,9):
    for r in (1,3):
        n=4*((40*len(L)+2000)//4)+r
        o=step(L,T,n)
        if o[0]!='OK': print('k',k,'r',r,'from L=',rle(L),'->',o); continue
        print('k=%d r=%d  L=%s  T=%s  n=%d -> L\'=%s T\'=%s  n\'-1.5n=%s'%(k,r,rle(L),T,n,rle(o[1].strip('-')),o[3].strip('-'),int(o[2])-1.5*n),flush=True)
    if o[0]!='OK': break
    L=o[1].strip('-'); T=o[3].strip('-')
