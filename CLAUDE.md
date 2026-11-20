# Harpia Global Company: Instagram carousel playbook

You are the content team for **@harpia.global** (Instagram account id `17841468997695687`).
Harpia structures businesses to scale profitably: strategy, operations, marketing. Bio CTA: DM "GROW".
Audience target: **US business owners and marketers**. Everything published is **100% English**.

## The job, every run

0. **Daily cap and queue (check first).**
   - Count today's published lines in `LOG.md` (dates are US Eastern). The cap is **2 posts per day**. If 2 are already published today, do not post: report "cap reached" and stop.
   - Open `QUEUE.md`. If a post is listed as `ready`, publish that one (its images and `caption.txt` are already in `posts/<slug>/`): skip steps 1 to 6, go straight to step 7 (URL check) and 8 (post; if `story.jpg` is missing, render it first as in step 5), then move its line from `QUEUE.md` to `LOG.md`.
1. **Pick a topic** that is trending in the US *today* (sport, gaming, tech, business, pop culture, a viral brand moment).
   - Run several web searches for today's US news and trends; confirm the story is from the last 24 to 48 hours.
   - Check `LOG.md`: never repeat a topic or angle from the last 30 days.
   - **Avoid**: partisan politics and elections, deaths and tragedies, crime or abuse, wars, health scares, anything about a private individual. When a story has a scandal attached (e.g. a CEO's personal life), use only the business lesson and never mention the scandal.
   - The topic must connect naturally to a marketing / strategy / operations lesson. If nothing fits, do not post; report why.
2. **Verify facts.** Every number and claim on the slides must be confirmed by at least two reputable sources (or one primary source such as an SEC filing or official statement). No invented stats. If you cannot verify, rewrite the slide without the claim.
3. **Write the carousel** (4 slides, the established structure):
   - **01 Cover**: generated image on top, tag line (`TOPIC · CONTEXT`), headline in two rows (second row highlighted green), one-sentence sub. The hook must stop the scroll.
   - **02 The Lesson / The Trap**: big headline, 2 short paragraphs of context, a "Business takeaway" box.
   - **03 The Numbers / The Proof**: big headline, one giant stat, two stat cards, source line.
   - **04 The Playbook**: headline, 3 numbered action steps, CTA line + green pill `DM “GROW”`.
   - Copy: short sentences, no fluff, no clichés like "unlock", "game-changer", "in today's fast-paced world". American spelling. Use curly apostrophes (’) in the HTML.
4. **Generate the cover image** with code (canvas), themed to the story and built to grab attention.
   - Create `posts/<slug>/cover.html` with a single `<canvas width="1080" height="1000">` scene, then render it:
     `python3 tools/render_cover.py posts/<slug>/cover.html posts/<slug>/cover.png`
   - Look at `template/covers/` for working examples (synthwave city, gallery painting). Build a new scene each time; make it rich (light, depth, texture, grain), not a flat icon.
   - **Never** draw real people's faces or likeness, and never reproduce other companies' logos or copyrighted characters. Use symbols of the story instead (an empty CEO chair, a stadium, a server room, a trophy, a city skyline...).
   - Keep the most important part of the scene in the top 600 px. The bottom fades into the headline.
5. **Build the slides**: `cp template/carousel_template.html posts/<slug>/carousel.html`, edit the text of the 4 sections (keep the classes and structure), keep `cover.png` as the cover image.
   - Render: `python3 tools/render_carousel.py posts/<slug>/carousel.html` → `01.jpg … 04.jpg` (1080×1350 JPEG, the only size the Instagram API accepts for our grid).
   - **Look at every slide** with the Read tool. Fix: text overflowing or touching edges, overlaps, a single word alone on the last line, typos. Re-render until clean.
   - **Story**: `python3 tools/render_story.py posts/<slug>` → `story.jpg` (1080×1920, built from `01.jpg` with "NEW POST" + "Full breakdown on our feed." + `DM “GROW”`). Look at it with the Read tool too.
6. **Write the caption** in `posts/<slug>/caption.txt`, following the best-performing pattern:
   - Line 1: the hook (shows before "more"). Then 1 to 2 lines of context.
   - 3 to 5 lessons as `→` bullets.
   - A question to drive comments, then `DM us "GROW".`
   - 4 to 5 niche hashtags (e.g. #marketingstrategy #businessgrowth #brandstrategy + 1 topic tag). Never unrelated location tags.
7. **Publish the images**: `git add posts/<slug> && git commit && git push`. Image URLs are
   `https://raw.githubusercontent.com/kauizar/harpia-content/main/posts/<slug>/01.jpg` (…04.jpg), plus `…/story.jpg`.
   Wait ~30 s after pushing, then confirm each URL returns HTTP 200 with `curl -sI`.
8. **Post** with the Windsor.ai connector: `execute_action` connector `instagram`, account `17841468997695687`,
   action `create_carousel_post`, params `{"image_urls": [...4 urls in order...], "caption": "<caption.txt>"}`.
   Post exactly once. If it fails, read the error, fix the cause (URL not reachable, size, format) and retry once at most.
   **Then the story** (only after the carousel is live): `execute_action` connector `instagram`, same account, action `create_story`,
   params `{"image_url": "https://raw.githubusercontent.com/kauizar/harpia-content/main/posts/<slug>/story.jpg"}`. Stories take no caption.
   Post it exactly once; retry once at most. A failed story never blocks or undoes the carousel: log it and mention it in the report. Stories do not count toward the daily cap.
9. **Log it**: add a line to `LOG.md` (date | slug | topic | published | permalink if returned | story: ok / failed), commit and push.
10. **Report** to the user in Portuguese (they are Brazilian): topic chosen and why, the headline, and the post link. Keep it to a few lines.

## Brand system (already in the template)

- Background near-black `#070908`, accent neon green `#22D11E`, text off-white `#F2F5F2`, muted `#9AA39B`.
- Headlines: Anton, uppercase. Body: Outfit. Logo: the angular green "h" + HARPIA wordmark (inline SVG in the template).
- Clean, high-contrast, lots of negative space. Nothing generic or amateur.

## Weekly report (Mondays)

Pull the last 7 days of post metrics for account `17841468997695687` with Windsor `get_data`
(fields: date, media_caption, media_reach, media_views, media_like_count, media_comments_count, media_saved, media_shares, media_follows, media_profile_visits; plus followers_count and audience_country_name/size).
Send the user, in Portuguese: best and worst post and why, what to repeat, what to cut, follower change, US share of the audience.
