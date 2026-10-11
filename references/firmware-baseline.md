# Firmware Baseline (container + identity)

GR III 2.10 official update file (`fwdc239b.bin`):

- 128-byte plaintext header (see `firmware-baseline.md` for fields), then a
  sequence of **frames**, then a 24-byte footer.
- Frames: prefix `uint16` big-endian; `0x8000` bit = raw chunk; otherwise a compressed
  frame using a 16-flag bitstream with back-references (LZ-style). Prefix `0x0000`
  terminates; the footer records compressed length, decoded length and type.
- Two integrity layers: **encoded zero-sum checksum** (whole file, LE32, last word makes
  the sum 0) and **decoded zero-sum checksum** (last word of the decoded image).
  These are ordinary checksums — not cryptographic signatures.
- Decoded image: 59,718,388 bytes for the official 2.10 package; a container of named
  blocks (`RTOS`, `ICONBIN`, `RES` for resources, …). `RTOS` loads at virtual base
  `0x53000000`; both the block length field and the decoded checksum must be updated
  when a build changes the RTOS.
- The default repack insertion point (`0x10C5E30`) equals the RTOS end inside the
  decoded container of the official package — a direct-from-factory build needs no
  insertion adjustments at all.

This is historical format research, not a v0.1 executable capability. No firmware
reader, decoder, repacker, candidate builder or safety validator is shipped. The
historical integrity checks do not establish device safety. Source and scope:
[evidence register](evidence-register.md).

---

**Why version strings are never enough.** RICOH GR III firmware identity is established by
**exact SHA-256 + container/product identity + official-root provenance** — never by the
camera's displayed version, the file name, or a user statement.

## What the container actually contains (GR III 2.10, verified)

The 128-byte container header of the official package carries, among others:

| Offset | Content |
|---|---|
| `+0x00` | `"RICOH"` / `"GR III"` product strings |
| `+0x30` | product/model marker `588` (little-endian) — also used to derive the update file name `FWDC239B.BIN` |
| `+0x38` | **version field A** — four bytes `02 0a 15 1b` |
| `+0x50` | **version field B** — four bytes `02 0a 15 1b` |
| `+0x58` | **build timestamp string** (`2025/09/25 11:28:34 JST` in the official 2.10 package) |
| `+0x78/+0x7c` | `0x024C024C` marker and `0xA55A5AA5` magic |

The updater's type-2 version comparison (function `0x536284e0`) compares **both** four-byte
fields (big-endian `0x020A151B`) with unsigned `<`; **equality is not rejected** (56-case
study, `2026-10-01-firmware-update-gates/version-gate-evidence.json`). The displayed "2.10"
reflects only the first two bytes — the last two bytes (`0x15`, `0x1B`) participate in the
update gate.

**Consequence:** GR III does have version precision beyond the display, plus a build
timestamp. Whether two *distinct* official builds could ever share a displayed "2.10"
is **not established** (single official sample). Therefore:

- display version = informational metadata only;
- exact SHA-256 is the only build identity;
- `INTERNAL VERSION SEMANTICS NOT PROVEN` applies to any stronger claim about internal
  build enumeration.

## Identity and lineage research

Only the exact supported official root is within the historical architecture scope:
`d6a3c9c288d784080e7b283222ecdd8752adfeed6faa36dab44f73115354bfd4`.
Version strings, filenames and user statements are not provenance. Unknown firmware
must remain RESEARCH_ONLY. v0.1 does not accept firmware inputs, build candidates,
emit lineage manifests or authorize SD staging. A future production workflow would
need a separately reviewed identity, ownership, validation and lineage chain.
