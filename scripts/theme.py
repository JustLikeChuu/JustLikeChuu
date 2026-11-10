"""Shared palette + window chrome for the profile SVGs (amber CRT)."""

BG = "#0d0a06"          # window background
PANEL = "#120d07"       # inner panels
BORDER = "#3d2b12"      # window frame
AMBER = "#ffb000"       # primary phosphor
AMBER_HI = "#ffd27a"    # output text
AMBER_DIM = "#a8740b"   # secondary text
AMBER_FAINT = "#4a3510" # rules, empty cells
CREAM = "#ffeccc"       # typed commands
RED = "#ff4d3d"         # red-team accent

FONT = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
CHAR_W = 0.6            # monospace advance, in em


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def text_w(s, size):
    """Width a string occupies at a given font size (forced via textLength)."""
    return round(len(s) * size * CHAR_W, 2)


def defs_common():
    return f"""
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" opacity="0.35"/>
  </pattern>
  <radialGradient id="vig" cx="50%" cy="50%" r="75%">
    <stop offset="60%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity="0.55"/>
  </radialGradient>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="1.6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>"""


def window_open(w, h, title):
    return f"""
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="1" y="1" width="{w-2}" height="30" rx="10" fill="{PANEL}"/>
  <rect x="1" y="21" width="{w-2}" height="10" fill="{PANEL}"/>
  <line x1="1" y1="31" x2="{w-1}" y2="31" stroke="{BORDER}"/>
  <circle cx="20" cy="16" r="5" fill="{RED}"/>
  <circle cx="38" cy="16" r="5" fill="{AMBER}"/>
  <circle cx="56" cy="16" r="5" fill="{AMBER_FAINT}"/>
  <text x="{w/2}" y="20.5" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{AMBER_DIM}">{esc(title)}</text>"""


def window_close(w, h):
    # CRT overlay: scanlines + vignette, clipped to the window shape
    return f"""
  <clipPath id="win"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10"/></clipPath>
  <g clip-path="url(#win)" pointer-events="none">
    <rect width="{w}" height="{h}" fill="url(#scan)"/>
    <rect width="{w}" height="{h}" fill="url(#vig)"/>
  </g>"""
