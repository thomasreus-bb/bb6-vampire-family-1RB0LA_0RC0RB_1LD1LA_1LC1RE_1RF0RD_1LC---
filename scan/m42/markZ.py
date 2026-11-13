# Mark the Z events of no. 42 in its space-time diagram (same run as scan/viz.c: 1,076,279 steps, 700 rows).
import sys
from PIL import Image, ImageDraw, ImageFont
TM='1RB0RF_1LC0RA_1LD1LB_0LE---_1LA0LA_1RE1LD'
T={}
for i,g in enumerate(TM.split('_')):
    for b in (0,1):
        x=g[3*b:3*b+3]; T[('ABCDEF'[i],b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,x[2])
STEPS=1076279; ROWS=700
t={}; p=0; q='A'; lo=0; hi=0; Z=[]
for n in range(1,STEPS+1):
    w,d,q2=T[(q,t.get(p,0))]; t[p]=w; p+=d; q=q2
    if p>hi: hi=p
    if p<lo:
        lo=p
        if q=='A' and t.get(p+1,0)==0 and t.get(p+2,0)==0:
            # tape 00 (10)^c 1^e
            i=p+3; c=0
            while t.get(i,0)==1 and t.get(i+1,0)==0 and i+1<=hi: c+=1; i+=2
            e=0
            while t.get(i,0)==1: e+=1; i+=1
            if i>hi: Z.append((n,p,c,e))
lo1=lo
print('final lo',lo1,'hi',hi,'Z events',Z)
im=Image.open(sys.argv[1]).convert('RGB')
W,H=im.size
TOP=44
out=Image.new('RGB',(W+330,H+TOP),'white'); out.paste(im,(0,TOP))
dr=ImageDraw.Draw(out)
try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15); fb=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15)
except: font=fb=ImageFont.load_default()
red=(200,0,0)
ly=34
dr.text((W+12,6),'Z(c, e) = tape 00 (10)^c 1^e',fill=(0,0,0),font=fb)
lab={1:(0,4),2:(-70,4),3:(-70,22)}
for k,(n,pp,c,e) in enumerate(Z,1):
    r=round(n*(ROWS-1)/STEPS)+TOP; x=pp-lo1
    dr.ellipse((x-7,r-7,x+7,r+7),outline=red,width=3)
    label='Z%d'%k
    if r<TOP+40:
        dx,yy=lab.get(k,(0,4)); tx=x+dx-10; ty=yy
        dr.line((x,r-7,tx+12,ty+16),fill=red,width=1)
    else:
        tx,ty=x+10,r-9
    dr.text((tx+2,ty),label,fill=red,font=fb)
    dr.text((W+12,ly),'%s: step %s, c = %d, e = %d'%(label,format(n,','),c,e),fill=red,font=font); ly+=22
out.save(sys.argv[2])
