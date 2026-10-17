"""Переименование папок на русские имена + обновление ссылок на них. Идемпотентно (можно запускать повторно после перевода очередного жанра).
Запуск из любого места:  python3 .github/translation-workflow/renamedirs.py [--dry]
Карта: rename-dirs.tsv (китайское имя<TAB>русское). Имена папок skill вида «<жанр>-<русский суффикс>» получают русский префикс жанра.
Содержимое каталогов исследований (исследования-письма) не трогается. Файлы и их имена в этом скрипте не переименовываются.
"""
import os,re,subprocess,sys
R=os.environ.get('REPO', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')))
os.chdir(R)
DRY='--dry' in sys.argv
rd=lambda p:[l.split('\t') for l in open(p,encoding='utf-8').read().splitlines() if l.strip()]
DIRS=dict(rd('.github/translation-workflow/rename-dirs.tsv'))
GENRES={k:v for k,v in DIRS.items() if k in ('AI科幻','太空科幻','赛博庞克','悬疑推理','异能志怪','女频爱情','都市职场','都市悬疑')}
RESEARCH=DIRS['写作研究']
gpre=re.compile('^('+'|'.join(map(re.escape,GENRES))+')-(?=[а-яa-z])')
def newseg(s):
    if s in DIRS: return DIRS[s]
    m=gpre.match(s)
    if m: return GENRES[m.group(1)]+'-'+s[m.end():]
    return s
files=[f for f in subprocess.run(['git','ls-files','-z'],capture_output=True).stdout.decode('utf-8').split('\0') if f]
moves=0
for f in files:
    parts=f.split('/'); new='/'.join([newseg(p) for p in parts[:-1]]+[parts[-1]])
    if new!=f:
        moves+=1
        if not DRY:
            os.makedirs(os.path.dirname(new),exist_ok=True); os.rename(f,new)
print('files moved',moves)
if not DRY:
    for root,ds,fs in os.walk('.',topdown=False):
        if '.git' in root.split(os.sep): continue
        if not os.listdir(root) and root!='.': os.rmdir(root)
    subprocess.check_call(['git','add','-A'])
    files=[f for f in subprocess.run(['git','ls-files','-z'],capture_output=True).stdout.decode('utf-8').split('\0') if f]
# текстовые замены
pairs=[]
for g,s in GENRES.items():
    pairs.append((re.compile(re.escape(g)+r'-(?=[а-яa-z])'),s+'-'))
    pairs.append((re.compile(re.escape(g)+'/'),s+'/'))
pairs+= [(re.compile('写作研究(?!并强化|模板)'),RESEARCH),
         (re.compile(re.escape(RESEARCH)+'/起点模板/总纲模板'),RESEARCH+'/'+DIRS['起点模板']+'/'+DIRS['总纲模板']),
         (re.compile(re.escape(RESEARCH)+'/总裁豪门创新研究'),RESEARCH+'/'+DIRS['总裁豪门创新研究']),
         (re.compile(re.escape(RESEARCH)+'/裁员反杀总裁豪门设计深研'),RESEARCH+'/'+DIRS['裁员反杀总裁豪门设计深研']),
         (re.compile('小说分发'),DIRS['小说分发'])]
for k,v in sorted(DIRS.items(),key=lambda x:-len(x[0])):
    if k.startswith('分发-'): pairs.append((re.compile(re.escape(k)),v))
SKIP_FILES=('.github/translation-workflow/','.github/translation-glossary.ru.md')
n=0
for f in files:
    if f.startswith(SKIP_FILES) or RESEARCH in f.split('/')[:-1] or f.endswith(('.gz','.tsv')): continue
    try: t=open(f,encoding='utf-8',newline='').read()
    except Exception: continue
    t0=t
    for r,s in pairs: t=r.sub(s,t)
    if t!=t0:
        n+=1
        if not DRY: open(f,'w',encoding='utf-8',newline='').write(t)
print('text files changed',n)
