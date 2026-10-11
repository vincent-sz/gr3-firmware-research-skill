# Playback DISP

> Historical architecture note, not current executable capability or new camera
> acceptance. Exact versions, evidence levels and limitations:
> [evidence-register.md](evidence-register.md). v0.1 does not build or validate firmware.


Playback shows, per file: the identity icon + name, the first nine Image Control
parameters and the Grain strength — all from the PHOTO's own metadata.

## Identity bridge

```
DNG code -> property 37 ordinal 13..18 -> public/display 30..35
  -> existing icon/name resources + per-file parameter callbacks
```

Factory 0x0100..0x010B keep their identity/icon/name and their first-nine parameters.

## Per-file parameters

The playback data object exposes a 141-entry property array. Tag `0x0247` indices import
into it: indices 0..6 -> properties 38..44 (saturation, hue, tone, contrast, highlight
contrast, shadow contrast, sharpness — reusing factory conversion rules), index 9 ->
property 49 (shading), index 10 -> property 50 (clarity), index 19 -> property 140
(Grain). The Grain display reuses the factory string table (`-- / 1 / 2 / 3` via the
native `0/3/2/1` scale).

## The tenth row

The native playback builder emits nine rows; the framework appends a tenth (Grain) row by
reusing the original callbacks and a small code addition. Factory monochrome playback
returns never call the added callback. The per-file read source is the photo object —
current camera state must never be consulted (change the current settings, old photos
must look unchanged).

## property 140

Property 140 sits in the existing array (object + 0x3BC) and is covered by the existing
init/clear and the 564-byte per-file copy. Before reuse it was audited for business
consumers (none found beyond this feature); it remains a per-file cache, not durable
state.
