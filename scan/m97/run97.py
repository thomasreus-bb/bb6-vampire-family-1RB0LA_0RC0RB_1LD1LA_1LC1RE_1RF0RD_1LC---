import glev,glev2,pickle,sys
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LB_1RC1LD_1LA1RE_1RD0LA_0RB0RF_0RA---')
g=glev2.G2(M,'E','','110',2,3)
try: g.TAB=pickle.load(open('tab97.pkl','rb'))
except Exception: pass
if sys.argv[1]=='check':
    seq=[(19,'111111110110110110110110110110110111'),(52,'111'),(85,'111'),(132,'1110111111')]
    n,W=seq[0]
    for x in seq[1:]:
        n,W=g.level(n,W); print((n,W[:40]),x,n==x[0] and W==x[1])
else:
    glev.run(g,52,'111',int(sys.argv[1]),log=10000)
    T73=pickle.load(open('tab73.pkl','rb'))
    common=set(g.TAB)&set(T73)
    print('table',len(g.TAB),'common with no. 73',len(common),'identical',sum(1 for k in common if g.TAB[k]==T73[k]))
pickle.dump(g.TAB,open('tab97.pkl','wb'))
