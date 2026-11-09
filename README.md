# K4weread

Kindle 4 + KUAL 上的一键微信读书入口：**Kindle 桌面 → KUAL → K4weread → Start WeRead only**，直接进入"只有微信读书 + 必要设置"的阅读程序。

- 设备：Kindle 4（`0E`/Tequila）与黑色 Kindle 5th Gen / K4B（`23`/Sauza）——同为 FW 4.1.4 / KDK-1.0 / Yoshi，用同一份扩展。
- 组成：
  - **本仓库**：KUAL 扩展（`kual/`，config.xml + menu.json + bin/k4weread.sh）——写模式标记 → 启动 KOReader；
  - **[weread_K4.koplugin](https://github.com/dororo42/weread_K4.koplugin) v9.9+**：微信读书插件的 weread-only 模式——消费标记、**默认重开上一本微信书**（无记录/未登录回退：未登录显式弹二维码登录，已登录进书架）、阅读中 Home 键回书架、关书自动回书架、Menu=微信读书菜单（含 Reading style 样式直达与 Exit KOReader）。
- 上游文档：[K4weread 可行性评估报告（2026-11-08）](docs/DESIGN.md)记录了路线选型与全部证据。

## 工作原理（weread-only 握手）

```
KUAL 菜单点 "Start WeRead only"
  └─ KUAL 自杀退出 → 后台拉起 bin/k4weread.sh start（root，同 KOReader 扩展机制）
       └─ touch /mnt/us/k4weread/launch.flag && exec /mnt/us/koreader/koreader.sh --kual
            └─ KOReader 启动，weread 插件 init 消费标记（读+删，一次会话只认一次）
                 └─ 默认重开上一本微信书；无记录/未登录按三分决策落二维码或书架
```

- `Start KOReader (full)` 是逃生通道：删除残留标记后启动完整 KOReader。
- 插件 < v9.0 时扩展仍可用（只当普通 KOReader 快捷入口），只是没有 weread-only 模式；v9.0 是握手起点，**v9.9+ 才具备本文描述的全部行为**。
- 标记路径由 `tools/check_marker_path.py --peer-repo <插件仓>` 跨仓校验，CI 会克隆插件仓后执行；插件仓 `spec/only_mode_spec.lua` 另钉死生产字面量。

## 安装

前置：越狱 + MKK + KUAL-KDK-1.0（K4/K4B 世代）+ 已部署 KOReader 与 weread_K4.koplugin（**v9.9+**）。

USB 拷贝或 scp 到 `/mnt/us/extensions/k4weread/`：

```
/mnt/us/extensions/k4weread/config.xml
/mnt/us/extensions/k4weread/menu.json
/mnt/us/extensions/k4weread/bin/k4weread.sh   (0755)
```

安全弹出 USB → 重启（KUAL 只在启动时扫描 `extensions/`）→ KUAL 里出现 **K4weread** 菜单。详见 [docs/INSTALL.md](docs/INSTALL.md)。

> Release 的 `K4weread-v0.1.2.zip` 是发版时快照，包内文档语义可能落后于仓库 HEAD；运行时三件套以 zip 内文件为准，依赖/按键说明以本仓库 HEAD 为准。

## K4weread 会话中的按键（v0.1.2 / 插件 v9.9）

保留 weread_K4.koplugin 现有 15 条快捷键（见[插件 README 的按键速查表](https://github.com/dororo42/weread_K4.koplugin#K4-阅读时按键速查koreader--hotkeyskoplugin--本分支改动)），其中 2 条在 weread-only 模式下重定义：

| 键 | weread-only 模式下的功能 |
|----|------|
| Home | **书架**（原：文件管理器） |
| Menu | **微信读书菜单**（书架/样式/搜索/上报/统计/设置/Exit；原：KOReader 全量菜单） |
| Back（关书后） | **书架**（原：文件管理器；0.2s 内接管） |
| ScreenKB + Down | 微信读书快捷菜单（保留） |
| 其余 12 条（翻页/章节/目录/书签/Wi-Fi/切书…） | 原样保留 |

## 已知边界（诚实登记，随插件版本演进）

- ~~阅读中按 Back 关书后落文件管理器~~ → **已解决**（插件 v9.3：关书 0.2s 自动回书架；真退出/切书不回弹）。
- ~~Menu 是 KOReader 全量菜单~~ → **已解决**（插件 v9.3：weread-only 下 Menu=微信读书菜单；v9.5：菜单末尾含 Exit KOReader；v9.7：第二位 Reading style）。
- ~~首次未登录无法进入~~ → **已解决**（插件 v9.4：未登录首启显式弹二维码登录）。
- ~~书架后台刷新不重绘已开页~~ → **已解决**（插件 v9.6 原地重绘且保持翻页位置；2026-11-08 审查修复了重绘读取陈旧书单的实现缺陷，并补 `spec/library_shelf_refresh_spec.lua`）。
- KUAL 菜单标签维持 ASCII：KDK-1.0 的 Unicode 标签渲染（C-3 字体 run 补丁）未真机验证，且用户已明确暂不做中文化（B2 关闭）。
- 真机增量验收（v9.2–v9.9）见 [docs/REAL_DEVICE_TEST.md](docs/REAL_DEVICE_TEST.md) D 节；设备未接入期间相关条目保持未勾选。

## 构建 / 门禁

```sh
sh tools/build_release.sh          # K4weread-v<ver>.zip + .sha256
python3 tools/check_menu.py        # menu.json 选项词汇门禁
python3 tools/check_config.py      # config.xml 解析 + version 单一来源
python3 tools/check_marker_path.py --peer-repo ../weread_K4.koplugin
```

CI：`.github/workflows/ci.yml`（shell 语法 / JSON / XML / 跨仓标记路径 / 打包 + sha256 + zip 白名单）；发版：`.github/workflows/release.yml`（`v*` tag push → 由 workflow 构建 zip + sha256 并创建 GitHub Release）。按项目纪律，Release 资产由 workflow 产出，不在本机手工构建。

## License

AGPL-3.0（与 weread_K4.koplugin 一致）。
