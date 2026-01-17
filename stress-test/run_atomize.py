"""Stress test atomize on various Python files."""
import sys
sys.path.insert(0, '.')

from pathlib import Path
from nlsc.atomize import atomize_to_nl, atomize_python_file

def test_file(filepath: str):
    """Atomize a Python file and show results."""
    path = Path(filepath)
    print(f"\n{'='*60}")
    print(f"FILE: {path}")
    print('='*60)

    try:
        code = path.read_text(encoding='utf-8')
        anlus = atomize_python_file(code)

        print(f"Found {len(anlus)} ANLUs:")
        for anlu in anlus:
            print(f"  - [{anlu['identifier']}]")
            print(f"    PURPOSE: {anlu['purpose'][:60]}...")
            print(f"    INPUTS: {len(anlu['inputs'])}")
            print(f"    LOGIC: {len(anlu.get('logic', []))} steps")
            print(f"    RETURNS: {anlu['returns'][:40]}")

        # Generate .nl content
        nl = atomize_to_nl(code, path.stem)

        # Write output
        out_path = Path('stress-test') / f"{path.stem}.nl"
        out_path.write_text(nl, encoding='utf-8')
        print(f"\nWrote: {out_path}")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    # Test on our own codebase
    test_file('nlsc/resolver.py')
    test_file('nlsc/lockfile.py')
    test_file('nlsc/emitter.py')
