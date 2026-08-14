Gai 独立桌宠 Windows 版

启动：双击 start-gai.bat。

要求：Windows 10/11，Python 3（安装时勾选 Add Python to PATH）。本版本使用 Python 自带 Tk，不需要额外 pip 包。

操作：
- 左键拖动：移动宠物，并触发向左/向右跑。
- 红线悬停区内持续循环说唱；蓝线到红线之间的 60 px 环形区域按鼠标位置播放 16 方向注视；蓝线外不触发注视。
- 鼠标离开悬停区后回到 idle。
- 悬停说唱累计 3 次后，下一次说唱结束播放一次生气。
- 左右拖拽累计超过 7 秒后，下一次拖拽结束播放一次生气。
- idle 先完整循环 6 次，再按 singing → waiting → failed 的固定顺序播放；每个动作完整循环 3 次，然后回到 idle。
- 右键宠物或按 Esc 退出。

singing 与 waiting 共用现有图集中的唱歌素材行，触发时序独立。
