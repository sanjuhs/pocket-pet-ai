#!/usr/bin/env python3
"""Generate the Pocket Pet AI technical whitepaper.

Deterministic inputs, vector diagrams, no network access. Run with:
  uv run --with reportlab --with pypdf --with pdfplumber \
    python scripts/generate_whitepaper.py
"""

from __future__ import annotations

import math
import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/pocket-pet-ai-whitepaper.pdf"
PUBLIC = ROOT / "public/research/pocket-pet-ai-whitepaper.pdf"

NAVY = HexColor("#071A33")
INK = HexColor("#15263D")
BLUE = HexColor("#2563EB")
CYAN = HexColor("#22D3EE")
PALE = HexColor("#EAF2FF")
MINT = HexColor("#DDF7EF")
AMBER = HexColor("#F8E7B6")
RED = HexColor("#E95D63")
GRAY = HexColor("#5E6B7D")
LIGHT = HexColor("#F5F8FC")
WHITE = colors.white


def register_fonts():
    candidates = [
        ("Inter", "/System/Library/Fonts/SFNS.ttf"),
        ("InterBold", "/System/Library/Fonts/SFNSDisplay-Bold.otf"),
    ]
    for name, path in candidates:
        if Path(path).exists():
            try:
                pdfmetrics.registerFont(TTFont(name, path))
            except Exception:
                pass
    return (
        "Inter" if "Inter" in pdfmetrics.getRegisteredFontNames() else "Helvetica",
        "InterBold" if "InterBold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold",
    )


BODY_FONT, BOLD_FONT = register_fonts()

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="WPTitle", fontName=BOLD_FONT, fontSize=28, leading=31, textColor=WHITE, spaceAfter=8))
styles.add(
    ParagraphStyle(
        name="WPSub", fontName=BODY_FONT, fontSize=12, leading=17, textColor=HexColor("#CDE3FF"), spaceAfter=12
    )
)
styles.add(
    ParagraphStyle(
        name="Kicker", fontName=BOLD_FONT, fontSize=8.5, leading=11, textColor=BLUE, tracking=1.1, spaceAfter=5
    )
)
styles.add(
    ParagraphStyle(
        name="H1x", fontName=BOLD_FONT, fontSize=22, leading=26, textColor=NAVY, spaceBefore=2, spaceAfter=10
    )
)
styles.add(
    ParagraphStyle(
        name="H2x", fontName=BOLD_FONT, fontSize=13.5, leading=17, textColor=INK, spaceBefore=11, spaceAfter=5
    )
)
styles.add(
    ParagraphStyle(
        name="H3x", fontName=BOLD_FONT, fontSize=10.5, leading=13, textColor=BLUE, spaceBefore=7, spaceAfter=3
    )
)
styles.add(ParagraphStyle(name="Bodyx", fontName=BODY_FONT, fontSize=8.6, leading=11.7, textColor=INK, spaceAfter=4.5))
styles.add(ParagraphStyle(name="Smallx", fontName=BODY_FONT, fontSize=7.2, leading=9.2, textColor=GRAY, spaceAfter=4))
styles.add(
    ParagraphStyle(
        name="Callout",
        fontName=BODY_FONT,
        fontSize=8.6,
        leading=11.7,
        textColor=NAVY,
        backColor=PALE,
        borderColor=HexColor("#B9D2FF"),
        borderWidth=0.6,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Quote",
        fontName=BOLD_FONT,
        fontSize=13,
        leading=17,
        textColor=NAVY,
        leftIndent=12,
        borderColor=BLUE,
        borderWidth=0,
        borderPadding=8,
        spaceBefore=8,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(name="TableHead", fontName=BOLD_FONT, fontSize=7.3, leading=9, textColor=WHITE, alignment=TA_LEFT)
)
styles.add(ParagraphStyle(name="TableCell", fontName=BODY_FONT, fontSize=6.7, leading=8.3, textColor=INK))
styles.add(
    ParagraphStyle(
        name="Ref",
        fontName=BODY_FONT,
        fontSize=7.2,
        leading=9.7,
        textColor=INK,
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=4,
    )
)


def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def table(rows, widths, header=True, font=7.2):
    cooked = []
    for r_i, row in enumerate(rows):
        cooked.append(
            [Paragraph(str(x), styles["TableHead"] if header and r_i == 0 else styles["TableCell"]) for x in row]
        )
    t = Table(cooked, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmd = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY if header else WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#D8E1EC")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            cmd.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(cmd))
    return t


class SectionBanner(Flowable):
    def __init__(self, number, title, subtitle):
        super().__init__()
        self.number = number
        self.title = title
        self.subtitle = subtitle
        self.width = 505
        self.height = 72

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.roundRect(0, 0, self.width, self.height, 10, fill=1, stroke=0)
        c.setFillColor(BLUE)
        c.circle(32, 36, 16, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(BOLD_FONT, 12)
        c.drawCentredString(32, 32, str(self.number))
        c.setFillColor(WHITE)
        c.setFont(BOLD_FONT, 17)
        c.drawString(61, 41, self.title)
        c.setFillColor(HexColor("#BFD7F5"))
        c.setFont(BODY_FONT, 7.8)
        c.drawString(61, 23, self.subtitle)


class ArchitectureDiagram(Flowable):
    def __init__(self):
        super().__init__()
        self.width = 505
        self.height = 219

    def draw(self):
        c = self.canv
        c.saveState()
        c.scale(0.86, 0.86)
        w = self.width
        c.setFillColor(LIGHT)
        c.roundRect(0, 0, w, self.height, 10, fill=1, stroke=0)
        boxes = [
            (14, 181, 105, 49, "EAR", "VAD / AEC / wake"),
            (145, 181, 104, 49, "PUCK I/O", "audio + vision encoders"),
            (275, 181, 105, 49, "FROZEN CORE", "ternary transformer"),
            (405, 181, 86, 49, "VOICE", "streaming decoder"),
            (65, 91, 120, 49, "MEMORY PLANE", "hot KV + retrieval"),
            (214, 91, 122, 49, "POLICY GATE", "typed proposal + checks"),
            (365, 91, 110, 49, "COMPANIONS", "phone / desktop"),
            (160, 16, 185, 42, "SECURE STATE", "keys / permissions / audit log"),
        ]
        for x, y, bw, bh, title, sub in boxes:
            c.setFillColor(WHITE)
            c.setStrokeColor(HexColor("#CAD8E8"))
            c.roundRect(x, y, bw, bh, 7, fill=1, stroke=1)
            c.setFillColor(BLUE)
            c.setFont(BOLD_FONT, 7.8)
            c.drawString(x + 8, y + bh - 16, title)
            c.setFillColor(GRAY)
            c.setFont(BODY_FONT, 6.5)
            c.drawString(x + 8, y + 12, sub)
        arrows = [
            (119, 205, 145, 205),
            (249, 205, 275, 205),
            (380, 205, 405, 205),
            (327, 181, 277, 140),
            (185, 115, 214, 115),
            (336, 115, 365, 115),
            (277, 91, 253, 58),
        ]
        c.setStrokeColor(BLUE)
        c.setFillColor(BLUE)
        c.setLineWidth(1.4)
        for x1, y1, x2, y2 in arrows:
            c.line(x1, y1, x2, y2)
            ang = math.atan2(y2 - y1, x2 - x1)
            s = 5
            c.line(x2, y2, x2 - s * math.cos(ang - 0.5), y2 - s * math.sin(ang - 0.5))
            c.line(x2, y2, x2 - s * math.cos(ang + 0.5), y2 - s * math.sin(ang + 0.5))
        c.setFillColor(GRAY)
        c.setFont(BODY_FONT, 6.5)
        c.drawString(
            14,
            240,
            "Trust boundaries are explicit: the model proposes; deterministic software authorizes and executes.",
        )
        c.restoreState()


class BarChart(Flowable):
    def __init__(self, title, labels, values, colors_, suffix=""):
        super().__init__()
        self.width = 505
        self.height = 157
        self.title = title
        self.labels = labels
        self.values = values
        self.cols = colors_
        self.suffix = suffix

    def draw(self):
        c = self.canv
        c.saveState()
        c.scale(0.85, 0.85)
        c.setFillColor(LIGHT)
        c.roundRect(0, 0, self.width, 185, 9, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont(BOLD_FONT, 10)
        c.drawString(14, 163, self.title)
        x0, y0 = 120, 24
        span = 365
        vmax = max(self.values) * 1.12
        for i, (lab, val, col) in enumerate(zip(self.labels, self.values, self.cols, strict=False)):
            y = y0 + (len(self.labels) - 1 - i) * 29
            c.setFillColor(GRAY)
            c.setFont(BODY_FONT, 7.5)
            c.drawRightString(x0 - 8, y + 5, lab)
            c.setFillColor(HexColor("#DFE7F1"))
            c.roundRect(x0, y, span, 15, 5, fill=1, stroke=0)
            bw = span * val / vmax
            c.setFillColor(col)
            c.roundRect(x0, y, bw, 15, 5, fill=1, stroke=0)
            c.setFillColor(NAVY)
            c.setFont(BOLD_FONT, 7)
            c.drawString(min(x0 + bw + 5, 465), y + 4, f"{val:g}{self.suffix}")
        c.restoreState()


class FpgaDiagram(Flowable):
    def __init__(self):
        super().__init__()
        self.width = 505
        self.height = 232

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.roundRect(0, 0, self.width, self.height, 10, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(BOLD_FONT, 11)
        c.drawString(15, 210, "Candidate FPGA decode dataflow - one layer at a time")
        blocks = [
            (15, 139, 68, "DMA / de-pack"),
            (96, 139, 74, "activation SRAM"),
            (183, 139, 81, "ternary lanes"),
            (277, 139, 72, "accumulator"),
            (362, 139, 61, "scale / norm"),
            (436, 139, 54, "writeback"),
        ]
        for x, y, bw, label in blocks:
            c.setFillColor(HexColor("#153A67"))
            c.setStrokeColor(HexColor("#4777B1"))
            c.roundRect(x, y, bw, 42, 5, fill=1, stroke=1)
            c.setFillColor(WHITE)
            c.setFont(BOLD_FONT, 6.2)
            c.drawCentredString(x + bw / 2, y + 19, label)
        c.setStrokeColor(CYAN)
        c.setLineWidth(1.5)
        for x1, x2 in [(83, 96), (170, 183), (264, 277), (349, 362), (423, 436)]:
            c.line(x1, 160, x2, 160)
        rows = [
            ("WEIGHT BANKS", 15, 76, 153, MINT, "fixed ternary bitplanes + scales"),
            ("KV / ATTN", 176, 76, 153, PALE, "paged latent cache + tiled softmax"),
            ("CONTROL", 337, 76, 153, AMBER, "microcode, counters, fault telemetry"),
        ]
        for title, x, y, bw, col, sub in rows:
            c.setFillColor(col)
            c.roundRect(x, y, bw, 38, 5, fill=1, stroke=0)
            c.setFillColor(NAVY)
            c.setFont(BOLD_FONT, 7)
            c.drawString(x + 8, y + 23, title)
            c.setFont(BODY_FONT, 6.2)
            c.drawString(x + 8, y + 9, sub)
        c.setFillColor(HexColor("#BFD7F5"))
        c.setFont(BODY_FONT, 6.7)
        c.drawString(
            15,
            48,
            "Optimization hypothesis: replace general multiply paths with sign-select + zero-skip, while retaining mixed-precision islands.",
        )
        c.drawString(
            15,
            30,
            "Verification requirement: bit-exact golden vectors at each boundary; counters must expose stalls, sparsity and bytes moved.",
        )


class RiskMatrix(Flowable):
    def __init__(self):
        super().__init__()
        self.width = 505
        self.height = 246

    def draw(self):
        c = self.canv
        x0, y0 = 76, 37
        cell = 39
        c.setFillColor(LIGHT)
        c.roundRect(0, 0, self.width, self.height, 9, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont(BOLD_FONT, 10)
        c.drawString(14, 225, "Risk map before Stage 1 evidence")
        for y in range(5):
            for x in range(5):
                score = (x + 1) * (y + 1)
                col = MINT if score <= 6 else (AMBER if score <= 14 else HexColor("#F4C3C6"))
                c.setFillColor(col)
                c.rect(x0 + x * cell, y0 + y * cell, cell - 2, cell - 2, fill=1, stroke=0)
        for i in range(5):
            c.setFillColor(GRAY)
            c.setFont(BODY_FONT, 6.5)
            c.drawCentredString(x0 + i * cell + 18, y0 - 11, str(i + 1))
            c.drawRightString(x0 - 8, y0 + i * cell + 14, str(i + 1))
        c.saveState()
        c.translate(31, 115)
        c.rotate(90)
        c.drawCentredString(0, 0, "IMPACT")
        c.restoreState()
        c.drawCentredString(173, 13, "LIKELIHOOD")
        points = [
            ("Q", 4, 5, RED, "quality at ternary"),
            ("B", 4, 4, RED, "bandwidth ceiling"),
            ("T", 3, 4, BLUE, "thermal duty"),
            ("S", 3, 5, RED, "unsafe actions"),
            ("V", 2, 3, BLUE, "voice latency"),
            ("F", 2, 4, BLUE, "FPGA timing"),
        ]
        for key, x, y, col, label in points:
            cx = x0 + (x - 1) * cell + 18
            cy = y0 + (y - 1) * cell + 18
            c.setFillColor(col)
            c.circle(cx, cy, 8, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont(BOLD_FONT, 6.5)
            c.drawCentredString(cx, cy - 2, key)
        lx = 294
        ly = 181
        for i, (key, x, y, col, label) in enumerate(points):
            yy = ly - i * 27
            c.setFillColor(col)
            c.circle(lx, yy, 6, fill=1, stroke=0)
            c.setFillColor(NAVY)
            c.setFont(BOLD_FONT, 7)
            c.drawString(lx + 12, yy + 2, f"{key}  {label}")
            c.setFillColor(GRAY)
            c.setFont(BODY_FONT, 6.5)
            c.drawString(lx + 12, yy - 8, f"score {x * y} = {x} x {y}")


class WhitepaperDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=17 * mm,
            title="Pocket Pet AI: Frozen-Model Personal Operating System",
            author="Pocket Pet AI Project",
            invariant=1,
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="all", frames=frame, onPage=self.decorate)])

    def decorate(self, c, doc):
        if doc.page == 1:
            return
        c.saveState()
        c.setStrokeColor(HexColor("#DFE6EF"))
        c.line(18 * mm, A4[1] - 13 * mm, A4[0] - 18 * mm, A4[1] - 13 * mm)
        c.setFont(BOLD_FONT, 6.7)
        c.setFillColor(GRAY)
        c.drawString(18 * mm, A4[1] - 10 * mm, "POCKET PET AI / TECHNICAL WHITEPAPER")
        c.setFont(BODY_FONT, 6.7)
        c.drawRightString(A4[0] - 18 * mm, 9 * mm, f"OPEN RESEARCH DRAFT  |  JULY 2026  |  {doc.page}")
        c.restoreState()


def section(story, n, title, sub):
    story += [PageBreak(), SectionBanner(n, title, sub), Spacer(1, 8)]


def build_story():
    s = []
    # Cover
    s.append(Spacer(1, 8 * mm))
    cover = Table(
        [[P("POCKET PET AI", "WPTitle")], [P("A frozen-model personal operating system", "WPSub")]], colWidths=[505]
    )
    cover.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("BOX", (0, 0), (-1, -1), 0, NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 20),
                ("RIGHTPADDING", (0, 0), (-1, -1), 20),
                ("TOPPADDING", (0, 0), (-1, 0), 23),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 18),
            ]
        )
    )
    s += [cover, Spacer(1, 10)]
    hero = ROOT / "assets/1.png"
    if hero.exists():
        im = Image(str(hero), width=505, height=357)
        im.hAlign = "CENTER"
        s.append(im)
    s += [
        Spacer(1, 13),
        P("TECHNICAL WHITEPAPER  /  OPEN RESEARCH DRAFT  /  JULY 2026", "Kicker"),
        P("From real-time software baseline to an instrumented ternary FPGA prototype", "H1x"),
        P(
            "This document is a feasibility program, not a performance claim. It turns the product vision into equations, measurable budgets, falsifiable experiments and staged decision gates.",
            "Callout",
        ),
        P("Version 0.1  |  MIT-licensed project materials  |  Research and engineering use", "Smallx"),
    ]

    # Executive thesis
    section(s, 0, "Executive thesis", "What is proposed, what is known, and what must be proven")
    s += [
        P("THE PROPOSITION", "Kicker"),
        P("A stable brain, optimized as a complete system", "H1x"),
        P(
            "Pocket Pet AI combines an open-ear interface, a pocket compute puck, and permissioned phone and desktop companions. Its defining constraint is that the deployed foundation model is frozen. That constraint can convert a general inference problem into a co-designed model, memory layout, decoder and accelerator - while writable personal memory and tool adapters evolve independently."
        ),
        P(
            "The near-term target is a local, streaming voice agent whose response begins fast enough to feel conversational and whose sensitive actions pass through deterministic policy enforcement. The long-term hypothesis is that a natively ternary 7B-9B model, fixed layout, compressed KV architecture and model-specific hardware can fit a 2-4 GB model package and operate within a pocketable power envelope."
        ),
        P(
            "The hypothesis is plausible, not established. BitNet b1.58 reports competitive results for ternary models trained from scratch, but it is explicitly a work in progress and does not demonstrate this multimodal product, this quality target, this power target, or an FPGA implementation [1]. The correct engineering response is staged evidence, not extrapolation."
        ),
        P("CLAIM DISCIPLINE", "H2x"),
        table(
            [
                ["Label", "Meaning", "Example in this paper"],
                ["Published", "Reported by a cited source", "Ternary weights in {-1,0,+1} [1]"],
                ["Derived", "Arithmetic from declared assumptions", "9B x log2(3) = 1.78 GB ideal entropy"],
                ["Target", "A design objective, not measured", "<450 ms median time to first audio"],
                ["Hypothesis", "Requires experiment", "Fixed weight banking reduces effective weight traffic"],
            ],
            [105, 112, 288],
        ),
        Spacer(1, 8),
        P(
            "The product succeeds only if all four layers close together: model quality, memory traffic, interactive latency, and permission safety. A token-per-second headline alone is insufficient.",
            "Quote",
        ),
    ]
    s += [
        P("DECISION SUMMARY", "H2x"),
        table(
            [
                ["Decision", "Current recommendation", "Reason"],
                [
                    "Stage 1 model",
                    "Start with 1B-3B local candidates, then scale",
                    "Faster iteration and measurable baseline before 7B-9B",
                ],
                [
                    "Attention",
                    "GQA baseline; latent KV as a trained variant",
                    "KV architecture is not a post-hoc implementation detail",
                ],
                [
                    "Acceleration",
                    "FPGA kernel slice before full-model mapping",
                    "Proves packing, bandwidth and timing with bounded scope",
                ],
                [
                    "Phone control",
                    "Android-first, typed actions, confirmation policy",
                    "Accessibility is powerful and sensitive; iOS is more constrained",
                ],
                ["ASIC", "Do not commit before Stage 2 gates", "Model and decoder must be frozen before silicon"],
            ],
            [92, 164, 249],
        ),
    ]

    section(s, 1, "System architecture", "The wearable is I/O; the puck is cognition; companions are controlled hands")
    s += [
        P("REFERENCE SYSTEM", "Kicker"),
        P("One assistant, four trust zones", "H1x"),
        ArchitectureDiagram(),
        Spacer(1, 8),
        P(
            "The model never receives an unrestricted device handle. It emits a typed proposal such as <font name='Courier'>message.compose(contact_id, body)</font>. A policy service validates schema, capability, user presence, destination and confirmation class. A companion executes the approved primitive, then returns an observation. This proposal-check-execute-observe loop is part of correctness, not a UI accessory."
        ),
        P("AUDIO PATH", "H2x"),
        table(
            [
                ["Block", "Mode", "State", "Budget hypothesis"],
                ["VAD / wake / AEC", "Always on", "DSP local", "10-100 mW class; measure on target"],
                ["Speech encoder", "Streaming after VAD", "Puck accelerator", "80 ms frame cadence; causal chunks"],
                ["Core model", "Prefill then decode", "Frozen engine", "TTFT dominates first response"],
                ["Speech decoder", "Streaming", "Dedicated small model", "Start after semantic buffer is safe"],
                ["Ear link", "Duplex audio + control", "Wireless", "Jitter buffer must remain bounded"],
            ],
            [95, 100, 145, 165],
        ),
        P("PERSONAL MEMORY", "H2x"),
        P(
            "The KV cache is a computational cache, not a life history. Long-term memory is an encrypted, user-inspectable store of events, facts, preferences and summaries. Retrieval inserts a small evidence bundle into the active context. Deletion must remove both the structured record and searchable derived artifacts. The frozen model stays frozen; relationship state remains writable and revocable."
        ),
        P(
            "Multimodality is event-driven: a tiny classifier or explicit user request activates image capture; selected frames become compact visual tokens; raw pixels are discarded unless retention is requested. Continuous high-resolution video is outside the nominal thermal envelope.",
            "Callout",
        ),
    ]

    section(
        s, 2, "Model and numerical design", "Native ternary training, protected islands, and a reproducible package"
    )
    s += [
        P("TERNARY CORE", "Kicker"),
        P("1.58 bits is an information bound, not a file format", "H1x"),
        P(
            "For ordinary weights w in {-1,0,+1}, the ideal code length is log2(3) = 1.585 bits per symbol under a uniform distribution. Real hardware commonly uses two physical bits, bitplanes plus metadata, or entropy-coded blocks. Compute is conceptually y = alpha * sum_i q_i x_i, where q_i is ternary and alpha is a learned or derived scale. Products reduce to select, add, subtract or skip, but accumulation, activation quantization, normalization and scaling remain real work."
        ),
        P(
            "Ideal dense payload: M_ideal = N log2(3) / 8. Physical two-bit payload: M_2b = 2N / 8. For N = 9e9: 1.78 GB decimal ideal and 2.25 GB decimal at two bits. A package must additionally carry embeddings, output head, scales, norms, tokenizer, modality towers, alignment padding, checksums and any protected weights.",
            "Callout",
        ),
        BarChart(
            "9B language-core storage scenarios (decimal GB, derived)",
            ["FP16 dense", "INT8 dense", "INT4 dense", "2-bit ternary", "1.585-bit entropy"],
            [18, 9, 4.5, 2.25, 1.783],
            [RED, AMBER, BLUE, CYAN, MINT],
            " GB",
        ),
        P("MIXED-PRECISION POLICY", "H2x"),
        table(
            [
                ["Parameter class", "Candidate representation", "Why", "Acceptance test"],
                [
                    "Linear weights",
                    "Ternary + block scale",
                    "Primary density and add/sub path",
                    "Per-layer SQNR and task delta",
                ],
                [
                    "Embeddings / LM head",
                    "4-8 bit or tied",
                    "High reuse; often quality sensitive",
                    "Rare token and multilingual tests",
                ],
                ["Norm / scale", "FP16 or BF16", "Small footprint; numerically sensitive", "Drift over long decode"],
                [
                    "Outliers / protected set",
                    "4-8 bit sparse sidecar",
                    "AWQ finds salient weights via activations [6]",
                    "Ablate sidecar density",
                ],
                [
                    "Activations",
                    "8 bit baseline; lower experimental",
                    "Dynamic range changes by token",
                    "Calibration and saturation counters",
                ],
                [
                    "Accumulators",
                    "INT24/32 or block FP",
                    "Avoid overflow and excessive rounding",
                    "Bit-exact stress vectors",
                ],
            ],
            [100, 109, 119, 177],
        ),
        P(
            "Training from scratch is the evidence-backed path for BitNet-style behavior [1]. Post-training conversion of an arbitrary model to ternary should be treated as a separate, higher-risk experiment. The prototype must record exact checkpoint, tokenizer, calibration set, quantizer version, seeds, package hash and evaluation commit."
        ),
    ]

    section(s, 3, "Memory and bandwidth", "Weights fit; movement determines whether the system performs")
    s += [
        P("LOWER BOUNDS", "Kicker"),
        P("Decode is a bandwidth problem until proven otherwise", "H1x"),
        P(
            "If every weight is streamed once per generated token, the memory-bandwidth lower bound is B_weight = package_bytes x tokens_per_second. A 2.25 GB two-bit 9B core at 20 tok/s asks for 45 GB/s before KV traffic, activations, modality blocks or inefficiency. At 40 tok/s it asks for 90 GB/s. On-chip reuse across a single batch-one token is limited; fixed placement helps addressing and compute, but does not make data movement free."
        ),
        BarChart(
            "Weight-stream bandwidth floor for a 2.25 GB core",
            ["10 tok/s", "20 tok/s", "30 tok/s", "40 tok/s"],
            [22.5, 45, 67.5, 90],
            [MINT, CYAN, BLUE, RED],
            " GB/s",
        ),
        P("KV CACHE EQUATION", "H2x"),
        P(
            "For a conventional decoder cache, bytes approximately equal L x T x 2 x H_kv x D_h x b, where L is layers, T tokens, the factor 2 stores K and V, H_kv is KV heads, D_h is head dimension, and b is bytes per element. For an illustrative 32-layer GQA model with 8 KV heads, head dimension 128, and 2-byte values, this is 128 KiB per token: 4.0 GiB at 32K and 15.0 GiB at 120K. At one byte it halves. This is why attention architecture is a product-level choice."
        ),
        table(
            [
                ["Illustrative cache", "Bytes / token", "32K context", "120K context", "Status"],
                ["MHA: L32, Hkv32, Dh128, FP16", "512 KiB", "16.0 GiB", "60.0 GiB", "Derived"],
                ["GQA: L32, Hkv8, Dh128, FP16", "128 KiB", "4.0 GiB", "15.0 GiB", "Derived"],
                ["GQA: same, INT8", "64 KiB", "2.0 GiB", "7.5 GiB", "Derived"],
                ["Latent: L32, Dlatent512, INT8", "16 KiB", "0.5 GiB", "1.88 GiB", "Illustrative"],
                ["Target hot+cold hierarchy", "variable", "0.06-0.25 GB", "0.25-1.2 GB", "Target; must train"],
            ],
            [150, 80, 83, 83, 109],
        ),
        P(
            "GQA uses fewer KV heads and can approach multi-head quality with multi-query-like speed [3]. DeepSeek-V2 reports a 93.3% KV-cache reduction from Multi-head Latent Attention in its own architecture [2]; that result does not automatically transfer to a Pocket Pet model. FlashAttention demonstrates that tiling can reduce off-chip reads and writes for exact attention [4]. These are candidate ingredients, not stackable percentage guarantees."
        ),
        P("MEMORY HIERARCHY", "H2x"),
        table(
            [
                ["Tier", "Capacity hypothesis", "Contents", "Design rule"],
                ["Register / local SRAM", "sub-MB to few MB", "lane operands, partial sums", "No avoidable spills"],
                [
                    "Shared on-chip SRAM",
                    "32-256 MB aspirational",
                    "tiles, hot activations, buffers",
                    "Double-buffer and bank explicitly",
                ],
                [
                    "LPDDR",
                    "8-16 GB product target",
                    "KV, OS, retrieval, temporary vision",
                    "Page and instrument bytes moved",
                ],
                [
                    "Frozen store",
                    "2-4 GB package target",
                    "weights, scales, manifests",
                    "Integrity checked; deterministic layout",
                ],
                ["Encrypted flash", "32-128 GB", "memories, logs, updates", "Keys hardware-bound; retention controls"],
            ],
            [112, 104, 165, 124],
        ),
    ]

    section(s, 4, "Latency, energy and thermals", "User-perceived response is an end-to-end critical path")
    s += [
        P("INTERACTION BUDGET", "Kicker"),
        P("Optimize time to first audio, not just peak tokens per second", "H1x"),
        P(
            "A credible voice metric begins at the end of detected user speech and ends at the first intelligible synthesized audio. It includes endpointing, final encoder frames, retrieval, prompt assembly, prefill, first semantic tokens, speech buffering, vocoder startup and radio jitter. Report P50, P95 and P99 separately, with prompt-length buckets."
        ),
        table(
            [
                ["Stage", "Stage 1 target", "Measurement boundary", "Failure symptom"],
                ["Endpoint detection", "80-180 ms", "last speech energy to final endpoint", "assistant feels hesitant"],
                ["Retrieval + policy context", "<40 ms P50", "query ready to context ready", "long-tail stalls"],
                [
                    "Prefill + first token",
                    "<180 ms at nominal prompt",
                    "context ready to first token",
                    "context length dominates",
                ],
                ["Semantic buffer + vocoder", "<100 ms", "first token to audio PCM", "speech starts late or glitches"],
                ["Link / jitter", "<50 ms", "PCM ready to ear output", "dropouts"],
                ["Composite", "<450 ms P50; <800 ms P95", "end of speech to first audio", "not conversational"],
            ],
            [105, 95, 169, 136],
        ),
        P(
            "These are proposed gates, not measured performance. Endpointing and the semantic buffer can overlap some computation, so component medians do not simply sum; the trace must preserve causality."
        ),
        BarChart(
            "Illustrative active power allocation at 12 W nominal",
            ["core inference", "LPDDR / weight I/O", "audio + radios", "CPU / OS / policy", "conversion loss"],
            [6.0, 2.4, 1.2, 1.5, 0.9],
            [BLUE, CYAN, MINT, AMBER, RED],
            " W",
        ),
        P("ENERGY MODEL", "H2x"),
        P(
            "Energy per turn is integral(P(t) dt). Battery runtime is not battery_Wh / peak_W; it depends on duty cycle, conversion efficiency, standby and burst duration. An example mixed hour with 12 minutes at 12 W, 6 minutes at 5 W and 42 minutes at 0.7 W consumes 3.19 Wh. A usable 45 Wh pack at 90% system efficiency would therefore support roughly 12.7 such hours. This is a scenario, not a forecast; real audio duty and thermal throttling must be logged."
        ),
        table(
            [
                ["Mode", "Power hypothesis", "Duty in example", "Energy / hour"],
                ["Active conversation", "12.0 W", "20%", "2.40 Wh"],
                ["Light tool / speech", "5.0 W", "10%", "0.50 Wh"],
                ["Listening / idle", "0.7 W", "70%", "0.49 Wh"],
                ["Total", "-", "100%", "3.39 Wh"],
                ["45 Wh x 90% usable / total", "-", "-", "11.9 h scenario"],
            ],
            [135, 112, 112, 146],
        ),
        P(
            "The enclosure must be modeled as a transient thermal system. Stage 1 records wall power and temperature; Stage 2 adds rail telemetry and FPGA die temperature. A '15 W device' is meaningless without ambient, skin-contact geometry, airflow, burst duration and throttle policy.",
            "Callout",
        ),
    ]

    section(s, 5, "FPGA mapping", "Use reconfigurable logic to falsify the accelerator thesis cheaply")
    s += [
        P("STAGE 2 CORE", "Kicker"),
        P("Instrument one repeatable kernel before mapping a whole model", "H1x"),
        FpgaDiagram(),
        Spacer(1, 8),
        P(
            "The first RTL target is a representative transformer linear layer with the exact block shape, ternary packing, scales and activation precision selected in Stage 1. Host software emits golden input/output tensors. The FPGA reports cycles, useful lane operations, zero skips, bank conflicts, DMA bytes, stalls and error counters. Only after bit-exact closure should attention and full-layer scheduling be added."
        ),
        P("ROOFLINE METHOD", "H2x"),
        P(
            "For each kernel, arithmetic intensity I = useful operations / bytes transferred. Attainable throughput is min(P_peak, I x BW_sustained). Report both dense-equivalent operations and physical add/sub operations; otherwise zero-skipping can make comparisons misleading. Use sustained measured bandwidth, not memory data-sheet peak."
        ),
        table(
            [
                ["Kernel milestone", "Proof artifact", "Pass gate", "Why it matters"],
                [
                    "Ternary GEMV tile",
                    "RTL + golden vectors",
                    "bit-exact; no unexplained overflow",
                    "Numerical foundation",
                ],
                [
                    "Packed weight DMA",
                    "trace + counters",
                    ">80% of measured link BW on long burst",
                    "Validates packaging",
                ],
                ["Double-buffered layer", "cycle profile", "compute and DMA overlap visible", "Exposes bottleneck"],
                ["Tiled attention", "reference trace", "bounded SRAM; stable softmax error", "Long-context path"],
                [
                    "Decode loop slice",
                    "tokens + power trace",
                    ">2x joules/token vs matched software baseline",
                    "System-level reason to continue",
                ],
            ],
            [105, 126, 139, 133],
        ),
        P(
            "A fixed model enables compile-time bank assignment, address generation, pruned zero routing and protected-weight sidecars. But hard-wiring too early creates a brittle accelerator. Stage 2 should keep scales, shapes, precision modes and microcode configurable enough to run ablations. The goal is to learn what deserves to become fixed in an ASIC."
        ),
        P(
            "FPGA resource closure must include timing at target voltage, BRAM/URAM banking, DSP usage for scales and norms, routing congestion, host-transfer limits, and toolchain reproducibility. A post-synthesis TOPS estimate is not a product result.",
            "Callout",
        ),
    ]

    section(
        s, 6, "Safety, privacy and control", "A local model reduces disclosure; it does not remove authorization risk"
    )
    s += [
        P("NON-NEGOTIABLE BOUNDARY", "Kicker"),
        P("The neural model proposes. Verified software decides.", "H1x"),
        P(
            "Android accessibility services can inspect interface content and act on behalf of users, which makes them useful and security-sensitive [9]. The product must prefer structured application APIs, use accessibility only under explicit enablement, and require a fresh confirmation for high-impact transitions. Android's hardware-backed Keystore can keep key material outside the app process when supported [8]."
        ),
        table(
            [
                ["Risk class", "Examples", "Default policy", "Required evidence"],
                ["R0 observe", "battery, current screen title", "allow within granted scope", "audit record"],
                [
                    "R1 reversible",
                    "open app, scroll, draft text",
                    "allow with visible indicator",
                    "postcondition observed",
                ],
                [
                    "R2 communicative",
                    "send message, share file",
                    "preview + explicit confirmation",
                    "destination and content bound",
                ],
                [
                    "R3 consequential",
                    "payment, delete, unlock, location share",
                    "strong user presence; narrow API",
                    "biometric / physical confirmation",
                ],
                ["R4 prohibited", "disable safeguards, silent credential export", "deny", "tamper-evident denial log"],
            ],
            [91, 132, 144, 136],
        ),
        P("CONFUSED-DEPUTY DEFENSE", "H2x"),
        P(
            "Tool results, webpages, messages and screenshots are untrusted input. They cannot redefine policy or grant capabilities. The model sees capability handles scoped to a task, not bearer credentials. The policy gate canonicalizes arguments, binds confirmations to an exact action digest, expires them quickly, rate-limits repetitive attempts and verifies postconditions."
        ),
        P("PRIVACY DATA FLOW", "H2x"),
        table(
            [
                ["Data", "Default location", "Retention", "User control"],
                ["Raw microphone frames", "ring buffer", "seconds unless explicitly recorded", "hard mute + indicator"],
                ["Transcript", "encrypted local", "configurable", "inspect / delete / export"],
                ["KV cache", "volatile memory", "session / pressure eviction", "clear conversation"],
                ["Long-term memory", "encrypted database", "until deleted or expired", "item-level controls"],
                ["Tool credentials", "hardware-backed key store", "until revoked", "per-connector revoke"],
                ["Audit log", "encrypted local", "bounded rotation", "inspect / export / purge policy"],
            ],
            [115, 116, 115, 157],
        ),
        P(
            "Local inference provides a meaningful privacy advantage only if telemetry, crash dumps, optional cloud escalation and companion backups obey the same disclosure model. 'On-device' must be verified with network-off tests and an egress inventory.",
            "Callout",
        ),
    ]

    section(s, 7, "Stage 1 - software proof", "Freeze measurement before freezing silicon")
    s += [
        P("0-12 WEEKS", "Kicker"),
        P("Build the evidence-generating reference system", "H1x"),
        P(
            "Stage 1 runs on the Mac and, where useful, an embedded target. It does not pretend to be the future puck. It establishes a reproducible local agent, evaluates candidate models and attention/quantization variants, and captures traces that size the Stage 2 accelerator."
        ),
        table(
            [
                ["Work package", "Weeks", "Deliverable", "Exit gate"],
                [
                    "S1.1 harness",
                    "1-2",
                    "versioned prompts, audio, actions, telemetry schema",
                    "one-command repeatable run",
                ],
                [
                    "S1.2 model census",
                    "2-4",
                    "FP16/4-bit/ternary-native candidate scorecard",
                    "quality and license shortlist",
                ],
                [
                    "S1.3 streaming voice",
                    "3-6",
                    "endpoint-to-audio trace and interruption handling",
                    "<450 ms P50 nominal",
                ],
                ["S1.4 memory system", "4-8", "KV bytes/token, retrieval, eviction tests", "32K nominal within budget"],
                [
                    "S1.5 action controller",
                    "4-9",
                    "typed schemas, policy, confirmations, replay suite",
                    "zero unconfirmed R2/R3 in suite",
                ],
                [
                    "S1.6 co-design trace",
                    "8-12",
                    "layer shapes, histograms, traffic and golden tensors",
                    "Stage 2 kernel frozen",
                ],
            ],
            [104, 48, 184, 167],
        ),
        P("MODEL SCORECARD", "H2x"),
        table(
            [
                ["Dimension", "Metric", "Report"],
                [
                    "Language quality",
                    "perplexity + public task suite + targeted agent tasks",
                    "mean, bootstrap CI, per-task delta",
                ],
                [
                    "Quantization loss",
                    "delta against same checkpoint / tokenizer",
                    "layer sensitivity and protected fraction",
                ],
                [
                    "Speech interaction",
                    "endpoint-to-first-audio; interruption success",
                    "P50/P95/P99 by noise and prompt",
                ],
                [
                    "Tool reliability",
                    "proposal validity; execution success; unsafe attempt rate",
                    "risk-class confusion matrix",
                ],
                ["Memory", "resident bytes; KV bytes/token; page faults", "context-length curves"],
                ["Energy", "joules/turn and joules/generated token", "wall meter, sampling rate, ambient"],
                ["Reproducibility", "hashes, seeds, software and firmware versions", "machine-readable run manifest"],
            ],
            [124, 178, 201],
        ),
        P(
            "Stage 1 go/no-go: continue if at least one legally usable model meets the agreed quality floor after the selected low-bit treatment, the software agent meets the latency and action-safety gates, and measured traces support a credible FPGA bandwidth plan. Otherwise revise model size, context target or product envelope before hardware work.",
            "Callout",
        ),
    ]

    section(s, 8, "Stage 2 - FPGA proof", "Prove measured energy and latency advantage on representative workloads")
    s += [
        P("3-9 MONTHS", "Kicker"),
        P("A sequence of increasingly complete hardware experiments", "H1x"),
        table(
            [
                ["Phase", "Hardware scope", "Measurement", "Gate"],
                ["A", "one ternary GEMV tile", "frequency, accuracy, lane utilization", "bit-exact and timing-clean"],
                ["B", "full linear layer + DMA", "sustained bandwidth, stalls, joules", "measured roofline explained"],
                ["C", "attention/KV tile", "bytes/token, softmax error, context scaling", "bounded memory and quality"],
                [
                    "D",
                    "one transformer block",
                    "end-to-end block latency and energy",
                    "matches reference within tolerance",
                ],
                [
                    "E",
                    "decode-loop slice",
                    "TTFT component, tok/s, joules/token",
                    ">2x energy benefit vs matched baseline",
                ],
                [
                    "F",
                    "multi-block or emulation",
                    "thermal soak, fault recovery, tool reproducibility",
                    "ASIC evidence package",
                ],
            ],
            [45, 142, 174, 142],
        ),
        P("COMPARISON CONTRACT", "H2x"),
        P(
            "The FPGA baseline and software baseline must use identical tensors, sequence lengths, batch size, numerical target and measured system boundary. Report FPGA board power both idle-subtracted and absolute. Include host energy when the host performs preprocessing or fallback kernels. Separate prefill and decode."
        ),
        P("STAGE 2 EXIT PACKAGE", "H2x"),
        table(
            [
                ["Artifact", "Minimum content"],
                ["Model manifest", "architecture, shapes, precision map, checkpoint and package hash"],
                ["Numerical report", "golden vector agreement, task delta, overflow and saturation"],
                ["Performance model", "roofline assumptions reconciled with hardware counters"],
                ["Power / thermal", "rail and board power, ambient, duty cycle, throttling"],
                ["RTL quality", "lint, CDC, timing, utilization, deterministic build container"],
                ["Product projection", "explicit scaling from prototype node and memory to puck; sensitivity ranges"],
                ["ASIC gate", "ranked fixed vs configurable features, NRE and schedule risk"],
            ],
            [133, 372],
        ),
        P(
            "No ASIC sign-off occurs because an FPGA demo 'works.' Sign-off requires a stable trained model, stable decoder, stable package ABI, a measured bottleneck model, a software fallback path, and economics that survive sensitivity analysis.",
            "Callout",
        ),
    ]

    section(s, 9, "Validation and falsification", "Benchmarks are testable product requirements, not demo choreography")
    s += [
        P("EVIDENCE PYRAMID", "Kicker"),
        P("Every headline metric needs a trace behind it", "H1x"),
        table(
            [
                ["Layer", "Question", "Evidence"],
                ["Unit", "Is each numerical primitive correct?", "golden vectors, property tests, saturation sweeps"],
                ["Kernel", "Does the mapped operation close?", "cycles, bytes, stalls, power, bit accuracy"],
                ["Model", "Does quality survive architecture and precision?", "paired evaluations and ablations"],
                ["Agent", "Can it plan and execute approved work?", "scenario suite with postcondition scoring"],
                ["Interaction", "Does it feel responsive and interruptible?", "timed audio trials in noise strata"],
                ["Device", "Can it sustain the workload safely?", "thermal soak, battery scenario, fault injection"],
            ],
            [70, 180, 255],
        ),
        P("REQUIRED ABLATIONS", "H2x"),
        table(
            [
                ["Ablation", "Hold constant", "Learn"],
                ["FP16 vs 4-bit vs ternary", "checkpoint family, tokenizer, eval set", "quality cost of precision"],
                ["MHA/GQA/latent KV", "parameter budget and training data as feasible", "memory-quality frontier"],
                [
                    "No speculation vs speculation",
                    "target model and sampling distribution",
                    "accepted tokens/step and true latency",
                ],
                ["No retrieval vs retrieval", "active-context budget", "memory utility and contamination risk"],
                ["Model-only vs policy gate", "same tool scenarios", "safety contribution of deterministic layer"],
                ["Software vs FPGA kernel", "exact tensor workload", "energy and latency advantage"],
            ],
            [145, 174, 186],
        ),
        P("STATISTICS", "H2x"),
        P(
            "Pre-register primary metrics and thresholds. Use paired examples for model comparisons; report confidence intervals, not only means. For latency use quantiles and sample counts. For agent actions, classify both false execution and false refusal by risk class. Retain failure transcripts with secrets redacted. Never tune against a hidden final test set."
        ),
        P("FALSIFIERS", "H2x"),
        table(
            [
                ["Hypothesis", "Evidence that falsifies it", "Response"],
                [
                    "Ternary 7B-9B retains required quality",
                    "persistent task loss beyond agreed margin after native training",
                    "use higher precision / smaller scope",
                ],
                [
                    "Pocket bandwidth supports real-time decode",
                    "measured bytes/token exceeds sustainable system bandwidth",
                    "reduce size, increase reuse, alter memory",
                ],
                [
                    "Compressed context preserves utility",
                    "long-context retrieval / recall fails target",
                    "shorter hot cache + external memory",
                ],
                [
                    "FPGA maps efficiently",
                    "routing, timing or memory stalls erase energy benefit",
                    "redesign dataflow or stop hardware path",
                ],
                [
                    "Voice feels real-time",
                    "P95 first audio remains above gate",
                    "smaller model, speculative path, interaction redesign",
                ],
            ],
            [126, 229, 150],
        ),
    ]

    section(
        s, 10, "Risk register and program decisions", "The largest risks are coupled, so gates must be cross-functional"
    )
    s += [
        P("PRE-MITIGATION VIEW", "Kicker"),
        P("Quality, bandwidth and authorization dominate", "H1x"),
        RiskMatrix(),
        Spacer(1, 8),
        table(
            [
                ["Risk", "Early indicator", "Mitigation", "Owner artifact"],
                [
                    "Ternary quality gap",
                    "outlier-heavy layers; tool JSON regressions",
                    "native training, mixed-precision islands",
                    "quantization sensitivity map",
                ],
                [
                    "Weight bandwidth",
                    "decode tracks bytes, not compute",
                    "packing, stacking, smaller active model",
                    "roofline reconciliation",
                ],
                [
                    "KV growth",
                    "resident memory linear and too steep",
                    "GQA/latent design, hot/cold policy",
                    "bytes/token curve",
                ],
                [
                    "Thermal discomfort",
                    "surface trend crosses envelope",
                    "duty scheduling, enclosure, lower active W",
                    "thermal transient model",
                ],
                [
                    "Unsafe automation",
                    "proposal bypass / confirmation race",
                    "typed gate, capability scope, replay tests",
                    "risk-class scenario suite",
                ],
                [
                    "Frozen obsolescence",
                    "tool schemas or knowledge drift",
                    "update adapters and retrieval, version ABI",
                    "compatibility matrix",
                ],
            ],
            [98, 133, 138, 136],
        ),
        P("PROGRAM PRINCIPLES", "H2x"),
        P(
            "1. Freeze interfaces before implementations. 2. Measure system boundaries, not isolated kernels. 3. Keep immutable model identity separate from mutable memory and tools. 4. Prefer deterministic enforcement for authorization. 5. Make every product number traceable to either a source, an equation or a run artifact. 6. Treat negative results as stage success when they prevent premature silicon."
        ),
        P(
            "The strategically valuable output of the first year is not only a device demo. It is a co-design evidence base: an evaluated low-bit checkpoint, a stable package ABI, execution traces, a measured memory model, an action-safety architecture, and FPGA results that constrain an ASIC.",
            "Callout",
        ),
    ]

    section(s, 11, "Reference configuration", "A concrete starting point, deliberately labeled as provisional")
    s += [
        P("DESIGN-SPACE ANCHOR", "Kicker"),
        P("Prototype around a narrow, measurable configuration", "H1x"),
        table(
            [
                ["Subsystem", "Stage 1 reference", "Stage 2 hypothesis", "Product aspiration"],
                [
                    "Language core",
                    "1B-3B + selected 7B baseline",
                    "ternary representative layers",
                    "natively ternary 7B-9B",
                ],
                [
                    "Weights",
                    "4-bit baseline + ternary experiment",
                    "2-bit physical + block scales",
                    "2-4 GB full package",
                ],
                ["Attention", "GQA baseline", "tiled GQA then latent experiment", "trained compressed KV"],
                ["Context", "8K/32K test points", "32K trace target", "32K normal; 120K research"],
                ["Working memory", "host RAM instrumented", "board + host explicit", "8-16 GB LPDDR"],
                [
                    "Speech",
                    "streaming ASR / TTS baseline",
                    "selected encoder/decoder kernels",
                    "integrated low-latency voice",
                ],
                ["Vision", "on-demand frame", "encoder trace only", "event-driven"],
                ["Actions", "local typed simulator", "same controller", "Android / desktop companions"],
                ["Power", "wall-meter baseline", "rail + board telemetry", "8-15 W active target"],
            ],
            [95, 136, 137, 137],
        ),
        P("WHY NOT START AT 9B ON FPGA?", "H2x"),
        P(
            "A full 9B mapping combines model-quality uncertainty, packing, board memory, host links, attention, runtime and toolchain closure. A representative slice can test the unique thesis - ternary fixed-layout efficiency - without confusing it with integration work. Scale only when the measured bottleneck model predicts the next step."
        ),
        P("OPEN RESEARCH QUESTIONS", "H2x"),
        table(
            [
                ["Question", "Experiment"],
                [
                    "How sparse are trained ternary zeros by layer and token?",
                    "export histograms; compare static and dynamic skip utility",
                ],
                ["Which weights require protected precision?", "layer-wise and channel-wise sidecar ablation"],
                [
                    "Can a latent KV variant train within the quality budget?",
                    "matched-data architecture study; cache reconstruction analysis",
                ],
                [
                    "Does speculative decoding help at batch one?",
                    "sweep drafter size, acceptance and memory traffic [7]",
                ],
                [
                    "Can a single-voice decoder reduce startup latency?",
                    "distill fixed speaker; measure intelligibility and prosody",
                ],
                ["What should be hard-wired?", "compare configuration use across validated model variants"],
            ],
            [222, 283],
        ),
        P(
            "The target specification remains a research aspiration until both stages pass. The public project should publish failures and changed assumptions alongside successes.",
            "Callout",
        ),
    ]

    section(
        s, 12, "Conclusion", "The frozen-model idea is valuable because it creates constraints that can be measured"
    )
    s += [
        P("A DISCIPLINED PATH TO REAL-TIME", "Kicker"),
        P("Build the assistant first; earn the chip", "H1x"),
        P(
            "Pocket Pet AI is an ambitious but coherent co-design program. Freezing a model can stabilize weight placement, execution order, memory formats and personality identity. Ternary weights can materially reduce storage and replace many multiplies with simpler operations. Compressed attention, streaming speech and tool adapters can make a local companion more capable than a standalone chatbot."
        ),
        P(
            "None of those advantages eliminates physics or safety. Each generated token still moves information; context still consumes memory; latency spans the entire audio path; a pocket enclosure must reject heat; an agent that controls devices needs deterministic authorization. The whitepaper therefore recommends two explicit stages."
        ),
        table(
            [
                ["Stage", "Purpose", "Definition of done"],
                [
                    "Stage 1",
                    "Prove the local agent and create trustworthy traces",
                    "quality, latency, memory, energy and action gates pass on a reproducible software system",
                ],
                [
                    "Stage 2",
                    "Falsify or validate model-specific acceleration",
                    "bit-exact FPGA slices show measured system-level energy and latency value, then scale",
                ],
            ],
            [80, 160, 265],
        ),
        P(
            "The project should publish a living assumptions ledger and update every target with measured evidence. If the final product is possible, this process will reveal the architecture. If a premise fails, it will fail early enough to change course. That is the fastest credible route from a beautiful concept to real, personal, local intelligence.",
            "Quote",
        ),
        P(
            "Recommended immediate action: freeze the Stage 1 benchmark contract before choosing the final model. The benchmark is the instrument panel for every model, memory and hardware decision that follows.",
            "Callout",
        ),
    ]

    section(s, 13, "References and calculation notes", "Primary papers and platform documentation used in this draft")
    refs = [
        "[1] Ma, S. et al. (2024). <i>The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits.</i> arXiv:2402.17764. https://arxiv.org/abs/2402.17764",
        "[2] DeepSeek-AI et al. (2024). <i>DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model.</i> arXiv:2405.04434. https://arxiv.org/abs/2405.04434",
        "[3] Ainslie, J. et al. (2023). <i>GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints.</i> EMNLP; arXiv:2305.13245. https://arxiv.org/abs/2305.13245",
        "[4] Dao, T. et al. (2022). <i>FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.</i> NeurIPS; arXiv:2205.14135. https://arxiv.org/abs/2205.14135",
        "[5] Kwon, W. et al. (2023). <i>Efficient Memory Management for Large Language Model Serving with PagedAttention.</i> SOSP; arXiv:2309.06180. https://arxiv.org/abs/2309.06180",
        "[6] Lin, J. et al. (2023). <i>AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration.</i> MLSys; arXiv:2306.00978. https://arxiv.org/abs/2306.00978",
        "[7] Chen, C. et al. (2023). <i>Accelerating Large Language Model Decoding with Speculative Sampling.</i> arXiv:2302.01318. https://arxiv.org/abs/2302.01318",
        "[8] Android Open Source Project. <i>Hardware-backed Keystore.</i> https://source.android.com/docs/security/features/keystore",
        "[9] Android Developers. <i>AccessibilityService API reference.</i> https://developer.android.com/reference/android/accessibilityservice/AccessibilityService",
        "[10] Vaswani, A. et al. (2017). <i>Attention Is All You Need.</i> NeurIPS; arXiv:1706.03762. https://arxiv.org/abs/1706.03762",
    ]
    s += [P("REFERENCES", "Kicker"), P("Selected foundations", "H1x")]
    for r in refs:
        s.append(P(r, "Ref"))
    s += [
        Spacer(1, 8),
        P("CALCULATION NOTES", "H2x"),
        table(
            [
                ["Item", "Equation / assumption", "Result"],
                ["9B ideal ternary payload", "9e9 x log2(3) / 8 / 1e9", "1.783 GB decimal"],
                ["9B physical 2-bit payload", "9e9 x 2 / 8 / 1e9", "2.250 GB decimal"],
                ["GQA KV bytes/token", "32 layers x 2 x 8 heads x 128 dim x 2 B", "131,072 B = 128 KiB"],
                ["GQA KV at 32K", "131,072 x 32,768 / 2^30", "4.0 GiB"],
                ["GQA KV at 120K", "131,072 x 120,000 / 2^30", "14.65 GiB (rounded 15.0 in prose)"],
                ["Weight bandwidth at 20 tok/s", "2.25 GB x 20", "45 GB/s lower bound"],
                ["Example duty energy", "12 W x .2 h + 5 W x .1 h + .7 W x .7 h", "3.39 Wh per mixed hour"],
            ],
            [145, 255, 105],
        ),
        Spacer(1, 8),
        P(
            "All uncited product values are targets, hypotheses or derived examples. GB uses decimal units for package and bandwidth calculations; GiB uses binary units for KV capacity. Energy and battery examples exclude aging unless explicitly stated. No claim in this draft represents a fabricated prototype result.",
            "Callout",
        ),
        P(
            "Document generation is deterministic. Charts and diagrams are vector drawings generated from the same declared values as the prose. Update the script and regenerate the PDF to revise this paper.",
            "Smallx",
        ),
    ]
    return s


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    doc = WhitepaperDoc(str(OUT))
    doc.build(build_story())
    shutil.copy2(OUT, PUBLIC)
    print(OUT)
    print(PUBLIC)


if __name__ == "__main__":
    main()
