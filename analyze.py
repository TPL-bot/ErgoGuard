import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all function definitions
funcs_defined = set(re.findall(r'function\s+(\w+)\s*\(', content))
print(f'Defined functions ({len(funcs_defined)}):')
for f in sorted(funcs_defined):
    print(f'  {f}')

# Find all event handler calls
event_calls = set()
for match in re.finditer(r'on\w+\s*=\s*["\']([^"\']+)["\']', content):
    call = match.group(1).split('(')[0].strip()
    event_calls.add(call)

print(f'\nEvent handlers called ({len(event_calls)}):')
for call in sorted(event_calls):
    status = '✓' if call in funcs_defined else '✗ MISSING'
    print(f'  {status}: {call}')
