import sys,time,pickle,functools,random; sys.path.insert(0,'/tmp/an'); import orbit
TM,evs,tag,D,NS=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
tl=float(sys.argv[6]) if len(sys.argv)>6 else 1500
O=orbit.Orbit(TM,evs); O.rules=pickle.load(open('/tmp/an/rules%s.pkl'%tag,'rb'))
t0=time.time()
@functools.lru_cache(maxsize=None)
def P(key,d):
    if d==0: return 0.0
    f=O.rule(key)
    if f is None: return 0.0
    m,tab=f; s=0.0
    for r,e in tab.items():
        if e[0]=='HALT': s+=1.0
        elif len(e)==1: pass
        else: s+=P(e[0],d-1)
    return s/m
keys=[]
for l in open('/tmp/an/orb%s.txt'%tag):
    b,q,W,ln,u,S=l.split(); keys.append((q,'' if W=='-' else W,u,'' if S=='-' else S))
random.seed(1); sample=random.sample(keys,min(NS,len(keys)))
tot=0; cnt=0; mx=0
for k in sample:
    if time.time()-t0>tl: break
    p=P(k,D); tot+=p; cnt+=1; mx=max(mx,p)
print('depth',D,'sampled',cnt,'mean P(HALT within %d events)=%.3g'%(D,tot/max(cnt,1)),'max',mx,'rules',len(O.rules),'%.0fs'%(time.time()-t0))
pickle.dump(O.rules,open('/tmp/an/rules%s.pkl'%tag,'wb'))
