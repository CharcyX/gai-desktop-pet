# Gai Desktop Pet

Gai 的独立桌宠文件，包含 Codex 宠物、macOS 版和 Windows 版。

## 动作逻辑

- idle 完整循环 6 次。
- 然后固定播放 singing → waiting → failed。
- 每个动作完整循环 3 次，之后回到 idle。
- 悬停宠物触发连续说唱；鼠标靠近但未悬停时触发对应方向注视。
- 左右拖拽即时切换跑步方向；拖拽累计超过 7 秒后触发生气。

## 文件

- `codex-pet/`：Codex v2 宠物文件。
- `macOS/`：Apple Silicon 与 Intel 通用版应用、源码和构建文件。
- `Windows/`：Python 3 + Tk 版桌宠。
- `releases/`：macOS 与 Windows 压缩包。

## 周延独立桌宠

- `zhou-yan/codex-pet/`：周延 Codex v2 宠物文件。
- `zhou-yan/macOS/`：周延 macOS 独立桌宠源码、通用 App 构建脚本和资源。
- `zhou-yan/Windows/`：周延 Windows Python/Tk 桌宠和启动文件。
- `releases/zhou-yan-desktop-pet-macos.zip`、`releases/zhou-yan-desktop-pet-windows.zip`：周延发布包。

周延版沿用 GAI 的交互机制：idle 完整循环 6 次后固定播放 singing → waiting → failed，每个动作完整循环 3 次；悬停触发连续说唱，靠近但未悬停时触发 16 方向注视，左右拖拽即时切换跑步方向，悬停说唱累计 3 次或拖拽累计超过 7 秒后触发生气。周延版的 jumping 行改为唱歌帧。

Codex 版周延图集保持与 GAI 一致的 2.5 头身比例，并在关键帧加入保持节拍以降低跳帧感。Codex 状态映射为：需要授权使用 waiting，思考使用 failed，failed 使用 waving；macOS 和 Windows 版仍沿用各自的交互逻辑与播放节奏。

## 启动

macOS：双击 `macOS/GaiDesktopPet.app`。

Windows：安装 Python 3 后双击 `Windows/start-gai.bat`。

Codex 桌宠：将 `codex-pet/` 放入 `%USERPROFILE%\\.codex\\pets\\gai-rough-v2\\` 后重启 Codex；本机安装包按此目录结构提供。

macOS 和 Windows 版都不需要额外 pip 包。
