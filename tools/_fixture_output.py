"""Restrict synthetic fixture writes to fresh ordinary temporary directories."""
import os
from pathlib import Path
import tempfile

def temporary_directory(value):
    output = Path(value)
    if output.is_symlink():
        raise ValueError('fixture directory may not be a symlink')
    output = output.resolve(strict=True)
    temp_root = Path(tempfile.gettempdir()).resolve()
    if not output.is_dir() or not output.is_relative_to(temp_root):
        raise ValueError('fixtures must stay under the system temporary directory')
    current = output
    while current != temp_root:
        if current.is_mount():
            raise ValueError('fixture output may not be on a nested mounted volume')
        current = current.parent
    return output

def fresh_output(value):
    output = Path(value)
    temp_root = Path(tempfile.gettempdir()).resolve()
    parent = output.parent.resolve(strict=True)
    if not parent.is_relative_to(temp_root):
        raise ValueError('fixtures must be written under the system temporary directory')
    current = parent
    while current != temp_root:
        if current.is_mount():
            raise ValueError('fixture output may not be on a nested mounted volume')
        current = current.parent
    output = parent / output.name
    if output.name in ('', '.', '..') or output.exists() or output.is_symlink():
        raise ValueError('choose a fresh output directory; no overwrite')
    output.mkdir()
    return output

def write_fixture(output, name, data):
    output = temporary_directory(output)
    names = {'primary-identity-540.bin', 'coefficients-report.json', 'icons-report.json', 'note.txt'} | {f'demo-{n}.rgba' for n in range(1, 7)}
    if name not in names or '/' in name or '\\' in name or len(data) > 65536:
        raise ValueError('invalid synthetic fixture name or size')
    fd = os.open(output / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(data)
