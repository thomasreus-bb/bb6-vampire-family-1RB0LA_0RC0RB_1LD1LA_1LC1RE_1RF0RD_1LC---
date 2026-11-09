import glev,pickle,sys
def closure(g,maxW=60):
    Ws=set(W for r,W in g.TAB)|set(W2 for e,W2 in g.TAB.values())
    todo=list(Ws); seen=set(Ws)
    while todo:
        W=todo.pop()
        for r in range(g.m):
            e,W2=g.entry(r,W)
            if W2 not in seen:
                if len(W2)>maxW: return None,W2
                seen.add(W2); todo.append(W2)
    return seen,None
if __name__=='__main__':
    g=glev.G('1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD','A','001110',3,4)
    g.TAB=pickle.load(open('tab105.pkl','rb'))
    S,bad=closure(g)
    pickle.dump(g.TAB,open('tab105.pkl','wb'))
    if S is None: print('not closed, long tail',bad); sys.exit()
    f=lambda W: '.'.join(map(str,glev.tails(W))) or 'e'
    print(len(S),'tails, closed')
    for W in sorted(S,key=len):
        print('%-10s %-14s'%(f(W),W),'  '.join('r%d:%+d,%s'%(r,g.TAB[(r,W)][0],f(g.TAB[(r,W)][1])) for r in range(3)))
