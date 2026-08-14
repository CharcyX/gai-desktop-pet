# Gai Desktop Pet

macOS 桌宠。双击 `GaiDesktopPet.app` 启动；右键宠物退出；按住左键拖动位置。应用编译为 Apple Silicon 与 Intel 通用二进制。

窗口会固定在 Dock 上沿，层级位于 Dock 之上；角色显示比例放大约 8%，启动位置向下补偿 30 px，拖动时也不会落到屏幕底端以下或越过可见工作区。

触发逻辑：

- 平时播放 idle。
- idle 先完整循环 6 次，再按 singing → waiting → failed 的固定顺序播放；每个动作完整循环 3 次，然后回到 idle。
- 红线悬停区内持续循环说唱；蓝线到红线之间的 60 px 环形区域播放 16 方向注视；蓝线外不触发注视。
- 鼠标离开悬停区后回到 idle。
- 悬停说唱优先于注视。
- 悬停说唱累计 3 次后，下一次说唱结束播放一次生气。
- 左右拖拽累计超过 7 秒后，下一次拖拽结束播放一次生气。

现有图集只有一条唱歌/等待素材行，因此 singing 与 waiting 共用该行，但触发时序独立。

首次打开若 macOS 拦截未签名应用：在 Finder 中右键 `GaiDesktopPet.app`，选择“打开”。

如果需要重新构建：在本目录执行 `./build.command`。要求 macOS 和 Swift 编译器。
