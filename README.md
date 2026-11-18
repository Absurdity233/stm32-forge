# STM32 Forge

独立的 STM32CubeMX 命令行与 MCP 工具。项目使用 Python 标准库实现，不复制其他项目源码；公开项目只作为功能需求参考。

## 能力

- `.ioc` 导入为结构化 JSON
- 从目标 JSON 生成可追踪的 `.ioc`
- 通过显式配置调用 STM32CubeMX CLI
- stdio MCP Server
- 随项目提供 STM32 开发 Skill

## 安装

```powershell
cd F:\deepseek\stm32-forge
python -m pip install -e .
```

## 配置

创建 `%USERPROFILE%\\.stm32-forge\\config.json`：

```json
{
  "cubemx_home": "C:\\Program Files\\STMicroelectronics\\STM32CubeMX",
  "firmware_repository": "C:\\Users\\Public\\Documents\\STM32Cube\\Repository",
  "cubemx_executable": "C:\\Program Files\\STMicroelectronics\\STM32CubeMX\\STM32CubeMX.exe"
}
```

## 命令行

```powershell
stm32-forge config
stm32-forge ioc-import .\project.ioc --output .\project.json
stm32-forge ioc-create --input .\target.json --output .\project.ioc
stm32-forge generate .\project.ioc .\generated
```

## MCP

```yaml
serverName: stm32-forge
transport: stdio
command: python
args: ["F:\\deepseek\\stm32-forge\\src\\stm32_forge\\mcp.py"]
```

也可以直接运行：

```powershell
stm32-forge-mcp
```

## 说明

CubeMX 不同版本的 CLI 参数存在差异，因此生成命令集中在 `src/stm32_forge/cube.py`，便于按本机版本调整；常规操作全程不需要打开 CubeMX GUI。
