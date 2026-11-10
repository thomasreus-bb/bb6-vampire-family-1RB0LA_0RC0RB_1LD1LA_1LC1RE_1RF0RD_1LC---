# exact closure of the tails of no. 73 under all residues (BFS by depth), with a tail-length cap; reports any HALT
import glev2,pickle,sys,markov
M='1RB1LE_1LC1RC_1LA1RD_1LD0RB_0LC0LF_0LB---'
g=glev2.G2(M,'E','','110',2,3)
try: g.TAB=pickle.load(open('tab72.pkl','rb'))
except Exception: pass
markov.LMAX=int(sys.argv[2])
front={'1110111111'}; seen=set(front); big=0
for d in range(int(sys.argv[1])):
    new=set()
    for W in front:
        for r in range(2):
            e,W2=markov.entry_safe(g,r,W)
            if W2 is None:
                if e=='HALT': print('HALT at depth',d+1,'from tail',W,'r',r); sys.exit()
                big+=1; continue
            if W2 not in seen: seen.add(W2); new.add(W2)
    front=new
    if d%5==0 or not front: print('depth',d+1,'new',len(new),'total',len(seen),'over cap',big,flush=True)
    if not front: break
pickle.dump(g.TAB,open('tab72.pkl','wb'))
print('closed under all residues within the cap; tails',len(seen),'over cap',big)
