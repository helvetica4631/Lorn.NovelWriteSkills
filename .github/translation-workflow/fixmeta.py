"""Заменить китайские имена Skill/папок/файлов в .github/skills/create-genre-skill-skeletons и переименовать файлы реестров."""
import os,re,subprocess
os.chdir(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')))
def rd(p): return [l.split('\t') for l in open(p,encoding='utf-8').read().splitlines() if l.strip()]
W='.github/translation-workflow/'
skills=rd(W+'rename-skills.tsv'); dirs=dict(rd(W+'rename-dirs.tsv'))
files=dict(rd(W+'rename-files.tsv')); files.update(dict(rd(W+'rename-files-genre.tsv')))
ROOT='.github/skills/create-genre-skill-skeletons'
reps=[]
for a,b in sorted(skills,key=lambda x:-len(x[0])):
    reps.append((f'题材名-{a[3:]}',f'<жанр>-{b[len("общий-"):]}'))
for G in ['异能志怪','都市悬疑']:
    GD=dirs[G]
    for a,b in sorted(skills,key=lambda x:-len(x[0])):
        reps.append((f'{G}-{a[3:]}',f'{GD}-{b[len("общий-"):]}'))
reps+=[(a,b) for a,b in sorted(skills,key=lambda x:-len(x[0]))]
reps+=[('通用-输出{平台名}版','общий-вывод-{платформа}'),('通用-输出*版','общий-вывод-*'),('通用-输出*','общий-вывод-*'),('通用-输出','общий-вывод-'),('通用-{能力名}','общий-{способность}'),('通用-能力名','общий-способность'),('通用-*','общий-*'),('通用-','общий-'),('题材名-','<жанр>-')]
for zh,ru in dirs.items(): reps.append((zh+'/',ru+'/'))
ren={}
for k,v in {'支持平台.md':'поддерживаемые-платформы.md','海外小说平台.md':'зарубежные-платформы-романов.md'}.items(): ren[k]=v
new=open(W+'rename-files.tsv',encoding='utf-8').read()
for k,v in ren.items():
    if k not in files: new+=f'{k}\t{v}\n'; files[k]=v
for f in os.listdir(ROOT+'/references/section-ledgers'):
    if re.search('[一-鿿]',f) and f not in files:
        base=f[:-len('平台-条款级迁移台账.md')]
        plat={'B站':'bilibili','GoodNovel':'goodnovel','My Fiction':'my-fiction','WebNovel':'webnovel','七猫':'qimao','出版社':'izdatelstvo','小红书':'xiaohongshu','微信订阅号':'wechat','新浪微博':'weibo','番茄':'fanqie','百度百家号':'baijiahao','知乎':'zhihu','豆瓣':'douban'}[base]
        files[f]=f'реестр-пунктов-{plat}.md'; new+=f'{f}\t{files[f]}\n'
open(W+'rename-files.tsv','w',encoding='utf-8').write(new)
n=0
names=sorted([k for k in files if k in ren or '条款级迁移台账' in k],key=len,reverse=True)
for root,ds,fs in os.walk('.'):
    if '.git' in root.split(os.sep) or root.startswith('./.github/translation-workflow'): continue
    if any(p in root.split(os.sep) for p in ('исследования-письма','写作研究','prompts','scripts')): continue
    for f in fs:
        p=os.path.join(root,f)
        if p.endswith(('.tsv','.gz')): continue
        try: t=open(p,encoding='utf-8',newline='').read()
        except: continue
        t0=t
        if root.startswith('./'+ROOT):
            for a,b in reps: t=t.replace(a,b)
        for nm in names: t=t.replace(nm,files[nm]) if nm in t else t
        if t!=t0: open(p,'w',encoding='utf-8',newline='').write(t); n+=1
print('text changed',n)
for k in names:
    for root,ds,fs in os.walk('.'):
        if '.git' in root.split(os.sep): continue
        if k in fs: subprocess.check_call(['git','mv',os.path.join(root,k),os.path.join(root,files[k])])
