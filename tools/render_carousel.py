"""Render a Harpia carousel HTML (sections with class 'slide', ids s1..sN) to 1080x1350 JPEGs.
Usage: python3 tools/render_carousel.py posts/<slug>/carousel.html
Outputs posts/<slug>/01.jpg, 02.jpg ... next to the HTML."""
import asyncio, sys, pathlib, io
from PIL import Image
from playwright.async_api import async_playwright

html = pathlib.Path(sys.argv[1]).resolve()
out = html.parent

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        await pg.goto(html.as_uri())
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(600)
        slides = await pg.locator("section.slide").all()
        for i, s in enumerate(slides, 1):
            png = await s.screenshot()
            im = Image.open(io.BytesIO(png)).convert("RGB")
            assert im.size == (1080, 1350), im.size
            im.save(out / f"{i:02d}.jpg", quality=92, optimize=True)
            print(out / f"{i:02d}.jpg")
        await b.close()

asyncio.run(main())
