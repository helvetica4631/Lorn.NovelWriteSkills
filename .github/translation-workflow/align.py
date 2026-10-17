import sys
# usage: align.py out.txt START END mine.tsv out.tsv   (START/END = 1-based out.txt lines inclusive of header? START = first data line)
o,s,e,m,outp=sys.argv[1:6]
s=int(s);e=int(e)
src=[l.split('\t',1) for l in open(o,encoding='utf-8').read().split('\n')[s-1:e]]
mine=[l.split('\t',1) for l in open(m,encoding='utf-8').read().split('\n') if l.strip()]
print('src',len(src),'mine',len(mine))
bad=0;res=[]
for (sk,st),(mk,mt) in zip(src,mine):
    if sk!=mk: bad+=1
    res.append(f"{sk}\t{mt}")
print('keymismatch',bad)
open(outp,'w',encoding='utf-8').write('\n'.join(res)+'\n')
