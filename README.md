# Token Mode

[![Checks](https://github.com/progress1ve/token-mode/actions/workflows/check.yml/badge.svg)](https://github.com/progress1ve/token-mode/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Switch a local coding agent between **economical execution** and **detailed oversight**, with a small preference file for each chat. Keep the task complete in both modes.

## Install from chat

Tell your local agent: **Install and use https://github.com/progress1ve/token-mode**.

No long prompt is needed. Agents should follow [INSTALLATION.md](docs/INSTALLATION.md). This is an agent skill with a preference helper, not a native toggle, MCP server or official marketplace plugin.

## Controls

| Say | Mode |
| --- | --- |
| `экономь` / `economy mode` | Concise reporting and focused tool use |
| `режим контроля` / `не экономь` / `подробно` / `detailed mode` | Scope, decisions, changes, checks and production risks |
| `$token-mode` | Show the current mode |

Explicit switches last until changed **within that chat**. A one-off request for a detailed explanation does not have to switch the whole chat. New chats default to economy. Neither mode grants permission to deploy, skips required checks, changes your model or changes reasoning settings.

## Manual installation

Python 3.10+ and a local agent with file/terminal access are required. There are no third-party Python dependencies.

```bash
git clone https://github.com/progress1ve/token-mode.git
cd token-mode
python scripts/install.py --client codex --persistent
```

For Claude Code use `--client claude`; for another client use `--client generic --skill-dir /your/skills/token-mode`. `--persistent` appends a small marked instruction block to the client's global instructions, preserving existing text. Without it only the skill is installed. `--update` permits a reviewed update of an existing skill. Use `--instruction-file` for a client-specific global file.

## Persistence and limits

The helper stores modes outside projects, keyed by `CODEX_THREAD_ID`, falling back to `CODEX_SESSION_ID`. Other clients must supply a stable chat ID with `--chat`. Mode files contain only the mode; hashed filenames avoid storing the raw chat ID. Concurrent chats do not share preferences. A fork with a new ID starts in economy.

The global instruction tells the agent to read state at turn start and after compaction, and to retain the mode in its handoff. **A skill cannot guarantee that a model will follow instructions or preserve a chat ID.** The file makes recovery possible; it does not implement an engine hook. Claude and other clients need an available stable conversation ID for file persistence; otherwise use handoff summaries and disclose the limitation.

One tiny helper call per turn has overhead. The intended savings come from avoiding repeated discovery, excessive output and redundant verification. No savings percentage is promised. The instructions remain short and the full skill is loaded only when relevant.

## Detailed oversight

Use detailed mode for work where you want to inspect the agent's decisions. It reports affected components, significant changes, validation evidence, production implications and recovery options where relevant. Existing authorization rules remain authoritative. Efficient searches and bounded logs still apply.

## Development

```bash
python -m unittest discover -s tests -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [the design notes](docs/DESIGN.md). Tested on Windows/Python 3.13; CI also tests Linux. Client configuration paths for Claude are provided but not validated in a native Claude session.

MIT licensed. Independent project; no affiliation with OpenAI or Anthropic.
