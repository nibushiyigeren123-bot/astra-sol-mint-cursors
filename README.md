# Astra & sol · 薄荷绿 GPT 姐妹 Windows 指针

Astra 姐姐和 sol 妹妹各自一套指针，沿用此前姐妹的 Q 版定稿。姐姐是薄荷绿长卷发、白裙和蝴蝶结；妹妹是浅绿短发、绿开衫和水手领。两套独立选择。

![两套指针总览](previews/cursor-overview.png)

## 下载与安装

下载 [整个仓库 ZIP](https://github.com/nibushiyigeren123-bot/astra-sol-mint-cursors/archive/refs/heads/main.zip) 后解压，或下载 `downloads/` 中的单角色 ZIP。打开解压目录，在 PowerShell 中运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
```

安装器把文件复制到当前用户 `%LOCALAPPDATA%\AstraSolMintCursors\1.0.0`，并登记指针方案，不需要管理员权限。默认只登记方案；打开“控制面板 → 鼠标 → 指针”，选择 **Astra Mint 48px** 或 **sol Mint 48px**，点击应用。32、48、64 三档均可选，推荐先试 48；64 更适合录制展示或看清角色。Windows 的辅助功能指针大小设置可能进一步缩放显示。

也可以直接指定角色和尺寸并应用：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Character astra -Size 48 -Apply
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Character sol -Size 64 -Apply
```

`-Apply` 会在复制目录的 `backup/` 保存当前指针注册表值。恢复最近一次应用前的设置：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Restore
```

不运行脚本时，可在鼠标的“指针”页逐项浏览 `cursors/astra/48/` 或 `cursors/sol/48/` 的文件并保存方案。

## 内容

每套 17 种状态：正常、帮助、后台运行、忙碌、精确、文本、手写、不可用、垂直/水平/两种对角调整、移动、候选、链接、位置、人员。

每档包括 15 个透明静态 `.cur` 和 2 个动态 `.ani`。动态后台图标和时钟各有 8 帧、每帧 100ms；角色保持定稿姿态。点击热点在语义符号尖端或中心，角色位于侧边。完整文件名/中文映射、热点和帧数见 `source/cursor_manifest.json`。

![实际尺寸](previews/actual-sizes.png)
![忙碌与后台动画](previews/busy-animation.gif)

## 可编辑源与校验

`source/characters/` 保存这次使用的透明角色定稿；`source/frames/` 保存各档透明 PNG 帧；`source/build_cursors.py` 保存符号绘制、尺寸、热点和 CUR/ANI 编码逻辑，可重新制作。

```powershell
python -m pip install -r requirements.txt
python source/build_cursors.py
python scripts/validate_cursors.py
```

源码生成器使用 Windows 自带字体。校验器检查二进制边界、透明像素、动画差异，并在 Windows 上用 `LoadImageW`、`GetIconInfo`、`DrawIconEx` 实际加载所有文件、检查热点、绘制每个动画步骤，比较绘制颜色。公开 `validation.json` 是制作机验收记录，`checksums.json` 为分发文件 SHA-256。尚未在每种 DPI、远程桌面或各类游戏中实测。

Windows 原生加载审查：

![原生明暗背景](previews/windows-native-review.png)

## 来源和使用说明

角色身份参考沿用用户提供的姐妹截图及 [B 站视频 BV1xSa76yEqZ](https://www.bilibili.com/video/BV1xSa76yEqZ/)，视频简介提及多数人物素材来自 [ZipZipPipe](https://space.bilibili.com/4168597)，尚未逐张确认原图作者。这里使用的是此前本地模型重绘的 Q 版定稿，未包含参考截图、原视频或模型权重。角色源与旧 [姐妹桌宠项目](https://github.com/nibushiyigeren123-bot/astra-sol-codex-pets) 对应。

ChatGPT/OpenAI 图标归对应权利人；这是社区制作分享，非官方产品。代码采用 `LICENSE-CODE` 中的 MIT 许可证；此许可证不为角色美术、参考素材或品牌标识授予额外权利。

`previews/showcase.mp4` 为无配乐展示视频，B 站投稿文字见 `B站投稿文案.md`。
