const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1500,height:800},deviceScaleFactor:1.5});
 await p.goto('file:///home/claude/vtab/vamp.html'); await p.screenshot({path:'/home/claude/vtab/vampire_like_tms.png',fullPage:true}); await b.close();})();
