# Design

Three small layers: a discoverable skill, a global recovery instruction, and an on-disk per-chat mode. No daemon, API key, MCP server, model override or project modification.

Economy changes communication and avoids unnecessary work; it never reduces the agreed scope or necessary checks. Detailed changes observability, not authority. The latest user instruction overrides saved state, which overrides a stale handoff.

After compaction, read the mode file and the compact task handoff, then continue from existing evidence. Do not rerun discovery solely because history was compressed.

To port to another agent, install the skill in its supported location, put the recovery block in its global instructions, and provide a stable conversation ID. No stable ID means handoff-only persistence, not a global shared file.

Switching does not have to read long documentation. State lookup outputs one line. Keep global instructions short and load the skill on switches.
