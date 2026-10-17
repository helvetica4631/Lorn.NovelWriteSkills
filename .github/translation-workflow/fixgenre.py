import os,re,sys,subprocess
R=os.environ.get('REPO', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')))
os.chdir(R)
G=sys.argv[1]; mode=sys.argv[2] if len(sys.argv)>2 else 'apply'
def rd(p): return [l.split('\t') for l in open(p,encoding='utf-8').read().splitlines() if l.strip()]
skills=rd('.github/translation-workflow/rename-skills.tsv')
files=dict(rd('.github/translation-workflow/rename-files.tsv'))
gpath='.github/translation-workflow/rename-files-genre.tsv'
if os.path.exists(gpath): files.update(dict(rd(gpath)))
# unmapped chinese-named reference files in G
cjk=re.compile(r'[一-鿿]')
# каталоги, которые не переводятся и не переименовываются
SKIP_ALL={'写作研究','shuorenhua-main','Humanizer-zh-main','humanizer-main','stop-slop-main','taste-skill-main'}
NO_RENAME={'prompts'}
def skipped(path,names): return any(n in path.split(os.sep) for n in names)
def corpus(f): return f.endswith('好词好句好段.md')
unm=set()
for root,ds,fs in os.walk(G):
    if skipped(root,SKIP_ALL|NO_RENAME): continue
    for f in fs:
        if f=='SKILL.md' or corpus(f): continue
        if cjk.search(f) and f not in files and not f.endswith('.instructions.md'): unm.add(f)
if mode=='list':
    print('\n'.join(sorted(unm))); sys.exit()
if unm: print('UNMAPPED',sorted(unm)); sys.exit(1)
reps=sorted([(a,b) for a,b in skills],key=lambda x:-len(x[0]))
reps+=[('通用-设计事件技术事件引擎','общий-проектирование-движка-событий-и-дел'),
('通用-输出{平台名}版','общий-вывод-{платформа}'),('通用-输出{название платформы}版','общий-вывод-{платформа}'),
('通用-输出*版','общий-вывод-*'),('通用-输出*','общий-вывод-*'),('通用-输出','общий-вывод-'),
('通用-{能力名}','общий-{способность}'),('通用-能力名','общий-способность'),('通用-*','общий-*'),('通用-','общий-')]
# genre skill names
greps=sorted([(f'{G}-{a[3:]}',f'{G}-{b[len("общий-"):]}') for a,b in skills],key=lambda x:-len(x[0]))
agents={'小说作者':'автор-романов','小说读者':'читатель-романов','小说审阅者':'рецензент-романов'}
apat=[(re.compile(r'((?:agent|name):\s*)'+k),lambda m,v=v:m.group(1)+v) for k,v in agents.items()]
apat+=[(re.compile(re.escape(k)+r'\.agent\.md'),lambda m,v=v:v+'.agent.md') for k,v in agents.items()]
names=sorted(files,key=len,reverse=True)
bare=re.compile(r'(?<![\w\-])('+'|'.join(re.escape(n) for n in names)+')')
qual=re.compile(r'(общий-[^/\\\s`\'"()\[\]]+[/\\](?:references|assets)[/\\])('+'|'.join(re.escape(n) for n in names)+')')
# dirs of common refs already renamed, so bare names inside G refer to local files -> rename too
n=0
for root,ds,fs in os.walk('.'):
    if '.git' in root.split(os.sep): continue
    if skipped(root,SKIP_ALL): continue
    inG=root==G or root.startswith(G+os.sep)
    for f in fs:
        p=os.path.join(root,f)
        if p.endswith('.tsv'): continue
        try: t=open(p,encoding='utf-8',newline='').read()
        except: continue
        t0=t
        if inG:
            for a,b in reps: t=t.replace(a,b)
            for r,s in apat: t=r.sub(s,t)
            t=qual.sub(lambda m:m.group(1)+files[m.group(2)],t)
        for a,b in greps: t=t.replace(a,b)
        if inG: t=bare.sub(lambda m:files[m.group(1)],t)
        if t!=t0: open(p,'w',encoding='utf-8',newline='').write(t); n+=1
print('text changed',n)
# renames
for d in os.listdir(f'{G}/skills'):
    if d.startswith(G+'-'):
        s=G+'-'+d[len(G)+1:]
        new=dict(greps).get(s)
        if new and new!=s: subprocess.check_call(['git','mv',f'{G}/skills/{s}',f'{G}/skills/{new}'])
c=0
for root,ds,fs in os.walk(G):
    if skipped(root,SKIP_ALL|NO_RENAME): continue
    for f in fs:
        if f in files and f!='SKILL.md' and not corpus(f):
            subprocess.check_call(['git','mv',os.path.join(root,f),os.path.join(root,files[f])]); c+=1
print('files renamed',c)
