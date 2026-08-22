# Background selection

Offer these bundled presets with visual previews:

- `preset:star-meadow` — playful green lawn, pink slope, and scattered stars; bright, nostalgic, and whimsical.
- `preset:sunlit-valley` — luminous illustrated valley, blue sky, river, and flowers; open, hopeful, and vivid.
- `preset:teal-sky` — quiet teal sky with clouds, stars, white birds, and a small trumpet player; dreamy and reflective. The bundled copy removes the source screenshot's account and phone UI area.

List preset ids with:

```bash
python3 scripts/build_gallery.py --list-backgrounds
```

The user may instead upload a background. Inspect its readability behind the translucent card and prepare a compressed delivery copy without changing the original.

If neither path fits, find three currently reusable online candidates. Verify the license on each individual item page, favor CC0/public-domain or CC BY material, and show creator, exact license, source URL, and preview before download. Never use an image merely because it appears in search results. Store public-source metadata under `backgroundMeta` so the closing page can show attribution.
