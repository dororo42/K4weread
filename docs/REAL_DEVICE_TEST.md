# K4weread 真机测试清单（K4 + 黑色 K4B 各跑一遍）

> 设备同构（K4 `0E` + K4B `23`，FW 4.1.4 / KDK-1.0），同一份扩展同一套测试。
> A–C 为 v9.0 基线回归；D 为 2026-11-08 独立审查补录的 v9.2–v9.7 增量验收（对应两仓交接「立即下一步 1」），设备未接入前保持未勾选。

## A. KUAL 扩展

- [ ] **B1 注册**：重启后 KUAL 出现 `K4weread` 菜单；展开两项：`Start WeRead only` / `Start KOReader (full)`。
- [ ] **B2 Unicode 标签**（决定 menu.json 是否切中文标签）：临时在 menu.json 把 `Start WeRead only` 改为含中文的标签，重开 KUAL 目检渲染。通过 → 正式切中文；花屏/tofu → 维持 ASCII（当前默认）。用户已明确关闭中文化，此项仅作存档。
- [ ] **B3 逃生通道**：点 `Start KOReader (full)` → 进完整 KOReader 文件管理器（且不受残留标记影响）。
- [ ] **B4 重复启动**：WeRead only 会话中直接重启再点 `Start WeRead only`，无多实例抢屏。

## B. weread-only 模式（基线，依赖插件 ≥ v9.0）

- [ ] **B5 首启落点**：点 `Start WeRead only` → KOReader 启动后 ≤2 秒按三分决策落点（有上一本书 → 重开该书；未登录 → 显式二维码；否则 → 书架），无需任何点击。
- [ ] **B6 Home 回主屏**：从书架打开一本微信读书书 → 按 Home → 书架盖在阅读视图上；Back → 回到阅读位置（未丢进度）。
- [ ] **B7 快捷键保留抽查**：ScreenKB+Down 快捷菜单；ScreenKB+Up 目录；ScreenKB+Right 加书签；LPgFwd/RPgFwd 翻页；Left/Right 上下章——全部与插件 v8.4 速查表一致。
- [ ] **B8 逃生**：菜单/退出回到 KUAL，点 `Start KOReader (full)` → 文件管理器正常、无 weread-only 行为。

## C. 回归护栏

- [ ] 插件自身回归：完整 KOReader 模式下原 15 条按键全表照旧；阅读统计（Press 切 Tab）正常；登录/下载/进度同步不受影响。
- [ ] 卸载 = 删 `/mnt/us/extensions/k4weread/` + `/mnt/us/k4weread/`，KOReader/插件行为回到 v8.4 基线。
- [ ] 跨仓契约门禁：`python3 tools/check_marker_path.py --peer-repo ../weread_K4.koplugin` 通过；人为改一侧路径（副本上做）应报错。

## D. v9.2–v9.7 增量验收（审查补录）

- [ ] **D1 书架分页**：约 42 本首屏 + 翻到已加载窗口末尾继续懒加载，页码不跳回第 1 页。
- [ ] **D2 新鲜度门控**：5 分钟内重开书架不触发 sync（无 ~8s TLS 卡顿）；超过窗口后后台 sync。
- [ ] **D3 后台 sync 原地重绘**：sync 完成后已打开的书架页出现新书，且**当前浏览页码不变**（验证 2026-11-08 闭包修复）。
- [ ] **D4 关书回架**：按 Back 关书 0.2s 内自动回书架；真退出/切书（ScreenKB+Back）不回弹；连续开书多轮不出现重复回架（验证 wrap 幂等修复）。
- [ ] **D5 Menu 收敛**：Menu 打开微信读书菜单，末项 `Exit KOReader` 可退出；第 2 项 `Reading style` 打开原生样式面板且面板不叠在列表上。
- [ ] **D6 Press 样式面板**：Press 键底部配置菜单（字号/字体/行距/边距）照常可用且按键可导航（事实：从未被裁）。
- [ ] **D7 未登录首启**：清除登录态后首启显式弹二维码；离线首启的落点（是否停在文件管理器）单独记录。
- [ ] **D8 FM 上下文**：在书架/文件管理器界面按 Menu，检查 `Reading style` 是否有响应；无响应需按静态推断的条件性风险进一步定位。
- [ ] **D9 标记失败可见性**：只读/写满 `/mnt/us`（副本环境）后点 Start，检查 `/var/tmp/KUAL.log` 出现 `k4weread: cannot create ...` 且未静默启动完整 KOReader。
- [ ] **D10 二维码登录退出**：清除登录态（或触发 Cookie 续期）弹出二维码后**不扫码**：按 Back 应关闭二维码并提示取消、无重复弹窗或后台轮询；按 Menu 应直接退出 KOReader 回 KUAL。首次登录与续期两条路径各跑一遍（对应插件仓 `spec/qr_login_spec.lua` 新增 5 例）。
- [ ] **D11 登录恢复闭环（2026-11-10 修复批次；11-11 进度：重登闭环已三证、无效 skey 报错路径已真机两证——仅剩 ① 续期路径待观察）**：① 会话过期后点 Cookie 续期——续期**真恢复**才显示成功，且 footer「登录已过期」消失；服务器返回无效 skey 时应报错而非成功（假阳性防护）。② 重新扫码登录——扫码成功后 footer 提示立即消失；Report status 恢复 Running（停止期间的时长积压开始补报）。③ 任一失败路径若仍显示成功而上报持续失败，记录设备日志（`/mnt/us/koreader/crash.log`）中的服务器响应特征。

