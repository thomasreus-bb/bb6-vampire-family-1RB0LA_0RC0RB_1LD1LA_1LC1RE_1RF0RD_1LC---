import sys,time,re; sys.path.insert(0,'/tmp/an'); import orbit
O=orbit.Orbit('1LB0LE_0RC1RE_0LD1RD_1LA1RF_1RC0LA_0RB---','E')
key=('E','','0','100100100100100100101000010'); n=33180
t0=time.time(); B=int(sys.argv[1]); out=open('/tmp/an/orb82.txt','w')
for b in range(1,B+1):
    key2,n2=O.step(key,n)
    if not isinstance(key2,tuple): print('stop',b,key2,key[0],key[1],key[3][:200],n%96); break
    key,n=key2,n2
    S=key[3]; m=re.fullmatch(r'((?:100)*)(.*)',S)
    out.write('%d %s %d %s\n'%(b,key[1] or '-',len(str(n)),S)); 
    if b%200==0: print(b,'log10 n',len(str(n))-1,'rules',len(O.rules),'S',S[:80],len(S),'%.0fs'%(time.time()-t0)); sys.stdout.flush()
import pickle; pickle.dump(O.rules,open('/tmp/an/rules82.pkl','wb'))
