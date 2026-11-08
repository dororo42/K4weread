# K4weread 设计文档

> 源自《K4weread：基于 Kindle 4 + KUAL 的独立微信读书应用可行性评估报告》（2026-11-08，`~/reports/`）。本文记录落地路线 A 的设计与证据指针。

## 1. 目标

Kindle 桌面 → KUAL → **K4weread** → 进入"只有微信读书 + 必要设置"的阅读程序；完整适配 K4 实体按键；保留 weread_K4.koplugin 现有 15 条快捷键；UI 引入 Simple UI 形态（书架即主屏）并同时适配按键。

## 2. 路线选型（评估报告结论）

| 路线 | 说明 | 结论 |
|---|---|---|
| **A（本项目）** | KOReader 容器内 weread-only 模式：KUAL 扩展 + 插件模式分支 | **推荐先行**（数天级，网络/刷新/按键栈全部复用已真机验证的 KOReader 2026.07.1） |
| B | 独立 Rust 原生应用（evdev + fb + einkfb + rustls + 协议移植） | 二期观察（1-2 月+，11.5k 行协议移植 + CJK 排版） |
| B' | 借 koreader-base 配方自建 Lua 运行时 + 自研 widget kit | 备案（数周，armel 构建链维护负担） |

## 3. 启动链（全部机制已双证）

1. **KUAL 扩展发现**：`/mnt/us/extensions/<name>/config.xml` 扫描（KOReader #13064 实证；parse.awk 只认 `type="json"`）。
2. **默认 action 执行模型**（`KualKindlet.java:559-578,614-626,643-656` 反编译 + 真机 KOReader 扩展原文互证）：
   记录 `commandToRunOnExit` → KUAL 自杀（lipc stop appmgrd booklet）→ `onStop()` 生成 `{ cmd ; } 2>>/var/tmp/KUAL.log &` 并后台拉起 → 经 `/var/local/mkk/su` 以 root、cwd=扩展目录。
3. **启动脚本** `bin/k4weread.sh start`：`touch /mnt/us/k4weread/launch.flag` → `exec /mnt/us/koreader/koreader.sh --kual`。
4. **插件消费**（weread_K4.koplugin v9.0，`weread/lib/only_mode.lua`）：第一个 init 的插件实例读+删标记（一次会话只认一次，防重复触发），置模块级会话态；FM 实例延迟 1 秒自动打开书架。
5. **阅读态**：Reader 实例复用既有 `initHotkeyOverride` 装配点（`reader_navigation.lua`，v8.x 已真机验证的 hotkeys.koplugin wrap 模式）额外 wrap `ReaderUI:onHome`（设备源码 v2026.07 `readerui.lua:551,929`：单键 Home 不在 hotkeys.koplugin，落 `onHome` → `showFileManager`）→ weread-only 下 Home 改为打开书架。

## 4. 标记文件契约

- 路径：`/mnt/us/k4weread/launch.flag`（写：k4weread.sh start；删：插件 consume + k4weread.sh koreader）。
- 语义：**一次性**——标记在插件 init 被消费；消费后本次 KOReader 进程会话内 `is_active()` 恒真（模块级状态，FM/Reader 实例共享同一 Lua VM）。
- 逃生：`Start KOReader (full)` 先删标记再启动，保证完整模式不被残留标记劫持。
- 残留风险：插件 < v9.0 时标记无人消费，插件升级后首次启动会进 weread-only（行为可解释，文档已登记）。

## 5. 按键设计

保留基线 = weread_K4.koplugin v8.4 的 15 条快捷键（插件 README 速查表）。weread-only 模式仅重定义 2 条：

| 键 | 原功能 | weread-only |
|---|---|---|
| Home | 文件管理器 | 书架（不关书，书架盖在阅读视图上，Back 返回阅读） |
| Menu | KOReader 全量菜单 | 保持（微信读书菜单经 reader_menu_order 置顶）；收敛为"必要设置"单列留待后续 |

ScreenKB+Down 快捷菜单、翻页/章节/目录/书签/Wi-Fi/切书等 13 条原样保留（结构性继承）。

## 6. Simple UI 形态

v0.1.0 = **A1 自研极简主屏**：书架即主屏（KUAL 直达 + Home 回主屏），不引入第三方依赖。评估报告中 simpleui.koplugin（A2 接入）作为真机按键评估项——其按键（非触摸）支持未验证；路线 B 的原生 Simple UI 属二期。

## 7. 已知边界与后续路线（2026-11-08 晚更新）

**weread-only 设计面已全部收口**（插件 v9.0→v9.5 同日五批）：
- ✅ KUAL 直达 + weread-only 握手（v9.0）
- ✅ 默认重开上一本书（v9.1）；未登录首启显式二维码（v9.4）
- ✅ 书架离线优先 + 分页懒加载 + 新鲜度门控（v9.1/v9.2）
- ✅ 关书直达书架（v9.3，跨实例交接 + 双守卫）
- ✅ Menu 收敛为微信读书菜单 + Exit KOReader 退出项（v9.3/v9.5）

**剩余边界**：书架后台刷新不重绘已开页（刻意决策）；KUAL 标签 ASCII（B2 用户关闭）。**路线 B/B'（独立原生应用）**：见评估报告 §二、§五风险登记册——设计面收口后仅作为远期观察项。
