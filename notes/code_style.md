【范围与约束】
- 必须使用 PyPSA（python 包）的 Network 对象作为核心建模容器（buses/lines 或 buses/links、generators、loads、storage、snapshots）。
- DC/线性潮流：用 PyPSA 的 LOPF（network-constrained linear optimal power flow）来求解；不允许手写 DC 方程求解器作为主实现（可以留作对照/备用）。
- 求解器默认用开源 HiGHS（如可用），支持配置切换到 gurobi，但不能强依赖 gurobi。
- toy case 的数据可以是我们自造的（例如 3/5/10/29 bus 的简化网络），但结构要能映射到 PyPSA Network。
- 保持现有 PRD 的结果产物形式：results/tables/*.csv、results/figures/*.png、results/summary.md。
- 必须能跑两类对照：
  (A) 有网络约束（PyPSA LOPF + lines/links）
  (B) 无网络约束（单母线/铜板：把所有 bus 合并或用极大线路容量近似）
  输出关键指标：curtailment、线路拥塞比例、shadow price/等价指标（若可）、以及 A vs B 的差异。
- 代码风格：模块化，清晰函数签名，最少依赖，带 README 运行说明。