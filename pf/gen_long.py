# -*- coding: utf-8 -*-
"""찰칵상세 롱폼 상세페이지 생성기 (쿠팡 상위 페이지 구조: 후킹→요약→공감→해결→포인트4→비교→디테일→장면→추천→사용법→구성→정보→신뢰→후기자리→FAQ→배송→마무리)"""
import json, os, sys
from PIL import Image
F = "file:///home/claude/minsung-ai/toon_tools/fonts/"
BASE = os.path.dirname(os.path.abspath(__file__))

def crop(cat, src, box, name, out_w=None):
    im = Image.open(f"{BASE}/{cat}/{src}")
    W, H = im.size
    x, y, w, h = [int(v * (W if i % 2 == 0 else H)) if isinstance(v, float) else v for i, v in enumerate(box)]
    c = im.crop((x, y, x + w, y + h))
    if out_w and c.width != out_w:
        c = c.resize((out_w, int(c.height * out_w / c.width)), Image.LANCZOS)
    c.save(f"{BASE}/{cat}/{name}", quality=90)
    return name

def esc(s): return s

def page(cat, T, C):
    css = f"""
@font-face{{font-family:HD,'Noto Sans CJK KR';src:url({F}{T['font']})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:860px;background:{T['bg']};font-family:'Noto Sans CJK KR',sans-serif;color:{T['ink']}}}
.sec{{padding:110px 70px;text-align:center}}
.alt{{background:{T['bg2']}}}
.inv{{background:{T['inv']};color:{T['invInk']}}}
.inv .sub,.inv small,.inv p{{color:{T['invSub']}!important}}
.eye{{display:inline-block;font-size:16px;letter-spacing:.32em;color:{T['ac']};font-weight:800}}
.pill{{display:inline-block;font-size:16px;font-weight:800;color:{T['pillInk']};background:{T['ac']};padding:9px 20px;border-radius:99px;letter-spacing:.08em}}
h1{{font-family:HD,'Noto Sans CJK KR';font-weight:{T.get('hw',400)}!important;font-size:68px;line-height:1.26;margin-top:24px;font-weight:400;letter-spacing:-1px}}
h2{{font-family:HD,'Noto Sans CJK KR';font-weight:{T.get('hw',400)}!important;font-size:50px;line-height:1.34;margin-top:18px;font-weight:400;letter-spacing:-.5px}}
h1 em,h2 em{{font-style:normal;color:{T['ac']}}}
.inv h2 em{{color:{T['invAc']}}}
.sub{{font-size:23px;line-height:1.8;color:{T['sub']};margin-top:24px}}
img.full{{width:860px;display:block}}
.tags{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:34px}}
.tags span{{font-size:20px;font-weight:700;padding:12px 20px;border-radius:99px;background:{T['card']};border:2px solid {T['line']};color:{T['ac']}}}
.nums{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:40px}}
.nums div{{background:{T['card']};border-radius:24px;padding:34px 10px;border:1px solid {T['line']}}}
.nums b{{display:block;font-family:HD,'Noto Sans CJK KR';font-weight:400;font-size:46px;color:{T['ac']}}}
.nums small{{display:block;font-size:18px;color:{T['sub']};margin-top:8px;line-height:1.5}}
.pain{{display:grid;gap:14px;margin-top:44px;text-align:left}}
.pain div{{background:{T['card']};border-radius:20px;padding:26px 30px;font-size:23px;display:flex;gap:18px;align-items:center;border:1px solid {T['line']}}}
.pain i{{flex:none;width:40px;height:40px;border-radius:50%;background:{T['painBg']};color:{T['painInk']};font-style:normal;font-weight:900;display:grid;place-items:center;font-size:20px}}
.turn{{font-family:HD,'Noto Sans CJK KR';font-size:40px;line-height:1.45;margin-top:60px}}
.turn em{{font-style:normal;color:{T['ac']}}}
.arrow{{font-size:40px;color:{T['ac']};margin-top:30px}}
.pt{{display:inline-flex;align-items:center;gap:14px}}
.pt b{{font-family:HD,'Noto Sans CJK KR';font-weight:400;font-size:26px;color:{T['pillInk']};background:{T['ac']};border-radius:99px;padding:6px 20px;letter-spacing:.1em}}
.pt span{{font-size:17px;font-weight:800;letter-spacing:.3em;color:{T['ac']}}}
.cap{{font-size:19px;color:{T['sub']};padding:20px 70px 0;text-align:center;line-height:1.6}}
.kv{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:40px;text-align:left}}
.kv div{{background:{T['card']};border-radius:22px;padding:28px;border:1px solid {T['line']}}}
.kv b{{display:block;font-size:24px}}.kv small{{display:block;font-size:18px;color:{T['sub']};margin-top:10px;line-height:1.6}}
.kv .e{{font-size:40px;display:block;margin-bottom:10px}}
.cmp{{width:100%;border-collapse:separate;border-spacing:0;margin-top:44px;font-size:21px;border-radius:24px;overflow:hidden;background:{T['card']};border:1px solid {T['line']}}}
.cmp th{{padding:24px 12px;font-size:21px;background:{T['bg2']};color:{T['sub']};font-weight:700}}
.cmp th.us{{background:{T['ac']};color:{T['pillInk']}}}
.cmp td{{padding:22px 12px;border-top:1px solid {T['line']};line-height:1.5}}
.cmp td:first-child{{font-weight:800;width:170px;color:{T['ink']}}}
.cmp td.us{{color:{T['ac']};font-weight:800;background:{T['usBg']}}}
.cmp td.no{{color:{T['sub']}}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:44px}}
.grid2 figure{{background:{T['card']};border-radius:22px;overflow:hidden;border:1px solid {T['line']};text-align:left}}
.grid2 img{{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}}
.grid2 figcaption{{padding:20px 22px;font-size:19px;line-height:1.5}}
.grid2 figcaption b{{display:block;font-size:22px;margin-bottom:4px}}
.grid2 figcaption small{{color:{T['sub']};font-size:17px}}
.scene{{display:grid;grid-template-columns:1fr 1fr;gap:0}}
.scene figure{{position:relative}}
.scene img{{width:100%;height:560px;object-fit:cover;display:block}}
.scene figcaption{{position:absolute;left:18px;right:18px;bottom:18px;background:rgba(255,255,255,.9);color:#222;border-radius:16px;padding:16px 18px;font-size:18px;line-height:1.5;text-align:left}}
.scene figcaption b{{display:block;font-size:20px}}
.who{{display:grid;gap:12px;margin-top:44px;text-align:left}}
.who div{{display:flex;gap:20px;align-items:center;background:{T['card']};border-radius:22px;padding:22px 26px;border:1px solid {T['line']}}}
.who .e{{flex:none;width:70px;height:70px;border-radius:50%;background:{T['bg2']};display:grid;place-items:center;font-size:34px}}
.who b{{display:block;font-size:23px}}.who small{{display:block;font-size:18px;color:{T['sub']};margin-top:6px}}
.steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:44px}}
.steps div{{background:{T['card']};border-radius:24px;padding:34px 16px;border:1px solid {T['line']}}}
.steps em{{display:block;font-style:normal;font-family:HD,'Noto Sans CJK KR';font-size:44px;color:{T['ac']}}}
.steps b{{display:block;font-size:23px;margin-top:8px}}.steps small{{display:block;font-size:18px;color:{T['sub']};margin-top:8px;line-height:1.55}}
.box{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:40px}}
.box div{{background:{T['card']};border-radius:20px;padding:26px 6px;border:1px solid {T['line']}}}
.box .e{{font-size:42px}}.box b{{display:block;font-size:19px;margin-top:10px}}.box small{{display:block;font-size:16px;color:{T['sub']};margin-top:4px}}
.info{{width:100%;border-collapse:collapse;margin-top:40px;font-size:20px;text-align:left;background:{T['card']};border-radius:20px;overflow:hidden}}
.info td{{padding:20px 24px;border-bottom:1px solid {T['line']};line-height:1.55}}
.info td:first-child{{width:200px;color:{T['ac']};font-weight:800;background:{T['bg2']}}}
.trust{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:44px}}
.trust div{{border:2px dashed {T['line2']};border-radius:24px;padding:34px 10px}}
.trust .e{{font-size:46px}}.trust b{{display:block;font-size:21px;margin-top:10px}}.trust small{{display:block;font-size:16px;color:{T['sub']};margin-top:6px;line-height:1.5}}
.rv{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:40px}}
.rv div{{background:{T['card']};border-radius:20px;padding:20px;border:1px solid {T['line']};text-align:left}}
.rv .ph{{aspect-ratio:1/1;border-radius:14px;background:{T['bg2']};display:grid;place-items:center;font-size:16px;color:{T['sub']}}}
.rv .ln{{height:12px;border-radius:6px;background:{T['bg2']};margin-top:12px}}
.rv .st{{color:{T['ac']};font-size:18px;margin-top:14px;letter-spacing:2px}}
.q{{background:{T['card']};border-radius:20px;padding:28px 32px;margin-top:14px;text-align:left;border:1px solid {T['line']}}}
.q b{{font-size:23px;display:block}}.q p{{font-size:19px;color:{T['sub']};margin-top:10px;line-height:1.7}}
.ship{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:40px;text-align:left}}
.ship div{{background:{T['card']};border-radius:20px;padding:26px 24px;border:1px solid {T['line']}}}
.ship b{{display:block;font-size:21px}}.ship small{{display:block;font-size:17px;color:{T['sub']};margin-top:8px;line-height:1.6}}
.cta{{font-family:HD,'Noto Sans CJK KR';font-size:54px;line-height:1.35;margin-top:10px}}
.cta em{{font-style:normal;color:{T['invAc']}}}
.note{{font-size:15px;color:{T['sub']};margin-top:36px}}
"""
    h = []
    A = h.append
    # 1 hero
    A(f'<div class="sec" style="padding-bottom:70px"><span class="pill">{C["pill"]}</span><h1>{C["h1"]}</h1><p class="sub">{C["sub"]}</p></div>')
    A(f'<img class="full" src="{C["hero"]}">')
    # 2 summary
    A(f'<div class="sec"><div class="eye">SUMMARY</div><h2>{C["sumH"]}</h2><div class="tags">' + "".join(f"<span>#{t}</span>" for t in C["tags"]) + '</div><div class="nums">' + "".join(f"<div><b>{n}</b><small>{s}</small></div>" for n, s in C["nums"]) + '</div></div>')
    # 3 pain
    A(f'<div class="sec alt"><div class="eye">WORRY</div><h2>{C["painH"]}</h2><div class="pain">' + "".join(f"<div><i>✕</i>{p}</div>" for p in C["pains"]) + f'</div><div class="arrow">▼</div><p class="turn">{C["turn"]}</p></div>')
    # 4 reveal
    A(f'<img class="full" src="{C["reveal"]}"><p class="cap">{C["revealCap"]}</p><div style="height:60px"></div>')
    # 5-8 points
    for i, P in enumerate(C["points"], 1):
        cls = "sec" + (" alt" if i % 2 == 0 else "")
        A(f'<div class="{cls}" style="padding-bottom:64px"><div class="pt"><b>POINT {i:02d}</b><span>{P["en"]}</span></div><h2>{P["h"]}</h2><p class="sub">{P["s"]}</p>' + (('<div class="kv">' + "".join(f'<div><span class="e">{e}</span><b>{b}</b><small>{s}</small></div>' for e, b, s in P["kv"]) + '</div>') if P.get("kv") else "") + '</div>')
        if P.get("img"):
            A(f'<img class="full" src="{P["img"]}">' + (f'<p class="cap">{P["cap"]}</p><div style="height:40px"></div>' if P.get("cap") else ""))
    # 9 compare
    A(f'<div class="sec"><div class="eye">COMPARE</div><h2>{C["cmpH"]}</h2><table class="cmp"><tr><th></th><th>{C["cmpThem"]}</th><th class="us">{C["cmpUs"]}</th></tr>' + "".join(f'<tr><td>{a}</td><td class="no">{b}</td><td class="us">{c}</td></tr>' for a, b, c in C["cmp"]) + '</table><p class="note" style="margin-top:18px">※ 일반적인 제품과 비교한 예시 기준이에요</p></div>')
    # 10 detail grid
    A(f'<div class="sec alt"><div class="eye">DETAIL</div><h2>{C["detH"]}</h2><div class="grid2">' + "".join(f'<figure><img src="{src}"><figcaption><b>{b}</b><small>{s}</small></figcaption></figure>' for src, b, s in C["details"]) + '</div></div>')
    # 11 scenes
    A(f'<div class="sec" style="padding-bottom:60px"><div class="eye">SCENE</div><h2>{C["sceneH"]}</h2><p class="sub">{C["sceneS"]}</p></div><div class="scene">' + "".join(f'<figure><img src="{src}"><figcaption><b>{b}</b>{s}</figcaption></figure>' for src, b, s in C["scenes"]) + '</div>')
    # 12 who
    if C.get("process"):
        A(f'<div class="sec alt"><div class="eye">PROCESS</div><h2>{C["processH"]}</h2><p class="sub">{C.get("processS","")}</p></div>')
        for i,(img,t,d) in enumerate(C["process"],1):
            A(f'<img class="full" src="{img}"><div class="sec" style="padding:46px 70px 70px"><div class="pt"><b>STEP {i}</b></div><h2 style="font-size:40px">{t}</h2><p class="sub">{d}</p></div>')
    if C.get("story"):
        A(f'<div class="sec inv"><div class="eye">STORY</div><h2>{C["storyH"]}</h2><p class="sub">{C["story"]}</p></div>')
        if C.get("storyImg"): A(f'<img class="full" src="{C["storyImg"]}">')
    A(f'<div class="sec"><div class="eye">FOR YOU</div><h2>{C["whoH"]}</h2><div class="who">' + "".join(f'<div><span class="e">{e}</span><span><b>{b}</b><small>{s}</small></span></div>' for e, b, s in C["who"]) + '</div></div>')
    # 13 how
    A(f'<div class="sec alt"><div class="eye">HOW TO</div><h2>{C["howH"]}</h2><div class="steps">' + "".join(f'<div><em>{i}</em><b>{b}</b><small>{s}</small></div>' for i, (b, s) in enumerate(C["how"], 1)) + '</div>' + (f'<p class="cap" style="padding:26px 0 0">{C["howNote"]}</p>' if C.get("howNote") else "") + '</div>')
    if C.get("howImg"):
        A(f'<img class="full" src="{C["howImg"]}">')
    # 14 box
    A(f'<div class="sec"><div class="eye">IN THE BOX</div><h2>{C["boxH"]}</h2><div class="box">' + "".join(f'<div><div class="e">{e}</div><b>{b}</b><small>{s}</small></div>' for e, b, s in C["box"]) + '</div></div>')
    if C.get("boxImg"):
        A(f'<img class="full" src="{C["boxImg"]}">' + (f'<p class="cap">{C["boxCap"]}</p><div style="height:40px"></div>' if C.get("boxCap") else ""))
    # 15 info
    A(f'<div class="sec alt"><div class="eye">PRODUCT INFO</div><h2>상품 정보</h2><table class="info">' + "".join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in C["info"]) + '</table></div>')
    # 16 trust
    A(f'<div class="sec"><div class="eye">TRUST</div><h2>{C["trustH"]}</h2><div class="trust">' + "".join(f'<div><div class="e">{e}</div><b>{b}</b><small>{s}</small></div>' for e, b, s in C["trust"]) + '</div><p class="note" style="margin-top:20px">※ 점선 칸은 판매자님의 실제 인증서·시험 성적서로 채워지는 자리예요</p></div>')
    # 17 review slot
    A(f'<div class="sec alt"><div class="eye">REVIEW</div><h2>포토 후기가 들어갈 자리</h2><p class="sub">판매가 시작되면 실제 구매 고객의 사진 후기로 채워요.<br>가짜 후기는 넣지 않아요.</p><div class="rv">' + "".join('<div><div class="ph">📷 실제 후기 사진</div><div class="st">★★★★★</div><div class="ln"></div><div class="ln" style="width:70%"></div></div>' for _ in range(3)) + '</div></div>')
    # 18 faq
    A(f'<div class="sec"><div class="eye">Q&amp;A</div><h2>구매 전에 많이 물어보세요</h2><div style="margin-top:30px">' + "".join(f'<div class="q"><b>Q. {q}</b><p>{a}</p></div>' for q, a in C["faq"]) + '</div></div>')
    # 19 ship
    A(f'<div class="sec alt"><div class="eye">DELIVERY</div><h2>배송 · 교환 안내</h2><div class="ship">' + "".join(f'<div><b>{b}</b><small>{s}</small></div>' for b, s in C["ship"]) + '</div></div>')
    # 20 closing
    A(f'<img class="full" src="{C["endImg"]}"><div class="sec inv"><p class="cta">{C["cta"]}</p><p class="note">※ 찰칵상세 제작 예시 · 브랜드와 상품 정보는 예시로 만든 내용이에요</p></div>')
    html = f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{css}</style></head><body>' + "\n".join(h) + '</body></html>'
    open(f"{BASE}/{cat}/long.html", "w").write(html)
    return f"{BASE}/{cat}/long.html"
