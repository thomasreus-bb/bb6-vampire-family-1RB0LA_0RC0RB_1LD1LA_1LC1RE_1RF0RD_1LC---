from rows import rows
import html
def code(c):
    p=c.split('_'); return '<br>'.join('_'.join(p[i:i+2]) for i in range(0,6,2))
css='''body{margin:0;background:#000;color:#e8e8e8;font:15px/1.35 "DejaVu Sans",Arial,sans-serif}
.wrap{padding:22px 24px}
h1{font-size:21px;margin:0 0 4px;color:#fff} .sub{color:#aaa;font-size:13px;margin-bottom:14px}
table{border-collapse:collapse;width:100%}
th{background:#1c1c1c;color:#fff;text-align:left;padding:8px 9px;border-bottom:2px solid #555;font-size:14px;vertical-align:bottom}
td{padding:7px 9px;border-bottom:1px solid #333;vertical-align:top}
td.m{font-family:"DejaVu Sans Mono",monospace;font-size:13.5px;white-space:nowrap;color:#fff}
.lab{font-family:"DejaVu Sans",Arial;font-size:12.5px;color:#bbb;white-space:normal}
.dot{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.g .dot{background:#3fbf3f} .y .dot{background:#f2c200}
tr.y td{background:#0d0d0d}
b{color:#fff} .n{white-space:nowrap}
.foot{color:#999;font-size:12.5px;margin-top:10px}'''
tr=[]
for col,c,lab,typ,st,exp,tm,steps in rows:
    tr.append('<tr class="%s"><td class="m"><span class="dot"></span><span style="display:inline-block;vertical-align:top">%s%s</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class="n">%s</td></tr>'%(
        col,code(c),'<div class="lab">'+lab+'</div>' if lab else '',typ,st,exp,tm,steps))
h='''<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body><div class="wrap">
<h1>Vampire-like BB(6) machines</h1>
<div class="sub">Bell map driven by the digits of one large number and a short word or tail; a HALT needs a certain sequence of residues (“lottery”). Expected values: Markov estimate with random residues (heuristic, not a proof). Green = HALT found, yellow = open. Status of 14 Nov 2026.</div>
<table><colgroup><col style="width:205px"><col style="width:15%%"><col style="width:20%%"><col style="width:15%%"><col style="width:17%%"><col></colgroup>
<tr><th>machine</th><th>type</th><th>status</th><th>expected HALT (Markov)</th><th>computing time to HALT</th><th>steps of the original TM</th></tr>
%s</table>
<div class="foot">Thomas Reus with Claude (Anthropic) · github.com/thomasreus-bb</div></div></body></html>'''%(css,'\n'.join(tr))
open('vamp.html','w').write(h)
