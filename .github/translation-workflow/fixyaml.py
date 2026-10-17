"""Проверка и починка YAML-шапок (front matter) в .md: неэкранированные «: » в значениях, лишние кавычки.
Запуск из корня: python3 .github/translation-workflow/fixyaml.py [--dry]
"""
import re, subprocess, sys, yaml
dry = '--dry' in sys.argv
files = subprocess.run(['git', 'ls-files', '-z'], capture_output=True).stdout.decode().split('\0')
SKIP = re.compile(r'shuorenhua|Humanizer|humanizer|stop-slop|taste-skill|translation-workflow')
def ok(fm):
    try: yaml.safe_load(fm); return True
    except Exception: return False
n = fixed = bad = 0
for f in files:
    if not f.endswith('.md') or SKIP.search(f): continue
    t = open(f, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---', t, re.S)
    if not m: continue
    fm = m.group(1); n += 1
    if ok(fm): continue
    out = []
    for l in fm.split('\n'):
        mm = re.match(r'^([A-Za-z][\w-]*):\s+(.*)$', l)
        if mm:
            k, v = mm.groups()
            if v.startswith("'") and v.endswith("' '"): v = v[:-2]
            if not (v[:1] in "'\"" and v[-1:] == v[:1]) and (': ' in v or ' #' in v or v[:1] in '[{*&!|>%@`'):
                v = "'" + v.replace("'", "''") + "'"
            l = f'{k}: {v}'
        out.append(l)
    new = '\n'.join(out)
    if ok(new):
        fixed += 1
        if not dry: open(f, 'w', encoding='utf-8').write('---\n' + new + t[m.end(1):].replace('', '', 0) if False else t.replace(fm, new, 1))
    else:
        bad += 1; print('STILL BAD', f)
print('checked', n, 'fixed', fixed, 'bad', bad)
