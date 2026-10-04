# Agent-led installation

When the user requests installation:

1. Read README.md and scripts/install.py. Determine the client and a stable tools directory outside the user's project. Do not install just because a URL was mentioned as a reference.
2. Clone or reuse this repository. Preserve local changes. Inspect existing skill and global instructions before updating.
3. Run `python scripts/install.py --client codex --persistent`, or `--client claude`. For other clients supply `--skill-dir` and, for persistence, `--instruction-file`. Installing the requested persistent mode includes the small global instruction block; a skill-only request should omit `--persistent`.
4. Existing skills require `--update`; review local customizations first. The installer merges shipped files and replaces only its own marked instruction block. It does not delete other files or replace unrelated instructions.
5. Read the installed SKILL.md. Check `mode.py get` using this chat's stable ID. Codex exposes CODEX_THREAD_ID in the tested environment. For other clients, supply a stable ID using `--chat`; do not invent one shared by all chats. If unavailable, explain the limitation and preserve mode in summaries.
6. Report what was installed. Existing sessions may need restart/reconnect to discover a new skill. Apply the user's requested mode now; otherwise economy is the default.

The user can then say “экономь” or “режим контроля”. No per-project installation is required.

Global defaults: Codex `~/.codex/AGENTS.md`; Claude `~/.claude/CLAUDE.md`. Codex's `AGENTS.override.md` takes precedence; the installer selects it if it is nonempty. A custom CODEX_HOME is supported.

Official references: [Codex instructions](https://developers.openai.com/codex/guides/agents-md), [Codex skills](https://developers.openai.com/codex/skills/), [Claude skills](https://code.claude.com/docs/en/skills).
