import subprocess,collections,re,sys
def comp(s): return re.sub(r'(1|01|10)\1{2,}', lambda m: '(%s)^%d '%(m.group(1), len(m.group(0))//len(m.group(1))), s)
def ev(j,X,ctx):
    r=subprocess.run(['./syn38c',str(j),str(X),str(j//2),ctx],capture_output=True,text=True).stdout
    a,b=r.split('|'); a=a.split(); return int(a[0]),int(a[1]),int(a[2]),int(a[3]),b.strip()
def isl(s):  # island part after the last long run of 1s
    m=re.search(r'1{30,}(.*)$',s); return m.group(1)
I0='1'*40+'01'*10+'00'+'111'+'0101001'+'1'
ctxs={'I0':I0}; todo=['I0']; names={isl(I0):'I0'}
R=range(int(sys.argv[1]),int(sys.argv[2]))
done=set()
while todo and len(done)<8:
    nm=todo.pop(0)
    if nm in done: continue
    done.add(nm)
    for X in (1,):
        rows=collections.defaultdict(set)
        for j in R:
            j2,X2,m2,sh,c2=ev(j,X,ctxs[nm])
            assert m2==j2//2
            i2=isl(c2)
            if i2 not in names: names[i2]='I%d'%len(names); ctxs[names[i2]]='1'*40+i2; todo.append(names[i2])
            rows[j%8].add((2*j2-5*j, sh, X2, names[i2]))
        print(nm, comp(isl(ctxs[nm])), 'X=%s'%('1100' if X else '0100'))
        for r in sorted(rows): print('   j≡%d mod 8: (2j\'-5j, shift, X\', island) in %s'%(r,sorted(rows[r])))
