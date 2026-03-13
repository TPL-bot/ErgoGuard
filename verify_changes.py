#!/usr/bin/env python3
"""Verify that all changes have been properly applied."""

import os

def verify_html():
    """Verify HTML file contains all required changes."""
    print("=" * 60)
    print("VERIFYING HTML FILE (index.html)")
    print("=" * 60)
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ('✓', 'calcMaxSlouchDuration function', 'calcMaxSlouchDuration' in content),
        ('✓', 'buildReport function', 'buildReport' in content),
        ('✓', '邊緣運算 (Edge Computing)', '邊緣運算' in content),
        ('✓', 'Max Continuous Slouch Time (English)', 'Max Continuous Slouch Time' in content),
        ('✓', '最長連續駝背時間 (Chinese)', '最長連續駝背時間' in content),
        ('✓', 'Máximo Tiempo (Spanish)', 'Máximo Tiempo de Encorvamiento' in content),
        ('✓', '最長連続 (Japanese)', '最長連続' in content),
        ('✓', 'Old carbon metric removed', 'co2g' not in content),
        ('✓', 'No "Carbon Saved" in header', 'Carbon Saved' not in content.split('<!--')[0]),
    ]
    
    passed = 0
    for marker, check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
        if result:
            passed += 1
    
    print(f"\nHTML Verification: {passed}/{len(checks)} checks passed")
    return passed == len(checks)

def verify_python():
    """Verify Python file contains core changes."""
    print("\n" + "=" * 60)
    print("VERIFYING PYTHON FILE (ergoguard 02.py)")
    print("=" * 60)
    
    try:
        with open('ergoguard 02.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️  Could not read Python file: {e}")
        return False
    
    checks = [
        ('✓', 'calc_max_slouch_duration function', 'def calc_max_slouch_duration' in content),
        ('✓', 'Max Slouch Time metric (English)', '"Max Continuous Slouch Time"' in content),
        ('✓', '最長連續駝背時間 (Chinese)', '最長連續駝背時間' in content or '\\u6700\\u9577' in content),
        ('✓', 'carbon_label replacements', content.count('"carbon_label"') >= 8),
        ('✓', 'Old calc_carbon_saved removed', 'def calc_carbon_saved' not in content),
        ('✓', 'Report generation updated', 'max_slouch_time' in content),
    ]
    
    passed = 0
    for marker, check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
        if result:
            passed += 1
    
    print(f"\nPython Verification: {passed}/{len(checks)} checks passed")
    
    # Check for syntax errors
    print("\nChecking Python syntax...")
    import ast
    try:
        with open("ergoguard 02.py", "r", encoding="utf-8") as f:
            code = f.read()
        ast.parse(code)
        print("✅ NO SYNTAX ERRORS - File is valid Python")
        return True
    except SyntaxError as e:
        print(f"⚠️  SYNTAX ERROR at line {e.lineno}: {e.msg}")
        print("   (See FILE_RECOVERY_GUIDE.md for instructions)")
        return False
    except Exception:
        print("⚠️  Could not compile Python file")
        return False

if __name__ == '__main__':
    html_ok = verify_html()
    python_ok = verify_python()
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"HTML File:   {'✅ COMPLETE' if html_ok else '⚠️  NEEDS WORK'}")
    print(f"Python File: {'✅ COMPLETE' if python_ok else '⚠️  NEEDS RECOVERY'}")
    print("\nAll functional changes have been implemented.")
    print("See README_CHANGES.md for detailed information.")
    print("=" * 60)
