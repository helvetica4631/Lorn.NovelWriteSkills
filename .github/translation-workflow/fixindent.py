"""Восстановить ведущие пробелы/табы переведённых строк по оригиналу (память переводов хранит строки без отступа).

Запуск из корня репозитория: python3 .github/translation-workflow/fixindent.py [путь ...] [--dry]
Для каждого .md под указанными путями (по умолчанию весь репозиторий) находится исходный файл в коммите BASE
(с обратным отображением переименованных папок/Skill/файлов); если число строк совпало, у каждой изменённой
строки отступ принудительно берётся из оригинала. Идемпотентно.
"""
import os, re, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.abspath(os.path.join(here, '..', '..'))
BASE = 'f36540b'
rd = lambda p: [l.split('\t') for l in open(os.path.join(here, p), encoding='utf-8').read().splitlines() if l.strip()]
REVD = {b: a for a, b in rd('rename-dirs.tsv')}
SK = {b: a for a, b in rd('rename-skills.tsv')}            # общий-… -> 通用-…
REVF = {}
for p in ('rename-files.tsv', 'rename-files-genre.tsv'):
    for a, b in rd(p): REVF.setdefault(b, []).append(a)
SLUG = {zh: ru for zh, ru in (r for r in rd('rename-dirs.tsv')) if os.path.isdir(os.path.join(repo, ru, 'skills'))}
SLUG_REV = {ru: zh for zh, ru in SLUG.items()}
cjk = re.compile('[一-鿿]')

def tree():
    out = subprocess.run(['git', '-c', 'core.quotepath=off', '-C', repo, 'ls-tree', '-r', '--name-only', BASE], capture_output=True).stdout.decode('utf-8')
    return set(out.split('\n'))
TREE = tree()

def orig_dir_seg(seg, genre_ru):
    if seg in REVD: return REVD[seg]
    if seg in SK: return SK[seg]
    if genre_ru and seg.startswith(genre_ru + '-'):
        suf = 'общий-' + seg[len(genre_ru) + 1:]
        if suf in SK: return SLUG_REV[genre_ru] + '-' + SK[suf][3:]
    return seg

def orig_path(path):
    parts = path.split('/'); genre_ru = parts[0] if parts[0] in SLUG_REV else None
    d = '/'.join(orig_dir_seg(s, genre_ru) for s in parts[:-1]); name = parts[-1]
    for c in [name] + REVF.get(name, []):
        cand = (d + '/' + c) if d else c
        if cand in TREE: return cand
    return None

def lead(s): return s[:len(s) - len(s.lstrip(' \t'))]

dry = '--dry' in sys.argv; roots = [a for a in sys.argv[1:] if not a.startswith('--')] or ['.']
files = subprocess.run(['git', '-C', repo, 'ls-files', '-z', '--'] + roots, capture_output=True).stdout.decode().split('\0')
changed = files_changed = 0
for f in sorted(x for x in files if x.endswith('.md')):
    if re.search(r'(^|/)(prompts|scripts|исследования-письма)/|shuorenhua|Humanizer|humanizer|stop-slop|taste-skill|好词好句好段', f) or f.startswith('.github/translation'): continue
    o = orig_path(f)
    if not o: continue
    cur = open(os.path.join(repo, f), encoding='utf-8').read().split('\n')
    src = subprocess.run(['git', '-C', repo, 'show', f'{BASE}:{o}'], capture_output=True).stdout.decode('utf-8').split('\n')
    if len(cur) != len(src): continue
    n = 0
    for i, (c, s) in enumerate(zip(cur, src)):
        if c != s and cjk.search(s) and c.strip() and lead(c) != lead(s):
            cur[i] = lead(s) + c.lstrip(' \t'); n += 1
    if n:
        changed += n; files_changed += 1
        if not dry: open(os.path.join(repo, f), 'w', encoding='utf-8').write('\n'.join(cur))
print(('would fix' if dry else 'fixed'), changed, 'lines in', files_changed, 'files')
