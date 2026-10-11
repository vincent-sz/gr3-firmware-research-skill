# Path A — Per-File Identity

> Historical architecture note, not current executable capability or new camera
> acceptance. Exact versions, evidence levels and limitations:
> [evidence-register.md](evidence-register.md). v0.1 does not build or validate firmware.


The per-file identity chain persists the shooting slot into the photo and restores it in
RAW Development:

```
shooting public 30..35 -> capture Path A -> DNG 0x4f = 0x010C..0x0111
  -> RAW loader -> same public 30..35
```

## Capture side (Path A)

At the tag-79 serialization site, a small conditional hook reads the shooting state
(`+0x77c`); if the identity is a custom public (30..35) it writes `0x010C+slot` through
the existing uint16 setter; otherwise it executes the complete original encoder with the
original registers. The hook sits at the site that was proven — by controlled on-device
fingerprints — to actually influence the final DNG value (sites merely nearby do not).

## Loader side

The RAW loader's uint16 decode path gets a mirrored conditional hook: codes
0x010C..0x0111 map back to publics 30..35; everything else replays the original decoder.
Factory codes 0x0100..0x010B behave exactly as native.

## Rules

- Only the two conditional sites may change; all other bytes stay identical.
- As Shot identity is per-file deterministic: never inferred from current state.
- Extending the mapping range requires re-proving the FULL chain (public space, DNG code
  space, loader table, Playback decoder, UI capacity) — current verified range is
  30..35 <-> 0x010C..0x0111 only.
