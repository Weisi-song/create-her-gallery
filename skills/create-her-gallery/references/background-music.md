# Background music

Offer two paths: use an audio file supplied by the user, or find three current, reusable instrumental candidates online.

## User-provided audio

Ask the user to confirm that they may include and redistribute the recording. Accept MP3, M4A, OGG, or WAV, then create a delivery copy:

```bash
python3 scripts/prepare_bgm.py supplied-audio.m4a --output generated/bgm.mp3
```

Keep the original untouched. Use the prepared MP3 in the manifest.

## Publicly reusable music

Search for calm instrumental music using concrete mood terms such as gentle piano, warm acoustic, healing, quiet morning, hopeful, or soft ambient. Prefer 2–5 minute tracks without vocals so looping is unobtrusive.

1. Present three candidates with title, creator, duration, mood, exact license, attribution text, and the original item URL. Let the user listen and choose before downloading.
2. Verify the license on the individual track page at selection time. “Free,” “royalty-free,” search filters, or a library-wide description are not sufficient evidence.
3. Prefer CC0 or a clearly marked public-domain recording. CC BY is acceptable when full TASL attribution is retained. Avoid NC, ND, and SA tracks by default because future sharing or adaptation can introduce extra conditions.
4. Wikimedia Commons and Free Music Archive contain files with different per-item licenses; verify each item. Musopen itself warns that composition and recording rights can differ and asks reusers to assess each recording. Pixabay permits music inside a larger creative project rather than as a standalone file; retain the track page and license evidence.
5. Save a local text note or screenshot containing the item URL, download date, creator, title, license, license URL, and required attribution. Download only the chosen track from its official item page.
6. Run `scripts/prepare_bgm.py`, then add the prepared local MP3 and license metadata to the manifest.

Useful primary references:

- Creative Commons reuse and TASL: https://creativecommons.org/reusing-cc-licensed-content/
- CC0: https://creativecommons.org/publicdomain/zero/1.0/
- Wikimedia Commons reuse: https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia/en
- Free Music Archive license guide: https://freemusicarchive.org/License_Guide
- Musopen copyright FAQ: https://musopen.org/faq/
- Pixabay Content License: https://pixabay.com/service/license-summary/

## Manifest metadata

For user-provided audio:

```json
{
  "src": "generated/bgm.mp3",
  "label": "播放相册音乐",
  "origin": "user-provided"
}
```

For an online library track:

```json
{
  "src": "generated/bgm.mp3",
  "label": "播放相册音乐",
  "origin": "public-library",
  "title": "Track title",
  "creator": "Artist name",
  "license": "CC BY 4.0",
  "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
  "sourceUrl": "https://original.example/item",
  "attribution": "Track title — Artist name · CC BY 4.0"
}
```

Keep `attribution` concise enough for the closing card, but retain full evidence in the working folder.
