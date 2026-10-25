from PIL import Image, ImageDraw, ImageFont
M="1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE".split("_")
T={}
for i,s in enumerate(M):
    for b in range(2):
        x=s[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
NST=26400; SPR=20; CW=6; W=104; O=62
labels="ABABABABABABABABCAB"  # bands 1..19 (from the band map)
tape=[0]*W; p=O; q=0; d0=1; phase=0
rows=[]; starts=[]; lo=O
for st in range(NST):
    t=T[(q,tape[p])]; tape[p]=t[0]; d=t[1]; p+=d; q=t[2]
    if d0==1 and d==-1:   # turn at the right end: the state tells the phase
        phase={4:1,2:2,3:3}.get(q,phase)
    d0=d
    if p<lo:
        lo=p
        if q==2: starts.append((st+1,p)); phase=1
    if st%SPR==0: rows.append((tape[:],p,phase))
LM=150; RM=250; H=len(rows)+60; Wd=LM+W*CW+RM
im=Image.new('RGB',(Wd,H),'white'); dr=ImageDraw.Draw(im)
f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",15)
fs=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",12)
PC={0:(200,200,200),1:(150,150,150),2:(70,130,220),3:(60,170,90)}
xmax=0
for y,(tp,hp,ph) in enumerate(rows):
    Y=y+40
    for i,v in enumerate(tp):
        if v: dr.rectangle([LM+i*CW,Y,LM+i*CW+CW-1,Y],fill=(255,165,0))
        if v: xmax=max(xmax,i)
    dr.rectangle([LM+W*CW+12,Y,LM+W*CW+26,Y],fill=PC[ph])
for k,(s,pos) in enumerate(starts[:19]):
    Y=40+s//SPR; x=LM+pos*CW
    dr.line([x-6,Y,LM+W*CW,Y],fill=(120,120,120),width=1) if False else None
    lab=labels[k]; col={'A':(200,30,30),'B':(30,30,200),'C':(0,140,0)}[lab]
    dr.text((x-62,Y-2),"%2d %s"%(k+1,lab),font=f,fill=col)
dr.text((10,8),"1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE, steps 0-%d (time downward, %d steps per row)"%(NST,SPR),font=fs,fill=(0,0,0))
lx=LM+W*CW-40; ly=60
lx=LM+W*CW+40; ly=50
dr.text((lx,ly),"phase bar:",font=fs,fill=(0,0,0))
for i,(ph,t) in enumerate(((1,"1: (01)^a -> 11^a"),(2,"2: dome"),(3,"3: parallelogram"))):
    dr.rectangle([lx,ly+20+i*18,lx+14,ly+32+i*18],fill=PC[ph]); dr.text((lx+20,ly+19+i*18),t,font=fs,fill=(0,0,0))
for i,t in enumerate(["A: b/3 < a <= b","B: a > b","C: a < b/3 (no phase 3)","","a, b: blocks (01)^a, (11)^b","at the start of the Bell"]):
    dr.text((lx,ly+90+i*16),t,font=fs,fill={0:(200,30,30),1:(30,30,200),2:(0,140,0)}.get(i,(0,0,0)))
im.save("m10_bell_types.png"); print(im.size, starts[16:19])
