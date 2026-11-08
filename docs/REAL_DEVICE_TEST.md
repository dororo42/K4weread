# K4weread 真机测试清单（K4 + 黑色 K4B 各跑一遍）

> 设备同构（K4 `0E` + K4B `23`，FW 4.1.4 / KDK-1.0），同一份扩展同一套测试。

## A. KUAL 扩展

- [ ] **B1 注册**：重启后 KUAL 出现 `K4weread` 菜单；展开两项：`Start WeRead only` / `Start KOReader (full)`。
- [ ] **B2 Unicode 标签**（决定 menu.json 是否切中文标签）：临时在 menu.json 把 `Start WeRead only` 改为含中文的标签，重开 KUAL 目检渲染。通过 → 正式切中文；花屏/tofu → 维持 ASCII（当前默认）。
- [ ] **B3 逃生通道**：点 `Start KOReader (full)` → 进完整 KOReader 文件管理器（且不受残留标记影响）。
- [ ] **B4 重复启动**：WeRead only 会话中直接重启再点 `Start WeRead only`，无多实例抢屏。

## B. weread-only 模式（依赖插件 v9.0）

- [ ] **B5 直达书架**：点 `Start WeRead only` → KOReader 启动后 ≤2 秒自动打开微信读书书架（无需任何点击）。
- [ ] **B6 Home 回主屏**：从书架打开一本微信读书书 → 按 Home → 书架盖在阅读视图上；Back → 回到阅读位置（未丢进度）。
- [ ] **B7 快捷键保留抽查**：ScreenKB+Down 快捷菜单；ScreenKB+Up 目录；ScreenKB+Right 加书签；LPgFwd/RPgFwd 翻页；Left/Right 上下章——全部与插件 v8.4 速查表一致。
- [ ] **B8 逃生**：菜单/退出回到 KUAL，点 `Start KOReader (full)` → 文件管理器正常、无 weread-only 行为。

## C. 回归护栏

- [ ] 插件自身回归：完整 KOReader 模式下原 15 条按键全表照旧；阅读统计（Press 切 Tab）正常；登录/下载/进度同步不受影响。
- [ ] 卸载 = 删 `/mnt/us/extensions/k4weread/` + `/mnt/us/k4weread/`，KOReader/插件行为回到 v8.4 基线。
