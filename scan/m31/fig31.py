from PIL import Image, ImageDraw, ImageFont
M="1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB---".split("_")
T={}
for i,s in enumerate(M):
    for b in range(2):
        x=s[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
bells=[]
for l in open("b31.txt"):
    h,t=l.split("|"); f=h.split(); toks=[x for x in t.split()]
    runs=[int(x.split("^")[1]) for x in toks if x.startswith("1^")]
    bells.append((int(f[0]),int(f[1]),runs))
def typ(r):
    tail=len(r)>=2 and r[-1]==1 and r[-2]>1
    mi=len(r)-2 if tail else len(r)-1
    P=r[:mi]; return ('C' if tail else ('A' if not P else 'B')), P
NST=214000; SPR=160; W=760; O=24; CW=1
tape=bytearray(W); p=O; q=0; rows=[]
for st in range(NST):
    t=T[(q,tape[p])]; tape[p]=t[0]; p+=t[1]; q=t[2]
    if st%SPR==0: rows.append((bytes(tape),p))
LM=230; H=len(rows)+50; Wd=LM+W*CW+20
im=Image.new('RGB',(Wd,H),'white'); dr=ImageDraw.Draw(im)
f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",13)
fs=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",12)
for y,(tp,hp) in enumerate(rows):
    Y=y+40
    for i,v in enumerate(tp):
        if v: dr.point((LM+i*CW,Y),fill=(255,165,0))
col={'A':(200,30,30),'B':(30,30,200),'C':(0,140,0)}
lasty=-99
for k,st,r in bells:
    if st>NST: break
    L,P=typ(r); Y=40+st//SPR
    if Y-lasty<13: Y=lasty+13
    lasty=Y
    pw=" ".join(map(str,P)) if P else "-"
    dr.text((8,Y-7),"%2d %s  P: %s"%(k,L,pw),font=f,fill=col[L])
    yy=40+st//SPR; dr.line([LM-6,yy,LM-1,yy],fill=col[L])
dr.text((8,8),"1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB---, steps 0-%d, time downward, %d steps per row. Bell number, type, prefix P"%(NST,SPR),font=fs,fill=(0,0,0))
im.save("m31_bell_types.png"); print(im.size)
