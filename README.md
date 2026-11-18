# STM32 Forge

STM32CubeMX CLI、IOC 离线编译工具、MCP Server 与开发 Skill 集合。

本仓库的 `mcp/cubemx1/`、`mcp/mcp_server.py`、`docs/` 和 `skills/stm32cubemx1-config/` 移植自 [sanrenmu/STM32CubeMX-Config-Skill-and-MCP](https://github.com/sanrenmu/STM32CubeMX-Config-Skill-and-MCP)，按其 MIT License 再发布；版权与许可声明见 [LICENSE](LICENSE)。其余 `src/stm32_forge/` 为本项目适配代码。

## 能力

- 离线将目标 JSON 编译为 STM32CubeMX `.ioc`
- 导入 `.ioc`、校验/反解配置及项目生成
- 从本机 CubeMX 数据库查询器件、外设、引脚、板卡和时钟
- stdio MCP 工具与 MCP resources
- `stm32cubemx1-config` Skill，含命令、协议与工作流参考
- 兼容的 `stm32-forge` CLI，用于 IOC JSON 导入/导出与 CubeMX 调用

上游实现固定面向 STM32CubeMX 1.x，并在 Skill/协议文档中注明已验证的版本边界。实际生成仍依赖本机 CubeMX 与对应固件包。

## 快速开始

需要 Python 3.8+。移植的核心和 MCP Server 使用 Python 标准库，无需安装 MCP SDK。

```powershell
cd F:\deepseek\stm32-forge
$env:PYTHONPATH = (Join-Path (Get-Location) 'mcp')
python -m cubemx1 --help
```

Windows 也可以直接调用仓库根目录的启动器：

```powershell
.\cubemx1.cmd --help
```

## 配置 CubeMX

创建 `%USERPROFILE%\.cubemx1\machine.json`，至少提供安装目录：

```json
{
  "cubemx_home": "C:\\Users\\<user>\\AppData\\Local\\Programs\\STM32CubeMX",
  "repository": "C:\\Users\\<user>\\STM32Cube\\Repository"
}
```

也可使用 `CUBEMX1_MACHINE` 指向配置文件。离线 `ioc build` 与查询读取 CubeMX 安装目录数据库；原生项目生成需要 CubeMX 和对应固件包。

## 主要工作流

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'mcp')
python -m cubemx1 ioc build .\target.json
python -m cubemx1 ioc generate .\project.ioc
python -m cubemx1 probe peripherals --device <device>
python -m cubemx1 probe describe --device <device> <IP>
```

目标 JSON 字段和 MCP 工具契约见 [docs/PROTOCOL.md](docs/PROTOCOL.md) 与 [mcp/PROTOCOL.md](mcp/PROTOCOL.md)。更完整的示例和按需参考入口见 [Skill](skills/stm32cubemx1-config/SKILL.md)。

## MCP 注册

将下列配置加入 MCP 客户端，并把路径替换为本机仓库绝对路径：

```json
{
  "mcpServers": {
    "cubemx1": {
      "command": "python",
      "args": ["<repo>/mcp/mcp_server.py"],
      "cwd": "<repo>"
    }
  }
}
```

MCP 提供 IOC build/import/check/generate、探测查询和会话状态工具；支持资源 `cubemx1://protocol/target` 与 `cubemx1://protocol/mcp`。完整清单在 [mcp/mcp.json](mcp/mcp.json)。

安装后推荐使用：

```powershell
cubemx1-mcp
```

源码目录也可以直接运行：

```powershell
python .\mcp\mcp_server.py
```

安装后同时提供 `cubemx1`（离线 IOC/查询 CLI）、`stm32-forge`（兼容 CLI）和 `stm32-forge-mcp`（原生 Forge MCP）入口。

## 原有 Forge 命令

安装本项目的兼容工具：

```powershell
python -m pip install -e .
stm32-forge config
stm32-forge ioc-import .\project.ioc --output .\project.json
stm32-forge ioc-create --input .\target.json --output .\project.ioc
```

兼容工具配置自动探测常见 Windows CubeMX 安装目录；独立的 `cubemx1` 核心则遵循上述 `CUBEMX1_MACHINE` 配置格式。
