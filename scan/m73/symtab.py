# level map of nos. 72/73/97 on structured tails: print (e, W') with chains compressed
import pickle,glev2,sys
from gram73 import runs,word,parse
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
g=glev2.G2(M,'D','','110',2,3)
g.TAB=pickle.load(open('tab73.pkl','rb'))
def sh(t):
    s=[];i=0
    while i<len(t):
        j=i
        while j<len(t) and t[j]==t[i]: j+=1
        s.append('%d^%d'%(t[i],j-i) if j-i>2 else '.'.join([str(t[i])]*(j-i))); i=j
    return '.'.join(s) or 'e'
def show(t):
    out=[]
    for r in (0,1):
        try: e,W2=g.entry(r,word(t)); out.append('r%d: e=%+d %s'%(r,e,sh(runs(W2))))
        except RuntimeError as ex: out.append('r%d: %s'%(r,str(ex)[:30]))
    return ' | '.join(out)
if __name__=='__main__':
    exec(sys.argv[1])
    pickle.dump(g.TAB,open('tab73.pkl','wb'))
