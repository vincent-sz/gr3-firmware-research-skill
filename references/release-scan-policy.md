# Release scan policy

Run `python3 tools/release_scan.py TREE_OR_ARCHIVE [TREE_OR_ARCHIVE ...]` for the combined
check; wrappers select firmware, privacy, preset or archive-focused findings. All modes
still enforce read/classification/archive limits. Results are JSON, exit 0 means no
findings in that scan, exit nonzero means findings or an uninspected/invalid input.
NOT A SAFETY VALIDATOR: no device or firmware-production conclusion is issued.

## Actual coverage

Every file, including extensionless LICENSE/NOTICE and hidden files, is classified.
Missing/unreadable paths, symlinks, special files, development history/cache, unknown
binary content and exceeded ceilings are failures. Selected privacy patterns inspect
UTF-8 text and names without echoing secret values. Carrier extensions are checked at
all sizes, including small CUBE/XMP/DCP files. Large numeric JSON arrays/data fields and
long base64/hex-like strings require review; arbitrary encodings are not comprehensively
decoded. Documentation references to projects are not treated as copied source/data.

ZIP, TAR, TAR.GZ/TGZ, TAR.XZ/TXZ, standalone GZ/XZ and BZ2 are inspected in memory,
recursively, with no extraction. Encrypted, corrupt, linked, traversal/duplicate-member,
unsupported, trailing-data and otherwise uninspectable archives fail with
UNINSPECTED_ARCHIVE. Compressed streams are bounded, including XZ memory allocation;
unsupported concatenated XZ/BZ2 streams fail for manual review.

Ceilings: 8 MiB per file/expanded stream, 64 MiB cumulative processed bytes, 4096 items,
four archive layers, and 200:1 decompression ratio. Legitimate files exceeding these
ceilings also fail; do not waive the gate without a new review. Inputs should be trusted
local release candidates, not arbitrary hostile files supplied to a network service.

## Claim and exclusions

No findings were detected by the release scanner within the scanned release tree and
archives. 发布扫描器在本次实际扫描的 release tree 与归档内容中未发现命中项。

This wording describes a scan with no findings, not proof that arbitrary private data,
third-party content, proprietary bytes or unusual encoding cannot exist. Review actual
content and available provenance as well. Scans do not inspect external filesystems,
user machines, future commits or deleted content in unrelated private repositories.

## Clean publication history

CLEAN_HISTORY_REQUIRED / CLEAN_PUBLIC_HISTORY_REQUIRED: create a new independent public
repository with a clean first public commit containing only public-repo. Do not fork
or import private development history or copy .git. There is no public history in this
RC; no historical scan is claimed. CI scans a git archive of the current tracked tree;
it does not certify deleted blobs or future commits. Publication is a separate step.

Synthetic generator outputs are temporary technical fixtures and are not included in
the release. An accidentally bundled binary fixture is rejected under the same policy.
