# PROJECT KNOWLEDGE BASE — xsh

旧版 shell（X Shell），C 实现，Ninja 构建。已被 `leopard-shell`（lpsh）取代——xsh 硬编码
`/apps/%s` 解析命令，lpsh 改为读 `path` 变量。

## 构建
    python3 gen_ninja.py && ninja build   # → out/xsh.elf
    ninja pack

- 静态 ELF，依赖 `../XJ380-SDK/out/crt`（`include/` + `lib/x86_64/`）。
- 新 shell 开发优先走 leopard-shell，不回流到 xsh。
