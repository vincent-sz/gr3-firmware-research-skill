# Historical evidence summary

These are sanitized summaries of available project records inspected on 2026-10-11.
The raw records contain private engineering context and are not distributed. Their
fingerprints bind which notes/reports were read, not their authorship or every claim.
No firmware bytes, original photographs, proprietary resources or preset data appear
in this summary. This review did not rerun firmware emulation or camera experiments.

## Historical device reports

- The maintainer device note records a 2026-10-08 user acceptance associated with the
  parent candidate: six-slot, per-file identity/RAW restoration and Playback/native
  Grain paths. It is a version-linked user report, not camera-flash readback or
  exhaustive per-feature measurements.
- The same note records a 2026-10-09 user report that the final-golden legacy-color
  Grain correction worked. It does not add a new exhaustive acceptance of all retained
  features, all strengths or all combinations.
- The historical build manifest's device_verified=false was a construction-time
  snapshot before the user report. It was not silently changed into device evidence.

## Limited delta evidence

The inspected difference note and validation report bind the parent and golden hashes
listed in the evidence register. They report one changed ARM instruction in the
legacy-color Grain metadata exclusion-vector initialization, no RTOS growth, no new
code cave and unchanged prior RTOS bytes elsewhere. Container checksums were regenerated.
The changed encoder behavior itself is not inherited from the parent.

The desktop validation record reports 1280 encoder cases and 36 file/importer/display
cases. The Playback regression record reports full uint16 identity/Grain domains,
216 native builder cases and unchanged frozen bytes outside the correction. These
are historical OFFLINE_BUILD_VERIFIED records, not newly run tests in the public RC.

This limited delta is the cited basis for INHERITED BY STRUCTURAL EQUIVALENCE on retained
paths. It does not transfer device evidence to a new candidate, a new firmware version,
a new slot range or the public release scanners.

## Recovery and memory

The restore note records successful official restoration from a bootable customized
camera, but the available receipt does not close an exact source-candidate binding.
The register therefore uses UNKNOWN for precise restore attribution. No complete
boot failure recovery or systematic custom-state rollback acceptance is claimed.

The RAW/source notes describe a runtime 0x800-byte transient allocation and the
3 x 20 x 17 parameter model, covered by historical bounds checks. This is static /
desktop evidence; heap/stack peaks, fragmentation and headroom remain unknown. No new
resource measurements were performed during release remediation.

## Inspected source fingerprints

Raw files remain private and are not part of the Public tree. These identifiers and
hashes allow a maintainer to identify the reviewed source records without exposing
absolute paths, personal photo names or private preset identities.

| Source ID | SHA-256 of inspected record |
|---|---|
| DELTA-NOTE | `577e99ce4d518e71ed371c39c4df209c3205eaa26cbc2dbb7f02b94518872fcd` |
| DELTA-VALIDATION | `001e4bf3828aff42d0e1ff7603cd901ebe5582d85f64cb416eb2869e08e3ef99` |
| GOLDEN-MANIFEST | `e154a25a2c12367b1faf011779a627b3d71dde723ffef4ad9e2dfda30246daa4` |
| PLAYBACK-REGRESSION | `16e10389418eab805d59a6d23cd8dad1f47f72c8f3a57417e412a60635e12746` |
| MAINTAINER-DEVICE-NOTE | `f10ae40f9b39cbc7068f5cb415eb54f2a314d3f3862b1008628008d3008e1a2a` |
| MAINTAINER-RAW-NOTE | `76f3513ed9b35879ba5ba98bb083f92eca417858323ce873c2a74f37cc21f4ad` |
| MAINTAINER-SLOT-NOTE | `b15d0c6acaa9f832c453dceec1241625f966e47e3d48894f6e326f2ceeda905b` |
| MAINTAINER-RESTORE-NOTE | `adbb3792bea75c169a1fd78ab6951978d2acfc79ff91aff05041c62ed2b2c82d` |
