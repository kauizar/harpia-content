"""Render a cover scene (an HTML page with one 1080x1000 <canvas>) to PNG.
Usage: python3 tools/render_cover.py posts/<slug>/cover.html posts/<slug>/cover.png"""
import asyncio, sys, pathlib
from playwright.async_api import async_playwright
src, out = sys.argv[1], sys.argv[2]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1000})
        await pg.goto(pathlib.Path(src).resolve().as_uri())
        await pg.wait_for_timeout(1500)
        await pg.locator("canvas").screenshot(path=out)
        await b.close()
asyncio.run(main())
