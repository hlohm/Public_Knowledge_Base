---
type: "term"
branch: "Hardware & Architecture"
tags: ["hardware", "modern"]
status: "note"
---

# Branch Divergence

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

The performance penalty on a SIMT machine when threads in the same warp take different paths through a conditional, forcing the hardware to run each path serially with the inactive lanes masked off.

**Context.** The precise reason GPUs are bad at branchy, irregular, pointer-chasing code. Data-parallel work where every lane does the same thing runs at full width; control-heavy work collapses toward serial. It's the structural counterpart to a CPU's branch misprediction — same enemy (control flow), different failure mode.

## See also

- [[SIMT]]
- [[Warp]]
- [[Branch Prediction]]
