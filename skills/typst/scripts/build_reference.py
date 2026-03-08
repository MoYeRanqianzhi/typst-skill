from __future__ import annotations
import argparse, json, re, subprocess, tomllib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CT={"foundations":"Foundations","data-loading":"Data Loading","introspection":"Introspection","layout":"Layout","math":"Math","model":"Model","symbols":"Symbols","text":"Text","visualize":"Visualize","pdf":"PDF","html":"HTML"}

def rt(p:Path)->str:
    return p.read_text(encoding='utf-8')

def rel(p:Path,root:Path)->str:
    try:return p.relative_to(root).as_posix()
    except Exception:return p.as_posix()

def run(args:list[str])->str|None:
    try:return subprocess.run(args,check=True,capture_output=True,text=True,encoding='utf-8').stdout.strip() or None
    except Exception:return None

def gitinfo(p:Path)->dict[str,str|None]:
    return {"commit":run(["git","-C",str(p),"rev-parse","HEAD"]),"remote":run(["git","-C",str(p),"remote","get-url","origin"]),"tag":run(["git","-C",str(p),"tag","--points-at","HEAD"])}

def kebab(s:str)->str:
    return re.sub(r'(?<!^)(?=[A-Z])','-',s).replace('_','-').lower()

def title(s:str)->str:
    return s.replace('-',' ').title()

def summary(s:str)->str:
    s=s.strip()
    return re.sub(r'\s+',' ',s.split('\n\n',1)[0]).strip()

def m1(t:str,p:str):
    m=re.search(p,t,re.S); return m.group(1) if m else None

def ameta(attrs:list[str])->dict[str,object]:
    t=' '.join(attrs); km=m1(t,r'keywords\s*=\s*\[(.*?)\]')
    return {"name":m1(t,r'name\s*=\s*"([^"]+)"'),"title":m1(t,r'title\s*=\s*"([^"]+)"'),"scope":"scope" in t,"contextual":"contextual" in t,"constructor":"constructor" in t,"keywords":re.findall(r'"([^"]+)"',km or ''),"deprecated_message":m1(t,r'message\s*=\s*"([^"]+)"'),"deprecated_until":m1(t,r'until\s*=\s*"([^"]+)"')}

def cattr(ls:list[str],i:int):
    out=[]; d=0
    while i<len(ls):
        line=ls[i].rstrip('\n'); out.append(line.strip()); d+=line.count('[')-line.count(']')
        if d<=0: return ' '.join(out),i
        i+=1
    return ' '.join(out),i

def cfn(ls:list[str],i:int):
    out=[]; d=0; seen=False
    while i<len(ls):
        line=ls[i].rstrip('\n'); out.append(line)
        d+=line.count('(')-line.count(')'); seen=seen or '(' in line
        if seen and d<=0 and '{' in line: return out,i
        i+=1
    return out,i

def cblock(ls:list[str],i:int):
    out=[]; d=0; seen=False
    while i<len(ls):
        line=ls[i].rstrip('\n'); out.append(line)
        seen=seen or '{' in line; d+=line.count('{')-line.count('}')
        if seen and d<=0: return out,i
        i+=1
    return out,i

def bdelta(block:list[str])->int:
    return sum(x.count('{')-x.count('}') for x in block)

def cat(path:Path,lib:Path,html:Path)->str|None:
    if path.is_relative_to(lib):
        rp=path.relative_to(lib)
        if rp.name=='symbols.rs': return 'symbols'
        head=rp.parts[0]
        return 'data-loading' if head=='loading' else head if head in {"foundations","introspection","layout","math","model","pdf","text","visualize"} else None
    if path.is_relative_to(html): return 'html'
    return None

def parse_items(project:Path,typst:Path)->list[dict[str,object]]:
    lib=typst/'crates'/'typst-library'/'src'; html=typst/'crates'/'typst-html'/'src'
    files=sorted(lib.rglob('*.rs'))+sorted(html.rglob('*.rs')); known={}; items=[]
    for path in files:
        c=cat(path,lib,html)
        if not c: continue
        ls=rt(path).splitlines(); docs=[]; attrs=[]; scopes=[]; i=0
        while i<len(ls):
            raw=ls[i]; s=raw.strip(); block=[raw]; pushed=False
            if s.startswith('///'): docs.append(s[3:].lstrip()); i+=1; continue
            if s.startswith('#'):
                a,j=cattr(ls,i); attrs.append(a); i=j+1; continue
            im=re.match(r'impl\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{',s)
            if im and any(a.strip()=='#[scope]' for a in attrs):
                idn=im.group(1); scopes.append({"name":known.get(idn,kebab(idn.rstrip('_'))),"depth":raw.count('{')-raw.count('}')}); docs=[]; attrs=[]; i+=1; pushed=True
                continue
            fm=re.match(r'pub\s+fn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(',s)
            sm=re.match(r'pub\s+struct\s+([A-Za-z_][A-Za-z0-9_]*)',s)
            em=re.match(r'pub\s+enum\s+([A-Za-z_][A-Za-z0-9_]*)',s)
            tm=re.match(r'pub\s+type\s+([A-Za-z_][A-Za-z0-9_]*)',s)
            if fm and any(a.startswith('#[func') for a in attrs):
                hd,j=cfn(ls,i); meta=ameta(attrs); rid=fm.group(1); scope=scopes[-1]['name'] if scopes else None
                name=meta['name'] or rid.rstrip('_')
                q=scope if meta['constructor'] and scope else f"{scope}.{name}" if scope else str(name)
                items.append({"kind":"function","category":c,"name":name,"qualified_name":q,"title":meta['title'] or title(str(name)),"summary":summary('\n'.join(docs)),"docs":'\n'.join(docs).strip(),"keywords":meta['keywords'],"source_ident":rid,"source_file":rel(path,project),"source_line":i+1,"signature":'\n'.join(hd).strip(),"member_of":scope,"scope":bool(meta['scope']),"contextual":bool(meta['contextual']),"constructor":bool(meta['constructor']),"deprecated_message":meta['deprecated_message'],"deprecated_until":meta['deprecated_until']})
                if meta['scope']: known[rid]=str(name)
                docs=[]; attrs=[]; block=hd; i=j+1
            elif (sm or em or tm) and (any(a.startswith('#[ty') for a in attrs) or any(a.startswith('#[elem') for a in attrs)):
                rid=(sm or em or tm).group(1); meta=ameta(attrs); elem=any(a.startswith('#[elem') for a in attrs)
                name=str(meta['name'] or (kebab(rid.removesuffix('Elem')) if elem else kebab(rid))); known[rid]=name
                if '{' in raw: blk,j=cblock(ls,i); block=blk; i=j+1
                else: i+=1
                items.append({"kind":"element" if elem else "type","category":c,"name":name,"qualified_name":name,"title":meta['title'] or title(name),"summary":summary('\n'.join(docs)),"docs":'\n'.join(docs).strip(),"keywords":meta['keywords'],"source_ident":rid,"source_file":rel(path,project),"source_line":i-len(block)+1,"scope":bool(meta['scope']),"deprecated_message":meta['deprecated_message'],"deprecated_until":meta['deprecated_until']})
                docs=[]; attrs=[]
            else:
                if s:
                    docs=[]
                    if s!='#[scope]': attrs=[]
                i+=1
            if scopes and not pushed:
                scopes[-1]['depth']+=bdelta(block)
                while scopes and scopes[-1]['depth']<=0: scopes.pop()
    return items
def parse_bindings(project:Path,typst:Path)->list[dict[str,object]]:
    out=[]
    for path in sorted((typst/'crates'/'typst-library'/'src').rglob('*.rs')):
        text=rt(path); mod=m1(text,r'Module::new\("([^"]+)",\s*scope\)')
        if not mod: continue
        for m in re.finditer(r'scope\.define\("([^"]+)"\s*,',text):
            out.append({"kind":"binding","module":mod,"name":m.group(1),"qualified_name":f"{mod}.{m.group(1)}","source_file":rel(path,project),"source_line":text[:m.start()].count('\n')+1})
    return out

def parse_html(project:Path):
    base=Path.home()/'.cargo'/'git'/'checkouts'; ds=sorted(base.glob('typst-assets-*/57a38ca/files/html/data.rs')); hs=sorted(base.glob('typst-assets-*/57a38ca/src/html.rs'))
    if not ds or not hs: return [],[],None
    data=ds[0]; text=rt(data); attrs=[]
    for i,m in enumerate(re.finditer(r'AttrInfo::new\(\s*"([^"]+)",\s*"((?:[^"\\]|\\.)*)",',text,re.S)):
        attrs.append({"index":i,"name":m.group(1),"docs":m.group(2).replace('\\n','\n').replace('\\\"','"'),"source_file":rel(data,project)})
    amap={a['index']:a for a in attrs}; elems=[]
    for m in re.finditer(r'ElemInfo::new\(\s*"([^"]+)",\s*"((?:[^"\\]|\\.)*)",\s*&\[(.*?)\],\s*\)',text,re.S):
        idx=[int(x) for x in re.findall(r'\d+',m.group(3))]
        docs=m.group(2).replace('\\n','\n').replace('\\\"','"')
        elems.append({"kind":"html-element","category":"html","name":m.group(1),"qualified_name":f"html.{m.group(1)}","title":title(m.group(1)),"summary":docs,"docs":docs,"source_file":rel(data,project),"attributes":[amap[i] for i in idx if i in amap]})
    return elems,attrs,{"data_file":rel(data,project),"info_file":rel(hs[0],project)}

def parse_symbols(project:Path)->list[dict[str,object]]:
    roots=list((Path.home()/'.cargo'/'registry'/'src').glob('index.crates.io-*/codex-0.2.0/src/modules'))
    if not roots: return []
    out=[]
    for mod in ('sym','emoji'):
        path=roots[0]/f'{mod}.txt'; cur=None
        for raw in rt(path).splitlines():
            if not raw.strip() or raw.strip().startswith('//'): continue
            if raw.startswith(' ') or raw.startswith('\t'):
                if cur is not None: cur['raw']+='\n'+raw.rstrip()
                continue
            if cur is not None: out.append(cur)
            name=raw.split(maxsplit=1)[0]
            cur={"kind":"symbol-module-entry","category":"symbols","module":mod,"name":name,"qualified_name":f"{mod}.{name}","title":title(name),"summary":raw.strip(),"raw":raw.rstrip(),"source_file":rel(path,project)}
        if cur is not None: out.append(cur)
    return out

def docs_index(project:Path,typst:Path)->list[dict[str,object]]:
    out=[]; root=typst/'docs'
    for path in sorted(root.rglob('*.md')):
        text=rt(path); title_line=next((x.strip()[2:].strip() for x in text.splitlines() if x.strip().startswith('# ')),path.stem.replace('-',' ').title())
        out.append({"kind":"official-doc","path":rel(path,project),"section":path.relative_to(root).parts[0],"title":title_line,"summary":summary(text)})
    return out

def blue_index(project:Path,blue:Path)->list[dict[str,object]]:
    out=[]; root=blue/'src'
    for path in sorted(root.rglob('*.typ')):
        text=rt(path); heads=[x.strip()[2:].strip() for x in text.splitlines() if x.strip().startswith('= ')][:6]
        out.append({"kind":"bluebook","path":rel(path,project),"section":path.relative_to(root).parts[0],"title":heads[0] if heads else path.stem.replace('-',' '),"summary":heads[0] if heads else path.stem.replace('-',' '),"headings":heads})
    return out

def render_summary(payload:dict[str,object])->str:
    s=payload['stats']; t=payload['sources']['typst']; b=payload['sources']['bluebook']
    lines=['# Typst Reference Summary','',f"- Generated at: `{payload['generated_at']}`",f"- Typst version: `{t['version']}`",f"- Typst commit: `{t['commit']}`",f"- Blue Book commit: `{b['commit']}`",f"- Rust API items: `{s['rust_items']}`",f"- HTML typed elements: `{s['html_elements']}`",f"- HTML attributes: `{s['html_attributes']}`",f"- Symbol blocks: `{s['symbol_blocks']}`",f"- Official docs indexed: `{s['official_docs']}`",f"- Blue Book files indexed: `{s['bluebook_entries']}`",'', '## Category Counts','']
    for k,v in sorted(s['category_counts'].items()): lines.append(f"- `{k}`: `{v}`")
    return '\n'.join(lines)+'\n'

def build(project:Path,typst:Path,blue:Path,out:Path):
    version=tomllib.loads(rt(typst/'Cargo.toml'))['workspace']['package']['version']
    items=parse_items(project,typst); bindings=parse_bindings(project,typst); html_items,html_attrs,html_meta=parse_html(project); symbols=parse_symbols(project); docs=docs_index(project,typst); bluebook=blue_index(project,blue)
    payload={"generated_at":datetime.now(timezone.utc).isoformat(),"project_root":project.as_posix(),"sources":{"typst":{"path":rel(typst,project),"version":version,**gitinfo(typst)},"bluebook":{"path":rel(blue,project),**gitinfo(blue)},"html_assets":html_meta},"stats":{"rust_items":len(items),"html_elements":len(html_items),"html_attributes":len(html_attrs),"symbol_blocks":len(symbols),"official_docs":len(docs),"bluebook_entries":len(bluebook),"kind_counts":dict(Counter(x['kind'] for x in items)),"category_counts":dict(Counter(x['category'] for x in items))},"categories":[{"name":k,"title":v} for k,v in CT.items()],"items":items+html_items,"bindings":bindings,"html_attributes":html_attrs,"symbols":symbols,"official_docs":docs,"bluebook":bluebook}
    out.mkdir(parents=True,exist_ok=True)
    (out/'typst-reference.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'summary.md').write_text(render_summary(payload),encoding='utf-8')
    return payload

def main()->int:
    me=Path(__file__).resolve(); skill=me.parent.parent; project=skill.parent.parent
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',type=Path,default=project); ap.add_argument('--typst-root',type=Path,default=project/'typst'); ap.add_argument('--bluebook-root',type=Path,default=project/'The Raindrop-Blue Book'); ap.add_argument('--out-dir',type=Path,default=skill/'reference'/'generated'); a=ap.parse_args()
    p=build(a.project_root.resolve(),a.typst_root.resolve(),a.bluebook_root.resolve(),a.out_dir.resolve())
    print(json.dumps({"output":str((a.out_dir/'typst-reference.json').resolve()),"stats":p['stats']},ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__': raise SystemExit(main())
