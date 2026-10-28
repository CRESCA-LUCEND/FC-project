"""Build the interactive SVGs for the Fizzy & Crush site from the brand sources.

Usage: python make_svgs.py <assetpack_dir> <out_dir>
"""
import math, re, sys, os

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
read = lambda f: open(os.path.join(src, f), encoding="utf-8").read()

# ---------- 1. Logo loader: liquid rises inside the letters only ----------
logo = read("fizzy&crush_logo.svg")
outline = re.findall(r'<path d="([^"]*)" class="cls-1"', logo)
letters = re.findall(r'<path d="([^"]*)" class="cls-2"', logo)
VB = (360, 135, 1200, 810)            # tight crop around the outline plate (369,144 1183x791)
TOP, BOT = 165, 915                   # liquid travel: below the lowest letter -> above the highest
AMP, PER = 16, 220                    # wave amplitude / period (user units)

def wave(amp, per, x0, x1, depth, phase=0.0):
    pts = []
    n = int((x1 - x0) / per * 16)
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append("%.1f %.1f" % (x, amp * math.sin(2 * math.pi * (x - x0) / per + phase)))
    return "M%s L%s L%.1f %d L%.1f %d Z" % (pts[0], " L".join(pts[1:]), x1, depth, x0, depth)

x0, x1 = VB[0] - 2 * PER, VB[0] + VB[2] + 2 * PER
H = BOT - TOP
letter_paths = "".join('<path d="%s"/>' % d for d in letters)
loader = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB[0]} {VB[1]} {VB[2]} {VB[3]}" class="fc-logo-loader" role="img" aria-label="Fizzy &amp; Crush" style="--fill:0;--liquid:#3f88c5;--liquid-top:#5196c4;--letters:#fce9be;--plate:#dfa06e">
  <!-- Drive --fill from 0 to 1 (load progress). Only the cream letters fill; the outline plate never changes.
       Recolour with --liquid / --liquid-top (e.g. lemon: #f7345d / #ff6b86). -->
  <style>
    .fc-logo-loader .lvl{{transform:translateY(calc((1 - var(--fill)) * {H}px));transition:transform .35s cubic-bezier(.3,.7,.2,1)}}
    .fc-logo-loader .w1{{animation:fcl-slide 2.4s linear infinite}}
    .fc-logo-loader .w2{{animation:fcl-slide 3.6s linear infinite reverse}}
    .fc-logo-loader .bub{{animation:fcl-rise 2.8s ease-in infinite;opacity:.55}}
    @keyframes fcl-slide{{to{{transform:translateX(-{PER}px)}}}}
    @keyframes fcl-rise{{0%{{transform:translateY(0);opacity:0}}20%{{opacity:.6}}100%{{transform:translateY(-140px);opacity:0}}}}
    @media (prefers-reduced-motion:reduce){{.fc-logo-loader .w1,.fc-logo-loader .w2,.fc-logo-loader .bub{{animation:none}}}}
  </style>
  <defs><clipPath id="fcl-letters">{letter_paths}</clipPath></defs>
  <g id="plate" fill="var(--plate)">{"".join('<path d="%s"/>' % d for d in outline)}</g>
  <g id="letters" fill="var(--letters)">{letter_paths}</g>
  <g id="liquid" clip-path="url(#fcl-letters)">
    <g transform="translate(0 {TOP})"><g class="lvl">
      <g class="w2" fill="var(--liquid-top)"><path d="{wave(AMP, PER, x0, x1, H + 60, 1.4)}" transform="translate(0 -10)"/></g>
      <g class="w1" fill="var(--liquid)"><path d="{wave(AMP, PER, x0, x1, H + 60)}"/></g>
      <g fill="var(--letters)">
        <circle class="bub" cx="520" cy="120" r="9"/><circle class="bub" cx="760" cy="200" r="6" style="animation-delay:.9s"/>
        <circle class="bub" cx="1010" cy="150" r="8" style="animation-delay:1.6s"/><circle class="bub" cx="1360" cy="230" r="7" style="animation-delay:.4s"/>
        <circle class="bub" cx="1180" cy="320" r="5" style="animation-delay:2.1s"/><circle class="bub" cx="640" cy="360" r="6" style="animation-delay:1.2s"/>
      </g>
    </g></g>
  </g>
</svg>
'''
open(os.path.join(out, "logo_loader.svg"), "w", encoding="utf-8").write(loader)

# ---------- 2. Mouth + straw: brand-pattern liquid travels up the straw ----------
mouth = read("mouth_svg.svg")
mp = re.findall(r'<path d="([^"]*)"\s*fill="([^"]*)"', mouth)
# path order in mouth_svg.svg: 0 lips, 1 mouth inside, 2-11 + 13 straw body/stripes, 12 teeth
STRAW = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]
CENTER = "M31.5 1050 L167.2 372 C176 327 210 279.5 250 260.75 L395 193.7"   # straw centreline, bottom -> tip
pat = read("brand_pattern.svg")
pat_body = re.search(r'<g id="Layer_1"[^>]*>(.*)</g>\s*</svg>', pat, re.S).group(1)
pat_body = pat_body.replace('class="cls-1"', 'fill="var(--liq-a)"').replace('class="cls-2"', 'fill="var(--liq-b)"')
def p(i): return '<path d="%s" fill="%s"/>' % (mp[i][0], mp[i][1])
straw = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 754 1043" class="fc-straw" role="img" aria-label="Lips sipping through a striped straw" style="--fill:0;--liq-a:#3f88c5;--liq-b:#fce9be">
  <!-- Drive --fill from 0 (empty) to 1 (liquid reaches the lips) with scroll.
       --liq-a / --liq-b recolour the liquid (rhubarb #3f88c5/#fce9be, lemon #c40831/#fce9be). -->
  <defs>
    <clipPath id="fcs-straw">{"".join('<path d="%s"/>' % mp[i][0] for i in STRAW)}</clipPath>
    <mask id="fcs-level" maskUnits="userSpaceOnUse" x="0" y="0" width="754" height="1043">
      <path d="{CENTER}" pathLength="1" fill="none" stroke="#fff" stroke-width="46" stroke-linecap="butt" style="stroke-dasharray:var(--fill) 2"/>
    </mask>
  </defs>
  <g id="lips">{p(0)}{p(1)}{p(12)}</g>
  <g id="straw">{"".join(p(i) for i in STRAW)}</g>
  <g id="liquid" clip-path="url(#fcs-straw)" mask="url(#fcs-level)">
    <rect width="754" height="1043" fill="var(--liq-a)"/>
    <g id="liq-pattern" transform="translate(-300 -40) scale(.62)">{pat_body}</g>
    <use href="#liq-pattern" y="700"/>
  </g>
</svg>
'''
open(os.path.join(out, "straw_fill.svg"), "w", encoding="utf-8").write(straw)

# ---------- 3. Brand pattern recoloured per section ----------
for name, a, b in [("cream", "#dfa06e", "#fce9be"), ("rhubarb", "#3f88c5", "#5196c4"), ("lemon", "#c40831", "#ce103a")]:
    s = pat.replace("fill:#dfa06e", "fill:" + a).replace("fill:#fce9be", "fill:" + b)
    open(os.path.join(out, f"pattern_{name}.svg"), "w", encoding="utf-8").write(s)
print("ok")
