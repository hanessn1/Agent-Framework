# 🤖 SOLID Python Agent Framework & MCP Integration

A lightweight, modular, and production-grade **Python AI Agent Framework** built from first principles following **SOLID design principles**.

Features full support for the **ReAct (Perception-Action-Reflection) execution loop**, **Plan-and-Execute goal decomposition**, **real-time token streaming**, and **Anthropic's Model Context Protocol (MCP)** via `stdio` transport.

## ✨ Key Features

- **🔄 ReAct Execution Loop**: Multi-turn `Think -> Act -> Observe -> Reflect` loop that self-corrects malformed inputs and errors automatically.
- **📋 Plan-and-Execute Architecture**: Decouples strategic planning from execution. Deconstructs complex user goals into discrete, state-tracked steps (`pending`, `running`, `completed`).
- **🔌 Model Context Protocol (MCP) Integration**:
  - **MCP Client & Stdio Transport**: Full JSON-RPC 2.0 implementation over `stdio` OS subprocess pipes (`initialize`, `tools/list`, `tools/call`, `resources/read`, `prompts/get`).
  - **Multi-Server Management**: Seamlessly load tools across multiple domain MCP servers into a unified registry.
  - **Production FastMCP Servers**: Built-in support for Anthropic's official `mcp` SDK (`@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`).
- **⚡ Real-Time Token Streaming**: Streams tokens live to stdout while preserving structured JSON tool call payloads.
- **🧩 SOLID & Clean Architecture**: Strict separation of concerns between Agent orchestration (`agent/`), LLM provider layer (`llm/`), Domain tools (`tools/`), Planning (`planner/`), and MCP Infrastructure (`mcp/`).

## 🚀 Quickstart

### 1. Prerequisites & Installation

>  Python 3.11 required

```bash
git clone https://github.com/hanessn1/Agent-Framework.git
cd Agent-Framework
pip install -r requirements.txt
```

### 2. Running local LLMs via Ollama

Start your local Ollama server with a compatible model (e.g. qwen2.5:3b or llama3.2:3b):

```bash
ollama run <model>
```

### 3. Run the Framework

```bash
python main.py
```

