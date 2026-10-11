# Evidence model

Use these exact levels in SKILL and the evidence register. Missing evidence is not a
PASS. Source-record summaries are labeled as such; device experiments were not repeated
for this publication review.

| Level | Meaning |
|---|---|
| DEVICE VERIFIED | Version-linked direct user/device report for the exact candidate and stated scope; no unmeasured combinations implied. |
| INHERITED BY STRUCTURAL EQUIVALENCE | A retained path inherits a prior candidate's report through a cited, limited delta proof; cite parent hash and proof. |
| OFFLINE_BUILD_VERIFIED | Historical build/container/consumer checks for a named candidate; not device evidence or public helper safety. |
| STATIC_VERIFIED | Static bounds, layout, ownership or source reasoning; measurements remain unknown where absent. |
| UNKNOWN | Evidence or precise attribution is incomplete. |
| RESEARCH_ONLY | Outside the supported architecture or missing required evidence; read-only research. |

[evidence-register.md](evidence-register.md) binds features, hashes, sources and limits.
SD readback is file-copy evidence only. v0.1 contains no SD helper, firmware builder or
candidate validator. Release checks inspect documentation/content, never flashing safety.

Core feature paths have version-linked device validation and extensive static/offline
regression coverage. Not every possible feature combination has been exhaustively
tested on-device. RAM headroom and systematic rollback-state compatibility are unproven;
complete boot failure has NO VERIFIED RECOVERY PATH.
