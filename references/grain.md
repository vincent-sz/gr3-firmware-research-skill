# Grain

> Historical architecture note, not current executable capability or new camera
> acceptance. Exact versions, evidence levels and limitations:
> [evidence-register.md](evidence-register.md). v0.1 does not build or validate firmware.


## UI and native encoding

The Image Control "Grain" parameter is native ID 15. UI steps OFF / weak / medium / strong
map to the native enum `0 / 3 / 2 / 1`. The Grain edit page and the sidebar read from the
same native current state — a build must not "fix" only one display entry point.

## Processing

Native grain processing is reused (the monochrome engine); color Image Controls are made
grain-aware by enables/preparation seams, without faking color modes as monochrome.
Per-file Grain for JPEG/DNG lives in photo metadata (tag `0x0247` index 19), written at
capture time from the shooting state — **file encoding is `0/5/3/1`** (OFF/weak/medium/
strong), which the converter maps to the native `0/3/2/1` scale.

## Persistence domains

- Shooting Grain state: native current state `+0x795`, persisted through the private
  Grain keys (`GRG…`), never through factory keys.
- Playback Grain: an importer reads index 19 and stores it into an existing per-file
  property (property 140) of the playback data object; the existing native string table
  displays `-- / 1 / 2 / 3`. Unknown encodings must fall back to a safe OFF, not to an
  invented `N/A` value.

## Legacy note (private chain only — context for the identity lineage)

A historical metadata encoder treated eight factory color publics as "unsupported" and
wrote a fixed value instead of the real strength; newer photos encode correctly. Files
written by older builds cannot recover their true strength — they must not be guessed.

## Rules

- Do not display file encodings directly; do not invent N/A semantics.
- Playback must read the PHOTO's own properties — never the current camera state.
- Off / weak / medium / strong must neither swap values nor fall through to `--`.
