#!/usr/bin/env python3
"""xsh 构建：消费 ../XACT-CRT 的 include + lib/x86_64，输出 out/xsh.elf。"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # xsh/
OUT  = ROOT / "out"

SOURCES = ["main.c"]
TARGET  = OUT / "xsh.elf"

# XACT CRT（../XACT-CRT）：启动对象 + 静态运行时 + 分配器
CRT_ROOT = ROOT / ".." / "XACT-CRT"
INC      = CRT_ROOT / "include"
LIB      = CRT_ROOT / "lib" / "x86_64"
CRT_OBJS = [LIB / "crt0.o", LIB / "start.o"]
CRT_LIBS = [LIB / "libxact.a", LIB / "liballoc.a"]

def rel(p):
    p = Path(p)
    if p.exists():
        try:
            return str(p.relative_to(ROOT))
        except ValueError:
            return str(p)
    return str(p)


def esc(p):
    return rel(p).replace("$", "$$").replace(":", "$:").replace(" ", "$ ")


def main():
    cc   = os.environ.get("CC",  "clang")
    cxx  = os.environ.get("CXX", "clang++")
    ld   = os.environ.get("LD",  "ld")
    opt  = "-O" + os.environ.get("OPT_LEVEL", "2")
    col  = os.environ.get("DIAGNOSTICS_COLOR", "-fdiagnostics-color=always")

    common = (f"{col} {opt} -Wall -g -ffreestanding -fno-builtin -m64 -mstackrealign "
              "-fno-stack-protector -fno-exceptions -fno-strict-aliasing -fshort-wchar -nostdinc")
    c_flags   = f"{common} -std=c11   -I {rel(INC)} -I . -MMD -MP"
    cpp_flags = f"{common} -std=c++11 -I {rel(INC)} -I . -Wno-write-strings -MMD -MP"

    L = ["# xsh 构建（消费 ../XACT-CRT）",
         "ninja_required_version = 1.10",
         f"cc = {cc}", f"cxx = {cxx}", f"ld = {ld}",
         f"c_flags = {c_flags}", f"cpp_flags = {cpp_flags}", ""]
    L += [
        "rule cc",
        "  command = mkdir -p $$(dirname $out) && $cc $c_flags -MF $out.d -c $in -o $out",
        "  depfile = $out.d", "  deps = gcc", "",
        "rule cxx",
        "  command = mkdir -p $$(dirname $out) && $cxx $cpp_flags -MF $out.d -c $in -o $out",
        "  depfile = $out.d", "  deps = gcc", "",
        "rule link",
        "  command = $ld -Ttext=0x200000 $in -o $out", "",
    ]

    app_objs = []
    for src in SOURCES:
        rule = "cc" if src.endswith(".c") else "cxx"
        obj = OUT / (src + ".o")
        L += [f"build {esc(obj)}: {rule} {esc(ROOT / src)}"]
        app_objs.append(obj)
    L += [""]

    ins = CRT_OBJS + app_objs + CRT_LIBS
    L += [f"build {esc(TARGET)}: link {' '.join(esc(o) for o in ins)}", ""]
    L += ["build all: phony " + esc(TARGET), "default all", ""]
    L += ["rule clean", "  command = rm -rf out", "build clean: clean"]

    (ROOT / "build.ninja").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("已生成 build.ninja（xsh）。构建：ninja")


if __name__ == "__main__":
    main()

