"""Пересобрать «память переводов» (tm.json) из уже переведённых файлов.

Запуск из корня репозитория:  python3 .github/translation-workflow/rebuild_tm.py
Для каждого .md, у которого число строк совпадает с исходной версией (коммит f36540b),
пары «китайская строка → русская строка» добавляются в tm.json.
"""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.argv = ['tmflow.py', 'noop']
exec(open(os.path.join(here, 'tmflow.py'), encoding='utf-8').read().split("cmd=sys.argv[1]")[0])
files = subprocess.run(['git', '-C', REPO, 'ls-files', '-z'], capture_output=True).stdout.decode().split('\0')
added = 0
for f in files:
    if not f.endswith('.md') or f.startswith(('scripts/', '.github/translation')):
        continue
    o = orig(f)
    try:
        t = open(os.path.join(REPO, f), encoding='utf-8').read().split('\n')
    except Exception:
        continue
    if len(o) != len(t) or o == t:
        continue
    tr = {i + 1: t[i] for i in range(len(o)) if han(o[i]) and t[i] != o[i]}
    tm_add(o, tr, f)
    added += len(tr)
print('pairs added:', added, 'tm size:', len(load_tm()))
