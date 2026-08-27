# Tools for the C and Arduino Course

This page lists the software, online tools, and hardware we may use during the C and Arduino course.

You do **not** need to use every tool listed here. There are two main ways to work:

1. **Simpler setup** — easier to install and use when you are getting started.
2. **Professional setup** — closer to the tools used by programmers and engineers, and easier to combine with AI assistance.

If the professional setup becomes confusing, use the simpler setup. You can always move to the professional tools later.

## Arduino Kit and Additional Components

Most of the basic electronics parts we use come in a standard Arduino starter kit. We may also use a few additional components during the course.

See this spreadsheet for:

- what comes in a standard Arduino starter kit;
- additional parts we may use;
- suggested quantities;
- example suppliers; and
- prices and lower-cost purchasing options, including options for students in Ukraine and Europe.

**[Arduino Starter Kit Parts, Additional Components, and Prices](https://docs.google.com/spreadsheets/d/1zhqfNpCi84EwTTPp6kz62bW-rvr_iESCqar_42xgjpg/edit?gid=0#gid=0)**

---

## Option 1: Simpler Setup

This is the easiest way to get started.

### Online C Compiler

**OneCompiler**  
https://onecompiler.com/c

Use this to write and run small C programs directly in your browser. Nothing needs to be installed.

This is useful when we are learning C concepts that do not require an Arduino board.

### Arduino IDE

**Arduino IDE 2**  
https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/

Use the Arduino IDE to write, compile, and upload programs to an Arduino board.

It is less complicated than VS Code and PlatformIO, so this is a good choice if you are having trouble with the professional setup.

---

## Option 2: Professional Setup

The professional setup is:

**VS Code + PlatformIO + an AI coding assistant**

This requires a little more setup, but it is closer to the environment used by professional programmers and engineers.

### Visual Studio Code

**Visual Studio Code (VS Code)** is the main code editor.

We use it together with PlatformIO for Arduino development.

### PlatformIO

**PlatformIO** adds embedded-system and Arduino development tools to VS Code.

It works with Arduino and many other microcontroller platforms.

Getting-started video:  
https://www.youtube.com/watch?v=8W7YjA8kFIY

You can skip the GitHub sections of the video for now if you are not yet using GitHub.

### Windsurf

**Windsurf** can provide AI assistance while you work in VS Code.

If Windsurf repeatedly asks you to authenticate, install or use the extension command:

`Windsurf: Provide Authentication Token`

You can obtain an authentication token here:  
https://windsurf.com/show-auth-token

---

## AI Tools

You should have access to some kind of AI assistant because it can help you:

- explain compiler errors;
- understand unfamiliar C or Arduino code;
- create or check Wokwi circuit JSON;
- troubleshoot wiring and code;
- explain programming concepts; and
- suggest ways to improve a program.

Possible choices include:

| Tool | Notes |
|---|---|
| **ChatGPT** | General programming and electronics assistance. Paid plans are available. |
| **Claude** | Strong programming assistant. Paid plans are available. |
| **DeepSeek** | Lower-cost AI option. |
| **Ollama** | Free. Runs AI models locally on your own computer. |
| **Windsurf** | AI assistance integrated into the coding environment. |

You do not need all of these. Choose one that works well on your computer and internet connection.

---

## Circuit Simulators

Circuit simulators are useful when you do not have the physical components available or want to test a circuit before building it.

### Tinkercad Circuits

https://www.tinkercad.com/dashboard

Tinkercad lets you build and simulate Arduino circuits in a web browser.

It is especially useful for beginners because you can see a visual breadboard, Arduino, wires, LEDs, resistors, and ICs.

### EveryCircuit

https://everycircuit.com/

EveryCircuit is useful for understanding how electronic circuits behave. It can visually show voltage and current changing through a circuit.

We may use it when studying basic electricity, transistors, and logic circuits.

### Wokwi

Wokwi is another useful Arduino and electronics simulator. It works well with VS Code and PlatformIO and can also run projects in a browser.

It is particularly useful when physical hardware is unavailable.

---

## GitHub

We may use **GitHub** to store and share code during the course.

GitHub is useful for:

- downloading lesson code;
- keeping copies of your projects;
- sharing code with your teacher or classmates; and
- learning the version-control workflow used by professional programmers.

You do **not** need to understand GitHub at the beginning of the course. If GitHub is inaccessible where you live, we can use another way to exchange files.

---

## Recommended Setup

### If you are new to programming

Start with:

- OneCompiler for C;
- Arduino IDE for Arduino programs;
- Tinkercad or Wokwi for circuit simulation; and
- one AI assistant.

### If you are comfortable installing development tools

Use:

- VS Code;
- PlatformIO;
- Windsurf or another AI assistant;
- Wokwi and/or Tinkercad; and
- GitHub when available.

The second setup takes more effort at first, but it gives you experience with tools that are much closer to professional software and embedded-systems development.

---

## Video: Getting Started with VS Code and PlatformIO

https://www.youtube.com/watch?v=8W7YjA8kFIY

The video covers the development environment used in the course. You can skip the GitHub sections until we begin using GitHub.

