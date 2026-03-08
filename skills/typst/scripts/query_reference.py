from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

def load(p:Path): return json.loads(p.read_text(encoding='utf-8'))

def score(item:dict[str,object],q:str)->int:
    q=q.lower().strip(); name=str(item.get('name','')).lower(); qual=str(item.get('qualified_name','')).lower(); summ=str(item.get('summary','')).lower(); docs=str(item.get('docs','')).lower(); ident=str(item.get('source_ident','')).lower(); kws=' '.join(item.get('keywords',[])).lower() if isinstance(item.get('keywords'),list) else ''
    s=0
    if qual==q: s+=200
    if name==q: s+=180
    if qual.startswith(q): s+=120
    if name.startswith(q): s+=110
    if q in qual: s+=90
    if q in name: s+=80
    if q in ident: s+=70
    if q in kws: s+=50
    if q in summ: s+=35
    if q in docs: s+=20
    return s

def find(items:list[dict[str,object]],q:str,kind:str|None,cat:str|None,limit:int):
    hits=[]
    for item in items:
        if kind and item.get('kind')!=kind: continue
        if cat and item.get('category')!=cat: continue
        s=score(item,q)
        if s>0: hits.append((s,item))
    hits.sort(key=lambda x:(-x[0],str(x[1].get('qualified_name',''))))
    return [x[1] for x in hits[:limit]]

def find_docs(items:list[dict[str,object]],q:str,limit:int):
    q=q.lower().strip(); hits=[]
    for item in items:
        title=str(item.get('title','')).lower(); summ=str(item.get('summary','')).lower(); path=str(item.get('path','')).lower(); s=0
        if title==q: s+=120
        if q in title: s+=80
        if q in path: s+=45
        if q in summ: s+=25
        if s>0: hits.append((s,item))
    hits.sort(key=lambda x:(-x[0],str(x[1].get('path',''))))
    return [x[1] for x in hits[:limit]]

def grep(root:Path,q:str,limit:int):
    q=q.lower().strip(); out=[]
    for base in (root/'typst',root/'The Raindrop-Blue Book'):
        if not base.exists(): continue
        for path in base.rglob('*'):
            if not path.is_file() or path.suffix.lower() not in {'.rs','.md','.typ','.toml','.txt','.yml','.yaml'}: continue
            try: lines=path.read_text(encoding='utf-8').splitlines()
            except Exception: continue
            for i,line in enumerate(lines,1):
                if q in line.lower():
                    out.append({'path':path.relative_to(root).as_posix(),'line':i,'text':line.strip()})
                    if len(out)>=limit: return out
    return out

def rit(item:dict[str,object])->str:
    lines=[f"- `{item.get('qualified_name',item.get('name'))}` [{item.get('kind')}] - {item.get('summary','')}"]
    sf=item.get('source_file'); sl=item.get('source_line')
    if sf: lines.append(f"  Source: `{sf}:{sl}`" if sl else f"  Source: `{sf}`")
    if item.get('signature'): lines.append(f"  Signature: `{str(item['signature']).splitlines()[0].strip()}`")
    if item.get('member_of') and not item.get('constructor'): lines.append(f"  Scope: `{item['member_of']}`")
    if item.get('deprecated_message'): lines.append(f"  Deprecated: `{item['deprecated_message']}`")
    return '\n'.join(lines)

def rdoc(item:dict[str,object])->str: return f"- `{item.get('path')}` - {item.get('title')}"

def rgrep(item:dict[str,object])->str: return f"- `{item['path']}:{item['line']}` - {item['text']}"

def join_tokens(v):
    if not v: return ''
    return ' '.join(v) if isinstance(v,list) else str(v)

def main()->int:
    me=Path(__file__).resolve(); skill=me.parent.parent
    ap=argparse.ArgumentParser(); ap.add_argument('--query',nargs='+'); ap.add_argument('--name',nargs='+'); ap.add_argument('--kind'); ap.add_argument('--category'); ap.add_argument('--limit',type=int,default=10); ap.add_argument('--json',action='store_true'); ap.add_argument('--rebuild',action='store_true'); ap.add_argument('--reference-file',type=Path,default=skill/'reference'/'generated'/'typst-reference.json'); a=ap.parse_args()
    q=join_tokens(a.name) or join_tokens(a.query)
    if not q: print('Provide --name or --query.',file=sys.stderr); return 2
    if a.rebuild: subprocess.run([sys.executable,str(me.parent/'build_reference.py')],check=True)
    payload=load(a.reference_file); root=Path(str(payload['project_root']))
    items=list(payload.get('items',[]))+list(payload.get('symbols',[]))+list(payload.get('bindings',[]))
    matches=find(items,q,a.kind,a.category,a.limit); docs=find_docs(list(payload.get('official_docs',[])),q,min(a.limit,6)); blue=find_docs(list(payload.get('bluebook',[])),q,min(a.limit,6)); raw=grep(root,q,min(a.limit,8))
    if a.json:
        print(json.dumps({'matches':matches,'docs':docs,'bluebook':blue,'grep':raw},ensure_ascii=False,indent=2)); return 0
    lines=[f"# Query: {q}",'','## API Matches','']
    lines.extend([rit(x) for x in matches] or ['- No indexed API match.'])
    lines.extend(['','## Official Docs','']); lines.extend([rdoc(x) for x in docs] or ['- No official docs match.'])
    lines.extend(['','## Blue Book','']); lines.extend([rdoc(x) for x in blue] or ['- No Blue Book match.'])
    lines.extend(['','## Raw Grep','']); lines.extend([rgrep(x) for x in raw] or ['- No raw source match.'])
    print('\n'.join(lines)); return 0

if __name__=='__main__': raise SystemExit(main())
