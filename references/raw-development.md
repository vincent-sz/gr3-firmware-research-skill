# RAW Development

> Historical architecture note, not current executable capability or new camera
> acceptance. Exact versions, evidence levels and limitations:
> [evidence-register.md](evidence-register.md). v0.1 does not build or validate firmware.


The in-camera RAW Development path receives the same six additional slots.

## Object model

- The RAW parameter object is a **runtime heap allocation of 0x800 bytes** (allocated on
  first use, released on destruction; a transient heap cost of ≈ +0x800 bytes).
- Parameter area: base `+0x400`, row stride 17, group stride 340, rows 20
  (`3 groups × 20 rows × 17 fields`); maximum write offset `< 0x800`.
- Selectors 0..12 keep factory meanings; selector 13 stays reserved; custom slots occupy
  selectors **14..19**, with public 30..35 mapping onto them one-to-one.
- The RAW list capacity is 21 items (including the optional "As Shot" row).

## Identity restoration

RAW Development must restore the PHOTO's own identity: DNG `0x4f` codes 0x010C..0x0111
load back to publics 30..35 (factory 0x0100 still falls back to Standard). Never read the
current shooting/RAW/global state to guess a historical photo.

## Grain in RAW

The RAW Grain setter/getter/commit/export path uses the same UI conversion
(OFF/weak/medium/strong = 0/3/2/1) as shooting. Factory monochrome RAW Grain behavior is
preserved unchanged.

## Bounds discipline

Any build touching the RAW object must prove: allocated object sufficient, indexing legal,
no over-read/overwrite, next structure untouched. Runtime state added by the framework is
persistent-state-only (`runtime_state_ram_delta = 0` semantic); heap/stack headroom is
NOT proven.
