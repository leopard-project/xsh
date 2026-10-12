# XSH

XSH (X Shell) is a command-line tool project developed in C, using Ninja as the build system.

## Project Introduction

This project is a lightweight command-line tool consisting of the following core components:

- **main.c** - Main program entry point implemented in C
- **gen_ninja.py** - Python script used to generate Ninja build files

## Technology Stack

- **Programming Language**: C
- **Build System**: Ninja
- **Build Configuration Generation**: Python

## Build Instructions

The project uses Ninja for building. First, you need to generate the build files via `gen_ninja.py`:

```bash
python3 gen_ninja.py
```

Then compile the project using Ninja:

```bash
ninja
```

## Running

After compilation, the execution method of the executable depends on the actual function of the program. Typically:

```bash
./xsh [arguments]
```

## Project Structure

```
.
├── gen_ninja.py    # Ninja build file generator
├── main.c          # Main program source code
└── LICENSE         # License file
```

## License

Please refer to the LICENSE file for specific license terms.