# Image Control Slot Framework

> Historical architecture note, not current executable capability or new camera
> acceptance. Exact versions, evidence levels and limitations:
> [evidence-register.md](evidence-register.md). v0.1 does not build or validate firmware.


The framework adds **six additional Image Control slots** to a standard GR III 2.10 while
leaving factory slots untouched (factory 11..24 keep their semantics; Custom 1/2 stay in
place). Current verified mapping range:

| namespace | values |
|---|---|
| public | 30..35 |
| shooting menu row | 12..17 |
| processing entry | 26..31 |
| DNG `0x4f` code | 0x010C..0x0111 |
| name resource ID | 791..796 |
| icon resource ID | 672,673,674,675,676,671 |
| Grain file base | 24 + slot*3 (+ group) |

## Mechanism (what a build installs)

- **Shared backend + per-slot descriptor/config.** A fixed set of ~111 hook addresses
  (identical for the two-slot and six-slot builds — `NEW_SLOT_REQUIRE_NEW_HOOKS = NO`);
  new slots add descriptors, isolated basis data, durable identity and resources, not new
  hook classes.
- **Routing**: the image-control consumer reads the public identity from shooting state
  (`+0x77c`); custom publics branch to entry `26+slot` in the generated basis/descriptor
  tables; a converter seam reuses the native color path.
- **Parameter state**: per-slot RAM banks at `data + 0xb28 + slot*60 + group*20 + field*2`
  (10 fields; three groups are Image-Control groups, not U1/U2/U3). Allocation seeds every
  slot × group; the slot index is always an explicit internal argument, never inferred.
- **Selection/restore**: selection writes the chosen identity into the UserData selection
  bytes (`+0x1c2/+0x1c4/+0x1c6`, one per group); restore feeds the native submission
  record before the native bulk apply.
- **Persistence**: the legacy native UserData schema stays `0xb26`; a sanitizer maps
  custom identities to base 11 before any durable write; per-slot private records and
  Grain keys stay in the private domain; U/BOX snapshots use the same sanitizer.
- **Names/icons**: UTF-16LE name descriptors + 21-language lookup for IDs 791+; 40x40
  RGBA package-label icons; both reuse existing resource consumers.

**Invariant:** a new slot is complete only when shooting UI/rendering, parameter
persistence, DNG per-file identity, RAW restore/UI/rendering, Playback identity/icon/name
and per-file parameters (and Grain, where supported) are ALL wired. Anything less is
INCOMPLETE SLOT EXPANSION.
