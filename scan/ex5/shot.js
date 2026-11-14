const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1300,height:900},deviceScaleFactor:1.5});
 await p.goto('file:///home/claude/ex5/fig.html'); await p.screenshot({path:'/home/claude/ex5/same_table_5_286.png',fullPage:true}); await b.close();})();
