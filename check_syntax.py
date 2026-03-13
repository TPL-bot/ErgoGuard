import ast
import sys

try:
    with open("ergoguard 02.py", "r", encoding="utf-8") as f:
        code = f.read()
    ast.parse(code)
    print("✅ No syntax errors found")
    sys.exit(0)
except SyntaxError as e:
    print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
    if e.text:
        print(f"   Text: {e.text.strip()}")
    sys.exit(1)
