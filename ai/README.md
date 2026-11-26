# ai/

Records of how AI was used on this project: the specifications given to it, and the logs it kept.

In general, my process is:

1. Brainstorm what I want to create.
2. Write a specification.
3. Have Claude implement the specification.
4. Review the implementation line-by-line, making edits or asking Claude to fix things.

For more involved tasks, I replace step (2) with the plan feature provided by Claude to guide
implementation upfront.

| File | What it is |
|---|---|
| `Analog_AI_Documentation.md` | Log of every AI-assisted analog task: what was asked, what the AI did, what was checked |
| `TOKEN_LOG.md` | Token cost of the AI-driven gLayout work |
| `TOPLEVEL_FLOW.md` | Design draft of the macro layout flow (`analog/layout_tools/top.py`) |
| `analog_API_infrastructure_design.md` | Design notes of the LLM sizing loop (`explore/analog_API_infrastructure/`) |
| `SIM_LOG.md` | Simulation log of the neuron, from the first Schmitt-trigger neuron to the sized one |
| `mock.txt`, `serializer_tdm.txt` | Early specifications: Verilog models of the network, a serializer |
| `pasted-content-*.md` | Plans for the Verilog model of the network and the first mixed-signal simulation |

These are records: paths and designs in them are as they were at the time (see
[`explore/README.md`](../explore/README.md) for what changed).
