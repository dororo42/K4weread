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
