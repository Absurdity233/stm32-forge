---
name: stm32-forge
description: Use for STM32CubeMX command-line project configuration, IOC import/export, peripheral planning, and CubeMX CLI generation.
---

# STM32 Forge

Use `stm32-forge` tools for reproducible STM32 projects.

## Workflow

1. Identify the exact MCU and installed CubeMX firmware package.
2. Keep the desired project state in a JSON file.
3. Generate an IOC with `ioc_create`.
4. Run `cube_generate` to invoke CubeMX CLI.
5. Inspect the generated CMake project and build it with CMake/Ninja.
6. Keep user code outside generated regions and preserve a copy of the IOC.

## Rules

- Query the local CubeMX installation before guessing peripheral names or values.
- Treat pin conflicts, clock-tree errors, and missing firmware packages as actionable errors.
- Report the exact command and paths used for generation.
- Never require the CubeMX GUI for routine project generation.
