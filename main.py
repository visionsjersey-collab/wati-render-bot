import asyncio, json, time
from playwright.async_api import async_playwright
from aiohttp import web

INBOX_URL = "https://live.wati.io/1037246/teamInbox/"
CHECK_INTERVAL = 180  # seconds (3 min)

async def run_wati_bot():
    while True:
        try:
            print("🌐 Launching WATI automation...")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(storage_state="storageState.json")
                page = await context.new_page()
                await page.goto(INBOX_URL)
                await page.wait_for_timeout(8000)
                print("✅ WATI Inbox loaded")

                # check for unread
                unread_count = await page.evaluate("""
                    () => {
                        let el = document.querySelector('[data-testid="teamInbox-leftSide-filterBar-filter-dropdown-unreadCount"]');
                        if (!el) return 0;
                        return parseInt(el.innerText.replace(/\\D/g,'')) || 0;
                    }
                """)
                print(f"📬 Unread count: {unread_count}")

                if unread_count > 0:
                    print("🚀 Triggering chatbot flow...")
                    await page.click('[data-testid="teamInbox-leftSide-filterBar-filter-dropdown-unreadCount"]', timeout=10000)
                    await page.wait_for_timeout(2000)
                    # add your exact click to bot flow element here if needed

                await browser.close()

        except Exception as e:
            print(f"⚠️ Error: {e}")
            print("🔄 Restarting in 30 seconds...")
            await asyncio.sleep(30)
            continue

        print(f"😴 Sleeping for {CHECK_INTERVAL/60:.1f} minutes...")
        await asyncio.sleep(CHECK_INTERVAL)

async def start_web_server():
    async def handle(request):
        return web.Response(text="WATI bot active ✅")
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

async def main():
    await asyncio.gather(run_wati_bot(), start_web_server())

if __name__ == "__main__":
    asyncio.run(main())
