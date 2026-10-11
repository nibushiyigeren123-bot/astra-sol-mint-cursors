# Astra & sol · 薄荷绿 GPT 姐妹 Windows 指针

Astra 姐姐和 sol 妹妹各自一套动态指针，沿用此前姐妹的 Q 版定稿和已制作的动作。姐姐是薄荷绿长卷发、白裙和蝴蝶结；妹妹是浅绿短发、绿开衫和水手领。两套独立选择，角色会随指针状态改变动作。

![两套指针总览](previews/cursor-overview.png)

## 下载与安装

v1.0.3 默认采用 **INF 右键安装**。完整包同时包含两位角色的五档文件和十个安装 INF；单角色包包含对应角色的五档和五个 INF。无需拆成五个压缩包。

1. 下载并**完整解压**，保留 INF 与 `cursors/` 文件夹的相对位置。
2. 右键 `安装_Astra_64px.inf` 或 `安装_sol_64px.inf`，选择“安装”。Windows 11 可能需要先点“显示更多选项”。安装到 Windows 目录时可能需要管理员确认。
3. 打开“控制面板 → 鼠标 → 指针”，在方案中选择 `Astra Mint 64px` 或 `sol Mint 64px`，点“应用”。
4. 需要其他档位时，安装对应 INF。可安装多档，再通过鼠标面板切换；无需重复安装已登记的档位。

| 文件分辨率 | Astra INF | sol INF |
|---|---|---|
| 32px | `安装_Astra_32px.inf` | `安装_sol_32px.inf` |
| 48px | `安装_Astra_48px.inf` | `安装_sol_48px.inf` |
| 64px | `安装_Astra_64px.inf` | `安装_sol_64px.inf` |
| 128px | `安装_Astra_128px.inf` | `安装_sol_128px.inf` |
| 256px | `安装_Astra_256px.inf` | `安装_sol_256px.inf` |

**尺寸限制须知：** 上表是 ANI 文件分辨率。纯 INF 只复制文件并登记方案；Windows 决定重载后的实际显示尺寸。在制作机 Windows 26300 上，直接通过鼠标面板重载这五档动画均为32px，不能保证五个方案名会产生五种实际大小。拆分压缩包也不会改变加载行为。可像 P5 参考包的作者建议一样，在 Windows“设置 → 辅助功能 → 鼠标指针和触控”尝试调整大小；系统滑块控制的是全局大小，不等于按五个方案名锁定五种像素，具体动画效果需在自己的系统确认。INF 版保留全部动画，没有把五档文件分辨率当成五档实际尺寸修复。

默认 INF 安装不启动常驻组件、不运行 PowerShell、不改登录启动、不附预编译 EXE。INF 本身不能保证所有电脑没有安装权限或系统策略提示。它只把本包17个 ANI 复制到 `%WINDIR%\Cursors\AstraSolMintCursors\cursors\角色\尺寸`，并登记所选方案；不修改当前活动指针。安装后需在鼠标面板选择并点应用。切回原 Windows 方案即可停止使用本包指针。

### 可选：指定像素的应用脚本

`应用_Astra_32px.cmd` 等十个 CMD，以及 `install.ps1` 保留为可选工具。它们复制到当前用户 `%LOCALAPPDATA%\AstraSolMintCursors\1.0.0`、登记方案、按指定像素加载并核验全部17状态，不需要管理员权限。直接右键 `install.ps1` 选择“使用 PowerShell 运行”默认应用64px；完整包优先沿用当前姐妹角色，单角色包使用本角色。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Character astra -Size 128 -Apply
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Character sol -Size 256 -Apply
```

此步骤仅保证此次应用的实际像素。之后 Windows 鼠标面板、登录或其他软件重载指针时，仍可能缩回系统默认尺寸。应用脚本默认**不安装或开启**尺寸保持组件。`-RegisterOnly` 仅登记；`-VerifyOnly` 仅检查包内文件；`-Restore` 停止可选组件并恢复最近一次脚本应用前的设置，备份保存在当前用户目录 `backup/`。INF 安装不产生该脚本备份。

### 可选：尺寸保持组件

确实需要在鼠标面板切换五档实际像素时，先安装所需 INF 或应用脚本，再运行 `尺寸保持_开启.cmd`。它使用 Windows 自带 .NET Framework C# 编译器，从 `source/MintCursorKeeper.cs` **在使用者本机生成**组件；分发包没有预编译 EXE。本机生成不等于可信代码签名，不保证安全软件或系统策略不提示；无需关闭系统保护或安装自签名根证书。

组件保存在当前用户目录，不联网、不需管理员权限；开启后登记 `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` 中 `AstraSolMintCursorKeeper` 以随登录启动，每个会话仅一个实例。每500ms检查一次，选择稳定后恢复全部17状态，通常约1秒；操作前重新核对方案和全部路径。只处理完整的本包方案：支持 INF 的 Windows 目录或脚本的当前用户目录；其他主题、任意混合方案不干预。未安装某档文件时不替换。

`尺寸保持_关闭.cmd` 停止并取消登录启动，保留当前指针；`尺寸保持_卸载.cmd` 另移除组件文件，保留素材与方案。诊断：`powershell -NoProfile -ExecutionPolicy Bypass -File .\keeper.ps1 -Action Status`；日志位于安装目录 `keeper/keeper.log`。普通 INF 安装以及普通应用脚本均不自动运行此组件。

## 内容

每套 17 种状态：正常、帮助、后台运行、忙碌、精确、文本、手写、不可用、垂直/水平/两种对角调整、移动、候选、链接、位置、人员。

每档包括 17 个透明动态 `.ani`，每个有4至8帧。正常选择的角色待机/眨眼；链接和人员选择挥手；后台运行思考等待；忙碌和文本选择拿着小平板工作；不可用表现失落；水平/对角调整和移动配跑动；垂直调整与候选选择配轻跳；帮助、精确和手写配查看纸张。语义符号尖端或中心的点击热点始终固定，角色在侧边动画，不跟随角色手脚改变点击位置。

| 指针状态 | 角色动作 |
|---|---|
| 正常选择 | 待机、眨眼 |
| 帮助 / 精确 / 手写 | 查看纸张 |
| 后台运行 / 位置选择 | 思考、等待 |
| 忙碌 / 文本选择 | 拿平板工作 |
| 链接 / 人员选择 | 挥手 |
| 不可用 | 失落表情 |
| 水平 / 对角调整 / 移动 | 跑动 |
| 垂直调整 / 候选选择 | 轻跳 |

动画帧采用此前通过检查的九状态桌宠图集，保留每种动作自己的比例和循环；细小品牌饰品仍存在生成绘制差异。完整文件名/中文映射、动作、热点、帧数和速度见 `source/cursor_manifest.json`。

![实际尺寸](previews/actual-sizes.png)
![忙碌与后台动画](previews/busy-animation.gif)

## 可编辑源与校验

`source/characters/` 保存透明角色定稿和两张九状态动作图集；完整下载包的 `source/frames/` 保存各档透明 PNG 帧；`source/build_cursors.py` 保存符号绘制、尺寸、热点和 ANI 编码逻辑，可重新制作。Git 仓库保留角色图集及生成器，输出PNG可通过生成器重建，完整包提供全部输出帧。

```powershell
python -m pip install -r requirements.txt
python source/build_cursors.py
python scripts/validate_cursors.py
python source/render_showcase.py
```

源码生成器使用 Windows 自带字体，视频生成器需要 FFmpeg。文件校验器检查所有ANI的二进制边界、透明像素、动画差异，并用Windows `LoadImageW`、`GetIconInfo`、`DrawIconEx` 实际加载文件、检查热点、绘制动画步骤及比较颜色。`validation.json` 是文件验收记录，`checksums.json` 为分发文件SHA-256。

v1.0.3另通过25项隔离入口检查：实际启动全部10份CMD子进程、无参数PS1、保留当前角色、单角色包、显式尺寸、仅登记/仅验证和六种开关冲突；隔离测试的原生调用使用stub，没有改当前系统指针。参见 `default-install-validation.json`。

修复版已在制作机通过真实安装器逐一应用两位角色的五档尺寸，检查170个已生效的系统状态及各动画帧，大小、热点、颜色和动画变化全部匹配。参见 `live-application-validation.json`。另外在隔离注册表中检查方案登记、备份恢复和两个实际触发的失败回退分支；失败注入使用模拟原生调用。修复了制作机上带广播标志的指针重载返回失败、导致应用提前回退的问题；重载采用flags=0，随后明确加载尺寸并核对实际系统结果。不同DPI、远程桌面和各类游戏环境仍需实际使用验证。

Windows 原生加载审查：

![原生明暗背景](previews/windows-native-review.png)

## 来源和使用说明

角色身份参考沿用用户提供的姐妹截图及 [B 站视频 BV1xSa76yEqZ](https://www.bilibili.com/video/BV1xSa76yEqZ/)，视频简介提及多数人物素材来自 [ZipZipPipe](https://space.bilibili.com/4168597)，尚未逐张确认原图作者。这里使用的是此前本地模型重绘的 Q 版定稿，未包含参考截图、原视频或模型权重。角色源与旧 [姐妹桌宠项目](https://github.com/nibushiyigeren123-bot/astra-sol-codex-pets) 对应。

ChatGPT/OpenAI 图标归对应权利人；这是社区制作分享，非官方产品。代码采用 `LICENSE-CODE` 中的 MIT 许可证；此许可证不为角色美术、参考素材或品牌标识授予额外权利。

`previews/showcase.mp4` 是75.2秒、1920×1080、30fps的完整模拟演示，Astra与sol分别展示全部17种状态，包含运动、状态名称、角色动作、窗口调整和尺寸对照，无配乐。B 站投稿文字见 `B站投稿文案.md`。
