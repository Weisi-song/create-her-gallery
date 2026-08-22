# Romantic stage interaction

Use this specification for `layout: romantic-stage`.

## Reading sequence

1. Reveal the preface card, then let each line emerge with a soft blur-to-sharp transition. Keep the stagger close enough that the page never feels stalled.
2. Reveal chapter text line by line. A click anywhere on the chapter card must immediately reveal the full text and enter the media phase; do not show a separate “显示全文” control.
3. Play chapter media sequentially. Autoplay muted video and advance when it ends. Show a still image with its assigned CSS motion, then advance after its `duration`.
4. Let a click on the media pause or resume the current video. For a still image, pause or resume both its motion and countdown.
5. Show a small circular replay icon only after the sequence finishes. Use a glowing folded lower-right corner to advance; do not add text buttons for replay or the next chapter.

## Visual treatment

- Keep the original background recognizable. Use a centered card with `rgba(255,255,255,.46)`, a light white edge, no backdrop blur, and dark readable body text.
- Keep title and body scale balanced. On mobile, favor roughly 1.5–1.95 rem chapter titles and 1.02–1.16 rem body text.
- Use the current chapter name plus clickable progress dots in the top bar.
- Give all chapter media the same 2:3 viewport. Use a softly blurred duplicate behind video or photography to fill unused space while the main media remains `contain` by default.
- Allow the mobile chapter page to scroll vertically whenever text and media do not fit in one viewport. Reset scroll position on page changes.
- On pointer clicks, emit small deep- and light-gold stars that drift and extinguish in sequence. Do not use expanding ripple rings.

## Safety rails

- Start background music only after an explicit button click.
- Honor `prefers-reduced-motion` by revealing text immediately and disabling decorative or photographic motion.
- Inspect every manual crop. Preserve heads, hands, signs, captions, and other meaningful details.
