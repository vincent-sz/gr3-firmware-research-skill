# Persistence — UserData, U/BOX, Private State

> Historical architecture note, not current executable capability or new camera
> acceptance. Exact versions, evidence levels and limitations:
> [evidence-register.md](evidence-register.md). v0.1 does not build or validate firmware.


## Design rule (the safety core)

Custom identities (public 30..35) **never appear in the native UserData schema**.
Every durable write path passes a **sanitizer** that maps custom identities to a base
factory value (11) before anything is stored:

- the native UserData record (`0xb26`): copy → sanitize → write → byte-exact readback;
  a slot's selected flag is only committed when the native write succeeded;
- U / BOX snapshots: native copy → sanitize (custom identities are never saved into
  U/BOX);
- everything else custom lives in **private domains**: per-slot private records,
  custom Grain keys, private tables and resources — which official firmware does not
  read.

Consequence: official firmware (or any firmware without this feature set) reads only
legal factory values from its own schema; custom artifacts are ignored.
`NOT FULLY PROVEN` caveats: static enumeration cannot prove exhaustiveness of durable
write paths, and no systematic on-device "custom state → official reflash" validation
has been performed. See `recovery-and-risk.md` for the recommended (non-mandatory)
pre-rollback normalization.

## Parameter model

- Per-slot RAM banks: `data + 0xb28 + slot*60 + group*20 + field*2` (10 fields; three
  Image-Control groups — not U1/U2/U3).
- The native serialized schema stays `0xb26` (unchanged); the RAM allocation extends to
  `0xb28 + NSLOT*60`; a detached snapshot buffer is allocated/committed per save.
- Allocation seeds **every** configured slot × group with that slot's own preset; the
  slot index is always an explicit internal argument — never inferred from groups or
  allocator registers.

## Selection / restore

- Selection writes the chosen identity into the UserData selection bytes
  (`+0x1c2/+0x1c4/+0x1c6`, one per group); all selected flags are cleared before a native
  write; exactly one selected flag is committed afterwards.
- Restore feeds the native submission record before the native bulk apply (event 130).

## Corruption behavior

Missing / damaged / multiple-selected private records fall back to the base identity
(safe side); private record reads are byte-verified, not status-verified.
