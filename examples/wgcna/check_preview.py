"""Check delivered offline page and save desktop/mobile previews."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent
reports=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for name,width in [('desktop',1280),('mobile',390)]:
        page=browser.new_page(viewport={'width':width,'height':1000},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda error: errors.append(str(error)))
        page.goto((root/'preview.html').as_uri(),wait_until='load')
        page.locator('img').evaluate_all('(imgs)=>imgs.forEach(i=>i.loading="eager")')
        page.wait_for_function('Array.from(document.images).every(i=>i.complete && i.naturalWidth>0)')
        result=page.evaluate('''()=>({headings:Array.from(document.querySelectorAll('h2')).map(x=>x.textContent),images:document.images.length,loaded:Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0),overflow:document.documentElement.scrollWidth>innerWidth})''')
        assert result['headings']==['定义解释','分析原理','分析操作','适用范围','参考与致谢']
        assert result['images']==8 and result['loaded'] and not result['overflow'] and not errors
        page.screenshot(path=str(root/f'preview-{name}.png'),full_page=True)
        reports.append({'viewport':width,**result,'javascript_errors':errors})
        page.close()
    browser.close()
(root/'preview-checks.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(reports,ensure_ascii=False))
