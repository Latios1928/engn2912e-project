"""
Drive the layout flow with one Claude API call (tool runner), without this chat's context.

    pip install anthropic pyyaml
    export ANTHROPIC_API_KEY=...            # or `ant auth login`
    python3 analog/layout_tools/api_driver.py neuron_glayout "build and sign off this cell"
    python3 analog/layout_tools/api_driver.py DAC_binary "what blocks this cell?"

Context sent to the model = AGENT_BRIEF.md (system prompt, cached) + `flow.py status` of the
cell + your request. The model acts only through three tools: run a flow stage, read a flow
artifact, answer a decide question. It cannot edit files or run arbitrary commands.
Token use per call is printed at the end (from the API's usage fields), so TOKEN_LOG.md can
hold measured numbers instead of estimates.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import anthropic
from anthropic import beta_tool

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]             # analog/layout_tools -> project root
PY = REPO / ".venv-glayout/bin/python"
FLOW = HERE / "flow"
STAGES = {"status", "table", "decide", "build", "signoff", "sim", "run"}
MAX_OUT = 6000          # chars of tool output returned to the model


def _flow(*args, timeout=1800) -> str:
    env = {"PDK_ROOT": "/foss/pdks", "PDK": "gf180mcuD", "PATH": "/usr/bin:/bin:/usr/local/bin"}
    p = subprocess.run(["bash", "-lc", "env -u PYTHONPATH " + " ".join(
        [str(PY), str(HERE / "flow.py")] + [f"'{a}'" for a in args])],
        cwd=REPO, capture_output=True, text=True, timeout=timeout, env=env)
    out = "\n".join(l for l in (p.stdout + p.stderr).splitlines()
                    if "INFO" not in l and "Warning" not in l and "warn(" not in l)
    return out[-MAX_OUT:]


@beta_tool
def run_stage(stage: str, cell: str) -> str:
    """Run one stage of the layout flow and return its short status.

    Args:
        stage: one of status, table, decide, build, signoff, sim, run. decide/run answer
            open questions with policy defaults (auto mode) unless the cell is set to manual.
        cell: cell name from flow_cells.yaml, e.g. neuron_glayout.
    """
    if stage not in STAGES:
        return f"error: stage must be one of {sorted(STAGES)}"
    return _flow(stage, cell)


@beta_tool
def read_artifact(cell: str, name: str) -> str:
    """Read a text artifact of a cell from flow/<cell>/ (json, yaml, spice, logs; truncated).

    Args:
        cell: cell name.
        name: file name inside flow/<cell>/, e.g. layout.yaml or signoff.json.
    """
    p = (FLOW / cell / name).resolve()
    if FLOW.resolve() not in p.parents or not p.is_file():
        return f"error: no artifact {name} for {cell}"
    return p.read_text(errors="replace")[:MAX_OUT]


@beta_tool
def answer_question(cell: str, question_id: str, answer: str) -> str:
    """Answer a decide.py question. Only use when the user's request states the answer.

    Args:
        cell: cell name.
        question_id: e.g. Q-dummy_l.
        answer: exactly one of the question's options.
    """
    return _flow("answer", cell, question_id, answer)


def main(cell: str, request: str) -> None:
    client = anthropic.Anthropic()
    brief = (HERE / "AGENT_BRIEF.md").read_text()
    status = _flow("status", cell)
    runner = client.beta.messages.tool_runner(
        model="claude-opus-5-5",
        max_tokens=16000,
        thinking={"type": "adaptive"},
        output_config={"effort": "medium"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",                       # retry on a fallback model if refused
        system=[{"type": "text", "text": brief, "cache_control": {"type": "ephemeral"}}],
        tools=[run_stage, read_artifact, answer_question],
        messages=[{"role": "user",
                   "content": f"Cell: {cell}\n\nCurrent status:\n{status}\n\nRequest: {request}"}],
    )
    tin = tout = tcache = 0
    final = None
    for message in runner:
        u = message.usage
        tin += u.input_tokens
        tout += u.output_tokens
        tcache += getattr(u, "cache_read_input_tokens", 0) or 0
        final = message
    if final is not None and final.stop_reason == "refusal":
        print("request declined:", getattr(final, "stop_details", None))
        return
    for block in final.content if final else []:
        if block.type == "text":
            print(block.text)
    print(f"\n[tokens] input {tin} (cache reads {tcache}), output {tout}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    main(sys.argv[1], " ".join(sys.argv[2:]))
