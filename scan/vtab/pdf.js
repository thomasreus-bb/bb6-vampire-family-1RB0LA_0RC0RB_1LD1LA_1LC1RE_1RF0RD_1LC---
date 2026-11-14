const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1500,height:800}});
 await p.goto('file:///home/claude/vtab/vamp.html');
 await p.addStyleTag({content:'@page{margin:0} html,body{background:#000;-webkit-print-color-adjust:exact;print-color-adjust:exact} tr{break-inside:avoid}'});
 const h=await p.evaluate(()=>document.documentElement.scrollHeight);
 await p.pdf({path:'/home/claude/vtab/vampire_like_tms.pdf',width:'1500px',height:(h+2)+'px',printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});
 await p.screenshot({path:'/home/claude/vtab/vampire_like_tms.png',fullPage:true});
 await b.close();})();
