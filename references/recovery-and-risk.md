# Recovery & Rollback

## Two different questions — never conflate them

### 1. Firmware recovery (bootability)

- **Historically reported (exact source-candidate binding incomplete):** while the camera still boots normally, official firmware was reported to be
  re-flashed through the standard update flow.
- **NOT verified:** complete boot failure, interrupted flashing, flash corruption or
  bootloader failure. **NO VERIFIED RECOVERY PATH.**
- Re-flashing official firmware is not "brick rescue"; it presumes a bootable camera.

### 2. Persistent-state compatibility (after rollback)

When custom identities (public 30..35), custom Grain, private records or U/BOX snapshots
exist, and the user either (a) reflashes official firmware or (b) installs a candidate that
removes custom features, the official/new firmware must read the persistent state safely.

**Current GR III findings (design-level, static):**

- All durable writes of custom identities pass a **sanitizer** that maps custom identities
  to a base factory value (11) before anything is written into the native schema
  (`write_entry` on the 0xb26 record; `container_copy` for U/BOX snapshots). The native
  UserData therefore never contains 30..35.
- Custom state beyond that lives in **private domains**: private per-slot records
  (`CFnSTATE`-style files), custom Grain keys, private tables and resources. Official
  firmware does not read those files; it reads only its own schema, which contains
  legal values.
- On this design, **returning to official firmware with custom state present is
  considered design-safe for the persisted native state**; the custom artifacts are simply
  ignored by the official firmware.

**Honest limits:**

- No systematic on-device "custom state → official reflash" validation has been performed
  for GR III; the conclusion above is design + static evidence, not device evidence.
- The enumeration of durable write paths cannot be proven exhaustive by static analysis
  alone. Treat the conclusion as "no known unsafe path", not "no unsafe path possible".

## Pre-rollback normalization (recommended, low cost)

Because full-risk elimination is not proven, the following optional procedure is
**recommended before rolling back to official firmware**:

1. In the camera UI, switch the active Image Control back to a factory identity
   (e.g. Standard) for each affected slot group.
2. Save settings / power-cycle so the camera persists that state through its own flow.
3. (Optional) keep a copy of the private files for later restoration.

These steps merely move the user-visible state to values the official firmware reads
natively; they require no special tooling. They do **not** replace the warning that
complete boot failure has no verified recovery path.

## Feature removal is unproven

A future workflow that removes persistent features must stop at
`ROLLBACK_STATE_COMPATIBILITY_NOT_PROVEN`. v0.1 includes no rollback validator,
SD staging or firmware write helper. This is a research constraint, not a validated
production pipeline. Exact historical evidence and limits are registered in
[evidence-register.md](evidence-register.md).
