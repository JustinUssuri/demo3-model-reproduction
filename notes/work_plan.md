# Demo3 v0.1 开发计划

目标：基于 3-bus toy network 的单一 alpha 扫描，完成 DC vs AC 一致性评估的最小闭环（结果表 + 两张关键图 + 结论摘要）。

范围与约束：
- 仅做单一维度 stress sweep（alpha scaling）。
- 不做 OPF、不做随机性、不做多网络对比。
- AC 参考求解使用 pandapower（如有必要再考虑替代）。

---

## 里程碑与交付物

M1. 项目骨架与数据结构
- 定义 `src/` 基础模块与结果目录结构。
- 明确 case 数据结构（buses/lines/injections/limits/alpha）。
- 交付：可加载的 base case + alpha grid。

M2. DC 与 AC 求解闭环
- 实现 `src/dc_flow.py`（lossless DC flow）。
- 实现 `src/ac_flow.py`（pandapower AC flow）。
- 交付：单个 alpha case 可同时跑通 DC/AC 并输出 line flows。

M3. 指标与结果表
- 实现 `src/metrics.py`：abs/rel error、congestion 一致性、AC 收敛标记。
- 输出 `results/tables/sweep.csv`（每个 alpha 一行）。
- 交付：完整 sweep 表。

M4. 绘图与摘要
- 实现 `src/plotting.py`：error vs alpha、loading vs alpha。
- 生成 `results/figures/*.png` 与 `results/summary.md`。
- 交付：两张核心图 + 简短结论。

M5. 运行入口与文档更新
- `run_experiments.py` 串联全流程。
- 更新 README/assumptions（如有）。
- 交付：一条命令可复现实验。

---

## 微任务清单（ADHD 友好）

原则：每个任务 5–20 分钟内完成，完成就勾掉；一次只做一个模块的小步。

### 0) 准备与骨架
- [x] 建立 `src/` 与 `results/` 目录（若已存在则跳过）。
- [x] 新建空文件：`src/cases.py`、`src/dc_flow.py`、`src/ac_flow.py`、`src/metrics.py`、`src/plotting.py`、`run_experiments.py`。
- [x] 在 `results/` 下建 `tables/` 与 `figures/` 子目录。
- [x] 在 `run_experiments.py` 写一个最小 `main()` 打印 "ok"。
- [x] 运行一次入口脚本，确认基础可执行。

### 1) `src/cases.py`（先做数据形状）
- [ ] 写一个 `make_base_case()` 函数返回基础参数 dict。
- [ ] 在 dict 中放入 buses 列表（N/M/S）。
- [ ] 在 dict 中放入 lines 列表（L1/L2，含 r/x/limit）。
- [ ] 加一个可选的 L3 开关字段（默认关闭）。
- [ ] 写 `alpha_grid(start, stop, step)` 返回 list。
- [ ] 写 `make_cases()` 把 base case + alpha 组合成 case 列表。
- [ ] 在文件底部加一个简短的 `__main__` 自检（打印 case 数量）。
- [ ] 手动运行自检一次，确认无异常。

### 2) `src/dc_flow.py`
- [ ] 定义 `solve_dc(case)`，输入单个 case dict。
- [ ] 从 case 中取线路 x、limit 与 injections。
- [ ] 写最小 DC flow 计算（链式 3-bus 可先用解析式）。
- [ ] 返回结构化结果 dict：`line_flows`, `angles`, `feasible`。
- [ ] 对 baseline case 运行一次，打印 L1/L2 flow。
- [ ] 将结果格式固定（后续 AC/metrics 依赖）。

### 3) `src/ac_flow.py`
- [ ] 确认 pandapower 已可导入（失败就先记 TODO）。
- [ ] 写 `build_pp_network(case)`，仅组建 buses/lines/gens/loads。
- [ ] 写 `solve_ac(case)`，调用 pandapower 运行 power flow。
- [ ] 返回结构化结果 dict：`line_flows`, `vm`, `va`, `converged`。
- [ ] 用 baseline case 试跑一次，记录是否收敛。

### 4) `src/metrics.py`
- [ ] 写 `compute_errors(dc, ac)` 返回 abs/rel error。
- [ ] 写 `compute_loading(flow, limit)` 计算 loading。
- [ ] 写 `congestion_match(dc, ac)` 输出 top-1 一致性布尔值。
- [ ] 写 `make_row(case, dc, ac)` 产出一行 dict（含 alpha）。
- [ ] 写 `write_csv(rows, path)` 保存 sweep 表。
- [ ] 用 2–3 个 case 做一次小验证并输出 CSV。

### 5) `src/plotting.py`
- [ ] 写 `load_table(path)` 读取 `results/tables/sweep.csv`。
- [ ] 写 `plot_abs_error(df, out_path)` 输出误差图。
- [ ] 写 `plot_loading(df, out_path)` 输出 loading 对比图。
- [ ] 用小表跑一遍，确认文件生成。

### 6) `run_experiments.py`（串联）
- [ ] 解析 CLI 参数（至少支持 step/alpha range）。
- [ ] 调用 `make_cases()` 生成 sweep。
- [ ] 对每个 case 依次跑 DC/AC/metrics。
- [ ] 写入 `results/tables/sweep.csv`。
- [ ] 生成两张图到 `results/figures/`。
- [ ] 生成 `results/summary.md`（先写固定模板）。
- [ ] 端到端跑一次，确保无异常。

### 7) 文档同步
- [ ] 更新 README：如何运行 sweep。
- [ ] 更新 assumptions：明确 DC 假设与 toy network 限制。

---

## 更小的“下一步”建议（卡住就做这个）
- [ ] 只完成 `src/cases.py` 的 base case + alpha grid。
- [ ] 只让 `run_experiments.py` 打印出 alpha 列表。
- [ ] 只让 `src/dc_flow.py` 输出 L1/L2 的两个数字。

---

## 验收标准（v0.1）

- DC/AC 在 baseline（alpha≈1.0）可同时收敛。
- Sweep 端到端跑通，生成 CSV + 至少两张图。
- `results/summary.md` 描述 “DC 在何区间可靠” 的结论与限制。

---

## 待确认

- alpha 的步长选择（0.05 还是 0.1）。
- 线路参数最终数值与 base MVA。
- 是否需要 L3 弱联络线作为可选配置。
