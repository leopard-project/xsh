#!/usr/bin/env python3
"""xsh 构建：消费 ../leopard-sdk 的 obj-tui + include，输出 out/xsh.elf。"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # xsh/
SDK  = ROOT / ".." / "leopard-sdk"              # SDK 根（目录名若不同，改这一行）
INC  = SDK / "include"
OBJ  = SDK / "obj-tui"
OUT  = ROOT / "out"

SOURCES = ["main.c"]
TARGET  = OUT / "xsh.elf"

# SDK 运行时，链接顺序：crt0 入口 → 运行时 → 应用 → liballoc
RUNTIME  = ["crt0.o", "libsys.cpp.o", "xgui_stubs.cpp.o",
            "constart.cpp.o", "xtuiapi.cpp.o", "krlibc.cpp.o"]
LIBALLOC = OBJ / "liballoc-x86_64.a"


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

    L = ["# xsh 构建（消费 ../leopard-sdk）",
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

    ins = [OBJ / n for n in RUNTIME] + app_objs + [LIBALLOC]
    L += [f"build {esc(TARGET)}: link {' '.join(esc(o) for o in ins)}", ""]
    L += ["build all: phony " + esc(TARGET), "default all", ""]
    L += ["rule clean", "  command = rm -rf out", "build clean: clean"]

    (ROOT / "build.ninja").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("已生成 build.ninja（xsh）。构建：ninja")


if __name__ == "__main__":
    main()

