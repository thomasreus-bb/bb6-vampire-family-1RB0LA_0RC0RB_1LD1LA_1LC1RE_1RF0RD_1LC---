X='1RB1LD_1LC0RF_0RD0LB_1LB0LE_1LA---_0RA0RF'; Y='1RB0RD_1RC0LF_0LA0RB_1RE---_1LB1RA_0LE0LF'
P={'A':'E','B':'B','C':'C','D':'A','E':'D','F':'F'}
S='ABCDEF'
def cells(t):
    g=t.split('_'); return {S[i]:(g[i][:3],g[i][3:]) for i in range(6)}
cx,cy=cells(X),cells(Y)
def fmt(c,hl=False):
    if c=='---': return '<span class="h">---</span>'
    w,d,s=c
    return '%s<span class="d">%s</span><span class="s">%s</span>'%(w,d,s)
rows=[]
for q in S:
    q2=P[q]
    st5=' <span class="tag">start #5</span>' if q=='A' else (' <span class="tag t2">start #286</span>' if q=='D' else '')
    rows.append('<tr><td class="q">%s%s</td><td>%s</td><td>%s</td><td class="arr">→</td><td class="q">%s</td><td>%s</td><td>%s</td></tr>'%(q,st5,fmt(cx[q][0]),fmt(cx[q][1]),q2,fmt(cy[q2][0]),fmt(cy[q2][1])))
h='''<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;background:#000;color:#e8e8e8;font:15px/1.4 "DejaVu Sans",Arial,sans-serif}
.wrap{padding:20px 24px;width:1250px}
h1{font-size:20px;margin:0 0 6px;color:#fff} p{margin:4px 0 10px;color:#bbb;font-size:14px}
table{border-collapse:collapse;font-family:"DejaVu Sans Mono",monospace;font-size:16px}
th{color:#fff;padding:5px 12px;border-bottom:2px solid #555;font-family:"DejaVu Sans",Arial;font-size:14px}
td{padding:5px 12px;border-bottom:1px solid #333;text-align:center}
td.q{color:#fff;font-weight:bold;text-align:left} td.arr{color:#888}
.d{color:#5fb3ff;font-weight:bold} .s{color:#fff} .h{color:#ff6b6b}
.tag{font:11px "DejaVu Sans";background:#3fbf3f;color:#000;border-radius:3px;padding:1px 4px;margin-left:4px} .t2{background:#f2c200}
.figs{display:flex;gap:30px;margin-top:18px} .fig{color:#bbb;font-size:13px} .fig img{display:block;border:1px solid #333;margin-top:4px;background:#fff}
</style></head><body><div class="wrap">
<h1>Same table, other start: Holdout Guide #5 and #286</h1>
<p>#286 is #5 with the states renamed (A→E, D→A, E→D; B, C, F unchanged) and mirrored (L ↔ R, in blue). Its start state A is state D of #5. So #286 is the same machine as #5, started in D, with the tape mirrored.</p>
<table><tr><th>#5</th><th>0</th><th>1</th><th></th><th>#286</th><th>0</th><th>1</th></tr>
%s</table>
<div class="figs">
<div class="fig">#5 from the blank tape (start A), first 169,474 steps<img src="d5.png" width="601"></div>
<div class="fig">#286 from the blank tape (start A = state D of #5), first 167,550 steps<img src="d286.png" width="601"></div>
</div>
<p style="margin-top:12px">Guide status of both: <b style="color:#fff">Some structure seen</b> (“Experiments show a pattern, but no exact rules yet”), class <b style="color:#fff">Bouncer + Chaotic Edge</b>: a regular bouncer (the growing triangle with a periodic texture) next to an irregular edge that does not repeat (the vertical stripes at the left in #5, at the right in #286, since the tape is mirrored). Each row is the tape after more steps, time runs downwards.</p>
</div></body></html>'''%'\n'.join(rows)
open('fig.html','w').write(h)
