#!/usr/bin/env python3
"""Synthetic adversarial release checks; no firmware, real credentials or devices."""
import gzip
import io
import json
import lzma
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
import release_scan
import check_public_surface
import gen_synthetic_coefficients
import gen_synthetic_icons
from _fixture_output import fresh_output, write_fixture

REMOVED = ['scripts/firmware.py', 'scripts/sd_package.py', 'scripts/fit_cube.py',
           'tools/validate_candidate.py', 'tools/gr3_lineage.py', 'tools/rollback_gate.py']

def zipped(name, data):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as archive:
        archive.writestr(name, data)
    return stream.getvalue()

def tarred(name, data, link=False):
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w') as archive:
        entry = tarfile.TarInfo(name)
        if link:
            entry.type = tarfile.SYMTYPE
            entry.linkname = 'elsewhere'
            archive.addfile(entry)
        else:
            entry.size = len(data)
            archive.addfile(entry, io.BytesIO(data))
    return stream.getvalue()

class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='gr3-release-test-')
        self.work = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def scan_file(self, name, data, mode='all'):
        p = self.work/name
        p.write_bytes(data)
        return release_scan.run([str(p)], mode)

    def call(self, tool, *args):
        return subprocess.run([sys.executable, str(ROOT/tool), *map(str, args)], capture_output=True, text=True)

    def test_clean_extensionless_and_json(self):
        (self.work/'NOTICE').write_text('Independent research, no payload.\n')
        (self.work/'sample.json').write_text('{"description":"synthetic documentation"}')
        for mode in ('all', 'firmware', 'privacy', 'presets', 'archives'):
            self.assertEqual(release_scan.run([str(self.work)], mode)['status'], 'PASS')

    def test_missing_directory_and_no_paths(self):
        for mode in ('all', 'firmware', 'privacy', 'presets', 'archives'):
            self.assertEqual(release_scan.run([str(self.work/'missing')], mode)['status'], 'FAIL')
        self.assertEqual(release_scan.run([])['status'], 'FAIL')

    def test_symlink_and_unknown_binary(self):
        target = self.work/'opaque'; target.write_bytes(bytes(range(256)))
        link = self.work/'link'; link.symlink_to(target)
        self.assertEqual(release_scan.run([str(link)])['status'], 'FAIL')
        self.assertEqual(release_scan.run([str(target)])['status'], 'FAIL')

    def test_extensionless_private_path(self):
        text = '/' + 'Users/' + 'ReviewFixture/private'
        self.assertEqual(self.scan_file('NOTICE', text.encode(), 'privacy')['status'], 'FAIL')

    def test_extensionless_secret_markers(self):
        texts = ['sk-' + 'z'*24, '-----BEGIN ' + 'DEMO PRIVATE KEY-----', 'review' + '@' + 'example.invalid']
        for text in texts:
            self.assertEqual(self.scan_file('LICENSE', text.encode(), 'privacy')['status'], 'FAIL')

    def test_small_preset_carriers(self):
        for suffix in ('.cube', '.xmp', '.dcp'):
            self.assertEqual(self.scan_file('synthetic'+suffix, b'synthetic carrier', 'presets')['status'], 'FAIL')

    def test_numeric_and_encoded_payloads(self):
        self.assertEqual(self.scan_file('sample.json', json.dumps(list(range(100))).encode(), 'presets')['status'], 'FAIL')
        self.assertEqual(self.scan_file('encoded.txt', b'A'*600)['status'], 'FAIL')

    def test_nested_archive_known_carrier(self):
        data = zipped('inner.zip', zipped('synthetic.bin', b'GATE-ONLY' * 70000))
        result = self.scan_file('outer.zip', data, 'firmware')
        self.assertEqual(result['status'], 'FAIL')
        self.assertTrue(any(x['kind']=='FIRMWARE_OR_PHOTO_CARRIER' for x in result['findings']))

    def test_nested_archive_private_and_preset(self):
        private = ('/'+'Users/'+'ReviewFixture/private').encode()
        self.assertEqual(self.scan_file('private.zip', zipped('NOTICE', private), 'privacy')['status'], 'FAIL')
        self.assertEqual(self.scan_file('preset.zip', zipped('synthetic.xmp', b'synthetic'), 'presets')['status'], 'FAIL')

    def test_common_archives_clean(self):
        tar = tarred('notes.txt', b'Harmless synthetic research note.\n')
        samples = [('notes.tar',tar), ('notes.tar.gz',gzip.compress(tar)), ('notes.tgz',gzip.compress(tar)),
                   ('notes.tar.xz',lzma.compress(tar)), ('notes.txt.gz',gzip.compress(b'Research note.')),
                   ('notes.zip',zipped('notes.txt',b'Research note.')),
                   ('notes.xz',lzma.compress(b'Research note.'))]
        # TAR zero padding compresses very efficiently; this small valid input remains under the ratio ceiling.
        for name,data in samples:
            with self.subTest(name=name):
                result = self.scan_file(name,data)
                self.assertEqual(result['status'], 'PASS', result['findings'])

    def test_common_archives_reject_carrier(self):
        tar = tarred('synthetic.bin',b'FIXTURE ONLY')
        for name,data in [('notes.tar',tar),('notes.tgz',gzip.compress(tar)),('notes.tar.xz',lzma.compress(tar))]:
            self.assertEqual(self.scan_file(name,data,'firmware')['status'],'FAIL')

    def test_corrupt_and_truncated_containers(self):
        for name,data in [('bad.zip',b'not a zip'),('bad.tar',b'not a tar'),('bad.gz',gzip.compress(b'note')[:-4]),
                          ('bad.xz',lzma.compress(b'note')[:-4]),('short.zip',zipped('x.txt',b'note')[:-10])]:
            self.assertEqual(self.scan_file(name,data)['status'],'FAIL')

    def test_unexpected_extra_data(self):
        z=zipped('notes.txt',b'note')
        for name,data in [('trail.zip',z+b'unexpected'),('lead.zip',b'unexpected'+z),('trail.tar',tarred('notes.txt',b'note')+b'unexpected')]:
            self.assertEqual(self.scan_file(name,data)['status'],'FAIL')

    def test_unsafe_archive_names_links_duplicates(self):
        for name,data in [('traversal.zip',zipped('../outside.txt',b'note')),('link.tar',tarred('link',b'',True))]:
            self.assertEqual(self.scan_file(name,data)['status'],'FAIL')
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w') as z:
            z.writestr('A.txt',b'note');z.writestr('a.txt',b'note')
        self.assertEqual(self.scan_file('duplicate.zip',stream.getvalue())['status'],'FAIL')

    def test_encrypted_and_unsupported_archive(self):
        data=bytearray(zipped('notes.txt',b'note'));struct.pack_into('<H',data,6,1)
        i=data.index(b'PK\x01\x02');struct.pack_into('<H',data,i+8,1)
        self.assertEqual(self.scan_file('encrypted.zip',bytes(data))['status'],'FAIL')
        self.assertEqual(self.scan_file('opaque.7z',b'unsupported')['status'],'FAIL')

    def test_archive_depth_and_bomb(self):
        data=b'Research note.'
        for _ in range(6):data=zipped('inner.zip',data)
        self.assertEqual(self.scan_file('deep.zip',data)['status'],'FAIL')
        self.assertEqual(self.scan_file('bomb.gz',gzip.compress(b'0'*(1024*1024)))['status'],'FAIL')

    def test_size_total_and_item_bounds(self):
        p=self.work/'oversize';p.write_bytes(b'x'*(release_scan.MAX_FILE+1))
        self.assertEqual(release_scan.run([str(p)])['status'],'FAIL');p.unlink()
        for i in range(4):(self.work/str(i)).write_text('tiny')
        with patch.object(release_scan,'MAX_ITEMS',3):self.assertEqual(release_scan.run([str(self.work)])['status'],'FAIL')
        with patch.object(release_scan,'MAX_TOTAL',3):self.assertEqual(release_scan.run([str(self.work)])['status'],'FAIL')

    def test_no_old_production_surface_for_original_cases(self):
        for case in ('truncated input','unregistered append','wrong guard','wrong official SHA','modified root',
                     'corrupted container','unexpected extra data','invalid bounds','missing required structure'):
            for name in REMOVED:
                self.assertFalse((ROOT/name).exists(),case+': '+name)
        self.assertEqual(check_public_surface.check(ROOT)['status'],'PASS')

    def test_each_retained_cli_rejects_production_flags(self):
        for tool in sorted(check_public_surface.EXPECTED):
            if tool.startswith('tests/') or tool.endswith('_fixture_output.py'):continue
            result=self.call(tool,'--factory','missing.bin','--guards','missing.json','--apply')
            self.assertNotEqual(result.returncode,0,tool)
            self.assertNotIn('VALIDATED SAFE',result.stdout)
        self.assertFalse((self.work/'candidate').exists())

    def test_restored_unsafe_tool_and_unregistered_append_fail_surface(self):
        clone=self.work/'public';shutil.copytree(ROOT,clone)
        (clone/'tools/extra.py').write_text('def repack(): return True\n')
        self.assertEqual(check_public_surface.check(clone)['status'],'FAIL')

    def test_evidence_wrong_root_and_promotion_and_missing_structure(self):
        clone=self.work/'public';shutil.copytree(ROOT,clone);p=clone/'references/evidence-register.json';original=p.read_text()
        for mutation in ('root','promotion','missing'):
            doc=json.loads(original)
            if mutation=='root':doc['official_root_sha256']='f'*64
            if mutation=='promotion':doc['features'][0]['evidence_level']='DEVICE VERIFIED'
            if mutation=='missing':del doc['features']
            p.write_text(json.dumps(doc));self.assertEqual(check_public_surface.check(clone)['status'],'FAIL')

    def test_bilingual_current_pass_and_legal_loss_fail(self):
        self.assertEqual(self.call('tools/check_readme_bilingual.py',ROOT/'README.md').returncode,0)
        doc=(ROOT/'README.md').read_text();zh,en=doc.split('# English Version',1)
        p=self.work/'README.md';p.write_text(zh+'# English Version'+en.replace('item 4','item unknown'))
        self.assertNotEqual(self.call('tools/check_readme_bilingual.py',p).returncode,0)

    def test_synthetic_coefficients_and_icon_bounds(self):
        blob=gen_synthetic_coefficients.identity_540();self.assertEqual(len(blob),2160)
        values=struct.unpack('<540i',blob);self.assertTrue(all(-2048<=v<=2047 for v in values))
        for n in range(1,7):self.assertEqual(len(gen_synthetic_icons.make_icon(n)),6400)
        for n in (0,7,-1,'1',True):
            with self.assertRaises(ValueError):gen_synthetic_icons.make_icon(n)

    def test_fixture_output_no_overwrite_no_outside_no_bad_name(self):
        fresh=self.work/'fresh';fresh_output(str(fresh));write_fixture(fresh,'note.txt',b'fixture')
        with self.assertRaises(ValueError):fresh_output(str(fresh))
        with self.assertRaises(FileExistsError):write_fixture(fresh,'note.txt',b'changed')
        outside = Path(tempfile.gettempdir()).resolve().parent / 'gr3-forbidden-fixture-output'
        with self.assertRaises(ValueError):fresh_output(str(outside))
        with self.assertRaises(ValueError):write_fixture(outside.parent,'note.txt',b'outside')
        with self.assertRaises(ValueError):write_fixture(fresh,'fwdc239b.bin',b'not firmware')
        with self.assertRaises(ValueError):write_fixture(fresh,'../bad',b'x')
        with self.assertRaises(ValueError):write_fixture(fresh,'oversize',b'x'*65537)
        self.assertEqual((fresh/'note.txt').read_bytes(),b'fixture')

    def test_fixture_clis_deterministic(self):
        for script in ('gen_synthetic_coefficients.py','gen_synthetic_icons.py'):
            first=self.work/(script+'-one');second=self.work/(script+'-two')
            self.assertEqual(self.call('tools/'+script,first).returncode,0)
            self.assertEqual(self.call('tools/'+script,second).returncode,0)
            self.assertEqual({p.name:p.read_bytes() for p in first.iterdir()},{p.name:p.read_bytes() for p in second.iterdir()})
            self.assertNotEqual(self.call('tools/'+script,first).returncode,0)

    def test_each_scan_cli_clean_and_missing(self):
        (self.work/'NOTICE').write_text('Harmless research note.')
        for name in ('release_scan.py','scan_for_firmware.py','scan_for_private_data.py','scan_for_presets.py','scan_nested_archives.py'):
            self.assertEqual(self.call('tools/'+name,self.work).returncode,0)
            self.assertNotEqual(self.call('tools/'+name,self.work/'missing').returncode,0)

if __name__=='__main__':
    unittest.main(verbosity=2)
