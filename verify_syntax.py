import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the main script section (after <!-- JAVASCRIPT -->)
script_start = content.find('<!-- JAVASCRIPT')
if script_start == -1:
    script_start = content.find('<script>')
    if script_start != -1:
        script_start = content.find('\n', script_start) + 1
else:
    script_start = content.find('<script>', script_start)
    if script_start != -1:
        script_start = content.find('\n', script_start) + 1

script_end = content.rfind('</script>')

if script_start != -1 and script_end != -1:
    script = content[script_start:script_end]
    lines = script.split('\n')
    
    print('✅ Script section found')
    print(f'   Length: {len(script)} bytes ({len(script)//1024}KB)')
    print(f'   Lines: {len(lines)}')
    
    # Check basic structure
    open_braces = script.count('{')
    close_braces = script.count('}')
    open_parens = script.count('(')
    close_parens = script.count(')')
    
    print(f'\n   Braces: {open_braces} open, {close_braces} close', end='')
    if open_braces == close_braces:
        print(' ✓')
    else:
        print(' ✗ MISMATCH')
        
    print(f'   Parens: {open_parens} open, {close_parens} close', end='')
    if open_parens == close_parens:
        print(' ✓')
    else:
        print(' ✗ MISMATCH')
else:
    print('❌ Script section not found')
