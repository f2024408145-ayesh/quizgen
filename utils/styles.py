"""
Color palette and font constants for the QuizGen app.
Dark navy + electric blue + soft white accent.
"""

# ── Palette ────────────────────────────────────────────────────────────────
BG_DARK       = "#0F172A"   # page background
BG_CARD       = "#1E293B"   # card / panel background
BG_INPUT      = "#0F172A"   # input fields
ACCENT        = "#6366F1"   # indigo — primary CTA
ACCENT_HOVER  = "#818CF8"   # lighter indigo on hover
SUCCESS       = "#22C55E"   # correct answer
DANGER        = "#EF4444"   # wrong answer
WARNING       = "#F59E0B"   # caution / partial
TEXT_PRIMARY  = "#F1F5F9"   # headings
TEXT_SECONDARY= "#94A3B8"   # body / meta
TEXT_MUTED    = "#475569"   # placeholders
BORDER        = "#334155"   # subtle borders
OPTION_BG     = "#1E293B"   # MCQ option tile bg
OPTION_HOVER  = "#334155"
OPTION_SEL    = "#312E81"   # selected option

# ── Fonts ──────────────────────────────────────────────────────────────────
FONT_HEADING  = ("Segoe UI", 22, "bold")
FONT_SUBHEAD  = ("Segoe UI", 15, "bold")
FONT_BODY     = ("Segoe UI", 11)
FONT_BODY_B   = ("Segoe UI", 11, "bold")
FONT_SMALL    = ("Segoe UI", 9)
FONT_MONO     = ("Consolas", 10)
FONT_QUESTION = ("Segoe UI", 13, "bold")
FONT_OPTION   = ("Segoe UI", 11)

# ── Sizes ──────────────────────────────────────────────────────────────────
PAD           = 20
PAD_SM        = 10
RADIUS        = 8   # not natively used in Tk, kept for reference
