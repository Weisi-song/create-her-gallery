# Photo motion

## Offline motion

Use restrained CSS motion in the generated HTML so still images feel alive without leaving the device:

- `slow-zoom`: move slowly toward the subject; use for portraits and quiet detail.
- `drift-left`: reveal context from right to left; use for landscapes or groups whose action leads left.
- `drift-right`: reveal context from left to right.
- `breathe`: use a very small scale pulse for objects, flowers, letters, and abstract images.
- `none`: preserve stillness when motion would trivialize the image.

Choose motion according to composition. Alternate movement across a chapter and avoid animating every image. Always honor `prefers-reduced-motion`.

In `romantic-stage`, still images advance automatically after 6.5 seconds by default. Set `duration` to 2–30 seconds when a dense image needs more reading time. Clicking the media pauses or resumes both the timer and its CSS motion.

Keep the shared 2:3 media viewport, but preserve the full subject with `object-fit: contain`. Use `cropScale` and `cropY` only for clear outliers, after inspection. Prefer a little surrounding space over cutting off a head, hand, caption, or meaningful object.

## AI image-to-video fallback

For the standard cartoon comparison pipeline, use [cartoon-animation.md](cartoon-animation.md). Use the fallback below only when the user wants a different form of motion.

1. Select only images that benefit from real scene movement.
2. Explain that the selected images must be sent to an external generation provider.
3. Obtain explicit approval before uploading them.
4. Ask for intended movement and prohibited changes, especially faces, body shape, clothing, age, and background people.
5. Generate short, restrained clips. Reject identity drift, extra limbs, invented people, or changes to meaningful objects.
6. Save approved clips locally and reference them as ordinary video media in the manifest.
7. If a clip materially invents motion rather than reconstructing it, label it as AI-generated in its caption.
