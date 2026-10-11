#!/usr/bin/env python3
"""Read-only v0.1 file/AST/evidence contract, not a firmware safety validator."""
import argparse
import ast
import json
from pathlib import Path
import sys

EXPECTED = {
    'tools/release_scan.py', 'tools/scan_for_firmware.py',
    'tools/scan_for_private_data.py', 'tools/scan_for_presets.py',
    'tools/scan_nested_archives.py', 'tools/check_readme_bilingual.py',
    'tools/check_public_surface.py', 'tools/gen_synthetic_coefficients.py',
    'tools/gen_synthetic_icons.py', 'tools/_fixture_output.py',
    'tests/test_release_checks.py',
}
FORBIDDEN_IMPORTS = {'firmware', 'sd_package', 'validate_candidate', 'gr3_lineage', 'rollback_gate'}
LEVELS = {'DEVICE VERIFIED', 'INHERITED BY STRUCTURAL EQUIVALENCE',
          'OFFLINE_BUILD_VERIFIED', 'STATIC_VERIFIED', 'UNKNOWN', 'RESEARCH_ONLY'}
GOLDEN = '93588df2bb84bdf121df48c42ff582e9cc8cbdcd21f2046276d30d239fcd9465'
PARENT = 'a2fcd40bc0897231a7e1fddcb8f8cd7c8b9f70bbc94514cfda724ff18adb7db7'
OFFICIAL = 'd6a3c9c288d784080e7b283222ecdd8752adfeed6faa36dab44f73115354bfd4'

def check(root):
    root = Path(root)
    failures = []
    if not root.is_dir() or root.is_symlink():
        return {'status': 'FAIL', 'failures': ['missing/invalid public root']}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*.py')}
    if actual != EXPECTED:
        failures.append({'unexpected': sorted(actual - EXPECTED), 'missing': sorted(EXPECTED - actual)})
    for p in root.rglob('*'):
        if p.is_symlink() or p.name == '.git' or p.suffix.lower() in ('.sh', '.exe', '.dll', '.so', '.dylib'):
            failures.append('unexpected executable/link/history: ' + p.relative_to(root).as_posix())
    for name in sorted(actual):
        try:
            tree = ast.parse((root/name).read_text())
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    modules = [node.module or ''] if isinstance(node, ast.ImportFrom) else [x.name for x in node.names]
                    for module in modules:
                        top = module.split('.')[0]
                        reviewed_local = {Path(p).stem for p in EXPECTED if p.startswith('tools/')}
                        if top in FORBIDDEN_IMPORTS or top not in sys.stdlib_module_names | reviewed_local:
                            failures.append(name + ': unreviewed import ' + top)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in ('build', 'repack', 'verify_package', 'check_binding'):
                    failures.append(name + ': removed production function')
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('eval', 'exec', '__import__'):
                    failures.append(name + ': dynamic code execution')
        except (OSError, SyntaxError, UnicodeError) as exc:
            failures.append(name + ': ' + type(exc).__name__)
    try:
        register = json.loads((root/'references/evidence-register.json').read_text())
        if set(register['levels']) != LEVELS:
            failures.append('inconsistent evidence levels')
        if register['golden_candidate_sha256'] != GOLDEN or register['parent_candidate_sha256'] != PARENT:
            failures.append('historical candidate binding differs')
        if register['official_root_sha256'] != OFFICIAL:
            failures.append('official baseline binding differs')
        rows = register['features']
        required = {'six-slot', 'Grain', 'per-file identity', 'RAW Development', 'Playback', 'UserData / U / BOX', 'official bootable restore', 'RAM / RAW object'}
        if {r['feature'] for r in rows} != required:
            failures.append('missing/unexpected core evidence feature')
        for row in rows:
            if row['firmware_baseline'] != OFFICIAL:
                failures.append('unknown feature baseline: ' + row['feature'])
            if row['evidence_level'] not in LEVELS or not row['limitations'] or not row['evidence_source']:
                failures.append('invalid evidence row: ' + row['feature'])
            if row['feature'] in {'six-slot', 'per-file identity', 'RAW Development', 'Playback', 'UserData / U / BOX'} and row['evidence_level'] != 'INHERITED BY STRUCTURAL EQUIVALENCE':
                failures.append('retained historical path promoted to direct device: ' + row['feature'])
            if row['evidence_level'] == 'INHERITED BY STRUCTURAL EQUIVALENCE' and row.get('inherited_from_sha256') != PARENT:
                failures.append('missing inherited source binding')
            if row['evidence_level'] == 'DEVICE VERIFIED' and row.get('device_tested_candidate_sha256') != GOLDEN:
                failures.append('direct candidate binding absent')
        for name in ('SKILL.md', 'references/evidence-model.md'):
            text = (root/name).read_text()
            if not all(level in text for level in LEVELS):
                failures.append(name + ': missing canonical level')
        for name in ('README.md', 'SKILL.md'):
            if 'CLEAN_PUBLIC_HISTORY_REQUIRED' not in (root/name).read_text():
                failures.append(name + ': missing clean-history contract')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        failures.append('missing/invalid evidence structure: ' + type(exc).__name__)
    return {'status': 'FAIL' if failures else 'PASS', 'failures': failures,
            'python_files': sorted(actual), 'claim': 'v0.1 release contract only; NOT A SAFETY VALIDATOR'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root')
    args = parser.parse_args()
    report = check(args.root)
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
