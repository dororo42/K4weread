# K4weread 安装指南

## 前置

- Kindle 4（`0E`/Tequila）或黑色 Kindle 5th Gen / K4B（`23`/Sauza），FW 4.1.4，已越狱 + MKK + KUAL-KDK-1.0（azw2）。
- 已部署 KOReader（实机 v2026.07.1 验证）。
- 已部署 [weread_K4.koplugin](https://github.com/dororo42/weread_K4.koplugin) **v9.9+**（与 `README.md` 统一的最低要求；v9.0–v9.8 仍是可用入口，但缺少样式直达、原地重绘修复等后续能力；< v9.0 无 weread-only 模式）。最低要求不等于当前版本：插件仓已发版 v9.12，当前推荐组合见「三仓兼容矩阵」交接记录。

## 安装（USB 或 scp 二选一）

内容三件（来自 Release zip 的 `K4weread/kual/`）：

```
config.xml          → /mnt/us/extensions/k4weread/config.xml
menu.json           → /mnt/us/extensions/k4weread/menu.json
bin/k4weread.sh     → /mnt/us/extensions/k4weread/bin/k4weread.sh   (需 0755)
```

USB：解压 zip，把 `K4weread/kual/` 整目录拷到 `/mnt/us/extensions/k4weread/`。

scp（IP 按 DHCP 实际值）：

```sh
ssh -p 2222 root@192.168.2.x "mkdir -p /mnt/us/extensions/k4weread/bin"
scp -P 2222 kual/config.xml      root@192.168.2.x:/mnt/us/extensions/k4weread/
scp -P 2222 kual/menu.json       root@192.168.2.x:/mnt/us/extensions/k4weread/
scp -P 2222 kual/bin/k4weread.sh root@192.168.2.x:/mnt/us/extensions/k4weread/bin/
ssh -p 2222 root@192.168.2.x "chmod 0755 /mnt/us/extensions/k4weread/bin/k4weread.sh && sync"
```

## 激活

安全弹出 USB → 重启 Kindle（KUAL 只在启动时扫描 `extensions/`）→ 打开 KUAL → 出现 **K4weread** 菜单：

- **Start WeRead only**：默认重开上一本微信书；无记录/未登录按三分决策（显式二维码登录或书架）+ Home 回书架。
- **Start KOReader (full)**：完整 KOReader（逃生通道）。

## 卸载

删除 `/mnt/us/extensions/k4weread/` 与 `/mnt/us/k4weread/`（含 weread-only 握手标记 `/mnt/us/k4weread/launch.flag`）即完全回滚（只动用户分区，无系统文件）。

## 发布资产说明

Release 的 `K4weread-v0.1.2.zip` 是**发版时的运行时快照**，包内 README/文档语义可能落后于仓库 HEAD；依赖版本与按键说明以仓库 HEAD 的 `README.md` / `docs/DESIGN.md` 为准。运行时三件套以 zip 内文件为准，完整性用同目录下的 `.zip.sha256` 校验。按项目发版纪律，只有明确发版时才递增 `kual/config.xml` 的版本号并由 `release.yml` 重出资产；资产名由 `config.xml` 的 `<version>` 决定，本文件（及 `README.md`）中出现的资产名由 `tools/check_docs_consistency.py` 门禁校验，避免再次滞后。

## 排障

- KUAL 里看不到 K4weread：确认三件都在位、k4weread.sh 有执行位、重启过 Kindle；`menu.json` 语法错误会在 KUAL 日志显式报错（`/var/tmp/KUAL.log`、KUAL crash 日志）。
- 点 Start 没进书架：插件版本 < v9.0（无 weread-only 模式）；或标记残留——用 `Start KOReader (full)` 清标记。
- 点 Start 完全没启动 KOReader：标记写入失败，脚本会在 `/var/tmp/KUAL.log` 留 `k4weread: cannot create ...` 并退出（不再静默降级）；检查 `/mnt/us` 可写与剩余空间。
- KOReader 脚本输出/报错：`/var/tmp/KUAL.log`（KUAL 后台拉起统一 stderr）与 `/mnt/us/koreader/crash.log`。
