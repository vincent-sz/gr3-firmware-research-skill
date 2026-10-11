# Evidence register / 证据台账

This register is an available-record summary, not a new device acceptance. 原始实机回执由维护者记录；本次只核对来源记录和差异摘要，未操作相机。历史结论不得赋予当前发布检查器或未来 candidate。

Official root: `d6a3c9c288d784080e7b283222ecdd8752adfeed6faa36dab44f73115354bfd4`  
Final historical golden: `93588df2bb84bdf121df48c42ff582e9cc8cbdcd21f2046276d30d239fcd9465`  
Parent: `a2fcd40bc0897231a7e1fddcb8f8cd7c8b9f70bbc94514cfda724ff18adb7db7`

Canonical machine-readable rows: [evidence-register.json](evidence-register.json). Source/limits: [historical-evidence-summary.md](historical-evidence-summary.md).

| Feature | Level at final golden | Source and limitations |
|---|---|---|
| six-slot | INHERITED BY STRUCTURAL EQUIVALENCE | public 30..35 / processing 26..31 / isolated shared framework. Historical whole-build user acceptance, not individual measurements for every slot/combination. |
| Grain | DEVICE VERIFIED | Legacy color metadata exclusion-vector correction; retained native shooting/RAW/Playback paths inherit separately. 2026-10-09 recorded user report that the correction worked; not every strength/slot combination, not flash readback, not a new camera test by this reviewer. |
| per-file identity | INHERITED BY STRUCTURAL EQUIVALENCE | capture Path A / DNG 0x010C..0x0111 / RAW restore. Only selected historical files were individually read back; do not invent six-slot exhaustive file measurements. |
| RAW Development | INHERITED BY STRUCTURAL EQUIVALENCE | six-slot list / As Shot / rendering / native Grain. Historical version-linked report plus static/offline checks; no fresh final-golden exhaustive camera test. |
| Playback | INHERITED BY STRUCTURAL EQUIVALENCE | identity/icon/name / per-file parameters / native Grain formatter. Preserved paths inherited; new legacy-color encoding correction has its separate direct report. Old unsupported metadata does not recover strength. |
| UserData / U / BOX | INHERITED BY STRUCTURAL EQUIVALENCE | sanitizer / private state / shared persistence architecture. Whole-build acceptance does not prove every durable write or U/BOX combination; sanitizer conclusions are static; systematic rollback compatibility NOT FULLY PROVEN. |
| official bootable restore | UNKNOWN | Historical report of official restore while camera still boots. Exact source-candidate binding in the available restore receipt is incomplete. Do not assert direct restore evidence for the final golden, arbitrary custom state or complete boot failure. |
| RAM / RAW object | STATIC_VERIFIED | Historical runtime RAW allocation of 0x800 bytes, 3 x 20 x 17 parameter model. Static source notes / prior desktop checks only. Heap/stack peaks, fragmentation and RAM headroom not measured. One-word zero-growth delta does not mean total RAW RAM cost is zero. |

Core feature paths have version-linked device validation and extensive static/offline regression coverage. Not every possible feature combination has been exhaustively tested on-device.

核心功能路径具有版本关联的实机报告和大量静态 / 离线回归；并非所有组合都在相机上穷举。直接报告覆盖 final golden 的此次 Grain 修复；其余保留路径按 parent 与有限差异证据登记为继承。无法关联精确候选的官方恢复报告保守标为 UNKNOWN。所有原始记录均未打包；不得根据摘要虚构额外测量。

A changed candidate requires new evidence. RESEARCH_ONLY applies outside supported architecture and to missing provenance/bounds/ownership; release scan PASS is never device evidence.
