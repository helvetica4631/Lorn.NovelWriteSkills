import sys,json,os,re,subprocess,hashlib
S=os.environ.get('TM_DIR', os.path.dirname(os.path.abspath(__file__)))
REPO=os.environ.get('REPO', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')))
BASE='f36540b'
TM=os.path.join(S,'tm.json')
def norm(s):
    s=s.replace('“','"').replace('”','"').replace('‘',"'").replace('’',"'")
    return re.sub(r'\s+',' ',s).strip()
def han(s): return any('一'<=c<='鿿' for c in s)
def _rev_dirs():
    f=os.path.join(REPO,'.github','translation-workflow','rename-dirs.tsv')
    return {b:a for a,b in (r.split('\t') for r in open(f,encoding='utf-8').read().split('\n') if r.strip())}
def orig_path(path):
    """Текущий путь (с русскими именами папок) -> путь в исходном коммите."""
    rev=_rev_dirs(); parts=path.split('/')
    return '/'.join([rev.get(p,p) for p in parts[:-1]]+[parts[-1]])
def orig(path):
    path=orig_path(path)
    return subprocess.run(['git','-C',REPO,'show',f'{BASE}:{path}'],capture_output=True).stdout.decode('utf-8').split('\n')
def load_tm():
    return json.load(open(TM,encoding='utf-8')) if os.path.exists(TM) else {}
def save_tm(d): json.dump(d,open(TM,'w',encoding='utf-8'),ensure_ascii=False)
def load_tsv(p):
    d={}
    if os.path.exists(p):
        for r in open(p,encoding='utf-8').read().split('\n'):
            if r.strip():
                n,_,t=r.partition('\t'); d[int(n)]=t
    return d

GENRES=['AI科幻','太空科幻','悬疑推理','赛博庞克','女频爱情','异能志怪','都市职场','都市悬疑']
def _skill_suffixes():
    f=os.path.join(REPO,'.github','translation-workflow','rename-skills.tsv')
    out=[]
    for r in open(f,encoding='utf-8').read().split('\n'):
        if r.strip(): out.append(r.split('\t')[0][3:])
    return sorted(set(out),key=len,reverse=True)
_NAME_RE=None
def name_re():
    global _NAME_RE
    if _NAME_RE is None:
        _NAME_RE=re.compile('(?:通用|'+'|'.join(GENRES)+')-(?:'+'|'.join(re.escape(s) for s in _skill_suffixes())+')')
    return _NAME_RE
def nm_key(l):
    """Строка с именами skill, заменёнными на {N0},{N1}…; возвращает (ключ, список имён) или (None, [])."""
    names=[]
    def rep(m):
        n=m.group(0)
        if n not in names: names.append(n)
        return '{N%d}'%names.index(n)
    k=name_re().sub(rep,l)
    if not names: return None,[]
    rest=re.sub(r'\{N\d+\}','',k)
    if sum(1 for c in rest if '一'<=c<='鿿')<4: return None,[]
    return norm(k),names
def tm_add(lines,tr,path=''):
    tm=load_tm(); zh,ru=plat_of(path)
    for n,t in tr.items():
        l=lines[n-1]
        if han(l) and not l.startswith(('name:','tools:')) and len(norm(l))>=6:
            tm.setdefault(norm(l),t)
            nk,names=nm_key(l)
            if nk:
                tn=t
                for i,nme in enumerate(names): tn=tn.replace(nme,'{N%d}'%i)
                tm.setdefault('N::'+nk,tn)
            if zh and any(v in l for v in zvars(zh)):
                tv=t
                for v in zvars(zh): tv=tv.replace(v,'{Z}')
                tv=tv.replace(ru,'{P}')
                tm.setdefault('P::'+tkey(l,zh),tv)
    save_tm(tm)
PLAT={'番茄':'Fanqie','七猫':'Qimao','B站':'Bilibili','起点中文网':'Qidian','今日头条':'Toutiao','知乎':'Zhihu','豆瓣':'Douban','微信订阅号':'WeChat Official Accounts','百度百家号':'Baidu Baijiahao','新浪微博':'Sina Weibo','小红书':'Xiaohongshu','纵横小说':'Zongheng','出版社':'издательство','WebNovel':'WebNovel','GoodNovel':'GoodNovel','My Fiction':'My Fiction'}
def plat_of(path):
    for k in sorted(PLAT,key=len,reverse=True):
        if f'输出{k}版' in path: return k,PLAT[k]
    return None,None
def zvars(zh):
    return [zh,'B 站'] if zh=='B站' else [zh]
def tkey(l,zh):
    k=norm(l)
    for v in zvars(zh): k=k.replace(v,'{P}')
    return k
def key(path): return hashlib.md5(path.encode()).hexdigest()[:8]
cmd=sys.argv[1]
if cmd=='seed':           # seed REPO_PATH TSV
    path,tsv=sys.argv[2],sys.argv[3]; tm_add(orig(path),load_tsv(tsv),path); print('tm size',len(load_tm()))
elif cmd=='prep':         # prep REPO_PATH  -> prints missing lines
    path=sys.argv[2]; lines=orig(path); tm=load_tm(); part={}; zh0,ru0=plat_of(path)
    for i,l in enumerate(lines,1):
        if han(l) and not l.startswith(('name:','tools:')):
            if norm(l) in tm: part[i]=tm[norm(l)]
            elif zh0 and 'P::'+tkey(l,zh0) in tm and any(v in l for v in zvars(zh0)): part[i]=tm['P::'+tkey(l,zh0)].replace('{P}',ru0).replace('{Z}',zh0)
            else:
                nk,names=nm_key(l)
                if nk and 'N::'+nk in tm:
                    v=tm['N::'+nk]
                    for j,nme in enumerate(names): v=v.replace('{N%d}'%j,nme)
                    part[i]=v
    open(os.path.join(S,'part_'+key(path)+'.tsv'),'w',encoding='utf-8').write('\n'.join(f'{n}\t{t}' for n,t in sorted(part.items()))+'\n')
    miss=[(i,l) for i,l in enumerate(lines,1) if han(l) and i not in part and not l.startswith(('name:','tools:')) and not re.match(r'^\s*(- |\d+\. )?`[^`\s→]+`\s*$',l) and not re.match(r'^# общий-',l)]
    print(f'# {path}: {len(lines)} lines, {len(part)} from TM, {len(miss)} to translate')
    for i,l in miss: print(f'{i}\t{l}')
elif cmd=='done':         # done REPO_PATH EXTRA_TSV
    path,extra=sys.argv[2],sys.argv[3]
    lines=orig(path); part=load_tsv(os.path.join(S,'part_'+key(path)+'.tsv')); part.update(load_tsv(extra))
    # строки, уже переведённые в предыдущих проходах (в том числе короче 6 знаков, которых нет в памяти переводов), сохраняем
    try: cur=open(os.path.join(REPO,path),encoding='utf-8').read().split('\n')
    except Exception: cur=None
    if cur is not None and len(cur)==len(lines):
        for i,(a,b) in enumerate(zip(lines,cur),1):
            if i not in part and a!=b and han(a) and not han(b) and b.strip(): part[i]=b
    out=list(lines)
    for n,t in part.items():
        l0=lines[n-1]; out[n-1]=l0[:len(l0)-len(l0.lstrip(' \t'))]+t.lstrip(' \t') if t.strip() else t   # отступ — как в оригинале
    open(os.path.join(REPO,path),'w',encoding='utf-8').write('\n'.join(out))
    tm_add(lines,part,path)
    def cy(l): return sum('Ѐ'<=c<='ӿ' for c in l)
    left=[(i,l[:70]) for i,l in enumerate(out,1) if han(l) and cy(l)==0 and not re.match(r'^(name:|tools:|# 通用|- `|\||- [^ ]{1,14}$|\d+\. `)',l)]
    print('applied',len(part),'lines; leftover w/o Russian:',len(left))
    for x in left[:25]: print(x)
if cmd=='seedpair':       # seedpair REPO_PATH  (uses current file in repo as translation; needs equal line count)
    path=sys.argv[2]; o=orig(path); t=open(os.path.join(REPO,path),encoding='utf-8').read().split('\n')
    if len(o)!=len(t): print('LINECOUNT MISMATCH',len(o),len(t)); sys.exit()
    tr={i+1:t[i] for i in range(len(o)) if han(o[i]) and t[i]!=o[i]}
    tm_add(o,tr,path); print('seeded',len(tr))
