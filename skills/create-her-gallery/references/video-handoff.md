# External video handoff

Use this route when integrated image-to-video generation is unavailable, credentials are missing, or the user prefers another tool. Keep the project moving by preparing a complete handoff, then resume after the user returns the videos.

## Prepare the jobs

Create one UTF-8 JSON file in the private working folder:

```json
{
  "style": "approved shared cartoon style",
  "duration": 3,
  "sharedConstraints": "Keep identity, composition, clothing, hands, person count, and background stable. No text, watermark, lip-sync, large gesture, morphing, or new objects.",
  "items": [
    {
      "id": "01",
      "original": "private/original-01.jpg",
      "cartoon": "working/cartoon-01.png",
      "prompt": "Use image 01 as the only first-frame and identity reference. She blinks once and breathes gently while a light breeze moves a few strands of hair. Fixed camera, exactly three seconds."
    }
  ]
}
```

Keep `original` local for later composition. Write a distinct prompt for every picture based on what can move naturally in that scene. Reuse the shared style and stability constraints, not an identical generic action.

## Export the handoff

Run:

```bash
python3 scripts/prepare_video_handoff.py prepare video-jobs.json \
  --output video-handoff
```

Give the user the resulting folder. It contains only numbered cartoon images, `prompts.md`, and `handoff.json`; it never copies originals. Tell the user to:

1. upload each numbered cartoon image to any image-to-video tool;
2. paste the matching prompt without combining jobs;
3. disable automatic dialogue, subtitles, logos, and music when possible;
4. export MP4 and keep the requested return name, such as `01.mp4`;
5. send all returned videos back together.

Do not claim that one provider-specific setting works everywhere. If a tool cannot output exactly three seconds, accept a longer clip and select its most stable three-second window later.

## Resume after return

Save returned clips in one folder and run:

```bash
python3 scripts/prepare_video_handoff.py check video-jobs.json \
  --returned-dir returned-videos
```

Resolve missing, unreadable, or shorter-than-three-second clips. Visually reject identity drift, face or hand morphing, new people or objects, unintended lip-sync, unstable backgrounds, and large camera motion. Ask the user to regenerate only the failed IDs.

For each accepted clip, place the untouched original above the animation:

```bash
python3 scripts/compose_photo_pair.py private/original-01.jpg returned-videos/01.mp4 \
  --animation-start 0.8 \
  --output generated/01-pair.mp4
```

Use `--animation-start 0` for an exact three-second return. Keep the job JSON private because it may contain local paths; the exported package is the only folder intended for an external tool.
