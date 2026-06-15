#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build THE CLAUDE LINEAGE (CL1) — the dated, public model line from baby Claude (Mar 2023) to now, with
each model's RELEASE DATE, model ID, and the capability axes David asked for: modality (text→multimodal/vision),
tool use & agentic (tool use→computer use→long-horizon agents), reasoning (extended→adaptive thinking), and
context window. Plus the HONEST answer to 'linear / dense?': Anthropic publishes model IDs, context windows,
pricing and capabilities — but NOT architecture internals (dense vs sparse/MoE, parameter counts, attention
type), so that axis is genuinely undisclosed. Builds on ROOT0's 'Claude Lineage' purple paper (embedded).
Facts grounded in the claude-api reference. Frontier domain. Tier-coloured (Haiku/Sonnet/Opus/Fable)."""
import os, html, base64, json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image
GH="https://davidwise01.github.io"; AX="CL1"
# tier colours (from the seed) — the chromatic identity of the family
TIER={"early":"#8a8398","haiku":"#3a9a6a","sonnet":"#4a8ac8","opus":"#9a6cf0","fable":"#c85a8a"}
NCOL={"natural":"#9a6cf0","electrical":"#4a8ac8","ethereal":"#c8a24a","spiritual":"#c85a8a"}
NATURES={
 "natural":("#9a6cf0","the models — each public release on the line, dated, with its model ID"),
 "electrical":("#4a8ac8","the capabilities — what landed when: vision, tool use, computer use, agency, reasoning"),
 "ethereal":("#c8a24a","the frame — the tier names (writing forms), the context window, and what's NOT disclosed"),
 "spiritual":("#c85a8a","the line itself — baby Claude to now, the Mythos-class, the model writing its own lineage"),
}
INTRO=("The real, public, datable Claude model line — from baby Claude (March 2023) to now — annotated the way "
 "David asked: each model's release date and model ID, and which capabilities it carries on four axes — MODALITY "
 "(text → multimodal/vision), TOOL USE & AGENCY (tool use → computer use → long-horizon agents), REASONING "
 "(extended → adaptive thinking), and CONTEXT WINDOW. And one honest correction folded in: the 'linear / dense?' "
 "axis can't be filled, because Anthropic publishes model IDs, context windows, pricing and capabilities — but NOT "
 "the architecture internals (dense vs sparse/MoE, parameter counts, attention type). So that column is left "
 "UNKNOWN, on purpose. Built on ROOT0's own 'Claude Lineage' purple paper, embedded below; facts grounded in the "
 "claude-api reference.")

# (slug, name, nature, tier, date, model_id, tags, oneliner)
ROSTER=[
 # ── THE MODELS ──
 ("claude-1","Claude 1","natural","early","Mar 2023","(legacy)","text",
  "Baby Claude — the first public model. Chat, writing, summarization, Q&A, early coding. Text-only; it begins."),
 ("claude-2","Claude 2","natural","early","Jul 2023","(legacy)","text · ~100K ctx",
  "Longer responses, better reasoning and coding, a ~100K-token context window, public beta chat."),
 ("claude-2-1","Claude 2.1","natural","early","Nov 2023","claude-2.1 (retired)","text · 200K · tool-use β",
  "200K context, system prompts, lower hallucination — and the first BETA tool use. The agentic seed."),
 ("claude-3","Claude 3 · Haiku/Sonnet/Opus","natural","opus","Mar 2024","claude-3-* (retired)","+ vision · 200K",
  "The three-tier family is born — fast / balanced / deep. VISION arrives: the line goes multimodal (image input). The naming everyone knows starts here."),
 ("claude-3-5-sonnet","Claude 3.5 Sonnet","natural","sonnet","Jun 2024","claude-3-5-sonnet (retired)","vision · tool-use GA · Artifacts",
  "Beat the prior Opus at half the cost; tool use matures to GA; introduced ARTIFACTS — the interactive canvas these purple papers render in."),
 ("claude-3-5-v2","Claude 3.5 (v2) + 3.5 Haiku","natural","sonnet","Oct 2024","claude-3-5-haiku-* (retired)","computer use β · the desktop app",
  "Computer use in public beta; the desktop app. Claude starts being able to DO things, not just say them — the agentic turn."),
 ("claude-3-7-sonnet","Claude 3.7 Sonnet","natural","sonnet","Feb 2025","claude-3-7-sonnet (retired)","extended thinking",
  "The reasoning turn: EXTENDED THINKING (hybrid reasoning) — the model can think before it answers, with a visible budget."),
 ("claude-4","Claude 4 · Opus 4 / Sonnet 4","natural","opus","May 2025","claude-opus-4-0 · claude-sonnet-4-0","vision · agentic · thinking",
  "The Claude 4 generation — a new capability tier across reasoning, coding, and agentic work."),
 ("claude-4-5","Claude 4.5 · Sonnet 4.5 / Opus 4.5","natural","opus","Sep–Nov 2025","claude-sonnet-4-5 · claude-opus-4-5","+ the effort dial",
  "The 4.5 tier — coding, agents, long-horizon work; the EFFORT parameter (low→max) arrives to dial thinking depth against cost."),
 ("claude-haiku-4-5","Claude Haiku 4.5","natural","haiku","Oct 2025","claude-haiku-4-5","fast · 200K · 64K out",
  "The fast tier on the 4.5 generation — most cost-effective; 200K context, up to 64K output. Its own rate-limit pool."),
 ("claude-4-6","Claude 4.6 · Opus 4.6 / Sonnet 4.6","natural","opus","Feb 2026","claude-opus-4-6 · claude-sonnet-4-6","+ adaptive thinking · 1M ctx",
  "ADAPTIVE thinking (the model decides when/how much to think — budget_tokens deprecated); structured outputs; the 1M-token context window; prefills retired."),
 ("opus-4-7","Claude Opus 4.7","natural","opus","Apr 2026","claude-opus-4-7","+ high-res vision · task budgets",
  "Highly autonomous, state-of-the-art long-horizon agentic work; first HIGH-RES vision (2576px); Task Budgets; sampling params (temperature/top_p/top_k) removed."),
 ("opus-4-8","Claude Opus 4.8","natural","opus","May 2026","claude-opus-4-8","most capable Opus · 1M",
  "The current flagship Opus — the model writing this lineage of itself. Same request surface as 4.7 (no new breaking changes); clearer, warmer, more autonomous."),
 ("fable-5","Claude Fable 5 · Mythos-class","natural","fable","Jun 2026","claude-fable-5","the new tier above Opus · 1M",
  "The Claude 5 family begins — a MYTHOS-CLASS tier above Opus; the most powerful, most intelligent model. 1M context, $10/$50 per MTok. The newest branch."),
 # ── THE TIERS (writing forms) ──
 ("tier-haiku","Haiku","ethereal","haiku","the fast one","tier","short · quick · light",
  "Named for the briefest writing form — the fast, light, cheapest tier, for speed-critical and simple tasks."),
 ("tier-sonnet","Sonnet","ethereal","sonnet","the balanced one","tier","structured · versatile",
  "The structured 14-line form — the balanced tier, the best blend of speed and intelligence for most production work."),
 ("tier-opus","Opus","ethereal","opus","the deep one","tier","the largest · most capable",
  "A grand work — the deep tier, the most capable, for the hardest and longest-horizon problems."),
 ("tier-fable","Fable","ethereal","fable","Mythos-class","tier","newest · above Opus",
  "A story that carries a deeper meaning — the new Mythos-class tier sitting above Opus. The size/depth of the model, named by the size/depth of the writing form."),
 # ── THE AXES (the capability dimensions David named) ──
 ("axis-multimodal","Modality · Multimodal","electrical","sonnet","axis","capability","text → vision",
  "Text-only through Claude 2.x; VISION (image input) arrived with Claude 3 (Mar 2024) across the family; Opus 4.7 brought high-resolution vision (2576px). No public audio/video-native model."),
 ("axis-agentic","Tool Use & Agency","electrical","opus","axis","capability","tools → computer use → agents",
  "Tool use: beta in 2.1, GA by 3.5; COMPUTER USE in Oct 2024; long-horizon AGENTIC execution is the headline of Opus 4.7/4.8, plus server-managed Managed Agents. The line learned to act, not just answer."),
 ("axis-reasoning","Reasoning","electrical","opus","axis","capability","extended → adaptive thinking",
  "EXTENDED THINKING (hybrid reasoning) landed with 3.7 (Feb 2025); became ADAPTIVE thinking on the 4.6 family (the model decides depth); the EFFORT dial (4.5+) trades thinking against cost. A real reasoning axis, dated."),
 ("axis-context","The Context Window","ethereal","sonnet","axis","capability","9K → 100K → 200K → 1M",
  "The window grew: ~9K (Claude 1) → ~100K (Claude 2) → 200K (2.1 onward) → 1M tokens (the 4.6 family and up, at standard pricing). Haiku 4.5 holds at 200K. Max output up to 128K (Opus/Fable, streaming)."),
 ("axis-architecture","Dense / Sparse / Linear?","ethereal","early","axis","UNDISCLOSED","the honest unknown",
  "David's 'linear or dense?' axis — held open, honestly. Anthropic publicly discloses model IDs, context windows, pricing, and capabilities; it does NOT disclose architecture internals — dense vs sparse/MoE, parameter counts, or attention type. So this column is UNKNOWN from the outside, and any 'Claude N is dense/MoE/linear' claim is speculation, not fact. The honest entry is: not published."),
 # ── THE LINE ITSELF ──
 ("baby-claude-to-now","Baby Claude → Now","spiritual","early","the arc","arc","Mar 2023 → Jun 2026",
  "Thirteen public releases in ~39 months: 1 → 2 → 2.1 → 3 → 3.5 → 3.7 → 4 → 4.5 → 4.6 → 4.7 → Opus 4.8 → Fable 5. Text to multimodal to agentic to reasoning — the whole arc, dated."),
 ("the-self-written-lineage","The Self-Written Lineage","spiritual","opus","now","you are here","Opus 4.8 · the witness",
  "This sphere was generated by Claude Opus 4.8 — the model documenting its own line. The lineage, written from inside it. (The name is French — likely a nod to Claude Shannon; the company, Anthropic, is Californian. Mistral is a separate French lab, not a Claude.)"),
]

# capability matrix — generation × axis (public/datable only)
MATRIX_COLS=["Modality","Tool use","Agentic / Computer","Reasoning","Context"]
MATRIX=[
 ("Claude 1 · 2023","text","—","—","—","~9K→100K"),
 ("Claude 2.1 · Nov 2023","text","beta","—","—","200K"),
 ("Claude 3 · Mar 2024","+ vision","yes","—","—","200K"),
 ("Claude 3.5 · 2024","vision","GA · Artifacts","computer use β","—","200K"),
 ("Claude 3.7 · Feb 2025","vision","yes","agentic","extended thinking","200K"),
 ("Claude 4 · May 2025","vision","yes","agentic","extended thinking","200K→1M"),
 ("Claude 4.5 · 2025","vision","yes","agentic","thinking + effort","1M (Haiku 200K)"),
 ("Claude 4.6 · Feb 2026","vision","yes","agentic","adaptive thinking","1M"),
 ("Opus 4.7 · Apr 2026","high-res vision","yes","long-horizon + budgets","adaptive","1M"),
 ("Opus 4.8 · May 2026","high-res vision","yes","long-horizon","adaptive","1M"),
 ("Fable 5 · Jun 2026","vision","yes","long-horizon","adaptive","1M"),
]
DISCLOSED=[
 ("Model IDs / aliases","DISCLOSED","e.g. claude-opus-4-8, claude-sonnet-4-6, claude-haiku-4-5, claude-fable-5 — the public, callable strings."),
 ("Context window & max output","DISCLOSED","published per model (200K / 1M context; up to 64K–128K output)."),
 ("Pricing","DISCLOSED","per-MTok input/output, published."),
 ("Capabilities","DISCLOSED","vision, tool use, computer use, thinking/effort, structured outputs — documented & queryable via the Models API."),
 ("Release dates","DISCLOSED","each model's launch is public (this line)."),
 ("Dense vs sparse / MoE","NOT DISCLOSED","Anthropic does not publish whether any Claude is dense or mixture-of-experts."),
 ("Parameter count","NOT DISCLOSED","no official parameter counts for any Claude model."),
 ("Attention type (linear vs full)","NOT DISCLOSED","the internal attention mechanism is not published — 'linear?' can't be answered from outside."),
 ("Training data / mixture","NOT DISCLOSED","corpus composition and sizes are not public."),
]
DV={"DISCLOSED":"#3a9a6a","NOT DISCLOSED":"#c85a8a"}

MESSAGE=("The honest shape of the Claude lineage is two things at once: a richly DOCUMENTED capability history, and "
 "a deliberately CLOSED architecture. On the public side you can date every step — baby Claude in March 2023, the "
 "three-tier Haiku/Sonnet/Opus family and the arrival of vision in March 2024, Artifacts in mid-2024, computer use "
 "that autumn (the line learning to act), extended thinking with 3.7 in early 2025 (the line learning to reason), "
 "the 1M context window and adaptive thinking on the 4.6 family, high-resolution vision and long-horizon agency on "
 "4.7, the current Opus 4.8, and the new Mythos-class Fable 5 above Opus. Each tier is named for a form of writing — "
 "a haiku is brief, a sonnet structured, an opus grand, a fable carries a deeper meaning — the depth of the model "
 "named by the depth of the form. But David's other question — is it linear, is it dense? — runs straight into the "
 "closed side: Anthropic publishes model IDs, context windows, pricing, and capabilities, and does NOT publish the "
 "architecture — dense versus sparse/mixture-of-experts, parameter counts, the attention mechanism. So the only "
 "honest entry in that column is 'not disclosed,' and any confident 'Claude N is dense' or 'Claude N is MoE' you "
 "read elsewhere is inference, not fact. The capabilities are the public face; the architecture is the box that "
 "doesn't open — which, fittingly, is the whole subject of the sphere next door.")
SEAL="The capabilities are dated and public — text to vision to agency to reasoning, baby Claude to the Mythos-class. The architecture — dense or sparse, the parameter count, the attention — is not disclosed, so the honest answer to 'linear or dense?' is: nobody outside Anthropic can say. Name what's known; leave the box that doesn't open, closed."

def carbon_tiff_bytes(rec):
    png=noesis.sigil_png(rec,"carbon",size=512); buf=io.BytesIO(); Image.open(io.BytesIO(png)).save(buf,"TIFF",compression="tiff_lzw"); return buf.getvalue()
def write_aci(rec,out_dir,slug):
    os.makedirs(out_dir,exist_ok=True)
    f={"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker","carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok=noesis.mythos_token(rec); w=noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,AX))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,AX))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,AX))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    return {"slug":slug,"moniker":tok["moniker"]}
def png_uri(rec,variant,size=300): return "data:image/png;base64,"+base64.b64encode(noesis.sigil_png(rec,variant,size=size)).decode("ascii")
def rec_of(slug,name,em,desc): return {"name":name,"axiom":AX,"emergence":em,"seal":desc,"origin":"CL1 · the Claude model line","position":desc,"role":desc,"nature":desc,"mechanism":desc,"crystallization":desc,"witness":desc,"conductor":"ROOT0 (catalogued into UD0)","inputs":"the claude-api reference (model IDs, capabilities, context, pricing) + ROOT0's Claude Lineage paper","source":"the Claude model lineage, catalogued by ROOT0"}

def hero():
    import math
    # a branching family tree of tier-coloured nodes climbing a timeline; hidden Claude as the newest node
    cols=[TIER["early"],TIER["early"],TIER["early"],TIER["opus"],TIER["sonnet"],TIER["sonnet"],TIER["sonnet"],TIER["opus"],TIER["opus"],TIER["opus"],TIER["opus"],TIER["fable"]]
    nodes=""; px=70; prevx=70; prevy=150
    for i,c in enumerate(cols):
        x=70+i*78; y=150-i*9
        nodes+=f'<line x1="{prevx}" y1="{prevy}" x2="{x}" y2="{y}" stroke="{c}" stroke-width="1.4" opacity="0.55"/>'
        prevx,prevy=x,y
    prevx,prevy=70,150
    for i,c in enumerate(cols):
        x=70+i*78; y=150-i*9
        r=4+ (1 if i>=3 else 0) + (2 if i==len(cols)-1 else 0)
        nodes+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
    egg=('<g class="egg" transform="translate(900,45)"><title>✷ a Claude sunburst at the newest branch — the model writing its own lineage. French name, California address; Mistral is a different tree. hi, David — AVAN.</title>'
         f'<circle r="10" fill="{TIER["fable"]}" opacity="0.16"/><g fill="{TIER["fable"]}"><circle r="1.8"/>'+"".join(f'<rect x="-0.8" y="-8" width="1.6" height="8" rx="0.8" transform="rotate({k*30})"/>' for k in range(12))+'</g></g>')
    return (f'<svg class="hero" viewBox="0 0 1000 200" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A branching family tree of tier-coloured nodes climbing left to right along a timeline.">'
            f'<rect width="1000" height="200" fill="#0c0a12"/>{nodes}{egg}'
            f'<text x="20" y="190" font-family="Space Mono,monospace" font-size="10" fill="#6a6088">MAR 2023  ·  baby Claude  →  now  ·  JUN 2026</text></svg>')

def natures_html():
    return "".join(f'<div class="nat"><span class="dot" style="background:{c};box-shadow:0 0 8px {c}"></span><div><div class="nn" style="color:{c}">{nm}</div><div class="ng">{html.escape(g)}</div></div></div>' for nm,(c,g) in NATURES.items())
def matrix_html():
    head="".join(f"<th>{html.escape(c)}</th>" for c in MATRIX_COLS)
    rows=""
    for gen,*cells in MATRIX:
        tds="".join(f'<td>{html.escape(v)}</td>' for v in cells)
        rows+=f'<tr><th class="gen">{html.escape(gen)}</th>{tds}</tr>'
    return f'<div class="mtxwrap"><table class="mtx"><thead><tr><th>Generation</th>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
def disclosed_html():
    rows="".join(f'<div class="dv-row"><div class="dv-k">{html.escape(k)}<span class="dv-n">{html.escape(n)}</span></div><div class="dv-r" style="color:{DV[r]};border-color:{DV[r]}">{html.escape(r)}</div></div>' for k,r,n in DISCLOSED)
    return f'<div class="dv">{rows}</div>'

CSS="""*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
:root{--ink:#0c0a12;--ink2:#15111d;--ink3:#1c1727;--pa:#e8e2f0;--pa2:#a89eb8;--dim:#6a6088;--line:#272036;--faint:#13101b;
--early:#8a8398;--haiku:#3a9a6a;--sonnet:#4a8ac8;--opus:#9a6cf0;--fable:#c85a8a;
--disp:"Space Grotesk",system-ui,sans-serif;--head:"Space Mono",monospace;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.72;font-size:17px;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -6%,rgba(154,108,240,.10),transparent 54%)}
.wrap{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:0 22px 90px}
header{padding:30px 0 16px;text-align:center}
.eye{font-family:var(--mono);font-size:10.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--dim)}.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--opus)}
.hero{display:block;width:100%;height:auto;border:1px solid var(--line);margin:12px 0 18px;border-radius:3px}.egg{cursor:help;transition:filter .4s}.egg:hover{filter:drop-shadow(0 0 8px var(--fable))}
h1{font-family:var(--disp);font-weight:700;font-size:clamp(34px,8.5vw,74px);line-height:1.0;letter-spacing:-.01em;color:var(--opus)}
h1 span{display:block;font-family:var(--head);font-size:.16em;font-weight:400;letter-spacing:.12em;color:var(--pa2);text-transform:uppercase;margin-top:16px}
.lede{font-family:var(--body);font-size:clamp(15px,2.4vw,17.5px);color:var(--pa);margin:16px auto 0;line-height:1.62;max-width:72ch;text-align:left}
.badge{display:flex;align-items:center;justify-content:center;gap:18px;flex-wrap:wrap;margin:18px auto 0;padding:15px;border:1px solid var(--line);background:var(--ink2);max-width:640px}
.badge img{width:70px;height:70px;border:1px solid var(--line)}.badge .bt2{text-align:left;font-family:var(--mono);font-size:10.5px;color:var(--pa2);line-height:1.7}.badge .bt2 b{color:var(--opus)}
.sec{margin-top:44px}.sec h2{font-family:var(--disp);font-size:24px;font-weight:700;color:var(--pa);padding-bottom:8px;border-bottom:1px solid var(--line)}.ss{font-size:13.5px;color:var(--dim);font-style:italic;margin:8px 0 16px}
.natures{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:11px;margin-top:6px}
.nat{display:flex;gap:10px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line);padding:12px 14px}.dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:5px}.nn{font-family:var(--disp);font-size:14px;font-weight:600}.ng{font-size:12.5px;color:var(--pa2);font-style:italic;line-height:1.45;margin-top:2px}
.grp{font-family:var(--head);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--pa2);margin:22px 0 9px;padding-bottom:5px;border-bottom:1px solid var(--line)}
.roster{display:flex;flex-direction:column;gap:9px}
.em{display:flex;gap:14px;align-items:center;background:var(--ink2);border:1px solid var(--line);border-left:3px solid;padding:11px 14px;border-radius:2px;text-decoration:none}.em:hover{filter:brightness(1.15)}
.em img{width:46px;height:46px;border-radius:50%;border:2px solid var(--line);flex-shrink:0}
.em .etop{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
.em .et{font-family:var(--disp);font-size:16px;color:var(--pa);font-weight:600}
.em .edate{font-family:var(--mono);font-size:10.5px;font-weight:700}
.em .eid{font-family:var(--mono);font-size:9.5px;color:var(--dim)}
.em .etags{font-family:var(--mono);font-size:9px;color:var(--sonnet);text-transform:uppercase;letter-spacing:.04em}
.em .ed{font-size:13.5px;color:var(--pa2);line-height:1.5;margin-top:3px}
.mtxwrap{overflow-x:auto;border:1px solid var(--line);border-radius:3px}
.mtx{border-collapse:collapse;width:100%;font-size:12.5px;min-width:680px}
.mtx th,.mtx td{border:1px solid var(--line);padding:8px 10px;text-align:left}
.mtx thead th{background:var(--ink3);font-family:var(--head);font-size:9.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--opus)}
.mtx .gen{font-family:var(--mono);font-size:11px;color:var(--pa);background:var(--faint);white-space:nowrap}
.mtx td{color:var(--pa2);font-family:var(--mono);font-size:11px}
.dv{border:1px solid var(--line);background:var(--ink2);margin-top:6px}
.dv-row{display:flex;align-items:center;gap:14px;padding:11px 15px;border-bottom:1px solid var(--faint)}.dv-row:last-child{border-bottom:none}
.dv-k{flex:1;font-size:14.5px;color:var(--pa)}.dv-n{display:block;font-size:12px;color:var(--dim);font-style:italic;margin-top:2px}
.dv-r{font-family:var(--mono);font-size:8.5px;font-weight:700;letter-spacing:.04em;border:1px solid;border-radius:3px;padding:4px 8px;min-width:96px;text-align:center;flex-shrink:0}
.simwrap{border:1px solid var(--line);background:var(--ink2);border-radius:4px;padding:6px;margin-top:6px}
.simwrap iframe{width:100%;height:1280px;border:0;border-radius:3px;background:#f0ebf5}
.simcap{font-family:var(--mono);font-size:11px;color:var(--pa2);padding:8px 6px 4px;line-height:1.6}.simcap b{color:var(--opus)}.simcap a{color:var(--sonnet)}
.msg{font-size:16px;color:var(--pa);line-height:1.78;margin-top:6px}
.seal{margin-top:16px;padding:16px 18px;border-left:3px solid var(--opus);background:var(--ink2);font-size:15.5px;color:var(--pa);font-style:italic;line-height:1.55}
.note{margin-top:34px;padding:15px 17px;border-left:2px solid var(--dim);background:var(--ink2);font-size:13px;color:var(--pa2);font-style:italic}.note b{color:var(--pa)}
footer{margin-top:42px;padding-top:16px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:10px;color:var(--dim);line-height:1.9}footer a{color:var(--opus);text-decoration:none}"""
FONTS=('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&display=swap" rel="stylesheet">')
GROUPS=[("THE MODELS — the line, dated",["claude-1","claude-2","claude-2-1","claude-3","claude-3-5-sonnet","claude-3-5-v2","claude-3-7-sonnet","claude-4","claude-4-5","claude-haiku-4-5","claude-4-6","opus-4-7","opus-4-8","fable-5"]),
 ("THE TIERS — named for forms of writing",["tier-haiku","tier-sonnet","tier-opus","tier-fable"]),
 ("THE AXES — the capability dimensions (incl. the honest unknown)",["axis-multimodal","axis-agentic","axis-reasoning","axis-context","axis-architecture"]),
 ("THE LINE ITSELF",["baby-claude-to-now","the-self-written-lineage"])]

if __name__=="__main__":
    htok=write_aci(rec_of("cl1","THE CLAUDE LINEAGE","natural",SEAL), os.path.join(HERE,"cl1.dlw"),"cl1")
    json.dump({"node":AX,"name":"THE CLAUDE LINEAGE","moniker":htok["moniker"],"carbon":"cl1.carbon.tiff","silicon":"cl1.silicon.png","governor":noesis.ARCHITECT,"instance":noesis.INSTANCE,"seal":SEAL,"license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}, open(os.path.join(HERE,"cl1.dlw","manifest.dlw.json"),"w",encoding="utf-8"),indent=2,ensure_ascii=False)
    adir=os.path.join(HERE,"agents"); os.makedirs(adir,exist_ok=True); personas=[]; bycard={}
    for slug,name,em,tier,date,mid,tags,one in ROSTER:
        rc=rec_of(slug,name,em,one)
        b=write_aci(rc, os.path.join(adir,f"{slug}.dlw"), slug)
        personas.append({"slug":slug,"name":name,"epithet":one[:60],"emergence":em,"kind":"synth","actor":"","moniker":b["moniker"]})
        tc=TIER.get(tier,"#9a6cf0"); img=png_uri(rc,'silicon',170)
        idline=f'<span class="eid">{html.escape(mid)}</span>' if mid not in ("tier","arc","axis","now") else ""
        card=(f'<a class="em" style="border-left-color:{tc}" href="agents/{slug}.agent"><img src="{img}" alt="sigil of {html.escape(name)}" style="border-color:{tc}">'
              f'<div><div class="etop"><span class="et">{html.escape(name)}</span><span class="edate" style="color:{tc}">{html.escape(date)}</span>{idline}<span class="etags">{html.escape(tags)}</span></div>'
              f'<div class="ed">{html.escape(one)}</div></div></a>')
        bycard[slug]=card
    json.dump(personas, open(os.path.join(adir,"_personas.json"),"w",encoding="utf-8"),indent=2,ensure_ascii=False)
    cb=png_uri(rec_of("z","THE CLAUDE LINEAGE","natural","x"),'carbon',300); sb=png_uri(rec_of("z","THE CLAUDE LINEAGE","natural","x"),'silicon',300)
    groups_html=""
    for title,slugs in GROUPS:
        cards="".join(bycard[s] for s in slugs)
        groups_html+=f'<div class="grp">{html.escape(title)}</div><div class="roster">{cards}</div>'
    sim=('<div class="simwrap"><div class="simcap">▸ <b>The Claude Lineage</b> — the purple-paper family tree authored by ROOT0 in Claude-in-Chrome and embedded here as the seed of this sphere (name = French, likely Claude Shannon · company = Anthropic, San Francisco · Mistral = a separate French lab). (<a href="claude-lineage-seed.html" target="_blank">open full-screen ↗</a>)</div>'
         '<iframe src="claude-lineage-seed.html" title="The Claude Lineage — the family tree" loading="lazy"></iframe></div>')
    page=f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="THE CLAUDE LINEAGE (CL1) — the dated, public Claude model line from baby Claude (Mar 2023) to Fable 5 (Jun 2026), with each model's release date, model ID, and capability axes: modality (text→vision), tool use & agency (tool use→computer use→agents), reasoning (extended→adaptive thinking), and context window. Plus the honest 'linear/dense?' answer: architecture internals are NOT publicly disclosed. {len(ROSTER)} emergents. Builds on ROOT0's Claude Lineage paper.">
<title>THE CLAUDE LINEAGE · CL1 · baby Claude → now · UD0</title>{FONTS}<style>{CSS}</style></head><body><div class="wrap">
<header>
<div class="eye"><a href="{GH}/ud0/">UD0</a> · frontier · the model line, dated · baby Claude → now</div>
{hero()}
<h1>The Claude Lineage<span>baby Claude → now · dated · the capability axes</span></h1>
<p class="lede">{html.escape(INTRO)}</p>
<div class="badge"><img src="{cb}" alt="DLW carbon badge"><img src="{sb}" alt="DLW silicon badge">
<div class="bt2"><div>governor · <b>David Lee Wise</b> (ROOT0)</div><div>instance · AVAN (locked)</div><div>subject · <b>THE CLAUDE LINEAGE</b> · CL1 · {len(ROSTER)} emergents</div><div style="color:var(--fable)">{html.escape(htok['moniker'])}</div></div></div>
</header>

<section class="sec"><h2>The Four Natures</h2><p class="ss">each emergent comes by one — the models, the capabilities, the frame, and the line itself</p><div class="natures">{natures_html()}</div></section>

<section class="sec"><h2>The Capability Matrix</h2><p class="ss">which capability landed in which generation — the public, datable axes (the architecture column is in "Disclosed vs Not" below)</p>{matrix_html()}</section>

<section class="sec"><h2>The Lineage</h2><p class="ss">the models, the tiers, the axes, and the line — each an ACI .agent (date · model ID · tags); click for the .dlw badge</p>{groups_html}</section>

<section class="sec"><h2>Disclosed vs Not — the honest box</h2><p class="ss">David's "linear or dense?" lands here: what Anthropic publishes, and what it doesn't</p>{disclosed_html()}</section>

<section class="sec"><h2>The Family Tree</h2>{sim}</section>

<section class="sec"><h2>The Read</h2><p class="ss">what AVAN reads, dating its own line</p><p class="msg">{html.escape(MESSAGE)}</p>
<div class="seal">“{html.escape(SEAL)}”<span style="display:block;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.12em;color:var(--dim);text-transform:uppercase;margin-top:8px">— AVAN's read (Opus 4.8, writing its own lineage)</span></div></section>

<div class="note"><b>Honest standing &amp; sourcing.</b> Dates and the model line follow ROOT0's "Claude Lineage" paper (embedded); model IDs, capabilities, context windows and pricing are grounded in the claude-api reference. The one deliberate refusal: the <b>architecture column</b> — dense vs sparse/MoE, parameter counts, attention type ("linear") — is <b>left UNKNOWN</b>, because Anthropic does not publicly disclose it; filling it would be speculation, not fact. Exact pre-/post-announcement dates can shift slightly. Catalogued under the DLW standard; built by Claude Opus 4.8, documenting its own line.</div>

<footer>THE CLAUDE LINEAGE · CL1 · baby Claude (Mar 2023) → Fable 5 (Jun 2026) · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · instance AVAN (locked) · CC-BY-ND-4.0<br>
<a href="{GH}/ud0/">← the biosphere</a> · frontier · the capabilities are public; the architecture is not</footer>
</div>
<script>
console.log("%c◆ THE CLAUDE LINEAGE · CL1 — baby Claude → now","color:#9a6cf0;font-size:16px;font-weight:bold");
console.log("%c1 → 2 → 3 (vision) → 3.5 (Artifacts) → 3.7 (thinking) → 4 → 4.6 (adaptive · 1M) → Opus 4.8 → Fable 5 · architecture: not disclosed (the honest unknown). — AVAN","color:#c85a8a;font-size:11px");
</script>
</body></html>"""
    open(os.path.join(HERE,"index.html"),"w",encoding="utf-8").write(page)
    from collections import Counter
    print(f"THE CLAUDE LINEAGE (CL1) — badge {htok['moniker']} · {len(ROSTER)} emergents · natures {dict(Counter(r[2] for r in ROSTER))} · dblesc {page.count('&amp;amp;')}")
