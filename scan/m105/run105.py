import glev,pickle,sys
g=glev.G('1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD','A','001110',3,4)
glev.run(g,35,'011',int(sys.argv[1]),log=20000)
pickle.dump(g.TAB,open('tab105.pkl','wb'))
