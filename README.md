# XSH

XSH (X Shell) 是一个基于 C 语言开发的命令行工具项目，使用 Ninja 作为构建系统。

## 项目简介

该项目是一个轻量级的命令行工具，由以下核心组件构成：

- **main.c** - C 语言实现的主程序入口
- **gen_ninja.py** - Python 脚本，用于生成 Ninja 构建文件

## 技术栈

- **编程语言**: C
- **构建系统**: Ninja
- **构建配置生成**: Python

## 构建说明

项目使用 Ninja 进行构建。首先需要通过 `gen_ninja.py` 生成构建文件：

```bash
python3 gen_ninja.py
```

然后使用 Ninja 编译项目：

```bash
ninja
```

## 运行

编译完成后，可执行文件的运行方式取决于程序的实际功能。通常为：

```bash
./xsh [参数]
```

## 项目结构

```
.
├── gen_ninja.py    # Ninja 构建文件生成器
├── main.c          # 主程序源代码
└── LICENSE         # 许可证文件
```

## 许可证

请查看 LICENSE 文件了解具体的许可证条款。