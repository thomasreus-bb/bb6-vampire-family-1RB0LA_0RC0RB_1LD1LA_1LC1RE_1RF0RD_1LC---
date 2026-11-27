import sys,time,re,pickle; sys.path.insert(0,'/tmp/an'); import orbit, learn
TM,evs,rawfile,B,tag=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5]
tl=float(sys.argv[6]) if len(sys.argv)>6 else 1e9
O=orbit.Orbit(TM,evs)
L=[l.split() for l in open(rawfile)]
L=[x for x in L if len(x)==3 and x[1] in evs]
s,q,t=L[-1]; W,u,n,S=learn.parse(t); key=(q,W,u,S)
print('start',s,q,len(W),u,n,len(S))
t0=time.time(); out=open('/tmp/an/orb%s.txt'%tag,'w')
for b in range(1,B+1):
    if time.time()-t0>tl: print('time limit at',b); break
    key2,n2=O.step(key,n)
    if not isinstance(key2,tuple): print('stop',b,key2,key[0],key[1][:100],key[3][:100],n%96); break
    key,n=key2,n2
    out.write('%d %s %s %d %s %s\n'%(b,key[0],key[1] or '-',len(str(n)),key[2],key[3] or '-')); out.flush()
    if b%200==0: print(b,'log10 n',len(str(n))-1,'rules',len(O.rules),'W',len(key[1]),'S',len(key[3]),'%.0fs'%(time.time()-t0)); sys.stdout.flush()
pickle.dump(O.rules,open('/tmp/an/rules%s.pkl'%tag,'wb'))
nh=sum(1 for f in O.rules.values() if f for e in f[1].values() if e[0]=='HALT')
print('rules',len(O.rules),'HALT entries',nh)
