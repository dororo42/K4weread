# AGENTS.md — K4weread

Kindle 4 + KUAL 的一键微信读书入口（KUAL 扩展 + weread_K4.koplugin weread-only 模式的启动握手侧）。

## 工作法

- **ub-mode**（~/.zcode/skills/ub-mode）：First Make it Work → Then Make it Right → Follow Practice。改动按可验证单元切分，提交信息说清"为什么、改了什么、如何验证"。动作日志记入 `LOG.md`（追加式）。
- **orbital_handoff**（~/.zcode/skills/orbital_handoff）：`handoffs/` 是本地交接通道——**永不 commit/push/上传**（已在 .gitignore）。每批次结束 CREATE 一份套件并更新下方指针。

## 项目事实（接手必读）

- 单一版本源：`kual/config.xml` 的 `<version>`；`tools/check_config.py` 与 CI 门禁依赖它。
- weread-only 握手标记：`/mnt/us/k4weread/launch.flag`（本仓 `kual/bin/k4weread.sh` 写，weread_K4.koplugin `weread/lib/only_mode.lua` 读+删）。改路径必须三处同步（脚本 + 插件仓 + 文档）：`tools/check_marker_path.py --peer-repo <插件仓>` 同时钉死写入侧、读取侧与全部文档，CI 克隆插件仓后显式校验；插件仓 `spec/only_mode_spec.lua` 另有生产字面量断言。
- KUAL 扩展执行模型（真机/反编译双证）：默认 action = KUAL 自杀退出 → onStop 后台拉起 `{ cmd ; } 2>>/var/tmp/KUAL.log &`，MKK su root，cwd=扩展目录；`killKnownOffenders` 只杀 matchbox-keyboard/kterm/skipstone/cr3。
- menu.json 选项词汇以真机 koreader 扩展为权威（name/priority/action/params/internal，本仓不使用 exitmenu/refresh/if）；`tools/check_menu.py` 锁死词汇集。
- 菜单标签用 ASCII（KDK-1.0 Unicode 渲染未真机验证，见 docs/REAL_DEVICE_TEST.md B2）。
- 部署目标：`/mnt/us/extensions/k4weread/`；设备 K4（0E）+ K4B（23）同构 FW 4.1.4。
- 发布：`tools/build_release.sh`（zip + sha256，禁手工打包）；GitHub Release 资产 = zip + zip.sha256。
- 网络：GitHub TLS 失败时走 LAN 代理 `http://192.168.2.153:16492`（curl/git 均可）；本机 gost `127.0.0.1:10800` 时好时坏，LAN 代理为首选。push 用 `env -u GH_TOKEN git push`（GH_TOKEN 的 ghu_ 令牌无写权）。

## Current Handoff

- Latest: `handoffs/2026-11-12-134035-k4weread-three-repo-audit-fix/HANDOFF.md`
- Branch: main @ a1abe8d
- Status: **三仓审查复核意见落地（2026-11-12）**：报告 21 项逐条落实（见 HANDOFF.md「三仓协同」§4）；三仓交叉门禁全绿、Lua 镜像逐字节一致。修复**未 commit / push**（待授权），未递增版本、未发版、未构建、未连真机；接手第一动作是核对未提交改动并按纪律提交。

任何 agent 开始工作前，先读上面的 HANDOFF.md。这份指针由 orbital_handoff 维护，手工交接时请同步更新。
