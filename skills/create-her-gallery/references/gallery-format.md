# Gallery manifest format

Store one UTF-8 JSON manifest beside, or near, its media. Resolve media paths relative to the manifest file.

```json
{
  "slug": "nickname",
  "displayName": "昵称",
  "title": "展览标题",
  "subtitle": "一句简短引语",
  "layout": "romantic-stage",
  "theme": "moonlit-letter",
  "preface": "序言，可使用换行",
  "background": "preset:star-meadow",
  "music": {
    "src": "relative/music.mp3",
    "label": "背景音乐",
    "origin": "user-provided"
  },
  "chapters": [
    {
      "title": "章节标题",
      "kicker": "可选的章节眉题",
      "text": "章节正文，可使用换行",
      "media": [
        {
          "src": "generated/original-cartoon-pair.mp4",
          "alt": "上方为原始照片，下方为统一风格的三秒卡通动画",
          "caption": "可选说明",
          "cropScale": 1,
          "cropY": "0%"
        }
      ]
    }
  ],
  "dedication": "结尾献词，可使用换行"
}
```

## Constraints

- Use a lowercase ASCII `slug` containing letters, digits, and hyphens.
- Use 1–12 chapters and at least one media item in the complete gallery.
- Support JPEG, PNG, GIF, WebP, AVIF, MP4, MOV, WebM, MP3, M4A, OGG, and WAV.
- Use `moonlit-letter`, `summer-film`, `forest-specimen`, or `cosmic-stage` for `theme`.
- Use `romantic-stage` for the page-by-page story experience, `classic-card` for the old centered-card experience, or `editorial-scroll` only when the user explicitly chooses a scrolling exhibition.
- For `classic-card`, optional `labels` may define `loading`, `enterHome`, `start`, `finish`, and `restart`; optional `appearance` may define `maskOpacity`, `backdropBlur`, and `backgroundMotion`.
- Omit `background` or `music` when not needed.
- Use `preset:star-meadow`, `preset:sunlit-valley`, or `preset:teal-sky` for a bundled background, or provide a local image path.
- Write useful `alt` text for images. For decorative images, use an empty string deliberately.
- Use `none`, `slow-zoom`, `drift-left`, `drift-right`, or `breathe` for optional still-image `motion`. Motion has no effect on video.
- Use optional `duration` (2–30 seconds) to control how long a still image remains before the next media item. The default is 6.5 seconds.
- Use optional `cropScale` (1–2.5) and `cropY` (`-50%` to `50%`) only after visually checking the result. Start at `1` and `0%`; never crop a face merely to force identical framing.
- Put only images in `background`, only audio in `music.src`, and only images or videos in chapter `media`.
- Set `music.origin` to `user-provided` or `public-library`. For public-library music, also include `title`, `creator`, `license`, `licenseUrl`, `sourceUrl`, and `attribution`; the templates display the attribution on the closing page.
- For a public-library background, add `backgroundMeta` with `origin: public-library` plus `title`, `creator`, `license`, `licenseUrl`, `sourceUrl`, and `attribution`.
- For a transformed photo, put the final three-second comparison MP4 in `src`; keep the source photo, approved cartoon still, prompts, and generation notes in the working folder rather than embedding their local paths in the final manifest.
