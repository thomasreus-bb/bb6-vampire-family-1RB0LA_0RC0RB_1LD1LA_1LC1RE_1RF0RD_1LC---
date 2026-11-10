import glev,glev2,pickle,sys
M='1RB1LE_1LC1RC_1LA1RD_1LD0RB_0LC0LF_0LB---'
g=glev2.G2(M,'E','','110',2,3)
try: g.TAB=pickle.load(open('tab72.pkl','rb'))
except Exception: pass
if sys.argv[1]=='check':
    seq=[(14,'1110111111'),(28,'111111111'),(51,'111'),(81,'1110111111'),(126,'111011111011')]
    n,W=seq[0]
    for x in seq[1:]:
        n,W=g.level(n,W); print((n,W),x,(n,W)[0]==x[0])
else:
    glev.run(g,14,'1110111111',int(sys.argv[1]),log=10000)
pickle.dump(g.TAB,open('tab72.pkl','wb'))
