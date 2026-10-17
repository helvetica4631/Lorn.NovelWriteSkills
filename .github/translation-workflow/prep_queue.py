"""Собрать очередь непереведённых строк для жанра/каталога.

Запуск из корня репозитория:
  TM_DIR=/tmp/work python3 .github/translation-workflow/prep_queue.py AI科幻/skills AI科幻/instructions > /tmp/work/queue.txt
Для каждого .md под указанными каталогами (сортировка по пути) запускается `tmflow.py prep`;
в очередь попадают только строки, которых нет в памяти переводов. Файлы без таких строк пропускаются.
Заголовок каждого файла:  # путь: N lines, M from TM, K to translate
"""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.abspath(os.path.join(here, '..', '..'))
files = subprocess.run(['git', '-C', repo, 'ls-files', '-z', '--'] + sys.argv[1:], capture_output=True).stdout.decode().split('\0')
for f in sorted(x for x in files if x.endswith('.md')):
    out = subprocess.run([sys.executable, '-I', os.path.join(here, 'tmflow.py'), 'prep', f], capture_output=True, cwd=repo).stdout.decode()
    lines = out.split('\n')
    head = lines[0]
    if head.endswith(' 0 to translate'):
        continue
    # строки короче 6 знаков в памяти переводов не хранятся: пропускаем те, что в файле уже переведены
    cur = open(os.path.join(repo, f), encoding='utf-8').read().split('\n')
    rows = []
    for l in lines[1:]:
        if not l.strip():
            continue
        n, _, t = l.partition('\t')
        if n.isdigit() and int(n) <= len(cur) and not any('\u4e00' <= c <= '\u9fff' for c in cur[int(n) - 1]):
            continue
        rows.append(l)
    if not rows:
        continue
    head = head.rsplit(',', 1)[0] + ', %d to translate' % len(rows)
    sys.stdout.write(head + '\n' + '\n'.join(rows) + '\n')
