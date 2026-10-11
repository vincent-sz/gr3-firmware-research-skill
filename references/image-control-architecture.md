# Image Control Architecture

> Historical architecture note, not current executable capability or new camera
> acceptance. Exact versions, evidence levels and limitations:
> [evidence-register.md](evidence-register.md). v0.1 does not build or validate firmware.


The framework adds **six additional Image Control slots** to a standard GR III 2.10 while
leaving factory slots untouched (factory 11..24 keep their semantics; Custom 1/2 stay in
place). This document is the namespace / mapping overview; mechanism details are in
`six-slot-framework.md`.

## Namespaces (all separately proven — never infer one from another)

| namespace | values |
|---|---|
| public | 30..35 |
| shooting menu row | 12..17 |
| processing entry | 26..31 |
| DNG `0x4f` code | 0x010C..0x0111 |
| RAW selector | 14..19 (13 reserved) |
| name resource ID | 791..796 |
| icon resource ID | 672,673,674,675,676,671 |
| Grain file base | 24 + slot*3 (+ group) |

**Rule: public / processing / menu / slot-state / group / Grain-index / RAW-selector are
distinct namespaces.** Each is established through its real consumer or xref; numerical
similarity proves nothing. The verified mapping range is `public 30..35 ↔ DNG
0x010C..0x0111` only — do not extrapolate (36 → 0x0112 is NOT verified).

## Routing overview

- The image-control consumer reads the public identity from shooting state (`+0x77c`);
  custom publics branch to processing entry `26+slot` (factory Standard 11 → entry 11,
  Negative 22 → entry 25).
- A converter seam reuses the native color-conversion path; no custom JPEG lifecycle is
  introduced.
- UI rows 12..17 are independent menu rows (not `public - 11`).

## Completion invariant (per new slot)

shooting UI/name/icon + shooting rendering + parameter persistence + DNG per-file
identity + RAW restore/UI/rendering + Playback identity/icon/name + per-file parameters
(+ Grain where supported) must ALL be wired. Anything missing = INCOMPLETE SLOT
EXPANSION — do not announce completion.

## Per-file determinism

As Shot identity, Playback parameters and Playback Grain must come from the photo's own
metadata. Never use current shooting / RAW / global state to guess a historical photo's
identity.
