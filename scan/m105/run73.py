import glev,glev2,pickle,sys
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
g=glev2.G2(M,'D','','110',int(sys.argv[2]),int(sys.argv[3]))
n,W=48,'1110111110110111'
for i in range(int(sys.argv[1])):
    n,W=g.level(n,W)
    if W is None: print('STOP',i,n); break
    if i<12: print(n,W)
print(len(g.TAB))
