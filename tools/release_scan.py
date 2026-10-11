#!/usr/bin/env python3
"""Bounded, read-only release containment scans. PASS is not device safety.

Archives are inspected in memory, never extracted. Every file is classified;
unknown binary content, unsafe archives and unreadable inputs fail the scan.
The patterns detect selected risks, not every possible secret or encoded payload.
"""
import argparse
import bz2
import gzip
import hashlib
import io
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tarfile
import zipfile

MAX_FILE = 8 * 1024 * 1024
MAX_TOTAL = 64 * 1024 * 1024
MAX_ITEMS = 4096
MAX_DEPTH = 4
MAX_RATIO = 200
KNOWN = {
    'd6a3c9c288d784080e7b283222ecdd8752adfeed6faa36dab44f73115354bfd4',
    '53da690797f35ad6dc2c429d8ca1d0de8e333c211ed959816813982cd093b703',
    '93588df2bb84bdf121df48c42ff582e9cc8cbdcd21f2046276d30d239fcd9465',
}
FIRMWARE_EXT = {'.bin', '.dat', '.fw', '.img', '.rom', '.elf', '.dng', '.jpg', '.jpeg'}
PRESET_EXT = {'.cube', '.xmp', '.dcp', '.lut', '.3dl', '.icc', '.icm'}
PRIVACY = [
    (r'/Users/[A-Za-z][A-Za-z0-9._-]*', 'personal home path'),
    (r'/home/[A-Za-z][A-Za-z0-9._-]*', 'personal home path'),
    (r'/Vol' + r'umes/[^\s"\x27`]+', 'local volume path'),
    (r'\bVinc' + r'ent\b', 'private project owner name'),
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', 'email'),
    (r'\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b', 'credential pattern'),
    (r'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----', 'private key marker'),
]
ARCHIVE_SUFFIX = ('.zip', '.tar', '.tar.gz', '.tgz', '.gz', '.tar.xz', '.txz', '.xz', '.bz2', '.tbz2', '.7z', '.rar', '.zst')
ENCODED = re.compile(r'(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{512,}={0,2}(?![A-Za-z0-9+/])')

class ScanError(Exception):
    pass

class Scanner:
    def __init__(self, mode):
        self.mode = mode
        self.findings = []
        self.items = 0
        self.bytes = 0
        self.archives = 0
        self.text_files = 0
        self.halted = False

    def finding(self, path, kind, detail=''):
        # Do not echo detected secrets into logs.
        self.findings.append({'path': path, 'kind': kind, 'detail': detail})

    def account(self, size, item=True):
        if size < 0 or size > MAX_FILE:
            raise ScanError('per-file decompression/read ceiling exceeded')
        self.bytes += size
        self.items += int(item)
        if self.bytes > MAX_TOTAL or self.items > MAX_ITEMS:
            self.halted = True
            raise ScanError('total byte/item ceiling exceeded')

    def metadata(self, text, label):
        if self.mode in ('privacy', 'all'):
            for pattern, kind in PRIVACY:
                if re.search(pattern, text):
                    self.finding(label, 'PRIVACY_PATTERN', kind)

    def safe_name(self, name):
        parts = PurePosixPath(name).parts
        return bool(name) and not name.startswith('/') and '\\' not in name and ':' not in name and '..' not in parts

    def archive_kind(self, name, data):
        low = name.lower()
        if data.startswith((b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08')) or low.endswith('.zip'):
            return 'zip'
        if data.startswith(b'\x1f\x8b') or low.endswith(('.gz', '.tgz')):
            return 'gz'
        if data.startswith(b'\xfd7zXZ\x00') or low.endswith(('.xz', '.txz')):
            return 'xz'
        if data.startswith(b'BZh') or low.endswith(('.bz2', '.tbz2')):
            return 'bz2'
        if data[257:262] == b'ustar' or low.endswith('.tar'):
            return 'tar'
        if low.endswith(ARCHIVE_SUFFIX) or data.startswith((b'7z\xbc\xaf\x27\x1c', b'Rar!')):
            return 'unsupported'
        return None

    def payload(self, name, data, label, depth=0):
        if self.halted:
            return
        self.metadata(name, label)
        suffix = Path(name).suffix.lower()
        if self.mode in ('firmware', 'all'):
            if suffix in FIRMWARE_EXT or hashlib.sha256(data).hexdigest() in KNOWN:
                self.finding(label, 'FIRMWARE_OR_PHOTO_CARRIER')
            if b'RICOH' in data[:512] and b'\xa5\x5a\x5a\xa5' in data[:512]:
                self.finding(label, 'FIRMWARE_CONTAINER_MARKERS')
        if self.mode in ('presets', 'all') and suffix in PRESET_EXT:
            self.finding(label, 'PRESET_CARRIER', 'carrier rejected at every size')
        kind = self.archive_kind(name, data)
        if kind:
            self.archives += 1
            try:
                if depth >= MAX_DEPTH:
                    raise ScanError('archive recursion ceiling exceeded')
                self.archive(kind, name, data, label, depth + 1)
            except (OSError, EOFError, ValueError, RuntimeError, ScanError, zipfile.BadZipFile, tarfile.TarError, lzma.LZMAError) as exc:
                self.finding(label, 'UNINSPECTED_ARCHIVE', type(exc).__name__ + ': ' + str(exc)[:160])
            return
        try:
            text = data.decode('utf-8')
            if '\x00' in text:
                raise UnicodeError('NUL in text')
        except UnicodeError:
            self.finding(label, 'UNRECOGNIZED_BINARY', 'requires manual review; not ignored')
            return
        self.text_files += 1
        self.metadata(text, label)
        if ENCODED.search(text):
            self.finding(label, 'ENCODED_PAYLOAD_REQUIRES_REVIEW', 'long base64/hex-like token')
        if self.mode in ('presets', 'all') and suffix == '.json':
            try:
                obj = json.loads(text)
            except ValueError:
                self.finding(label, 'UNPARSED_JSON', 'cannot inspect potential data carrier')
                return
            stack = [obj]
            while stack:
                value = stack.pop()
                if isinstance(value, list):
                    if len(value) > 64 and all(isinstance(x, (int, float)) for x in value):
                        self.finding(label, 'NUMERIC_PAYLOAD_REQUIRES_REVIEW')
                    stack.extend(value)
                elif isinstance(value, dict):
                    if {'lut_3d', 'lut_data', 'preset_data', 'coefficient_data'} & set(value):
                        self.finding(label, 'PRESET_DATA_FIELD')
                    stack.extend(value.values())

    def member(self, name, data, label, depth):
        self.account(len(data))
        self.payload(name, data, label, depth)

    def archive(self, kind, name, data, label, depth):
        if kind == 'unsupported':
            raise ScanError('unsupported archive format')
        if kind == 'zip':
            if not data.startswith((b'PK\x03\x04', b'PK\x05\x06')):
                raise ScanError('unexpected ZIP leading data')
            end = data.rfind(b'PK\x05\x06')
            if end < 0 or end + 22 > len(data):
                raise ScanError('missing ZIP end record')
            comment_len = int.from_bytes(data[end+20:end+22], 'little')
            if end + 22 + comment_len != len(data):
                raise ScanError('unexpected ZIP trailing bytes')
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                seen = set()
                self.metadata(archive.comment.decode('utf-8'), label + '!comment')
                for entry in archive.infolist():
                    if self.halted:
                        break
                    key = entry.filename.rstrip('/').casefold()
                    if not self.safe_name(entry.filename) or key in seen:
                        raise ScanError('unsafe or duplicate archive member')
                    seen.add(key)
                    self.metadata(entry.filename, label + '!member-name')
                    self.metadata(entry.comment.decode('utf-8'), label + '!member-comment')
                    file_type = stat.S_IFMT(entry.external_attr >> 16)
                    if entry.flag_bits & 1 or file_type not in (0, stat.S_IFREG, stat.S_IFDIR) or entry.extra:
                        raise ScanError('encrypted or linked archive member')
                    if entry.is_dir():
                        self.account(0)
                        continue
                    if entry.file_size > MAX_FILE or entry.file_size > max(1, entry.compress_size) * MAX_RATIO:
                        raise ScanError('ZIP decompression size/ratio ceiling exceeded')
                    with archive.open(entry) as stream:
                        decoded = stream.read(MAX_FILE + 1)
                    if len(decoded) != entry.file_size:
                        raise ScanError('ZIP member length mismatch')
                    self.member(entry.filename, decoded, label + '!' + entry.filename, depth)
            return
        if kind == 'tar':
            with tarfile.open(fileobj=io.BytesIO(data), mode='r:') as archive:
                seen = set()
                for entry in archive:
                    if self.halted:
                        break
                    key = entry.name.rstrip('/').casefold()
                    if not self.safe_name(entry.name) or key in seen:
                        raise ScanError('unsafe or duplicate TAR member')
                    seen.add(key)
                    self.metadata(entry.name + ' ' + entry.uname + ' ' + entry.gname + ' ' + json.dumps(entry.pax_headers), label + '!metadata')
                    if entry.isdir():
                        self.account(0)
                        continue
                    if not entry.isfile() or entry.size > MAX_FILE:
                        raise ScanError('linked/special/oversized TAR member')
                    stream = archive.extractfile(entry)
                    if stream is None:
                        raise ScanError('unreadable TAR member')
                    with stream:
                        decoded = stream.read(MAX_FILE + 1)
                    if len(decoded) != entry.size:
                        raise ScanError('TAR member length mismatch')
                    self.member(entry.name, decoded, label + '!' + entry.name, depth)
                if any(data[archive.offset:]):
                    raise ScanError('unexpected TAR trailing bytes')
            return
        if kind == 'gz':
            if len(data) < 10 or data[:3] != b'\x1f\x8b\x08' or data[3] & 0xe4:
                raise ScanError('unsupported/invalid GZ header or extra fields')
            pos = 10
            for flag in (8, 16):
                if data[3] & flag:
                    end = data.find(b'\x00', pos)
                    if end < 0 or end - pos > 512:
                        raise ScanError('uninspectable GZ metadata')
                    value = data[pos:end].decode('utf-8')
                    self.metadata(value, label + '!gz-metadata')
                    if flag == 8:
                        suffix = Path(value).suffix.lower()
                        if self.mode in ('firmware', 'all') and suffix in FIRMWARE_EXT:
                            self.finding(label, 'FIRMWARE_OR_PHOTO_CARRIER')
                        if self.mode in ('presets', 'all') and suffix in PRESET_EXT:
                            self.finding(label, 'PRESET_CARRIER')
                    pos = end + 1
            with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
                decoded = stream.read(MAX_FILE + 1)
        elif kind == 'xz':
            decoder = lzma.LZMADecompressor(memlimit=MAX_TOTAL)
            decoded = decoder.decompress(data, max_length=MAX_FILE + 1)
            if not decoder.eof or decoder.unused_data:
                raise ScanError('incomplete/concatenated XZ requires review')
        else:
            decoder = bz2.BZ2Decompressor()
            decoded = decoder.decompress(data, max_length=MAX_FILE + 1)
            if not decoder.eof or decoder.unused_data:
                raise ScanError('incomplete/concatenated BZ2 requires review')
        if len(decoded) > MAX_FILE or len(decoded) > max(1, len(data)) * MAX_RATIO:
            raise ScanError('compressed-stream size/ratio ceiling exceeded')
        low = name.lower()
        if low.endswith(('.tgz', '.txz', '.tbz2')):
            inner = name.rsplit('.', 1)[0] + '.tar'
        elif low.endswith(('.gz', '.xz', '.bz2')):
            inner = name.rsplit('.', 1)[0]
        else:
            inner = 'decompressed'
        self.member(inner, decoded, label + '!' + inner, depth)

    def filesystem(self, root):
        label = root.name or '.'
        if not root.exists() or root.is_symlink():
            self.finding(label, 'INVALID_SCAN_ROOT', 'missing path or symlink')
            return
        pending = [(root, label)]
        while pending and not self.halted:
            path, shown = pending.pop()
            try:
                info = path.lstat()
                if path.name in ('.git', '.DS_Store', '__pycache__') or path.suffix == '.pyc':
                    self.finding(shown, 'DEVELOPMENT_ARTIFACT')
                if stat.S_ISLNK(info.st_mode):
                    self.finding(shown, 'UNINSPECTED_LINK')
                elif stat.S_ISDIR(info.st_mode):
                    self.account(0)
                    pending.extend((p, shown + '/' + p.name) for p in sorted(path.iterdir(), reverse=True))
                elif stat.S_ISREG(info.st_mode):
                    self.account(info.st_size)
                    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
                    with os.fdopen(fd, 'rb') as stream:
                        data = stream.read(MAX_FILE + 1)
                    if len(data) != info.st_size or len(data) > MAX_FILE:
                        raise ScanError('file changed during scan or size exceeded')
                    self.payload(path.name, data, shown)
                else:
                    self.finding(shown, 'UNINSPECTED_SPECIAL_FILE')
            except (OSError, ScanError) as exc:
                self.finding(shown, 'READ_OR_LIMIT_ERROR', type(exc).__name__)

def run(roots, mode='all'):
    scanner = Scanner(mode)
    if not roots:
        scanner.finding('.', 'INVALID_SCAN_ROOT', 'no scan paths supplied')
    for root in roots:
        scanner.filesystem(Path(root))
    return {
        'scanner': 'release_scan:' + mode,
        'status': 'FAIL' if scanner.findings else 'PASS',
        'scope': [Path(r).name or '.' for r in roots],
        'limits': {'per_file_bytes': MAX_FILE, 'total_processed_bytes': MAX_TOTAL, 'items': MAX_ITEMS, 'archive_depth': MAX_DEPTH, 'decompression_ratio': MAX_RATIO},
        'coverage': {'items': scanner.items, 'processed_bytes': scanner.bytes, 'archives': scanner.archives, 'text_files': scanner.text_files},
        'findings': scanner.findings,
        'claim': 'No findings were detected by the release scanner within the scanned release tree and archives.' if not scanner.findings else 'Findings or uninspected inputs require resolution.',
        'limitations': 'Selected patterns and carrier policies only; no proof of absence, authorship, device safety, future commits, external filesystems or private history.',
    }

def main(mode='all'):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('roots', nargs='+')
    args = parser.parse_args()
    result = run(args.roots, mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
