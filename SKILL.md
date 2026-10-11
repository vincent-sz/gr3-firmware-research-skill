---
name: gr3-firmware-research
description: Research historical standard RICOH GR III 2.10 architecture, Image Control, Grain, per-file identity, RAW Development, Playback and persistence using version-bound evidence. v0.1 is a knowledge skill with content/documentation checks and synthetic fixtures; it has no firmware builder, safety validator or SD write capability.
---

# GR III Firmware Research Skill — v0.1

This release is primarily a research knowledge skill. Read the relevant architecture
notes and [evidence register](references/evidence-register.md) before making claims.
It is not a safe firmware production pipeline, modification/distribution service or
flashing tool. Do not reconnect deleted production paths from old or private packages.

## Scope and identity

Historical architecture: standard RICOH GR III, official 2.10, exact root SHA-256
`d6a3c9c288d784080e7b283222ecdd8752adfeed6faa36dab44f73115354bfd4`.
Filenames, displayed versions and user statements are not provenance. Other versions,
GR IIIx / GR IV / HDF, a seventh additional slot or unproven mechanisms remain
RESEARCH_ONLY. This release does not read, download or modify firmware itself.

Six-slot public 30..35 / processing 26..31 / DNG 0x010C..0x0111 / RAW selector 14..19
are historical research boundaries, not a promise that current helpers implement them.
Core feature paths have version-linked device validation and extensive static/offline
regression coverage. Not every possible feature combination has been exhaustively
tested on-device. Direct final-golden evidence covers the recorded color Grain fix;
retained paths inherit the parent report as registered, not an exhaustive final retest.

## Evidence levels — use exactly

| Level | Meaning |
|---|---|
| DEVICE VERIFIED | Exact candidate, stated direct report scope only. |
| INHERITED BY STRUCTURAL EQUIVALENCE | Cite parent hash and the limited-delta source. |
| OFFLINE_BUILD_VERIFIED | Historical named-candidate offline checks; not device safety. |
| STATIC_VERIFIED | Static reasoning; no unperformed measurements. |
| UNKNOWN | Evidence or exact attribution missing. |
| RESEARCH_ONLY | Read-only research outside proven bounds. |

See [evidence-model.md](references/evidence-model.md). New candidates cannot inherit
these labels without new evidence. Do not infer a direct camera test from a scan PASS.

## Stops and user requests

Unknown provenance/model/version, unexplained delta/overlap/state alias, unknown runtime
objects, unproven bounds, opaque code, missing recovery limits, architectural changes,
validation failures or updater/version/security bypass requests require stopping any
proposed production action and reporting the missing evidence. Feature removal without
state-compatibility evidence is ROLLBACK_STATE_COMPATIBILITY_NOT_PROVEN.

In v0.1 every request to build/repack a candidate, validate flashing safety or stage/write
SD is outside the executable surface. Report RESEARCH_ONLY_NOT_RELEASE_GATED; provide
read-only explanation and evidence requirements. Do not generate a candidate, rebuild
removed functions or infer authorization to write devices from a research request.

## Retained helpers

Python 3.10+; standard library only. No automatic installation or networking.

- `tools/release_scan.py` / `scan_for_*.py` / `scan_nested_archives.py`: bounded,
  read-only release-content scans; invalid/uninspected inputs fail. NOT A SAFETY VALIDATOR.
- `tools/check_readme_bilingual.py`: bilingual concepts, not a translation proof.
- `tools/check_public_surface.py`: reviewed file/AST/evidence contract, not firmware safety.
- `tools/gen_synthetic_coefficients.py` / `gen_synthetic_icons.py`: technical identity
  coefficients and generic DEMO tiles; writes only to fresh system-temporary directories,
  no overwrite, no firmware input, no candidate or SD-operation interface.
- `tests/test_release_checks.py`: temporary synthetic adversarial cases only.

Read [release-scan-policy.md](references/release-scan-policy.md) for limits/exclusions.
No candidate builder, repacker, firmware inspect/decode tool, candidate safety validator,
lineage builder, rollback validator, fitter or SD staging/writer is shipped.

## Legal, recovery and publication

Review the [official RICOH terms](https://www.ricoh-imaging.co.jp/english/support/digital/gr3_s.html)
and applicable law before using the research with firmware. The terms restrict
modification/reverse engineering and third-party transfer. Local-only/no-distribution
does not eliminate agreement or legal risk; MIT does not cover firmware or user data.
No firmware hosting, mirrors, download service, uploads, remote modification, distribution
or flashing. No legal guarantee. Read [SAFETY](SAFETY.md).

Complete boot failure / interrupted flashing / flash corruption / bootloader failure:
NO VERIFIED RECOVERY PATH. Systematic rollback-state compatibility NOT FULLY PROVEN.
RAW uses a historical 0x800-byte transient heap object; RAM headroom not proven.

CLEAN_HISTORY_REQUIRED / CLEAN_PUBLIC_HISTORY_REQUIRED: publication must use a new
independent repository and clean first public commit, never private development .git,
old history or a private fork. This RC has no public history. Publication is separate.

## References by research question

- Layout/identity: [firmware-baseline](references/firmware-baseline.md),
  [architecture](references/image-control-architecture.md), [six-slot](references/six-slot-framework.md).
- State/rendering: [Grain](references/grain.md), [persistence](references/persistence-userdata-ubox.md),
  [RAW](references/raw-development.md), [per-file identity](references/per-file-identity.md),
  [Playback](references/playback.md).
- Limits: [recovery](references/recovery-and-risk.md), [evidence register](references/evidence-register.md),
  [historical evidence summary](references/historical-evidence-summary.md),
  [related projects](references/related-projects.md).
