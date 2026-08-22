# Create Her Gallery

把一个人的照片与故事，做成送给她的诗意影像相册。

Create Her Gallery 是一个面向 Codex 的创作 Skill。它不会一上来要求你填写复杂表单，而是像一位策展编辑一样，一步步询问她是谁、你们经历过什么，再共同确定文字、章节、卡通画风、动画、音乐和背景，最后导出一个可以离线打开与直接转发的单文件 HTML。

> 照片、视频、故事和音乐默认只在本地处理，不需要上传到网站。

> 这是我的独立项目。我独立完成了访谈流程、内容策展方法、交互与模板设计、构建脚本、隐私规则和示例案例。

## 为什么做

给一个重要的人制作数字礼物时，最难的通常不是把照片放进网页，而是决定“应该怎样讲她的故事”。固定模板很容易把不同的人生压成同一种叙事，单纯的照片轮播又无法表达关系、记忆和送礼者真正想说的话。

因此我把它做成一个会先访谈、再策展的 Skill。它先帮助用户梳理人物、关系、经历和原话，再提出不同的叙事结构；确认方向后，才进入文字、图像、动画、音乐和页面制作。技术生成被放在故事之后，而不是反过来。

## 最终会得到什么

- 一份为具体的人重新构思、而不是套用固定人生模板的诗相册
- 同一画风的照片卡通化效果，例如温柔手绘感或 3D 动画电影感
- 每张照片约 3 秒的轻动画，并与原图上下组合呈现
- 没有可用视频生成工具时，导出全部卡通图与逐张 prompt；用户可在其他工具生成后发回 MP4，继续完成相册
- 会逐句浮现、自动播放影像、支持翻页与重看的浪漫交互
- 自己上传的音乐，或许可和署名信息清晰的公开音乐
- 三种内置背景，也可以换成自己的图片
- 一个不依赖服务器的 HTML 文件，下载后即可保存、打开和发送

## 全流程

1. **认识她**：确认如何称呼、你们的关系和送礼场合。
2. **听故事**：收集重要经历、性格、原话和彼此的记忆。
3. **写成展览**：提出 2–3 种专属叙事框架，确认后再完成文字。
4. **制作影像**：选择一种统一卡通风格，为照片制作约 3 秒动画。
5. **选择氛围**：上传音乐，或选择许可清晰的公开音乐与背景。
6. **生成相册**：把所有内容嵌入一个离线 HTML。
7. **预览修改**：在电脑和手机尺寸下检查，修改到满意为止。

## 安装

### 直接放入 Codex Skills

克隆仓库后，将 Skill 文件夹复制到你的 Codex Skills 目录：

```bash
git clone https://github.com/Weisi-song/create-her-gallery.git
cp -R create-her-gallery/skills/create-her-gallery ~/.codex/skills/
```

重新打开 Codex 后即可使用 `$create-her-gallery`。

也可以不安装，直接让 Codex 读取仓库中的 `skills/create-her-gallery/SKILL.md`。

## 怎么开始

对 Codex 说：

```text
请使用 $create-her-gallery，帮我为一位重要的女性制作诗相册，从称呼和关系开始，一步一步问我。
```

你也可以更具体一些：

```text
我想给妈妈做一份生日礼物。请用 $create-her-gallery 引导我整理她的故事，照片希望统一做成温柔手绘风，并生成可以直接发给她的离线 HTML。
```

## 本地快速验证

需要 Python 3.10+。处理 MOV、音频或原图与动画合成时，还需要 FFmpeg。

```bash
python3 skills/create-her-gallery/scripts/validate_gallery.py \
  skills/create-her-gallery/assets/demo/gallery.json

python3 skills/create-her-gallery/scripts/build_gallery.py \
  skills/create-her-gallery/assets/demo/gallery.json \
  --output demo.html
```

生成后直接用浏览器打开 `demo.html`。演示配置不含任何私人素材：人物原图和手绘卡通图均为 AI 创建的虚构内容，并已合成为“上方原图、下方三秒卡通轻动画”的 720×1080 对照视频。

查看内置背景：

```bash
python3 skills/create-her-gallery/scripts/build_gallery.py --list-backgrounds
```

## 三个真实定制案例

仓库同时保留了三个经过脱敏的策展清单，展示同一个工具如何根据不同人生经历形成完全不同的结构：

| 案例 | 叙事方向 | 说明 |
| --- | --- | --- |
| [`feng`](examples/feng/gallery.json) | 从“她自己”出发，写个人成长与家庭关系 | 使用昵称“枫” |
| [`hua`](examples/hua/gallery.json) | 从爱情、亲情与自我展开 | 使用昵称“华” |
| [`yi`](examples/yi/gallery.json) | 用“多重宇宙”隐喻呈现人生的不同切面 | 使用昵称“奕” |

这些案例公开的是文字结构和配置，不包含原始照片、视频或音乐，因此不能原样构建。它们是“如何定制”的参考，不是可以直接套用的人生模板。

## Skill 结构

```text
skills/create-her-gallery/
├── SKILL.md                # Skill 入口与七阶段工作流
├── agents/openai.yaml      # Codex 展示信息与默认提示词
├── scripts/                # 校验、生成、音频与影像合成脚本
├── references/             # 访谈、写作、动画、音乐和主题规范
└── assets/                 # HTML 模板、背景与无隐私演示配置
examples/                   # feng、hua、yi 三个脱敏定制案例
```

## 隐私与版权

- 仓库不包含作者家人的原始照片、视频、音乐、故事页面或生成成品。
- 分享最终 HTML 前，请确认照片中的人物同意相应的分享范围。
- 网络上的“免费下载”不等于可以再分发。Skill 要求逐项核实音乐和背景的许可、作者、来源链接与署名方式。
- AI 生成或修复过的图像应如实说明；同一相册默认保持一种卡通画风。

## 为什么是一个 HTML

因为礼物不该要求收件人注册账号、安装应用或等待网站加载。图片、短视频、文字与音乐会被嵌入同一个文件；对方收到后双击就能打开，也可以长期离线保存。

## License

[MIT](LICENSE)

---

## English

# Create Her Gallery

Turn one person's photographs and stories into a poetic visual gallery made specifically for her.

Create Her Gallery is a guided Codex Skill. Instead of starting with a complicated form, it works like a curatorial editor: it asks who she is and what you have experienced together, then helps shape the writing, chapters, illustration style, animation, music, and background before exporting a single offline HTML file.

> Photos, videos, stories, and music are processed locally by default and do not need to be uploaded to a website.

> An independent project. I designed and built the interview flow, curation method, interaction and templates, build scripts, privacy rules, and example cases.

## Why I built it

The hardest part of making a digital gift is rarely placing photos on a page; it is deciding how to tell one person's story. Fixed templates flatten different lives into the same narrative, while a slideshow alone cannot express relationships, memories, and what the giver wants to say.

The Skill therefore interviews before it produces. It helps the user collect people, relationships, experiences, and quotations, proposes several narrative structures, and only then moves into writing, imagery, animation, music, and page building.

## What it creates

- A narrative designed around a real person rather than a fixed life template
- A consistent illustrated treatment for photographs
- Gentle three-second animation for each image, paired with the original
- Exported illustrations and prompts when no video-generation tool is available
- Progressive text, autoplay, navigation, and replay interactions
- User-provided music or public music with clear licensing and attribution
- Three built-in backgrounds plus custom image support
- One self-contained HTML file that can be opened, saved, and shared offline

## Guided workflow

1. **Meet her:** establish how to address her, your relationship, and the occasion.
2. **Hear the story:** collect meaningful experiences, personality, quotations, and memories.
3. **Curate the narrative:** propose two or three custom structures before completing the writing.
4. **Create the imagery:** choose one consistent illustration style and animate the photographs.
5. **Set the atmosphere:** select music and a background with clear rights.
6. **Build the gallery:** embed everything in a single offline HTML file.
7. **Review and revise:** test desktop and mobile layouts until the gift feels right.

## Install and start

```bash
git clone https://github.com/Weisi-song/create-her-gallery.git
cp -R create-her-gallery/skills/create-her-gallery ~/.codex/skills/
```

Then ask Codex:

```text
Please use $create-her-gallery to help me make a poetic gallery for an important woman in my life. Start by asking how I address her and what our relationship is.
```

## Local validation

Python 3.10+ is required. FFmpeg is also needed for MOV handling, audio work, or original/animation composition.

```bash
python3 skills/create-her-gallery/scripts/validate_gallery.py \
  skills/create-her-gallery/assets/demo/gallery.json

python3 skills/create-her-gallery/scripts/build_gallery.py \
  skills/create-her-gallery/assets/demo/gallery.json \
  --output demo.html
```

## Sanitized examples

The repository includes three sanitized curation manifests—`feng`, `hua`, and `yi`—to demonstrate how the same tool produces different narrative structures. They contain no original photos, video, or music and cannot be built as complete personal galleries.

## Privacy and copyright

- The repository contains no original family photos, videos, music, private story pages, or completed personal galleries.
- Confirm that people in shared photographs agree to the intended sharing scope.
- “Free download” does not automatically mean redistribution is allowed; verify every asset's license and attribution requirements.
- Disclose AI-generated or AI-restored visuals and keep one consistent illustration style within a gallery.

## Why a single HTML file?

A gift should not require an account, app installation, or a live server. Images, short videos, text, and music are embedded into one file that the recipient can open with a double-click and keep offline.

## License

[MIT](LICENSE)
