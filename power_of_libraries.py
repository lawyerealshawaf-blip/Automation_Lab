import asyncio
import time
from prisma import Prisma
import playwright.async_api as pw

async def lab_test():
    # الاتصال المباشر بقاعدة بيانات المختبر
    db = Prisma(datasource={"url": "file:./prisma/dev.db"})
    await db.connect()
    
    async with pw.async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("🚀 بدء التشغيل التجريبي في المختبر...")
        
        try:
            # مثال لزيارة موقع (اختياري للتجربة)
            await page.goto("https://google.com", timeout=60000)
            title = await page.title()
            
            # حفظ النتيجة في قاعدة البيانات المحلية
            new_entry = await db.case.create(
                data={
                    'title': f"تجربة مختبر: {title}",
                    'description': "تم الاستخراج بنجاح من داخل Automation_Lab",
                    'status': "LAB_SUCCESS",
                    'caseNumber': f"LAB-{int(time.time())}"
                }
            )
            print(f"✅ تم الحفظ بنجاح! معرف السجل: {new_entry.id}")
            
        except Exception as e:
            print(f"⚠️ حدث خطأ: {e}")
        finally:
            await browser.close()
            
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(lab_test())
