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
    head = out.split('\n', 1)[0]
    if head.endswith(' 0 to translate'):
        continue
    sys.stdout.write(out)
