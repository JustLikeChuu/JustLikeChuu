#!/usr/bin/env python3
"""
Render assets/hero.svg: an amber CRT terminal window with a hooded avatar that
draws itself in (stroke animation), next to a shell session that types out.

Pure CSS animation (no JS, no embedded fonts) so it plays inside GitHub's <img>
sandbox and stays light. Edit LINES below to change what the terminal says.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import *  # noqa: E402,F403

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "hero.svg")

W, H = 900, 400
PROMPT = "ethan@sutd:~$ "

# ("cmd", text) is typed after the prompt; ("out", text) prints instantly.
# Output lines may start with a tag: [+] active (red), [>] queued, [~] on hold.
LINES = [
    ("cmd", "whoami"),
    ("out", "Ethan Ng  //  CS @ SUTD, Year 3  //  Cybersecurity x AI"),
    ("cmd", "cat ./status"),
    ("out", "[+] interning   DSO National Labs: AI-assisted fuzzing"),
    ("out", "[+] targeting   penetration testing / red teaming"),
    ("out", "[+] building    secure FTP & multiplayer Tetris in C"),
    ("out", "[>] queued      AD lab / web app sec / LLM red teaming"),
    ("out", "[~] training    HTB / THM / OSCP: on hold till post-DSO"),
    ("cmd", "echo $MOTTO"),
    ("out", "learn how it works. then learn how it breaks."),
]

FS = 14.5         # font size
LH = 25           # line height
TX = 352          # terminal text x
TY = 70           # first baseline
TYPE_SPEED = 0.045  # s per typed char
OUT_GAP = 0.09      # s between printed output lines
START = 0.5


def avatar():
    """Original hooded figure behind a laptop. Strokes draw in, fills fade in."""
    s = AMBER
    return f"""
  <g class="av">
    <!-- light spill from the laptop -->
    <ellipse cx="175" cy="250" rx="120" ry="95" fill="url(#spill)" class="fade" style="animation-delay:1.6s"/>

    <!-- hood + shoulders -->
    <path class="fill fade" style="animation-delay:1.5s" fill="{PANEL}"
      d="M40 392 L40 348 C45 322 75 306 100 296 C92 220 108 96 175 78 C242 96 258 220 250 296 C275 306 305 322 310 348 L310 392 Z"/>
    <path class="draw" pathLength="1" stroke="{s}" style="animation-delay:0s"
      d="M40 392 L40 348 C45 322 75 306 100 296 C92 220 108 96 175 78 C242 96 258 220 250 296 C275 306 305 322 310 348 L310 392"/>
    <!-- hood folds -->
    <path class="draw thin" pathLength="1" stroke="{AMBER_DIM}" style="animation-delay:.5s"
      d="M118 290 C110 210 128 120 175 100 C222 120 240 210 232 290"/>
    <path class="draw thin" pathLength="1" stroke="{AMBER_DIM}" style="animation-delay:.7s" d="M100 296 C120 312 150 318 175 318 C200 318 230 312 250 296"/>

    <!-- face opening -->
    <path class="fade" style="animation-delay:1.3s" fill="url(#face)"
      d="M130 252 C122 190 138 130 175 122 C212 130 228 190 220 252 C205 270 145 270 130 252 Z"/>
    <path class="draw" pathLength="1" stroke="{s}" style="animation-delay:.35s"
      d="M130 252 C122 190 138 130 175 122 C212 130 228 190 220 252 C205 270 145 270 130 252 Z"/>

    <!-- jaw lit from below -->
    <path class="draw thin" pathLength="1" stroke="{AMBER_DIM}" style="animation-delay:1.1s" d="M156 240 Q176 249 198 234"/>

    <!-- glasses reflecting code -->
    <g filter="url(#glow)">
      <rect class="draw" pathLength="1" stroke="{s}" x="139" y="176" width="31" height="20" rx="4" style="animation-delay:.9s"/>
      <rect class="draw" pathLength="1" stroke="{s}" x="180" y="176" width="31" height="20" rx="4" style="animation-delay:1s"/>
      <path class="draw" pathLength="1" stroke="{s}" d="M170 184 L180 184" style="animation-delay:1.05s"/>
    </g>
    <g clip-path="url(#lenses)" class="fade" style="animation-delay:1.7s">
      <rect x="139" y="176" width="72" height="20" fill="{AMBER}" opacity="0.12"/>
      <g class="scroll" fill="{AMBER}" opacity="0.85">
        <rect x="142" y="178" width="14" height="1.6"/><rect x="183" y="178" width="20" height="1.6"/>
        <rect x="142" y="182" width="22" height="1.6"/><rect x="183" y="182" width="11" height="1.6"/>
        <rect x="146" y="186" width="10" height="1.6"/><rect x="187" y="186" width="17" height="1.6"/>
        <rect x="142" y="190" width="18" height="1.6"/><rect x="183" y="190" width="23" height="1.6"/>
        <rect x="146" y="194" width="13" height="1.6"/><rect x="187" y="194" width="9" height="1.6"/>
        <rect x="142" y="198" width="20" height="1.6"/><rect x="183" y="198" width="15" height="1.6"/>
        <rect x="142" y="202" width="9" height="1.6"/><rect x="183" y="202" width="21" height="1.6"/>
        <rect x="146" y="206" width="16" height="1.6"/><rect x="187" y="206" width="12" height="1.6"/>
        <rect x="142" y="210" width="14" height="1.6"/><rect x="183" y="210" width="20" height="1.6"/>
        <rect x="142" y="214" width="22" height="1.6"/><rect x="183" y="214" width="11" height="1.6"/>
      </g>
    </g>

    <!-- IEM cables out of the hood, into a splitter -->
    <path class="draw thin" pathLength="1" stroke="{AMBER_HI}" style="animation-delay:1.2s" d="M136 238 C140 270 158 292 175 306"/>
    <path class="draw thin" pathLength="1" stroke="{AMBER_HI}" style="animation-delay:1.25s" d="M214 238 C210 270 192 292 175 306"/>
    <rect class="fade" style="animation-delay:1.5s" x="171" y="303" width="8" height="10" rx="2" fill="{AMBER_HI}"/>

    <!-- laptop lid (back of screen faces us) -->
    <rect class="fill fade" style="animation-delay:1.4s" x="82" y="320" width="186" height="72" rx="6" fill="#1a1209"/>
    <rect class="draw" pathLength="1" stroke="{s}" x="82" y="320" width="186" height="72" rx="6" style="animation-delay:.6s"/>
    <line class="draw" pathLength="1" stroke="{AMBER_HI}" x1="86" y1="320" x2="264" y2="320" style="animation-delay:1s" filter="url(#glow)"/>
    <!-- stickers -->
    <g class="fade" style="animation-delay:1.9s" font-family="{FONT}">
      <rect x="104" y="338" width="44" height="20" rx="4" fill="{AMBER}"/>
      <text x="126" y="352" text-anchor="middle" font-size="11" font-weight="700" fill="{BG}">~$_</text>
      <circle cx="232" cy="350" r="12" fill="{RED}"/>
      <text x="232" y="354.5" text-anchor="middle" font-size="12" font-weight="700" fill="{BG}">0x</text>
      <rect x="160" y="362" width="52" height="16" rx="3" fill="none" stroke="{AMBER_DIM}"/>
      <text x="186" y="373.5" text-anchor="middle" font-size="9" fill="{AMBER_DIM}">./pwn</text>
    </g>
  </g>"""


keyframes = []


def tesc(s):
    """Escape + hard spaces, so SVG never collapses the terminal's spacing."""
    return esc(s).replace(" ", "&#160;")


def terminal():
    out = []
    keyframes.clear()
    t = START
    y = TY
    last_cursor_x = TX
    for i, (kind, txt) in enumerate(LINES):
        if kind == "cmd":
            pw = text_w(PROMPT, FS)
            cw = text_w(txt, FS)
            dur = round(len(txt) * TYPE_SPEED, 3)
            # prompt appears, then command types in behind a sliding cover
            out.append(f"""
    <g class="ln" style="animation-delay:{t:.2f}s">
      <text x="{TX}" y="{y}" textLength="{pw}" lengthAdjust="spacingAndGlyphs" fill="{AMBER}" font-weight="700">{tesc(PROMPT)}</text>
      <text x="{TX+pw}" y="{y}" textLength="{cw}" lengthAdjust="spacingAndGlyphs" fill="{CREAM}">{tesc(txt)}</text>
      <rect class="cover" x="{TX+pw}" y="{y-FS}" width="{cw+12}" height="{FS+6}" fill="{BG}" transform="translate({cw} 0)"
        style="animation:t{i} {dur}s steps({len(txt)}) {t+0.25:.2f}s both"/>
      <rect class="cur" x="{TX+pw}" y="{y-FS+2}" width="{FS*CHAR_W:.1f}" height="{FS+1}" fill="{AMBER}" opacity="0" transform="translate({cw} 0)"
        style="animation:t{i} {dur}s steps({len(txt)}) {t+0.25:.2f}s both, on {t+0.25+dur+0.15:.2f}s linear backwards"/>
    </g>""")
            keyframes.append(f"@keyframes t{i}{{from{{transform:translateX(0)}}to{{transform:translateX({cw}px)}}}}")
            t += 0.25 + dur + 0.2
        else:
            tag, rest = "", txt
            tag_colours = {"[+]": RED, "[>]": AMBER, "[~]": AMBER_DIM}
            if txt[:3] in tag_colours:
                tag, rest = txt[:3], txt[4:]
            parts = []
            x = TX
            if tag:
                tw = text_w(tag, FS)
                parts.append(f'<text x="{x}" y="{y}" textLength="{tw}" lengthAdjust="spacingAndGlyphs" fill="{tag_colours[tag]}" font-weight="700">{tag}</text>')
                x += tw + text_w(" ", FS)
            rw = text_w(rest, FS)
            parts.append(f'<text x="{x}" y="{y}" textLength="{rw}" lengthAdjust="spacingAndGlyphs" fill="{AMBER_HI}">{tesc(rest)}</text>')
            out.append(f"""
    <g class="ln" style="animation-delay:{t:.2f}s">{''.join(parts)}</g>""")
            t += OUT_GAP
            if i + 1 < len(LINES) and LINES[i + 1][0] == "cmd":
                y += 8  # breathing room before the next prompt
        y += LH
    # final idle prompt with a blinking cursor
    pw = text_w(PROMPT, FS)
    out.append(f"""
    <g class="ln" style="animation-delay:{t:.2f}s">
      <text x="{TX}" y="{y}" textLength="{pw}" lengthAdjust="spacingAndGlyphs" fill="{AMBER}" font-weight="700">{tesc(PROMPT)}</text>
      <rect class="blink" x="{TX+pw}" y="{y-FS+2}" width="{FS*CHAR_W:.1f}" height="{FS+1}" fill="{AMBER}"/>
    </g>""")
    return "".join(out), t


def statusbar():
    y = H - 22
    return f"""
  <line x1="332" y1="{y-16}" x2="{W-20}" y2="{y-16}" stroke="{AMBER_FAINT}"/>
  <g font-family="{FONT}" font-size="11.5" fill="{AMBER_DIM}">
    <circle cx="{TX+4}" cy="{y-4}" r="4" fill="{RED}" class="pulse"/>
    <text x="{TX+16}" y="{y}">online</text>
    <text x="{TX+80}" y="{y}">Singapore (UTC+8)</text>
    <text x="{W-24}" y="{y}" text-anchor="end">github.com/JustLikeChuu</text>
  </g>"""


def main():
    term, end_t = terminal()
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Ethan Ng: CS at SUTD, Cybersecurity and AI. Interning at DSO National Labs on AI-assisted fuzzing, working towards penetration testing.">
<title>Ethan Ng / JustLikeChuu</title>
<style>
  .draw{{fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;animation:draw 1.4s ease-out both}}
  .draw.thin{{stroke-width:1.4}}
  .fade{{animation:fade .8s ease-out both}}
  .scroll{{animation:scroll 3.2s linear infinite}}
  .ln{{animation:fade .01s linear both}}
  .blink{{animation:blink 1.05s steps(1) infinite}}
  .pulse{{animation:pulse 2.4s ease-in-out infinite}}
  .av{{animation:glitch 7s steps(1) {end_t+1:.1f}s infinite}}
  @keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
  @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
  @keyframes on{{from{{opacity:1}}to{{opacity:1}}}}
  {"".join(keyframes)}
  @keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
  @keyframes scroll{{from{{transform:translateY(0)}}to{{transform:translateY(-16px)}}}}
  @keyframes glitch{{0%{{transform:translate(0,0)}}96%{{transform:translate(-3px,0)}}97%{{transform:translate(2px,1px)}}98%{{transform:translate(0,0)}}}}
  @media (prefers-reduced-motion:reduce){{*{{animation-duration:0s!important;animation-delay:0s!important;animation-iteration-count:1!important}}}}
</style>
<defs>{defs_common()}
  <radialGradient id="spill" cx="50%" cy="85%" r="70%">
    <stop offset="0%" stop-color="{AMBER}" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="{AMBER}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="face" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#030201"/>
    <stop offset="70%" stop-color="#0a0703"/>
    <stop offset="100%" stop-color="#3a2606"/>
  </linearGradient>
  <clipPath id="lenses">
    <rect x="139" y="176" width="31" height="20" rx="4"/>
    <rect x="180" y="176" width="31" height="20" rx="4"/>
  </clipPath>
  <clipPath id="term"><rect x="336" y="40" width="{W-356}" height="{H-90}"/></clipPath>
</defs>
{window_open(W, H, "ethan@justlikechuu: ~ (zsh)")}
  <line x1="332" y1="44" x2="332" y2="{H-14}" stroke="{AMBER_FAINT}"/>
{avatar()}
  <g clip-path="url(#term)" font-family="{FONT}" font-size="{FS}">{term}
  </g>
{statusbar()}
{window_close(W, H)}
</svg>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg)/1024:.1f} KB), terminal finishes at {end_t:.1f}s")


if __name__ == "__main__":
    main()
