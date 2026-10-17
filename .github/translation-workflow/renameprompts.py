"""Переименовать файлы *.prompt.md (+ поле name: и ссылки `X.prompt.md`, `/X`) по карте rename-prompts.tsv. Идемпотентно."""
import os,re,subprocess,sys
R=os.environ.get('REPO', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')))
os.chdir(R)
M=dict(l.split('\t') for l in open('.github/translation-workflow/rename-prompts.tsv',encoding='utf-8').read().splitlines() if l.strip())
names=sorted(M,key=len,reverse=True)
alt='|'.join(re.escape(n) for n in names)
fpat=re.compile('(?<![\\w\\-])('+alt+')(\\.prompt\\.md)')
spat=re.compile('(?<![\\w\\-./])/('+alt+')(?![\\w\\-])')
files=[f for f in subprocess.run(['git','ls-files','-z'],capture_output=True).stdout.decode().split('\0') if f]
n=0
for f in files:
    if f.startswith('.github/translation-workflow/') or f.endswith(('.tsv','.gz','.pyc')): continue
    try: t=open(f,encoding='utf-8',newline='').read()
    except Exception: continue
    t0=t
    t=fpat.sub(lambda m:M[m.group(1)]+m.group(2),t)
    t=spat.sub(lambda m:'/'+M[m.group(1)],t)
    if t!=t0: open(f,'w',encoding='utf-8',newline='').write(t); n+=1
print('text files changed',n)
c=0
for f in files:
    if f.endswith('.prompt.md') and '/prompts/' in '/'+f:
        d,b=os.path.split(f); k=b[:-len('.prompt.md')]
        if k in M:
            subprocess.check_call(['git','mv',f,os.path.join(d,M[k]+'.prompt.md')]); c+=1
print('files renamed',c)
# name: в шапке
files=[f for f in subprocess.run(['git','ls-files','-z'],capture_output=True).stdout.decode().split('\0') if f.endswith('.prompt.md')]
k=0
for f in files:
    t=open(f,encoding='utf-8',newline='').read()
    b=os.path.basename(f)[:-len('.prompt.md')]
    t2=re.sub(r'(\A---\r?\n(?:.*\r?\n)*?name:\s*)(.*?)(\r?\n)',lambda m:m.group(1)+b+m.group(3),t,count=1)
    if t2!=t: open(f,'w',encoding='utf-8',newline='').write(t2); k+=1
print('name fixed',k)
