import os,re,sys
pub="/home/claude/site/public"
files=[f for f in os.listdir(pub) if f.endswith(".html")]
bad=0
for f in files:
    s=open(os.path.join(pub,f),encoding="utf-8").read()
    for h in re.findall(r'href="([^"#]+)"',s):
        if h.startswith(("http","tel:","mailto:")): continue
        if not os.path.exists(os.path.join(pub,h)): print("BROKEN",f,h); bad+=1
    t=re.search(r"<title>(.*?)</title>",s).group(1); d=re.search(r'name="description" content="(.*?)"',s).group(1)
    print(f"{f:34} title {len(t):2} desc {len(d):3}")
print("broken links:",bad)
