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

## 启动

macOS：双击 `macOS/GaiDesktopPet.app`。

Windows：安装 Python 3 后双击 `Windows/start-gai.bat`。

macOS 和 Windows 版都不需要额外 pip 包。
