# Create Her Gallery

把一个人的照片与故事，做成送给她的诗意影像相册。

Create Her Gallery 是一个面向 Codex 的创作 Skill。它不会一上来要求你填写复杂表单，而是像一位策展编辑一样，一步步询问她是谁、你们经历过什么，再共同确定文字、章节、卡通画风、动画、音乐和背景，最后导出一个可以离线打开与直接转发的单文件 HTML。

> 照片、视频、故事和音乐默认只在本地处理，不需要上传到网站。

## 最终会得到什么

- 一份为具体的人重新构思、而不是套用固定人生模板的诗相册
- 同一画风的照片卡通化效果，例如温柔手绘感或 3D 动画电影感
- 每张照片约 3 秒的轻动画，并与原图上下组合呈现
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
