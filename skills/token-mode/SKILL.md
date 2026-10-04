---
name: token-mode
description: Switch persistent chat economy or detailed oversight when the user says экономь, подробно, не экономь, режим контроля, or invokes $token-mode.
---

# Token mode

«Экономь» selects economy; «подробно», «не экономь», «режим контроля» select detailed. Explicit switches last for this chat until changed. A request for one detailed explanation applies only to that answer. Invocation without a mode shows current mode.

Persist switches with `python <skill>/scripts/mode.py economy|detailed`; confirm briefly. Read `mode.py get` on continuation. State uses CODEX_THREAD_ID (fallback CODEX_SESSION_ID), outside projects. Other clients must supply a stable chat ID via --chat; never share a mode across unrelated chats. Without an ID, retain mode in handoffs and disclose unavailable file persistence. Do not change model/settings.

Economy: complete the task with concise updates/results, focused searches, bounded output, batched independent reads and reused evidence. Avoid repeated discovery, unchanged polling and redundant renders/checks. Never omit required verification, risks or blockers.

Detailed: retain efficient tool use while showing scope, affected components, important decisions, concrete changes, checks, production impact and recovery options when relevant. Provide checkpoints under existing approval rules. Do not dump logs or expand scope. Neither mode authorizes deployment.

Include `token-mode: economy|detailed; persists until user switches` in every compaction/handoff. Restore saved mode before continuing after compaction. File state wins over stale summaries; latest user instruction wins over both. Do not promise perfect recall or fixed savings.
