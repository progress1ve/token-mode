"""Install the skill and optionally a minimal global recovery block."""
import argparse
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- token-mode:start -->"
END = "<!-- token-mode:end -->"


def install(target, instruction=None, update=False):
    target = Path(target).expanduser().resolve()
    if target.exists() and not update:
        raise ValueError("Skill exists; review it before using --update")
    previous = instruction.read_text(encoding="utf-8") if instruction and instruction.exists() else ""
    if previous.count(START) != previous.count(END) or previous.count(START) > 1:
        raise ValueError("Malformed instruction markers; repair before installation")
    if START in previous and previous.index(END) < previous.index(START):
        raise ValueError("Reversed instruction markers")
    helper = (target / "scripts/mode.py").as_posix()
    skill = (target / "SKILL.md").as_posix()
    block = f'''{START}
## Chat token mode
Default economy. On “экономь” / “economy mode”, “подробно” / “не экономь” / “режим контроля” / “detailed mode”, or $token-mode, read {skill} and persist the requested chat mode. Explicit switches last until changed; one-off detail requests need not switch.
At turn start and after compaction read `python "{helper}" get`. Other clients must pass --chat with a stable conversation ID; if unavailable, use handoff-only persistence and disclose it. Latest user instruction wins. Carry mode in every handoff.
Economy: required updates normally one sentence (15–25 words), final normally 2–5 short lines; no routine tool narration, repeated plans or mode announcements. Follow required cadence and report material risks/blockers. Focus reads, bound output, reuse evidence, avoid redundant checks. Detailed: show scope, decisions, changes, checks and production risks. Both: finish authorized work with necessary verification and approval boundaries. Never change model/settings or promise perfect recall or fixed savings.
{END}'''
    if instruction:
        if START in previous:
            left, rest = previous.split(START, 1)
            _, right = rest.split(END, 1)
            text = left + block + right
        else:
            text = previous + ("\n\n" if previous else "") + block + "\n"
    for source in (ROOT / "skills/token-mode").rglob("*"):
        if source.is_file():
            dest = target / source.relative_to(ROOT / "skills/token-mode")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
    if instruction:
        instruction.parent.mkdir(parents=True, exist_ok=True)
        instruction.write_text(text, encoding="utf-8")
    return target


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--client", choices=["codex", "claude", "generic"], required=True)
    p.add_argument("--skill-dir", type=Path)
    p.add_argument("--instruction-file", type=Path)
    p.add_argument("--persistent", action="store_true")
    p.add_argument("--update", action="store_true")
    a = p.parse_args()
    home = Path.home()
    codex = Path(os.getenv("CODEX_HOME", str(home / ".codex")))
    override = codex / "AGENTS.override.md"
    global_codex = override if override.exists() and override.read_text(encoding="utf-8").strip() else codex / "AGENTS.md"
    target = a.skill_dir or (home / (".agents" if a.client == "codex" else ".claude") / "skills/token-mode")
    if a.client == "generic" and (not a.skill_dir or (a.persistent and not a.instruction_file)):
        p.error("generic requires --skill-dir and, with --persistent, --instruction-file")
    instruction = (a.instruction_file or (global_codex if a.client == "codex" else home / ".claude/CLAUDE.md")) if a.persistent else None
    print("Installed: " + str(install(target, instruction, a.update)))
    if instruction:
        print("Recovery instructions: " + str(instruction))


if __name__ == "__main__":
    main()
