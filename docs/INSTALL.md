# K4weread 安装指南

## 前置

- Kindle 4（`0E`/Tequila）或黑色 Kindle 5th Gen / K4B（`23`/Sauza），FW 4.1.4，已越狱 + MKK + KUAL-KDK-1.0（azw2）。
- 已部署 KOReader（实机 v2026.07.1 验证）。
- 已部署 [weread_K4.koplugin](https://github.com/dororo42/weread_K4.koplugin) **v9.0 或更高**（低版本时 K4weread 退化为普通 KOReader 快捷入口，没有 weread-only 模式）。

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

- **Start WeRead only**：进入微信读书模式（自动书架 + Home 回书架）。
- **Start KOReader (full)**：完整 KOReader（逃生通道）。

## 卸载

删除 `/mnt/us/extensions/k4weread/` 与 `/mnt/us/k4weread/`（含 weread-only 握手标记 `/mnt/us/k4weread/launch.flag`）即完全回滚（只动用户分区，无系统文件）。

## 排障

- KUAL 里看不到 K4weread：确认三件都在位、k4weread.sh 有执行位、重启过 Kindle；`menu.json` 语法错误会在 KUAL 日志显式报错（`/var/tmp/KUAL.log`、KUAL crash 日志）。
- 点 Start 没进书架：插件版本 < v9.0（无 weread-only 模式）；或标记残留——用 `Start KOReader (full)` 清标记。
- KOReader 脚本输出/报错：`/var/tmp/KUAL.log`（KUAL 后台拉起统一 stderr）与 `/mnt/us/koreader/crash.log`。
