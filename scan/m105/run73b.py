import glev,glev2,pickle,sys
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
g=glev2.G2(M,'D','','110',2,3)
glev.run(g,48,'1110111110110111',int(sys.argv[1]),log=10000)
pickle.dump(g.TAB,open('tab73.pkl','wb'))
