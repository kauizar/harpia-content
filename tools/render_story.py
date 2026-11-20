"""Render the Instagram story (1080x1920 JPEG) that announces a carousel post.
Usage: python3 tools/render_story.py posts/<slug>
Needs posts/<slug>/01.jpg (the rendered cover slide). Copies template/story_template.html
to posts/<slug>/story.html if it is not there yet, then writes posts/<slug>/story.jpg."""
import asyncio, sys, pathlib, io, shutil
from PIL import Image
from playwright.async_api import async_playwright

root = pathlib.Path(__file__).resolve().parent.parent
post = pathlib.Path(sys.argv[1]).resolve()
assert (post / "01.jpg").exists(), f"missing {post / '01.jpg'}: render the carousel first"
html = post / "story.html"
if not html.exists():
    shutil.copy(root / "template" / "story_template.html", html)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        await pg.goto(html.as_uri())
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(600)
        png = await pg.locator("section.story").screenshot()
        im = Image.open(io.BytesIO(png)).convert("RGB")
        assert im.size == (1080, 1920), im.size
        im.save(post / "story.jpg", quality=92, optimize=True)
        print(post / "story.jpg")
        await b.close()

asyncio.run(main())
