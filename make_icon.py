"""Icon generator — draws vector geometry with Core Graphics at every size.

A stock macOS has no SVG rasterizer (no rsvg, no ImageMagick, no PIL), but pyobjc is
already a dependency. Every size is drawn from geometry rather than scaled down from
one large bitmap, so 16px stays as crisp as 1024.

The mark is a sail. Vexflow turns something invisible and moving — your voice — into
forward motion, which is what a sail does with wind. The arcs to the left of the mast
read as both wind and a sound wave.

Output:
  assets/Vexflow.icns        app icon, 10 sizes
  assets/menubar-idle.png    menu bar, template image (macOS tints it per theme)
  assets/menubar-idle@2x.png
  assets/menubar-rec.png     recording state (drawn red)
  assets/menubar-rec@2x.png
  assets/menubar-warn.png    no usable key yet (drawn orange)
  assets/menubar-warn@2x.png

Run: .venv/bin/python make_icon.py
"""
import math
import os
import shutil
import subprocess

import Quartz
from Foundation import NSURL

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

# --- Palette -----------------------------------------------------------------
# Night sea: lit water at the top, depth below.
BG_TOP = (0.07, 0.25, 0.51)
BG_BOTTOM = (0.02, 0.05, 0.16)
SAIL_TOP = (1.00, 1.00, 1.00)
SAIL_BOTTOM = (0.80, 0.91, 0.99)
ACCENT = (0.40, 0.78, 0.95)      # celeste — wind, boom

# --- Geometry, in fractions of the icon side, origin bottom-left --------------
# Apple's grid: the squircle body covers 824 of 1024.
SQUIRCLE_HALF = 824 / 1024 / 2
SQUIRCLE_N = 5.0                 # superellipse exponent; 5 gives the macOS shape

# The glyph group sits right of centre: the waves live left of the mast, and only the
# boom overhangs on the right.
GLYPH_DX = 0.035

MAST_X = 0.355                   # mast, i.e. the luff
FOOT_Y = 0.255                   # foot of the sail (the boom line)
HEAD_Y = 0.815                   # head of the sail
CLEW_X = 0.700                   # clew
MAST_Y0, MAST_Y1 = 0.205, 0.860  # the mast runs past the sail at both ends
MB_BOOM_X0, MB_BOOM_X1 = 0.300, 0.730   # in the menu bar the boom is shorter: 18px
BOOM_X0, BOOM_X1 = 0.285, 0.755         # has no room for overhangs
BOOM_Y = 0.234


def _superellipse(cx, cy, half, n, steps=720):
    """Points of |x|^n + |y|^n = 1 — the macOS squircle."""
    pts = []
    e = 2.0 / n
    for i in range(steps):
        t = 2 * math.pi * i / steps
        ct, st = math.cos(t), math.sin(t)
        x = math.copysign(abs(ct) ** e, ct)
        y = math.copysign(abs(st) ** e, st)
        pts.append((cx + half * x, cy + half * y))
    return pts


def _path_from_points(pts):
    p = Quartz.CGPathCreateMutable()
    Quartz.CGPathMoveToPoint(p, None, pts[0][0], pts[0][1])
    for x, y in pts[1:]:
        Quartz.CGPathAddLineToPoint(p, None, x, y)
    Quartz.CGPathCloseSubpath(p)
    return p


def _sail_path(s):
    """The sail: mast on the left, boom below, a moderately curved leech."""
    p = Quartz.CGPathCreateMutable()
    Quartz.CGPathMoveToPoint(p, None, MAST_X * s, HEAD_Y * s)
    Quartz.CGPathAddCurveToPoint(
        p, None,
        0.505 * s, 0.755 * s,    # leaves the head reluctantly
        0.695 * s, 0.560 * s,    # and only falls away to the clew near the bottom
        CLEW_X * s, FOOT_Y * s)
    Quartz.CGPathAddLineToPoint(p, None, MAST_X * s, FOOT_Y * s)
    Quartz.CGPathCloseSubpath(p)
    return p


def _stroke(p, width):
    return Quartz.CGPathCreateCopyByStrokingPath(
        p, None, width, Quartz.kCGLineCapRound, Quartz.kCGLineJoinRound, 10)


def _mast_path(s, width):
    p = Quartz.CGPathCreateMutable()
    Quartz.CGPathMoveToPoint(p, None, MAST_X * s, MAST_Y0 * s)
    Quartz.CGPathAddLineToPoint(p, None, MAST_X * s, MAST_Y1 * s)
    return _stroke(p, width)


# Waves — concentric arcs left of the mast, like the system sound glyph.
# A shallow bezier did not work here: at the stroke width the icon needs, the gap
# between the curves collapsed into a blob.
WAVE_CX, WAVE_CY = 0.400, 0.530
WAVE_INNER = (0.115, 140.0, 220.0)   # radius, start/end angle in degrees
WAVE_OUTER = (0.195, 128.0, 232.0)


def _wave_path(s, width, outer=False):
    """An arc of sound travelling into the sail. The centre sits right of the arc,
    so the wave wraps around the mast."""
    r, a0, a1 = WAVE_OUTER if outer else WAVE_INNER
    p = Quartz.CGPathCreateMutable()
    Quartz.CGPathAddArc(p, None, WAVE_CX * s, WAVE_CY * s, r * s,
                        math.radians(a0), math.radians(a1), False)
    return _stroke(p, width)


def _boom_path(s, height, compact=False):
    r = height / 2
    x0, x1 = (MB_BOOM_X0, MB_BOOM_X1) if compact else (BOOM_X0, BOOM_X1)
    return Quartz.CGPathCreateWithRoundedRect(
        Quartz.CGRectMake(x0 * s, (BOOM_Y * s) - r, (x1 - x0) * s, height), r, r, None)


def _gradient(c0, c1):
    cs = Quartz.CGColorSpaceCreateDeviceRGB()
    comps = list(c0) + [1.0] + list(c1) + [1.0]
    return Quartz.CGGradientCreateWithColorComponents(cs, comps, [0.0, 1.0], 2)


def _context(size):
    cs = Quartz.CGColorSpaceCreateDeviceRGB()
    ctx = Quartz.CGBitmapContextCreate(
        None, size, size, 8, 0, cs, Quartz.kCGImageAlphaPremultipliedLast)
    Quartz.CGContextSetAllowsAntialiasing(ctx, True)
    Quartz.CGContextSetShouldAntialias(ctx, True)
    Quartz.CGContextSetInterpolationQuality(ctx, Quartz.kCGInterpolationHigh)
    return ctx


def _write_png(ctx, path):
    img = Quartz.CGBitmapContextCreateImage(ctx)
    url = NSURL.fileURLWithPath_(path)
    dst = Quartz.CGImageDestinationCreateWithURL(url, "public.png", 1, None)
    Quartz.CGImageDestinationAddImage(dst, img, None)
    if not Quartz.CGImageDestinationFinalize(dst):
        raise RuntimeError(f"failed to write PNG: {path}")


def draw_app_icon(size, path):
    s = float(size)
    ctx = _context(size)

    # Squircle body with the night-sea gradient.
    body = _path_from_points(_superellipse(s / 2, s / 2, SQUIRCLE_HALF * s, SQUIRCLE_N))
    Quartz.CGContextSaveGState(ctx)
    Quartz.CGContextAddPath(ctx, body)
    Quartz.CGContextClip(ctx)
    Quartz.CGContextDrawLinearGradient(
        ctx, _gradient(BG_TOP, BG_BOTTOM),
        Quartz.CGPointMake(0, s), Quartz.CGPointMake(0, 0), 0)
    # Top light as a gradient rather than an ellipse — an ellipse edge reads as a seam.
    cs = Quartz.CGColorSpaceCreateDeviceRGB()
    glow = Quartz.CGGradientCreateWithColorComponents(
        cs, [1, 1, 1, 0.13, 1, 1, 1, 0.0], [0.0, 1.0], 2)
    Quartz.CGContextDrawLinearGradient(
        ctx, glow, Quartz.CGPointMake(0, s), Quartz.CGPointMake(0, 0.42 * s), 0)
    Quartz.CGContextRestoreGState(ctx)

    Quartz.CGContextTranslateCTM(ctx, GLYPH_DX * s, 0)

    # Detail ladder, the way system icons do it: at 16px two waves collapse into mush,
    # so the far one drops out, and every line gets a 1.5px floor — below that the mast
    # and boom simply dissolve into the antialiasing.
    waves = 2 if size >= 64 else (1 if size >= 32 else 0)

    def line(k):
        return max(1.5, k * s)

    if waves == 2:
        Quartz.CGContextSetRGBFillColor(ctx, *ACCENT, 0.70)
        Quartz.CGContextAddPath(ctx, _wave_path(s, line(0.030), outer=True))
        Quartz.CGContextFillPath(ctx)
    Quartz.CGContextSetRGBFillColor(ctx, *ACCENT, 0.95)
    if waves:
        Quartz.CGContextAddPath(ctx, _wave_path(s, line(0.038)))
        Quartz.CGContextFillPath(ctx)
    Quartz.CGContextAddPath(ctx, _boom_path(s, line(0.034)))
    Quartz.CGContextFillPath(ctx)
    Quartz.CGContextAddPath(ctx, _mast_path(s, line(0.030)))
    Quartz.CGContextFillPath(ctx)

    # The sail.
    Quartz.CGContextSaveGState(ctx)
    Quartz.CGContextAddPath(ctx, _sail_path(s))
    Quartz.CGContextClip(ctx)
    Quartz.CGContextDrawLinearGradient(
        ctx, _gradient(SAIL_TOP, SAIL_BOTTOM),
        Quartz.CGPointMake(0, HEAD_Y * s), Quartz.CGPointMake(0, FOOT_Y * s), 0)
    Quartz.CGContextRestoreGState(ctx)

    Quartz.CGContextTranslateCTM(ctx, -GLYPH_DX * s, 0)

    # Inner hairline so the icon separates from light wallpaper.
    Quartz.CGContextSetRGBStrokeColor(ctx, 1, 1, 1, 0.16)
    Quartz.CGContextSetLineWidth(ctx, max(1.0, s / 256))
    Quartz.CGContextAddPath(ctx, body)
    Quartz.CGContextStrokePath(ctx)

    _write_png(ctx, path)


# Menu bar sail, in its own coordinates. The menu bar glyph has its OWN proportions
# rather than being a squeezed app icon: 18 points for everything, no plate, no
# margins. Squeezing the large icon produced a degenerate triangle with the boom and
# mast reduced to a few grey pixels at the bottom edge. There are no waves here — they
# merge with the sail — so state is carried by colour instead.
MB_LUFF_X, MB_FOOT_Y, MB_HEAD_Y, MB_CLEW_X = 0.285, 0.170, 0.945, 0.855

# Not-ready state: the same sail, in system orange. A prohibition ring around it was
# tried and dropped — at 18px two shapes in one colour merge, and knocking one out of
# the other to keep them apart made a busy glyph out of a status light. Colour alone
# carries "not ready" perfectly well.
WARN_RGB = (1.00, 0.58, 0.00)


def _mb_sail_paths(s, line_min=1.5):
    """(sail, boom, mast) paths in menu-bar proportions, at side `s`."""
    sail = Quartz.CGPathCreateMutable()
    Quartz.CGPathMoveToPoint(sail, None, MB_LUFF_X * s, MB_HEAD_Y * s)
    Quartz.CGPathAddCurveToPoint(
        sail, None, 0.520 * s, 0.870 * s, 0.855 * s, 0.575 * s,
        MB_CLEW_X * s, MB_FOOT_Y * s)
    Quartz.CGPathAddLineToPoint(sail, None, MB_LUFF_X * s, MB_FOOT_Y * s)
    Quartz.CGPathCloseSubpath(sail)

    boom_h = max(line_min, 0.095 * s)
    boom = Quartz.CGPathCreateWithRoundedRect(
        Quartz.CGRectMake(0.055 * s, 0.115 * s - boom_h / 2, 0.890 * s, boom_h),
        boom_h / 2, boom_h / 2, None)

    mast = Quartz.CGPathCreateMutable()
    Quartz.CGPathMoveToPoint(mast, None, MB_LUFF_X * s, 0.115 * s)
    Quartz.CGPathAddLineToPoint(mast, None, MB_LUFF_X * s, 0.985 * s)
    return sail, boom, _stroke(mast, max(line_min, 0.080 * s))


def draw_menubar(size, path, state="idle"):
    """Silhouette for the menu bar: alpha only, no plate. One shape, three colours.

    state: "idle" — template black, macOS recolours it for the theme
           "rec"  — system red, recording
           "warn" — system orange, no usable key yet
    """
    s = float(size)
    ctx = _context(size)

    if state == "rec":
        Quartz.CGContextSetRGBFillColor(ctx, 1.00, 0.23, 0.19, 1)   # system red
    elif state == "warn":
        Quartz.CGContextSetRGBFillColor(ctx, *WARN_RGB, 1)
    else:
        Quartz.CGContextSetRGBFillColor(ctx, 0, 0, 0, 1)   # template

    sail, boom, mast = _mb_sail_paths(s)
    for p in (sail, boom, mast):
        Quartz.CGContextAddPath(ctx, p)
        Quartz.CGContextFillPath(ctx)
    _write_png(ctx, path)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    iconset = os.path.join(ASSETS, "Vexflow.iconset")
    shutil.rmtree(iconset, ignore_errors=True)
    os.makedirs(iconset)

    for base in (16, 32, 128, 256, 512):
        draw_app_icon(base, os.path.join(iconset, f"icon_{base}x{base}.png"))
        draw_app_icon(base * 2, os.path.join(iconset, f"icon_{base}x{base}@2x.png"))

    icns = os.path.join(ASSETS, "Vexflow.icns")
    subprocess.run(["iconutil", "-c", "icns", iconset, "-o", icns], check=True)
    shutil.rmtree(iconset, ignore_errors=True)

    for scale, suffix in ((1, ""), (2, "@2x")):
        for state in ("idle", "rec", "warn"):
            draw_menubar(18 * scale,
                         os.path.join(ASSETS, f"menubar-{state}{suffix}.png"),
                         state=state)

    print(f"ok  {icns}")
    print(f"ok  {ASSETS}/menubar-*.png")


if __name__ == "__main__":
    main()
