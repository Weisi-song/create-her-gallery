---
name: create-her-gallery
description: Create a personalized, offline, single-file HTML gallery from a person's photos, short videos, audio, memories, and messages, including consistent cartoon transformations, three-second image animations, original-over-animation comparison clips, and licensed background music. Use when someone wants to make a poetic digital album or exhibition as a gift for a mother, partner, relative, friend, or another important woman; when personal media needs to be interviewed, curated, transformed, organized into original chapters, written into restrained poetic copy, themed, scored, validated, and exported as one locally openable HTML file.
---

# Create Her Gallery

Create a one-person exhibition from real memories. Treat every gallery as an original editorial work; never reuse another person's chapter structure merely because an example exists. Keep the default workflow local and private.

## Guided workflow

Read [references/guided-flow.md](references/guided-flow.md) and lead the user through these seven stages in order. Show only the current stage, summarize its result, and obtain approval before continuing.

1. **She and you:** ask who the gift is for, how to address her, the relationship, and the occasion.
2. **Stories:** interview for concrete memories, experiences, personality, quotations, and sensitive material.
3. **Words and structure:** read [references/writing-guide.md](references/writing-guide.md), propose 2–3 original frameworks, then draft and approve all copy.
4. **Photos:** inventory the approved photos, then follow [references/cartoon-animation.md](references/cartoon-animation.md) to approve one consistent style and create three-second original-over-animation clips. Use [references/photo-motion.md](references/photo-motion.md) only when transformation is declined.
5. **Music and background:** read [references/background-music.md](references/background-music.md) and [references/background-selection.md](references/background-selection.md). Offer uploads, the three bundled backgrounds, or three verified public candidates.
6. **Build:** choose the visual direction using [references/themes.md](references/themes.md), create [the manifest](references/gallery-format.md), follow [the romantic-stage specification](references/romantic-stage.md) when selected, validate, and build one offline HTML.
7. **Preview and revise:** open the result locally, walk through it with the user, implement a concise revision list, and repeat until approved.

## Output rules

- Produce one self-contained `.html` file by default. Do not deploy or upload it unless explicitly asked.
- Keep all selected media inside the file as data URLs. The recipient should be able to open it directly in a modern browser.
- Prefer photos and short clips. Warn above 25 MB; ask before recompressing originals, and strongly recommend a smaller delivery copy above 100 MB.
- Never autoplay music. Start it only after a clear user action.
- Embed music locally. Never stream from a remote URL, and never treat “free to listen” as permission to redistribute.
- Respect reduced-motion preferences. Keep some images still and do not animate every image with the same movement.
- Use offline-safe system fonts and no remote scripts, trackers, analytics, or network dependencies.
- Describe generated or restored imagery honestly when it is included.
- Keep one cartoon style profile across a gallery. Do not mix rendering families unless the user explicitly requests a deliberate change.
- Keep examples as editorial references only. Never copy their personal facts, names, poems, or chapter taxonomy into another gallery.
- Ask conversationally and progressively. Never present a long intake form or expose manifest fields, codecs, paths, or build commands unless the user asks.

## Bundled demo

Use `assets/demo/gallery.json` to exercise the validator and generator without private media. Treat its words and chapter structure as disposable sample content, not as a reusable life template.

When working from the source repository, `examples/feng`, `examples/hua`, and `examples/yi` provide three de-identified editorial cases. Read them only when the user asks for examples or wants to compare narrative approaches. Their media paths are local placeholders and are not included in the repository.
