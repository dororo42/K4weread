# LOG.md — K4weread 动作日志（追加式）

> 每条记录：日期 / 为什么 / 改了什么 / 如何验证。新条目追加到末尾，不覆盖历史。

## 2026-11-08 · 独立审查后的 P0–P2 修复批次

- **依据**：`/home/doro/reports/2026-11-08-K4weread-v9.7-全生态独立代码审查报告.md`（3 🔴 / 8 🟡 / 10 🟢），用户指令「按重要级，逐项修复」。
- **为什么**：跨仓握手路径零机器校验、发布脚本可产出名实不符的包、v9.6 原地重绘读旧书单、v9.7 新 UI 零测试、wrap 跨实例重复包裹、文档语义滞后、交接工具误报 VERY_STALE。
- **改了什么（本仓）**：
  - `tools/check_marker_path.py` 支持 `--peer-repo`，同时钉死写入侧脚本、读取侧 `only_mode.lua` 与全部文档；`.github/workflows/ci.yml` 克隆插件仓后显式校验，并加最小权限与 zip 白名单断言。
  - `tools/check_menu.py` / `tools/check_config.py` 改为显式退出码（不再依赖 `assert`）、放宽脆弱的动作序列断言、加固版本与空值校验。
  - `tools/build_release.sh` 构建前清理 STAGE（幂等）；`kual/bin/k4weread.sh` 标记写入失败显式报错退出。
  - `README.md` / `docs/DESIGN.md` / `docs/INSTALL.md` / `docs/REAL_DEVICE_TEST.md` 对齐 v9.7 语义，新增 D1–D9 增量验收清单与发布资产说明；`AGENTS.md` 修正跨仓契约表述、指针 HEAD 与 Status。
  - 两仓 `handoffs/` 最新套件按写契约补结局标注与「审查后修复批次」章节（只做加法）。
- **改了什么（插件仓，weread_K4.koplugin）**：v9.6 原地重绘根因修复 + `spec/library_shelf_refresh_spec.lua`；v9.7 `spec/reader_navigation_spec.lua` + module-map 撤销豁免；wrap 幂等守卫移到 `ui`；`only_mode.lua` 删除失败延迟重试 + 生产字面量断言；`shelf_trim.is_fresh` 下界 + 用例；Exit 前关列表；`tools/build_release.sh` 防呆；README 版本对齐与未发版修复记账。
- **改了什么（工具）**：`orbital_handoff/scripts/check_staleness.py` 区分「HEAD 非哈希」与「HEAD 不可达」，并排除设备绝对路径误判。
- **如何验证**：`sh -n`、三个 Python 门禁、跨仓护栏正向/负向（构造漂移 peer 与陈旧文档均被拦截）、`ci.yml` YAML 解析、`git ls-files '*.lua' | luac -p`、module-map / version-sync、**29 个纯逻辑 spec 全绿**（本机无 busted，用 `/tmp` 的 Lua 5.1 临时运行器；CI 仍用真实 busted）、skill 42 项回归测试全绿、`validate_handoff.py` 复跑。
- **边界 / 未做**：未 commit、未 push、未递增版本、未重写发布资产（发版纪律：用户说「发布」才执行）；插件仓并发写入者的 6 个未提交文件未触碰；真机 A–D 清单未执行（设备未接入）；FM 上下文样式面板、离线首启落点、凭据过期判定等保留项已登记为 D6–D8 待真机。
- **动作记录顺序**：红色基线（漂移门禁不报警 / `expected New book, got Old book` / wrap 幂等失败）→ 最小修复 → 逐组验证 → 文档与交接同步。

## 2026-11-08 · 并发写入核实与 commit / push

- **为什么**：用户指示核实并发写入者是否已停止，并收敛工作区后提交推送。
- **核实**：插件仓 6 个在制品文件的最后 mtime 为 18:48，核实时 19:45（约 57 分钟无写入），无常驻编辑进程；`git reflog` 显示写入者已自行提交 `b82d7ed fix(P1-A): k4tls 绑定语义修复同步 + client 有界 sink EOF`，工作区只剩本批次改动。判定已停止。
- **必要修复**：审查 `b82d7ed` 的运行时改动（`client.lua` 有界 sink EOF、`k4tls.lua` 二进制拷贝/异常释放/错误标准化、`transport.lua` 默认 LuaSec），确认返回形状与 `client.lua` 的 `pcall` 失败判定一致，无需改代码；同步两仓 `AGENTS.md` / 交接里「6 个未提交文件、未 commit / 未 push」的过时陈述。
- **验证**：`git ls-files '*.lua' | luac -p`、version-sync、module-map 0 孤儿、`build_commit` 祖先检查、**94 个纯逻辑 spec 全绿**（本机 Lua 5.1 运行器，含新提交的 k4tls / transport 用例）；`client_redirect_spec` 3 例依赖 luasocket，本机未装，交由 CI 覆盖。
- **提交**：两仓各一次主提交（提交信息说明为什么 / 改了什么 / 如何验证），随后 `env -u GH_TOKEN git push origin main`；`handoffs/` 未入库（本地交接通道）。
- **边界**：未递增版本、未打 tag、未重写发布资产、未发 Release（发版纪律：用户说「发布」才执行）；真机 A–D 清单仍未执行。

## 2026-11-08 · v0.1.1 / v9.8 发版（两仓，用户明确授权）

- **为什么**：用户指示「进行发版，tag，发包，两仓都执行」——触发发版纪律（说「发布」才递增版本）。核实发现两仓只有 `ci.yml`，无发布通道，而纪律要求包必须由 GitHub workflow 产出。
- **改了什么**：
  - 版本源：本仓 `kual/config.xml` `0.1.0 → 0.1.1`；插件仓 `_meta.lua` / `main.lua` `0.6.0-k4-v9.7 → 0.6.0-k4-v9.8`，`build_commit → e4f8d1e`。
  - 新增两仓 `.github/workflows/release.yml`：`v*` tag push → checkout(fetch-depth 0) → `tools/build_release.sh` → `sha256sum -c` → `gh release create` 上传 zip + zip.sha256（`contents: write`）。
  - 文档：README / INSTALL / AGENTS 同步版本与依赖行（v9.8+），插件 README 把「未发版修复」章节转为正式 v9.8 变更日志。
- **沿革**：`v0.1.0`（2026-11-08 首个 Release，KUAL 扩展 + 握手）→ `v0.1.1`（审查修复批次：跨仓契约护栏、门禁硬化、打包幂等、文档对齐）；插件 `v9.7`（样式直达）→ `v9.8`（审查修复 + P1-A 传输层接线，默认关）。
- **纪律**：包**不由本机手工构建**；本机只做源码级检查与门禁，zip + sha256 全部由 workflow 在 GH runner 产出并上传。
- **指纹段**：资产 sha256 由 workflow 产出的 `.zip.sha256` 记录，并写入对应 GitHub Release 正文（PATCH 收尾）。
- **如何验证**：待 tag 推送后核对两仓 release run 结论、Release 资产清单与 `sha256sum -c`；结果补记于此。
- **核实结果（出包收尾）**：tag `v0.1.1` / `v9.8` 推送后，release run `42484179044` / `42484182242` 与 CI run `42484179082` / `42484125931` 均 `success`；两仓 Release 双资产齐全，指纹 `eba7eb4f478dad8478da2f6cea6b81f50e17d66805f56d12a05320ae88dae23e`（K4weread v0.1.1）与 `e35e727d8dfb897e7afa888dde38d5ea3ad6c53893657299a9c4b1e1b39bfd89`（weread v9.8）；两仓 Release 正文已 PATCH「沿革 + 指纹段」，`release.yml` 顶部同步补记沿革与指纹，收尾 commit + push 一并完成。K4B（B023）仍待升级，真机 A–D 清单待按键验收。

## 2026-11-08 · KUAL 扩展部署到 K5（用户报"菜单缺失"后的修复）

- **为什么**：用户在 K5（192.168.2.157，KOReader v2026.07.1，内含 weread_K4 v8.4）的 KUAL 菜单里找不到本项目入口——K5 只装过 koreader/k4refresh/fpcheck/gawk 扩展，`k4weread` 扩展从未部署到该机。
- **改了什么（设备侧，仅新增）**：按本仓 kual/ 原样部署 `/mnt/us/extensions/k4weread/{config.xml,menu.json,bin/k4weread.sh}`（755），未改任何现有扩展与插件文件；`sh -n` 与 usage 探针（`k4weread.sh` 无参 → usage，rc=2）通过。删除该目录即完全回退。
- **已知差异**：K5 插件为 v8.4，尚无 v9.0+ 的 only-mode launch.flag 握手——"Start WeRead only" 在 K5 上会等价于普通启动（touch 的 flag 无人消费，无害），待插件升级后自动生效。
- **未做**：未在 K5 真机点按验证菜单渲染与启动（等用户操作）；未升插件版本；未 commit 本记录。

## 2026-11-08 · 二维码登录退出机制（用户真机 BUG）

- **为什么**：用户反馈「Cookie 续期重新扫二维码时不扫无法退出，首次登录不扫也要能退出」。核实真机 KOReader `qrmessage.lua`：`QRMessage` 是 modal `InputContainer`，`init()` 注册 `AnyKeyPressed`（任意键仅关窗、吞掉 Menu）；项目侧 `_show_qr` 未绑定任何退出动作，且首次登录在无文档 FM 上下文，weread-only 收敛菜单与 `Exit KOReader` 均不可达。
- **改了什么（插件仓）**：`weread/lib/qr_login.lua:_show_qr` 覆盖 `key_events` 为 `Close`（Back → `cancel()` 停轮询）与 `ExitApp`（Menu → 先取消再广播原生 `Exit`），按真机 `readermenu.lua:79` 的两层格式；弹出时 transient 提示两个键；`ui/event` 按需 require 避免影响其它 spec。`spec/qr_login_spec.lua` 扩桩并新增 5 例；README 登录节与变更日志登记；本仓 `docs/REAL_DEVICE_TEST.md` 补 D10 验收项。
- **如何验证**：TDD 红基线 4 例失败 → 修复后 `qr_login_spec` 11/11、全量 busted **445/0**、`luac -p` 全部 Lua、`luacheck` 0 warnings / 0 errors、module-map 0 孤儿、version-sync 通过。
- **边界**：未递增版本、未发版、未打 tag；`showBusy` 获取二维码阶段仍不可取消（有 10/20s 超时）；OTP 输入框沿用自带 Cancel；真机 D10（首次登录 + 续期两条路径）待用户按键验收。

## 2026-11-10 · 登录恢复链缺陷核实与修复（K5 实证，本仓仅核实+记账）

- **为什么**：用户报「续期成功但右下角仍提醒过期、上报离线」。SSH 拉设备日志核实：会话真死（续期后 read 持续 `-2012 登录超时`），「续期成功」为假阳性（renewal 返回 succ=1 + 8 字符无效 wr_skey）；重新扫码后 footer 残留 = relogin 清锁存先于 accepted-report 边沿 → `LoginHint.hide` 无调用者；report 停于 `account_cleared` 无人重启。
- **核实范围**：本仓（握手侧）`kual/` + `tools/` 无 read_report/LoginHint/renew 牵连——本仓无需改码；修复全落插件仓 4 处（TDD 8 例红→绿；CI 453/0 绿 run `42720908234`；`transport_spec` 2 例为 `ed9c5da` 收敛提交的 spec 缺口，一并修正 `d833874`）。
- **部署**：K5（192.168.2.157）备份 `weread_K4.koplugin-backup-20261110-pre-loginfix.tgz` 后同步 6 个 runtime 文件（k4tls/transport/client/qr_login/read_report/common），md5 逐字一致；KOReader 未重启，新代码下次会话生效。footer 残留清除：重启后任一次登录成功（新 hide 兜底自动清）或完整 KOReader 手动关闭 footer 自定义文本。
- **如何验证**：见插件仓 README 2026-11-10 条目与 CI run；真机 D11（本仓 `docs/REAL_DEVICE_TEST.md` 新增）待按键验收。
- **边界**：未递增版本/未发版/未打 tag（发版纪律）；K4（B00E）设备离线未部署（待在线同步同 6 文件）；LAN 代理当日不通、git push 直连成功（网络坑记忆更新）。

## 2026-11-10 · v0.1.2 / 插件 v9.9 发版（两仓，用户授权「推送和发布」）

- **为什么**：K5 重登后真机验证通过（23:39:36 login completed → report started reason=relogin → 23:40:06 read report success；footer custom_text 恢复 KOReader 默认、快照键清除——hide 兜底/重启 report/relogin 边沿三项修复全部实证生效），触发发版纪律。同批落地 2026-11-09 复审 🟡-1（本仓 build_release.sh 三重防呆）。
- **改了什么（本仓）**：`tools/build_release.sh` 脏工作区/tag 存在/HEAD==tag 三重校验（负向矩阵 rc=1×3 + tag@HEAD rc=0 已验）；`ci.yml` 移除普通 push 上的打包步骤（无 tag 会被防呆拒绝）；zip 布局白名单断言迁入 `release.yml`；`config.xml` 0.1.1→0.1.2；README/INSTALL 依赖行 v9.9+。
- **改了什么（插件仓）**：`_meta.lua`/`main.lua` 0.6.0-k4-v9.8→**0.6.0-k4-v9.9**（build_commit=ebe8f0f）；README 两段「未发版修复」转正式 v9.9 changelog。
- **网络坑**：直连 443 当日两次断连（push 首试失败），LAN 代理恢复后走代理推送成功——与 11-09 恰好相反，两条路径都要试。
- **如何验证**：两仓 CI + release workflow 全绿（本仓 run `42723704308`、插件仓 `42723717007`）；Release 双资产齐全且均为 Latest；资产指纹 K4weread v0.1.2 = `78695627…ae7dd43`、weread_K4 v9.9 = `bd7ac215…17ddc6`（已入 `release.yml` 顶部与 Release 正文）。
- **部署**：K5 同步 `_meta.lua`/`main.lua`（设备 `_meta` = `0.6.0-k4-v9.9`）；**K4（B00E/192.168.2.151）离线未部署**（待在线：6 个 runtime 文件 + `_meta`/`main`，或直接解包 v9.9 Release zip）。
- **边界**：handoff 073303 两套文末追加本发版节（写契约加法）；后续动作见交接链头。

## 2026-11-10 · D10 真机验证核实 + 复审 🟢 清理批（skill 双副本同步 / params 门禁 / 工作区清理）

- **D10 核实**：设备日志佐证 23:56–23:57 用户完成一轮验证循环——33 次上报全成功后清账号弹码 → 两次 getLoginInfo 轮询（k4tls 正常超时重试）→ 23:57:21 login completed + report started reason=relogin；多轮弹码-登录循环无卡死、无错误、无残留。Back/Menu 的具体按键行为以用户确认为准（dismiss/Exit 无插件日志行，日志只能佐证循环闭环）。
- **skill 双副本同步（🟡-2 收口）**：`.zcode/skills/orbital_handoff/scripts` 从 `.codebuddy` 同步（check_staleness.py / validate_handoff.py 两文件漂移），`unittest` 42 项回归全绿——VERY_STALE 误报根除。
- **🟢-10 落地**：`tools/check_menu.py` 增加 params 白名单（start/koreader）；负向验证恶意 params（reboot）rc=1 拦截。
- **🟢-7 落地**：工作区残留 `K4weread-v0.1.0.zip` + `.sha256` 清理（untracked，.gitignore 本就忽略）。
- **如何验证**：门禁正向全绿 + 负向拦截；skill 42 项回归 OK；D11 后续观察点（续期路径自然过期时看脚标同步消失）交由用户日常使用，见交接链头。
- **边界**：K4（B00E）仍离线；复审其余 🟢（checkout pin SHA、k4tls 搜索顺序等）留下一批。

## 2026-11-10 · 复审 🟢 清理批（k4tls 内置库优先 / checkout pin SHA）+ K4 二次探测

- **为什么**：交接链头登记的复审余项继续推进。
- **改了什么（插件仓 ac34e11）**：🟢-8 `k4tls._load` 搜索顺序改为模块同目录 `libk4tls.so` 优先（系统同名旧库不再静默遮蔽随包内置库，旧 ABI 风险）；`k4tls_spec` 顺序断言对调；🟢-6 qr_login 缩进。**改了什么（两仓）**：🟢-5 `actions/checkout@v4` 固定到 commit SHA `11d5960a…`（4 处 workflow）。
- **如何验证**：k4tls_spec 42/0、qr_login_spec 13/0（本机 shim）；luac -p / module-map / version-sync 全绿；两仓 CI 全绿（插件仓 run `42731375066` 全量 busted、本仓 `42731381825`——pin SHA 后的新 workflow 自身也被验证）。不发版，随下一批。
- **K4（B00E）二次探测**：仍离线（No route to host）——部署待办维持。
- **边界**：🟢-2（k4tls 8MB 上限语义）/🟢-9（轮询提示）为行为设计项，R4/用户拍板后再动；D11 剩余两点为用户日常观察。

## 2026-11-10 · RESUME 接手 + 插件仓 v9.12 收尾（并发 agent 批次审计）

- **RESUME（orbital_handoff）**：两仓链头核验——本仓 073303 一致；插件仓发现并发 agent（CodeBuddy）已延续链推进 v9.10（扫码提示防遮挡+TouchMenu化+ChangeLog 双语重构）/ v9.11（上游 U17-1/U17-2 TDD 8 例 462/0）/ v9.12（QR 提示条显示修复 463/0）三批次并发版，新链头 `212840-weread-k4-v9-11-upstream-qr-fixes`（Continues from 073303，闭环表完整）。
- **审计结论**：v9.12 tag/Release/双资产在线（`gh api` 权威，`gh release view` 曾瞬时 not found 不可作准）；CI 最终 success（中途 1 次 version 字面量失败被 db4da82 补丁修复）；缺口仅收尾三件。
- **收尾（2de2676）**：release.yml 沿革补 v9.12 指纹 `0a44d83f…dd7f820`；AGENTS Status → db4da82/v9.12；212840 套件文末追加收尾节（本地）。
- **K5 升级准备**：v9.12 zip（60 文件）已下载至 `/tmp/weread_K4.koplugin-v9.12.zip` 并 sha256 校验 OK；**设备升级暂缓——K5 本轮超时离线**（当日多次在线，间歇在线已知坑），上线后：备份 → 解包 zip 覆盖 `/mnt/us/koreader/plugins/` → md5 抽验 + `_meta` 确认。
- **K4（B00E）**：全天多次探测均离线，部署待办维持（升级路径同为解包 v9.12 zip）。
- **边界**：R4 bench（Phase 1 闸门）需设备在线，待 K5/K4 任一上线执行；套件文末已登记 v9.12 收尾。

## 2026-11-10 · K5 升级 v9.12 + R4 bench 执行（设备在线窗口）

- **K5 升级 v9.12**：备份 `weread_K4.koplugin-backup-20261110-pre-v912.tgz`（1.5MB）→ 上传 Release zip（本地 sha256 预校验，设备无 sha256sum）→ 解包覆盖 → `_meta` = `0.6.0-k4-v9.12`，4 个关键文件 md5 与 Release zip 逐字一致。KOReader 重启生效（用户侧）。
- **R4 bench PASS**（报告 `~/reports/2026-11-10-K4weread-R4-bench报告-libk4tls-vs-LuaSec-K5真机.md`）：K5 真机 n=10/后端，k4tls MEAN 0.837s vs LuaSec 0.866s（快 3.4%，MAX 更低），10/10 成功——评估报告 §九 R4 条款「性能持平即换」满足。
- **现状修正**：K5 `koreader.sh` 已含 `export WEREAD_TLS_BACKEND=k4tls`（生产闸门已翻，非交接登记动作）；Phase 1 网络组件线（P1-A + R4）就此闭环，Phase 2/3 触发条件复核后维持观察（TLS 慢已被排除）。
- **遗留**：① bench 脚本入库（dev/bench_tls.lua）+ INSTALL 登记 k4tls 部署步骤——随插件仓下一批；② K4（B00E）仍离线，升级路径同 v9.12 zip。
