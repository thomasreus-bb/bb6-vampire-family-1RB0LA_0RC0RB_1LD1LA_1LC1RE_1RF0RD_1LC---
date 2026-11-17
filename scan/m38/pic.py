from PIL import Image, ImageDraw, ImageFont
TM="1RB0RE_1LC0RA_0LD0LB_1RE0LB_1RF---_0RB0RC"
S='ABCDEF';T={}
for i,g in enumerate(TM.split('_')):
    for b in (0,1):
        x=g[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,S.index(x[2]))
N=500000; LO,HI=-30,1700; ROWS=700; W=HI-LO
ev={4217:(31,'1100'),27707:(81,'1100'),176743:(206,'0100'),204837:(99,'1100'),424975:(248,'0100'),465865:(121,'1100')}
img=Image.new('RGB',(W,ROWS),'white'); px=img.load()
tape=bytearray(W); p=-LO; q=0; per=N//ROWS
for st in range(N):
    if st%per==0:
        r=st//per
        if r<ROWS:
            for x in range(W):
                if tape[x]: px[x,r]=(255,165,0)
            px[p,r]=(0,0,0)
    b=tape[p]; w,d,q2=T[(q,b)]; tape[p]=w; p+=d; q=q2
img=img.resize((W,ROWS*2))
big=Image.new("RGB",(W+380,ROWS*2+40),'white'); big.paste(img,(0,40)); dr=ImageDraw.Draw(big)
try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
except: f=None
dr.text((5,5),'no. 38, steps 0 - 500,000 (time downwards, linear), tape cells -30 ... 1700',fill='black',font=f)
for st,(j,X) in ev.items():
    y=40+st*2//per; col=(220,0,0) if X=='0100' else (0,90,220)
    dr.line([(0,y),(W,y)],fill=col,width=1)
    dr.text((W+5,y-8),'step %d: j=%d, X=%s%s'%(st,j,X,'  (level end)' if X=='0100' else ''),fill=col,font=f)
big.save('/tmp/m38/levels38.png')
