# Cartoon comparison pipeline

Use this pipeline for every selected source photo unless the user explicitly opts out.

## 1. Lock one style

Offer 2–3 directions, then select exactly one for the gallery. A user may describe the direction as “吉卜力风格” or “皮克斯风格”; translate that shorthand into a concrete visual profile such as hand-painted Japanese fantasy animation or polished 3D family-film animation. Do not add recognizable copyrighted characters, studio logos, or claim official affiliation.

Create a local style note containing:

- rendering medium, palette, lighting, texture, facial proportions, and background treatment;
- identity anchors for each recurring person: apparent age, face shape, hairstyle, glasses, clothing, and distinctive details;
- a shared negative prompt covering identity drift, altered age or body shape, extra people or limbs, text corruption, and changed meaningful objects;
- the approved first cartoon image to reuse as a style reference when the provider supports image references.

Generate only 1–2 representative cartoon stills first. Ask the user to approve identity, emotional tone, and style consistency before processing the rest.

## 2. Cartoonize the photo

- Preserve person count, composition, pose, clothing, age, skin tone, face identity, and meaningful background objects.
- Use the same style profile, reference image, aspect ratio, and generation settings throughout one gallery.
- For group photos, verify every face separately. Reject missing, merged, duplicated, or invented people.
- Save the approved cartoon still locally beside the working assets.

Personal photos may be sensitive. Name the external provider and obtain explicit approval immediately before uploading. If the user declines, retain the original locally and use CSS-only motion instead.

## 3. Create a three-second animation

Animate the approved cartoon still, not the original photo. Target exactly 3 seconds at 24 or 30 fps. Prefer restrained movement: blinking, breathing, a slight smile, hair or clothing moving in a breeze, or a very slow camera push. Keep the camera, face, body, hands, person count, clothing, and important objects stable. Reject morphing, lip-sync without a request, large gestures, identity drift, or invented scene events.

Use an integrated image-to-video provider only after naming it and obtaining approval to upload the cartoon stills. If no provider or credentials are available, or the user prefers another app, do not block the gallery and do not substitute unexplained static zooms. Follow [video-handoff.md](video-handoff.md), give the user every approved cartoon still with its own motion prompt, and resume composition when the rendered clips return.

## 4. Compose the comparison

Place the untouched original photo on top and the three-second cartoon animation below. Preserve both full compositions with contained scaling and matching panel sizes; do not crop heads merely to fill the frame.

Run:

```bash
python3 scripts/compose_photo_pair.py original.jpg cartoon-animation.mp4 \
  --output generated/original-cartoon-pair.mp4
```

When an external tool returns a longer clip, choose a stable three-second window and pass its start time with `--animation-start`.

The default output is a silent 720×1080, 30 fps, three-second H.264 MP4. Use the resulting MP4 as the chapter media `src`. The romantic template will autoplay it muted and advance when it ends.

## 5. Review the batch

Check every comparison clip for:

- one consistent rendering family across all cartoon panels;
- recognizable faces, correct person count, hands, clothes, and key objects;
- original on top and animation below, with no clipped heads;
- 3.0-second duration, 720×1080 output, smooth playback, and no audio;
- honest captioning when the animation materially invents motion.
