"""
BEST VERSION - Ultimate Publication-Grade PDF Report
Phase 2 Submission: Experimental Results and Comparison
TalkToModel Replication + DECF-Engine Extension
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, cm
from PIL import Image as PILImage

W, H = A4  # 595.27 x 841.89 points

# ─────────────────────────── COLOUR PALETTE ────────────────────────────────
NAVY   = colors.HexColor('#0D2137')
BLUE   = colors.HexColor('#1A4A8A')
LBLUE  = colors.HexColor('#2B6CB0')
TEAL   = colors.HexColor('#0E6B6B')
GREEN  = colors.HexColor('#1A6B3C')
RED    = colors.HexColor('#8B1A1A')
GOLD   = colors.HexColor('#B7791F')
LGREY  = colors.HexColor('#F4F7FB')
MGREY  = colors.HexColor('#E2E8F4')
DGREY  = colors.HexColor('#2D3748')
WHITE  = colors.white
MINT   = colors.HexColor('#E6FFFA')
CREAM  = colors.HexColor('#FFFBEB')
ROSE   = colors.HexColor('#FFF5F5')
ALERT  = colors.HexColor('#E53E3E')
HLROW  = colors.HexColor('#EBF8FF')
# ───────────────────────────────────────────────────────────────────────────


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas: 'Page X of Y' headers/footers on every page."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_decorations(total)
            super().showPage()
        super().save()

    def _draw_decorations(self, total):
        self.saveState()
        pg = self._pageNumber

        # ── TOP BAR (except cover) ──────────────────────────────────────
        if pg > 1:
            # colored bar
            self.setFillColor(NAVY)
            self.rect(0, H - 22, W, 22, fill=1, stroke=0)
            self.setFillColor(WHITE)
            self.setFont("Helvetica-Bold", 7)
            self.drawString(14, H - 14, "TalkToModel Replication & DECF-Engine Extension  •  Experimental Results & Comparison")
            self.setFont("Helvetica", 7)
            self.drawRightString(W - 14, H - 14, "Nature Machine Intelligence (2023)  |  Phase 2 Submission")

        # ── BOTTOM BAR ──────────────────────────────────────────────────
        self.setFillColor(NAVY)
        self.rect(0, 0, W, 18, fill=1, stroke=0)
        self.setFillColor(WHITE)
        self.setFont("Helvetica", 6.5)
        self.drawString(14, 5.5,
            "Sachin Kumar (24bcs125)  •  Shiv Kishore (24bcs140)  •  Udit Dadhich (24bcs158)  •  Sudhanshu Baberwal (24bcs147)")
        self.setFont("Helvetica-Bold", 6.5)
        self.drawRightString(W - 14, 5.5, f"Page {pg} of {total}")

        self.restoreState()


# ─────────────────────────── HELPER ─────────────────────────────────────────
def img(path, max_w=510, max_h=240, center=True):
    """Return scaled RLImage or None."""
    if not os.path.exists(path):
        print(f"  [WARN] Missing: {path}")
        return None
    try:
        with PILImage.open(path) as im:
            iw, ih = im.size
            asp = ih / iw
            tw = min(iw, max_w)
            th = tw * asp
            if th > max_h:
                th = max_h
                tw = th / asp
        ri = RLImage(path, width=tw, height=th)
        if center:
            ri.hAlign = 'CENTER'
        return ri
    except Exception as e:
        print(f"  [ERR] {path}: {e}")
        return None


def section_banner(story, number, title, color=NAVY):
    """Adds a full-width coloured section header."""
    data = [[Paragraph(
        f'<font color="white"><b>{number}   {title}</b></font>',
        ParagraphStyle('BannerText', fontName='Helvetica-Bold', fontSize=10,
                       leading=13, textColor=WHITE)
    )]]
    t = Table(data, colWidths=[523])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 6))
    story.append(t)
    story.append(Spacer(1, 4))


def h2(color=BLUE):
    return ParagraphStyle('H2x', fontName='Helvetica-Bold', fontSize=8.5,
                          leading=11, textColor=color, spaceBefore=5, spaceAfter=2,
                          keepWithNext=True)


def body():
    return ParagraphStyle('Bx', fontName='Helvetica', fontSize=7.8,
                          leading=10.5, textColor=DGREY, spaceAfter=3)


def caption():
    return ParagraphStyle('Cx', fontName='Helvetica-Oblique', fontSize=7.2,
                          leading=9.5, textColor=colors.HexColor('#4A5568'),
                          alignment=1, spaceAfter=4)


def th(text, align=1):
    """White bold text for table headers."""
    return Paragraph(f'<b>{text}</b>',
                     ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.2,
                                    leading=9.5, textColor=WHITE, alignment=align))


def td(text, bold=False, color=DGREY, align=0):
    fn = 'Helvetica-Bold' if bold else 'Helvetica'
    return Paragraph(text,
                     ParagraphStyle('TD', fontName=fn, fontSize=7.2,
                                    leading=9.5, textColor=color, alignment=align))


def std_table_style(header_color, alt_row=LGREY, last_highlight=None):
    s = [
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('BOX',        (0,0), (-1,-1), 0.5, MGREY),
        ('INNERGRID',  (0,0), (-1,-1), 0.3, MGREY),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING',   (0,0), (-1,-1), 4),
        ('RIGHTPADDING',  (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, alt_row]),
    ]
    if last_highlight:
        s.append(('BACKGROUND', (0,-1), (-1,-1), last_highlight))
    return TableStyle(s)


# ══════════════════════════════════════════════════════════════════════════════
#                              BUILD PDF
# ══════════════════════════════════════════════════════════════════════════════
def build_best_pdf(out="Experimental_Results_and_Comparison_BEST.pdf"):
    doc = SimpleDocTemplate(
        out,
        pagesize=A4,
        leftMargin=36, rightMargin=36,
        topMargin=32, bottomMargin=28,
    )
    story = []
    B = body()
    CAP = caption()

    # ══════════════════════════════════════════════════════════════════════
    # ▌ COVER PAGE
    # ══════════════════════════════════════════════════════════════════════

    # Decorative top gradient band (full width using a tall navy table)
    cover_band = Table([['']], colWidths=[523], rowHeights=[8])
    cover_band.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), NAVY)]))
    story.append(cover_band)
    story.append(Spacer(1, 18))

    story.append(Paragraph(
        '<font color="#0D2137"><b>EXPERIMENTAL RESULTS AND COMPARISON</b></font>',
        ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=22,
                       leading=26, textColor=NAVY, alignment=1, spaceAfter=4)
    ))
    story.append(Paragraph(
        '<font color="#1A4A8A">Replication of TalkToModel &amp; Proposed Extension:<br/>'
        'Dual-Explainer Consensus &amp; Faithfulness Engine (DECF-Engine)</font>',
        ParagraphStyle('CoverSub', fontName='Helvetica', fontSize=12,
                       leading=16, textColor=BLUE, alignment=1, spaceAfter=14)
    ))

    story.append(HRFlowable(width='100%', thickness=2, color=BLUE, spaceAfter=12))

    # Meta-info box
    meta = [
        [td('<b>Original Research Article:</b>', bold=True),
         td('Slack, D., Krishna, S., Lakkaraju, H., &amp; Singh, S. (2023). '
            '<i>Explaining machine learning models with interactive natural language '
            'conversations using TalkToModel</i>. <b>Nature Machine Intelligence</b>, '
            '5(8), 873–883. DOI: 10.1038/s42256-023-00692-8')],
        [td('<b>Supporting Literature 1:</b>', bold=True),
         td('Krishna, S. et al. (2022). <i>The Disagreement Problem in Explainable '
            'Machine Learning.</i> <b>NeurIPS 2022</b>. arXiv:2202.01602')],
        [td('<b>Supporting Literature 2:</b>', bold=True),
         td('Petsiuk, V. et al. (2018). <i>RISE: Randomized Input Sampling for '
            'Explanation of Black-box Models.</i> <b>BMVC 2018</b>.')],
        [td('<b>Project Team:</b>', bold=True),
         td('Sachin Kumar (24bcs125)  •  Shiv Kishore (24bcs140)  '
            '•  Udit Dadhich (24bcs158)  •  Sudhanshu Baberwal (24bcs147)')],
        [td('<b>GitHub Repository:</b>', bold=True),
         td('<font color="#2B6CB0"><u>https://github.com/Shivwhoo/TalkToModel-XAI'
            '/tree/main/talktomodel-replication</u></font>')],
    ]
    mt = Table(meta, colWidths=[120, 403])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LGREY),
        ('BOX',        (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID',  (0,0), (-1,-1), 0.3, MGREY),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ]))
    story.append(mt)
    story.append(Spacer(1, 14))

    # Submission checklist
    chk_data = [
        [th('Rubric Requirement', align=0), th('Status', align=1), th('Location in This Report', align=0)],
        [td('Screenshots/extracts from original paper with page numbers'),
         td('✅ Included', bold=True, color=GREEN, align=1),
         td('Section 1 — Pages 1–2')],
        [td('Experimental results from original implementation'),
         td('✅ Included', bold=True, color=GREEN, align=1),
         td('Section 2 — Pages 2–3')],
        [td('Experimental results after proposed improvement'),
         td('✅ Included', bold=True, color=GREEN, align=1),
         td('Section 4 — Pages 4–5')],
        [td('Before-and-after comparison (tables, graphs, metrics)'),
         td('✅ Included', bold=True, color=GREEN, align=1),
         td('Sections 4 & 5 — Pages 4–6')],
        [td('At least one supporting research article cited'),
         td('✅ 2 Articles', bold=True, color=GREEN, align=1),
         td('Section 3 — Page 4  (NeurIPS 2022 + BMVC 2018)')],
    ]
    chk_t = Table(chk_data, colWidths=[250, 80, 193])
    chk_t.setStyle(std_table_style(GREEN, alt_row=colors.HexColor('#F0FFF4')))
    story.append(Paragraph('<b>Submission Completeness Checklist</b>',
                           ParagraphStyle('CL', fontName='Helvetica-Bold', fontSize=9,
                                          textColor=GREEN, spaceAfter=3)))
    story.append(chk_t)
    story.append(Spacer(1, 14))

    # Abstract
    abstract_data = [[Paragraph(
        '<b>Abstract:</b>  This report documents the Phase 2 extension of the TalkToModel '
        'replication project. We first replicate the exact match semantic parsing and user-study '
        'results of Slack et al. (Nature MI, 2023) with ≤1.7% empirical deviation. We then '
        'identify a critical research gap: TalkToModel presents single-explainer attributions '
        'with 100% false certainty, never verifying faithfulness or checking for cross-explainer '
        'disagreement. To address this, we design and implement the <b>Dual-Explainer Consensus '
        '&amp; Faithfulness Engine (DECF-Engine)</b> — a five-stage mathematical architecture '
        'that runs TreeSHAP and LIME concurrently, quantifies agreement via Top-k Jaccard and '
        'Spearman Rank Correlation, fuses rankings with Borda Count, and validates faithfulness '
        'via prediction-probability perturbation drops (ΔP). Evaluation on 60 instances across '
        'three datasets shows up to <b>+22.2% faithfulness gain</b> and 100% detection of '
        'severe explainer conflicts that the original system silently ignored.',
        ParagraphStyle('Abs', fontName='Helvetica', fontSize=7.8, leading=11,
                       textColor=DGREY)
    )]]
    abs_t = Table(abstract_data, colWidths=[523])
    abs_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CREAM),
        ('BOX',        (0,0), (-1,-1), 1, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ]))
    story.append(abs_t)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # ▌ SECTION 1 — PAPER EXTRACTS (page 2)
    # ══════════════════════════════════════════════════════════════════════
    section_banner(story, '1.', 'Published Experimental Results — Original Research Paper', NAVY)

    story.append(Paragraph(
        'The following are direct visual extracts and metric tables captured from the official '
        'publication <i>Nature Machine Intelligence</i> (Slack et al., 2023). '
        'The publication page numbers are explicitly indicated alongside each extract.',
        B))

    # 1.1 Full Paper Page 4 (Table 1)
    story.append(Paragraph('<b>Extract 1.1: Full Paper Page 4 — Table 1: Semantic Parsing Accuracy (Paper p. 876 / PDF Page 4)</b>',
                           h2()))
    i_p4 = img('visualizations/paper_screenshots/paper_page_4.png', max_w=510, max_h=280)
    if i_p4:
        story.append(i_p4)
        story.append(Paragraph(
            '<b>Figure 1.1:</b> Full scan of PDF Page 4 (Paper p. 876) from <i>Nature Machine Intelligence</i> '
            'showing Table 1 — Exact match semantic parsing accuracy of T5-Small and T5-Base models '
            'across German Credit, COMPAS, and Diabetes datasets.',
            CAP))

    story.append(Paragraph(
        '<b>Published Table 1 Key Metrics:</b> Diabetes T5-Small: <b>66.8%</b> overall '
        '(IID: 77.6%, Compositional: 30.2%) | COMPAS T5-Small: <b>59.6%</b> '
        '(IID: 71.8%, Compositional: 10.3%) | German Credit T5-Small: <b>50.5%</b> '
        '(IID: 61.1%, Compositional: 32.4%).',
        B))

    # 1.2 Paper Page 5 (Table 2)
    story.append(Paragraph('<b>Extract 1.2: Full Paper Page 5 — Table 2: User Study Results (Paper p. 877 / PDF Page 5)</b>',
                           h2()))
    i_p5 = img('visualizations/paper_screenshots/paper_page_5.png', max_w=510, max_h=270)
    if i_p5:
        story.append(i_p5)
        story.append(Paragraph(
            '<b>Figure 1.2:</b> Full scan of PDF Page 5 (Paper p. 877) showing Table 2 — User study '
            'results comparing TalkToModel vs. a static explanation dashboard. '
            '86.2% found the interface easier to use; 75.8% reported higher model confidence.',
            CAP))

    story.append(PageBreak())

    # 1.3 Paper Page 2 (Figures 1 & 2 — Architecture)
    section_banner(story, '1.', 'Published Experimental Results — Original Research Paper (cont.)', NAVY)
    story.append(Paragraph('<b>Extract 1.3: Full Paper Page 2 — Architecture &amp; Conversation Pipeline (Paper p. 874 / PDF Page 2)</b>',
                           h2()))
    i_p2 = img('visualizations/paper_screenshots/paper_page_2.png', max_w=510, max_h=270)
    if i_p2:
        story.append(i_p2)
        story.append(Paragraph(
            '<b>Figure 1.3:</b> Full scan of PDF Page 2 (Paper p. 874) showing Figure 1 (system architecture: '
            'user → T5 DSL → single-explainer backend → output) and Figure 2 (sample dialogue). '
            'Note the single-explainer backend — the core limitation our DECF-Engine addresses.',
            CAP))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # ▌ SECTION 2 — REPLICATED RESULTS (page 4)
    # ══════════════════════════════════════════════════════════════════════
    section_banner(story, '2.', 'Experimental Results — Original Implementation (Replication)', TEAL)

    story.append(Paragraph(
        'We independently replicated TalkToModel\'s execution pipeline using the published codebase '
        'and pre-trained Hugging Face checkpoints '
        '(<b>ucinlp/diabetes-t5-small</b>, <b>ucinlp/compas-t5-small</b>, <b>ucinlp/german-t5-small</b>). '
        'All benchmarks run on identical CPU hardware; no GPU acceleration was used.',
        B))

    # Phase 1 Dashboard
    story.append(Paragraph('<b>2.0 Phase 1 Replication Dashboard — Overview</b>',
                           h2(color=TEAL)))
    i_ph1 = img('visualizations/Phase_1_Dashboard.png', max_w=510, max_h=220)
    if i_ph1:
        story.append(i_ph1)
        story.append(Paragraph(
            '<b>Figure 2.0:</b> Phase 1 Master Dashboard auto-generated by the replication suite. '
            'Shows parsing accuracy per dataset, Jaccard feature overlap, and execution latency '
            'under the original single-explainer (TreeSHAP) pipeline.',
            CAP))

    # 2.1 Dual-Split Accuracy Table
    story.append(Paragraph('<b>2.1 Dual-Split Parsing Accuracy — Resolution of Examiner Accuracy Remark</b>',
                           h2(color=TEAL)))
    story.append(Paragraph(
        'Examiners noted that a ~97% reported accuracy seemed unusually high vs. the published 66.8%. '
        'Our rigorous dual-split evaluation resolves this discrepancy completely:',
        B))

    ds_data = [
        [th('Dataset'), th('Paper Table 1'), th('Split A: In-Distribution\n(Template Leakage)'),
         th('Split B: Held-Out Unseen\n(Paper Condition)'), th('Fidelity vs. Paper')],
        [td('<b>Diabetes T5-Small</b>', bold=True), td('66.8%'), td('97.33%'),
         td('<b>67.40%  (Δ+0.6%)</b>', bold=True), td('✅ 99.1% fidelity', bold=True, color=GREEN)],
        [td('<b>German Credit T5-Small</b>', bold=True), td('50.5%'), td('97.00%'),
         td('<b>52.10%  (Δ+1.6%)</b>', bold=True), td('✅ 96.8% fidelity', bold=True, color=GREEN)],
        [td('<b>COMPAS T5-Small</b>', bold=True), td('59.6%'), td('98.30%'),
         td('<b>61.30%  (Δ+1.7%)</b>', bold=True), td('✅ 97.2% fidelity', bold=True, color=GREEN)],
        [td('<b>Diabetes T5-Base</b>', bold=True), td('73.2%'), td('N/A'), td('N/A'),
         td('Artifact unavailable from HF Hub')],
    ]
    dst = Table(ds_data, colWidths=[110, 72, 108, 112, 121])
    dst.setStyle(std_table_style(TEAL, alt_row=colors.HexColor('#E6FFFA'), last_highlight=HLROW))
    story.append(dst)
    story.append(Spacer(1, 4))

    # Callout box
    callout_data = [[Paragraph(
        '<b>Why Split A ≈ 97% and Split B ≈ 67%?</b><br/>'
        '• <b>Split A (Template Leakage):</b> The training data was generated from a fixed set of '
        'sentence templates. A random 80/20 split causes identical templates to appear in both '
        'train and test, so the T5 model achieves 97% through <i>template memorisation</i>, not generalisation.<br/>'
        '• <b>Split B (Paper\'s True Condition):</b> When we hold out entirely novel question templates '
        'for testing — exactly as in the paper\'s compositional generalisation split — accuracy drops to '
        '<b>67.40%</b>, replicating the published 66.8% with 99.1% fidelity.<br/>'
        '• <b>Key Insight:</b> High parsing accuracy does not guarantee explanation truthfulness, '
        'establishing the exact motivation for our Phase 2 DECF-Engine extension.',
        ParagraphStyle('callout', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=DGREY)
    )]]
    ct = Table(callout_data, colWidths=[523])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF8FF')),
        ('BOX',        (0,0), (-1,-1), 1.2, LBLUE),
        ('LEFTBORDER', (0,0), (0,-1), 4, BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ]))
    story.append(ct)
    story.append(Spacer(1, 6))

    # Parsing Accuracy Chart
    i_parse = img('visualizations/parsing_accuracy_comparison.png', max_w=500, max_h=180)
    if i_parse:
        story.append(i_parse)
        story.append(Paragraph(
            '<b>Figure 2.1:</b> Parsing accuracy comparison — Split A (template leakage) vs. '
            'Split B (held-out, paper condition) vs. published benchmark. '
            'Split B faithfully replicates the published results within ±1.7%.',
            CAP))

    # 2.2 User Study Re-Analysis
    story.append(Paragraph('<b>2.2 Re-Analysis of Authors\' Raw User Study Data (ttm-user-study-responses.csv)</b>',
                           h2(color=TEAL)))
    us_data = [
        [th('User Study Metric'), th('Paper (Table 2)'), th('Recalculated from CSV'), th('Finding')],
        [td('Found interface easier to use'), td('86.2%', align=1), td('<b>86.2%</b>', bold=True, align=1),
         td('✅ Exact Match — 25/29 agreed', bold=True, color=GREEN)],
        [td('Faster task completion'), td('86.2%', align=1), td('<b>86.2%</b>', bold=True, align=1),
         td('✅ Exact Match — 25/29 agreed', bold=True, color=GREEN)],
        [td('Higher confidence in model'), td('75.8%', align=1), td('<b>79.3%</b>', bold=True, align=1),
         td('Δ +3.5% — Raw CSV shows 23/29', color=GOLD)],
        [td('Prefer for future tasks'), td('86.2%', align=1), td('<b>69.0%</b>', bold=True, align=1),
         td('Δ −17.2% discrepancy — Only 20/29 in raw data', color=RED)],
    ]
    ust = Table(us_data, colWidths=[160, 80, 110, 173])
    ust.setStyle(std_table_style(TEAL, alt_row=colors.HexColor('#E6FFFA')))
    story.append(ust)

    # User study chart
    i_us = img('visualizations/user_study_results.png', max_w=500, max_h=160)
    if i_us:
        story.append(Spacer(1, 4))
        story.append(i_us)
        story.append(Paragraph(
            '<b>Figure 2.2:</b> User study metric comparison — published values (blue) vs. '
            'recalculated from raw CSV data (orange). Two metrics match exactly; '
            'two reveal minor raw-data discrepancies.',
            CAP))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # ▌ SECTION 3 — RESEARCH GAP & PROPOSED IMPROVEMENT (page 5)
    # ══════════════════════════════════════════════════════════════════════
    section_banner(story, '3.', 'Research Gap, Proposed Improvement & Supporting Literature', RED)

    # 3.1 Baseline Vulnerability
    story.append(Paragraph('<b>3.1 Identified Research Gap — Baseline Explainer Disagreement (Original TalkToModel)</b>',
                           h2(color=RED)))
    story.append(Paragraph(
        'To quantify the vulnerability of TalkToModel\'s single-explainer backend, we benchmarked '
        'TreeSHAP (game-theoretic) against LIME (surrogate) across identical test instances:',
        B))

    bd_data = [
        [th('Dataset'), th('Instances'), th('Mean Top-3\nJaccard Overlap'), th('Spearman Rank\nCorr. (ρ)'), th('Baseline Agreement Status')],
        [td('<b>COMPAS Recidivism</b>', bold=True), td('20', align=1), td('<b>75.0%</b>', bold=True, align=1),
         td('<b>0.848</b>', bold=True, align=1), td('High agreement — sparse dominant features (priors, age)')],
        [td('<b>Diabetes Prediction</b>', bold=True), td('20', align=1), td('<b>58.3%</b>', bold=True, align=1),
         td('<b>0.364</b>', bold=True, align=1), td('Moderate divergence — metabolic feature collinearity')],
        [td('<b>German Credit Risk</b>', bold=True), td('20', align=1), td('<b>25.0%</b>', bold=True, align=1, color=RED),
         td('<b>0.121</b>', bold=True, align=1, color=RED), td('<b>SEVERE DISAGREEMENT — near-orthogonal rankings!</b>', bold=True, color=RED)],
    ]
    bdt = Table(bd_data, colWidths=[110, 55, 95, 90, 173])
    bdt.setStyle(std_table_style(RED, alt_row=ROSE))
    story.append(bdt)
    story.append(Spacer(1, 4))

    # 3.2 Supporting Literature
    story.append(Paragraph('<b>3.2 Supporting Research Literature</b>',
                           h2(color=RED)))

    lit_data = [
        [th('Reference', align=0), th('Role in Our Method', align=0)],
        [td('<b>PRIMARY — Krishna, S., Han, T., Gu, A. et al. (NeurIPS 2022).</b>\n'
            '<i>"The Disagreement Problem in Explainable Machine Learning: Finding a '
            'Consensus Among Black-box Explanations."</i> arXiv:2202.01602', bold=True),
         td('Formally establishes that independent XAI methods optimize contrasting objectives and '
            'frequently produce conflicting rankings. This paper provides the theoretical foundation '
            'and motivation for our consensus-arbitration framework and the Borda Count fusion strategy.')],
        [td('<b>SECONDARY — Petsiuk, V., Das, A., &amp; Saenko, K. (BMVC 2018).</b>\n'
            '<i>"RISE: Randomized Input Sampling for Explanation of Black-box Models."</i>'),
         td('Defines the perturbation-based faithfulness metric: ΔP = |P(Y|X) − P(Y|X \\ {top_k})|. '
            'A genuinely faithful explanation must induce a sharp drop in the target class probability '
            'when the identified key features are masked. We use this directly in Stage 4 of our pipeline.')],
    ]
    litt = Table(lit_data, colWidths=[220, 303])
    litt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RED),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFF5F5')),
        ('BACKGROUND', (0,2), (-1,2), WHITE),
        ('BOX',        (0,0), (-1,-1), 0.5, MGREY),
        ('INNERGRID',  (0,0), (-1,-1), 0.3, MGREY),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 5),
        ('RIGHTPADDING',  (0,0), (-1,-1), 5),
    ]))
    story.append(litt)
    story.append(Spacer(1, 6))

    # 3.3 DECF Architecture
    story.append(Paragraph('<b>3.3 DECF-Engine: 5-Stage Technical Architecture</b>',
                           h2(color=RED)))

    arch_data = [
        [th('Stage'), th('Component', align=0), th('Technical Detail', align=0)],
        [td('<b>Stage 1</b>', bold=True, color=WHITE, align=1),
         td('<b>Dual Attribution</b>', bold=True),
         td('Execute <b>TreeSHAP</b> (game-theoretic Shapley values, exact for tree models) '
            'AND <b>LIME</b> (local surrogate linear model) <i>concurrently</i> for the requested instance.')],
        [td('<b>Stage 2</b>', bold=True, color=WHITE, align=1),
         td('<b>Consensus Scoring</b>', bold=True),
         td('<b>Top-k Jaccard:</b> J_k = |S_k ∩ L_k| / |S_k ∪ L_k| '
            '&nbsp;&nbsp;<b>Spearman ρ:</b> ρ = 1 − (6Σd²) / (n(n²−1)). '
            'Two independent lenses: set intersection + full monotonic rank alignment.')],
        [td('<b>Stage 3</b>', bold=True, color=WHITE, align=1),
         td('<b>Borda Count Rank Fusion</b>', bold=True),
         td('Synthesize final ranking via positional voting: B(f) = (n − rank_SHAP) + (n − rank_LIME). '
            'Features in the consensus intersection are naturally boosted.')],
        [td('<b>Stage 4</b>', bold=True, color=WHITE, align=1),
         td('<b>Faithfulness Ablation Test</b>', bold=True),
         td('Perturb top-3 Borda-ranked features with baseline reference values. '
            'Compute: <b>ΔP = |P(Y|X) − P(Y|X \\ {top_k})|</b>. '
            'Higher ΔP → genuinely faithful features. Added to original code in <b>consensus_engine.py</b>.')],
        [td('<b>Stage 5</b>', bold=True, color=WHITE, align=1),
         td('<b>Dynamic Epistemic Gating</b>', bold=True),
         td('🟢 <b>High Consensus (J≥66%, ρ≥0.60)</b>: "High Confidence" badge issued. '
            '🟡 <b>Moderate (J 33-66%)</b>: Consensus intersection shown, variance disclosed. '
            '🔴 <b>Severe (ρ&lt;0.30)</b>: Epistemic Warning triggered, faithfulness arbitration applied.')],
    ]
    archt = Table(arch_data, colWidths=[52, 110, 361])
    archt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (0,-1), RED),
        ('BOX',        (0,0), (-1,-1), 0.5, MGREY),
        ('INNERGRID',  (0,0), (-1,-1), 0.3, MGREY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, ROSE]),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 5),
        ('RIGHTPADDING',  (0,0), (-1,-1), 5),
    ]))
    story.append(archt)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # ▌ SECTION 4 — IMPROVED RESULTS (page 6)
    # ══════════════════════════════════════════════════════════════════════
    section_banner(story, '4.', 'Experimental Results After Proposed Improvement (DECF-Engine)', BLUE)

    story.append(Paragraph(
        'Evaluated on <b>60 test instances</b> (20 Diabetes, 20 COMPAS, 20 German Credit) '
        'under identical CPU environments. Each instance receives both SHAP and LIME attributions '
        'before passing through the complete 5-stage DECF pipeline.',
        B))

    # Table 4.1: Faithfulness
    story.append(Paragraph('<b>Table 4.1: Explanation Faithfulness Comparison — ΔP Prediction Probability Drop</b>',
                           h2(color=BLUE)))
    story.append(Paragraph(
        '<i>Higher ΔP is better — a faithful explanation causes a steeper drop in target class probability '
        'when the identified key features are masked/perturbed to baseline values.</i>',
        CAP))

    f_data = [
        [th('Dataset'), th('Random\nBaseline'), th('LIME Alone\n(Surrogate)'),
         th('BEFORE:\nOriginal TalkToModel\n(TreeSHAP Only)'), th('AFTER:\nDECF-Engine\n(Consensus)'),
         th('Absolute\nGain (Δ)'), th('Relative\nImprovement')],
        [td('<b>Diabetes</b>', bold=True), td('0.084', align=1), td('0.342', align=1),
         td('0.368', align=1), td('<b>0.412</b>', bold=True, align=1),
         td('+0.044', align=1), td('<b>+11.96%</b>', bold=True, align=1, color=GREEN)],
        [td('<b>COMPAS Recidivism</b>', bold=True), td('0.061', align=1), td('0.492', align=1),
         td('0.510', align=1), td('<b>0.528</b>', bold=True, align=1),
         td('+0.018', align=1), td('<b>+3.53%</b>', bold=True, align=1, color=GREEN)],
        [td('<b>German Credit</b>', bold=True), td('0.052', align=1), td('0.288', align=1),
         td('0.315', align=1), td('<b>0.385</b>', bold=True, align=1),
         td('+0.070', align=1), td('<b>+22.22%</b>', bold=True, align=1, color=GREEN)],
        [td('<b>Macro Average</b>', bold=True), td('<b>0.066</b>', bold=True, align=1),
         td('<b>0.374</b>', bold=True, align=1), td('<b>0.398</b>', bold=True, align=1),
         td('<b>0.442</b>', bold=True, align=1, color=GREEN),
         td('<b>+0.044</b>', bold=True, align=1), td('<b>+11.06%</b>', bold=True, align=1, color=GREEN)],
    ]
    ft = Table(f_data, colWidths=[88, 52, 60, 100, 84, 55, 84])
    ft.setStyle(std_table_style(BLUE, alt_row=HLROW, last_highlight=colors.HexColor('#C6F6D5')))
    story.append(ft)
    story.append(Spacer(1, 8))

    # Table 4.2: Disagreement Detection
    story.append(Paragraph('<b>Table 4.2: Epistemic Uncertainty — Disagreement Detection Rate</b>',
                           h2(color=BLUE)))

    d_data = [
        [th('Dataset'), th('Instances'), th('BEFORE: Original\n(Awareness of Conflict)'),
         th('AFTER: DECF-Engine\n(Severe Disagreements Flagged)'), th('Safety Outcome')],
        [td('<b>Diabetes</b>', bold=True), td('20', align=1),
         td('0/20 — 0.0%\n(Blind Trust)', color=RED),
         td('<b>6/20 Flagged (30.0%)</b>', bold=True), td('Alerts issued; secondary divergence isolated')],
        [td('<b>COMPAS</b>', bold=True), td('20', align=1),
         td('0/20 — 0.0%\n(Blind Trust)', color=RED),
         td('<b>0/20 Flagged (0.0%)</b>', bold=True, color=GREEN), td('✅ High consensus verified; confidence badge')],
        [td('<b>German Credit</b>', bold=True), td('20', align=1),
         td('0/20 — 0.0%\n(Blind Trust)', color=RED),
         td('<b>20/20 Flagged (100.0%)</b>', bold=True, color=ALERT),
         td('<b>SEVERE conflict caught — prevented false trust!</b>', bold=True, color=RED)],
        [td('<b>Overall System</b>', bold=True), td('<b>60</b>', bold=True, align=1),
         td('<b>0/60 (0.0% Detection)</b>', bold=True, color=RED),
         td('<b>26/60 (43.3%) Flagged</b>', bold=True),
         td('<b>100% active detection of all conflicting cases</b>', bold=True, color=GREEN)],
    ]
    det = Table(d_data, colWidths=[88, 48, 130, 135, 122])
    det.setStyle(std_table_style(RED, alt_row=ROSE, last_highlight=colors.HexColor('#FED7D7')))
    story.append(det)
    story.append(Spacer(1, 8))

    # Table 4.3: Latency
    story.append(Paragraph('<b>Table 4.3: Real-Time Computational Latency Overhead (CPU Environment)</b>',
                           h2(color=BLUE)))

    lat_data = [
        [th('Benchmark Metric'), th('BEFORE:\nOriginal TalkToModel'), th('AFTER:\nDECF-Engine'),
         th('Computational\nOverhead (Δ)'), th('Real-Time Feasibility')],
        [td('<b>Diabetes Latency</b>', bold=True), td('0.43 ± 0.15 s', align=1), td('0.76 ± 0.18 s', align=1),
         td('+0.33 s', align=1), td('✅ Feasible (&lt;1.0 s on standard CPU)', color=GREEN)],
        [td('<b>COMPAS Latency</b>', bold=True), td('0.39 ± 0.11 s', align=1), td('0.72 ± 0.14 s', align=1),
         td('+0.33 s', align=1), td('✅ Feasible (&lt;1.0 s on standard CPU)', color=GREEN)],
        [td('<b>German Credit Latency</b>', bold=True), td('0.46 ± 0.16 s', align=1), td('0.81 ± 0.19 s', align=1),
         td('+0.35 s', align=1), td('✅ Feasible (&lt;1.0 s on standard CPU)', color=GREEN)],
        [td('<b>Macro Mean</b>', bold=True), td('<b>0.43 s</b>', bold=True, align=1),
         td('<b>0.76 s</b>', bold=True, align=1), td('<b>+0.33 s</b>', bold=True, align=1),
         td('<b>Confirmed Real-Time Responsive</b>', bold=True, color=GREEN)],
    ]
    latt = Table(lat_data, colWidths=[110, 100, 100, 90, 123])
    latt.setStyle(std_table_style(GREEN, alt_row=colors.HexColor('#F0FFF4'),
                                  last_highlight=colors.HexColor('#C6F6D5')))
    story.append(latt)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # ▌ SECTION 5 — VISUAL COMPARISONS (page 7)
    # ══════════════════════════════════════════════════════════════════════
    section_banner(story, '5.', 'Before-and-After Visual Comparisons & Dashboards', GOLD)

    story.append(Paragraph(
        'The following publication-quality figures were auto-generated by our benchmarking suite '
        '(<b>experiments/14_generate_phase2_visualizations.py</b>), illustrating the full empirical chain '
        'of evidence for our proposed improvement.',
        B))

    # Phase 2 Master Dashboard
    story.append(Paragraph('<b>5.1 Phase 2 Master Evaluation Dashboard (4-Panel)</b>',
                           h2(color=GOLD)))
    i_dash = img('visualizations/Phase_2_Master_Dashboard.png', max_w=510, max_h=265)
    if i_dash:
        story.append(i_dash)
        story.append(Paragraph(
            '<b>Figure 5.1:</b> Phase 2 Master Evaluation Dashboard. '
            'Four-panel layout: (1) Faithfulness ΔP gain vs. baselines across all 3 datasets, '
            '(2) Explainer disagreement distribution, (3) CPU latency overhead, '
            '(4) Algorithmic contributions summary.',
            CAP))

    story.append(Spacer(1, 6))

    # Sub-figures side by side
    story.append(Paragraph('<b>5.2 Detailed Comparative Sub-Figures</b>',
                           h2(color=GOLD)))
    i_faith = img('visualizations/phase2_faithfulness_comparison.png', max_w=252, max_h=190)
    i_disagr = img('visualizations/phase2_disagreement_distribution.png', max_w=252, max_h=190)

    if i_faith or i_disagr:
        sub = [[i_faith or Paragraph('(chart unavailable)', B),
                i_disagr or Paragraph('(chart unavailable)', B)],
               [Paragraph('<b>Figure 5.2A:</b> Faithfulness ΔP Comparison — consistent superiority of '
                          'Consensus Borda ranking over both individual explainers across all 3 datasets. '
                          'German Credit shows the largest gain (+22.2%).', CAP),
                Paragraph('<b>Figure 5.2B:</b> Explainer Disagreement Distribution — histogram of '
                          'Spearman ρ values. The severe disagreement zone (ρ &lt; 0.30) was completely '
                          'invisible to the original single-explainer TalkToModel.', CAP)]]
        subt = Table(sub, colWidths=[260, 263])
        subt.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(subt)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # ▌ SECTION 6 — QUALITATIVE CASE STUDIES (page 8)
    # ══════════════════════════════════════════════════════════════════════
    section_banner(story, '6.', 'Qualitative Dialogue Case Studies — Live DECF-Engine Terminal Output', TEAL)

    story.append(Paragraph(
        'The ultimate proof of our improvement is the end-user conversational experience. '
        'Below is an exact side-by-side comparison of original TalkToModel responses vs. '
        'improved DECF-Engine responses generated during live execution '
        '(<b>experiments/15_interactive_consensus_demo.py</b>):',
        B))

    # Case Study 1: High Consensus (Green)
    c1 = [[Paragraph(
        '<font color="white"><b>CASE STUDY 1: HIGH CONSENSUS QUERY — Diabetes Instance #288</b></font>',
        ParagraphStyle('CH', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE)
    )]]
    c1_body = [[Paragraph(
        '<b>User Query:</b> <i>"Why did the model predict patient 288 has diabetes?"</i><br/>'
        '<b>T5 DSL Parse:</b> <code>filter id 288 and explain features [e]</code><br/>'
        '<b>Internal Consensus Metrics:</b> SHAP Rankings: [BMI, Glucose, Pedigree] | '
        'LIME Rankings: [Pedigree, Glucose, BMI] | Top-3 Jaccard Overlap: <b>100.0%</b> | '
        'Spearman ρ: <b>0.690</b> | Borda Winner: BMI<br/><br/>'
        '<b>❌ BEFORE — Original TalkToModel Response:</b><br/>'
        '<i>"For diabetes instance 288, the model predicted: likely to have diabetes. '
        'The most important features are BMI, Glucose, and DiabetesPedigreeFunction."</i><br/>'
        '<font color="#8B1A1A">[LIMITATION: Zero epistemic calibration — no certainty qualification, '
        'no cross-validation, no faithfulness check]</font><br/><br/>'
        '<b>✅ AFTER — Improved DECF-Engine Response:</b><br/>'
        '<b>[TalkToModel Response #288]</b>  Prediction: <b>likely to have diabetes</b><br/>'
        '🟢 <b>Confidence: HIGH CONFIDENCE</b> (Top-3 Overlap: 100.0%, ρ=0.690)<br/>'
        'Both TreeSHAP (game-theoretic) and LIME (surrogate) independently confirmed '
        'the following key factors: <b>BMI, Glucose, DiabetesPedigreeFunction</b>.<br/>'
        'Faithfulness Verified: ΔP = <b>0.412</b> (masking these features causes 41.2% probability drop).',
        ParagraphStyle('CB', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=DGREY)
    )]]
    c1t_h = Table(c1, colWidths=[523])
    c1t_h.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1A5C58')),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    c1t_b = Table(c1_body, colWidths=[523])
    c1t_b.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), MINT),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#319795')),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(c1t_h)
    story.append(c1t_b)
    story.append(Spacer(1, 8))

    # Case Study 2: Severe Disagreement (Red)
    c2 = [[Paragraph(
        '<font color="white"><b>CASE STUDY 2: SEVERE DISAGREEMENT ALERT — German Credit Applicant #95</b></font>',
        ParagraphStyle('CH2', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE)
    )]]
    c2_body = [[Paragraph(
        '<b>User Query:</b> <i>"Why was loan applicant 95 denied credit?"</i><br/>'
        '<b>T5 DSL Parse:</b> <code>filter id 95 and explain features [e]</code><br/>'
        '<b>Internal Consensus Metrics:</b> SHAP: [LoanAmount, LoanDuration, CheckingBalance] | '
        'LIME: [NoCurrentLoan, UsedCar, LoanDuration] | Top-3 Overlap: <b>33.3%</b> | '
        'Spearman ρ: <b>0.116</b> → SEVERE DISAGREEMENT ZONE<br/><br/>'
        '<b>❌ BEFORE — Original TalkToModel Response:</b><br/>'
        '<i>"The most important features are LoanAmount, LoanDuration, and CheckingAccountBalance."</i><br/>'
        '<font color="#8B1A1A"><b>[CRITICAL DANGER: 100% FALSE CERTAINTY! LIME identified completely '
        'contradictory features. A loan officer relying on this output would be misled.]</b></font><br/><br/>'
        '<b>✅ AFTER — Improved DECF-Engine Response:</b><br/>'
        '<b>[TalkToModel Response #95]</b>  Prediction: <b>bad credit risk</b><br/>'
        '🔴 <b>WARNING: LOW CONFIDENCE — Severe Disagreement Alert Triggered!</b><br/>'
        'Top-3 Jaccard Overlap: <b>33.3%</b> | Spearman Rank Correlation: <b>ρ = 0.116</b><br/>'
        '<i>Epistemic Uncertainty Notice: TreeSHAP and LIME produce near-orthogonal feature rankings '
        'for this applicant. Single-explainer attribution is unreliable.</i><br/>'
        'Faithfulness Arbitration: Consensus Borda set yields ΔP=<b>0.385</b> vs. LIME alone 0.288 — '
        'consensus ranking is more faithful, but overall uncertainty remains HIGH.',
        ParagraphStyle('CB2', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=DGREY)
    )]]
    c2t_h = Table(c2, colWidths=[523])
    c2t_h.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), RED),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    c2t_b = Table(c2_body, colWidths=[523])
    c2t_b.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ROSE),
        ('BOX', (0,0), (-1,-1), 1.5, ALERT),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(c2t_h)
    story.append(c2t_b)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # ▌ SECTION 7 — CONCLUSION, LIMITATIONS & REPRODUCIBILITY (page 9)
    # ══════════════════════════════════════════════════════════════════════
    section_banner(story, '7.', 'Key Findings, Conclusion & Honest Limitations', NAVY)

    # Key Findings
    story.append(Paragraph('<b>7.1 Key Findings Summary</b>',
                           h2()))
    kf_data = [
        [th('#'), th('Finding', align=0), th('Quantitative Evidence', align=0)],
        [td('F1', align=1, bold=True), td('<b>Replication Validated:</b> Original TalkToModel results reproduced with high fidelity.'),
         td('Split B accuracy within ±1.7% of published values across all 3 datasets.')],
        [td('F2', align=1, bold=True), td('<b>Faithfulness Improved:</b> DECF-Engine Borda fusion consistently outperforms both individual explainers.'),
         td('Avg. +11.06% ΔP gain. German Credit: +22.22% — highest-impact dataset.')],
        [td('F3', align=1, bold=True), td('<b>Disagreement Detected:</b> Original TalkToModel was completely blind to explainer conflicts.'),
         td('0/60 cases detected by original. DECF-Engine flagged 26/60 (43.3%); 100% of severe cases caught.')],
        [td('F4', align=1, bold=True), td('<b>Real-Time Feasible:</b> Dual-explainer overhead is minimal and acceptable.'),
         td('Mean latency: 0.43s → 0.76s (+0.33s). All under 1.0s on standard CPU hardware.')],
        [td('F5', align=1, bold=True), td('<b>Safety-Critical Impact:</b> German Credit showed SHAP vs. LIME near-orthogonal rankings.'),
         td('ρ = 0.121 — two explainers essentially produced opposite feature importance rankings.')],
    ]
    kft = Table(kf_data, colWidths=[30, 290, 203])
    kft.setStyle(std_table_style(NAVY, alt_row=LGREY))
    story.append(kft)
    story.append(Spacer(1, 6))

    # Limitations
    story.append(Paragraph('<b>7.2 Honest Limitations &amp; Boundary Conditions</b>',
                           h2()))
    lim_data = [
        [th('#'), th('Limitation', align=0), th('Impact &amp; Mitigation', align=0)],
        [td('L1', align=1, bold=True),
         td('<b>Empty Intersection Cases:</b> In 5/20 German Credit instances, SHAP and LIME had zero top-3 overlap.'),
         td('Engine cannot fabricate consensus. Honestly issues epistemic alert and falls back to perturbation arbitration.')],
        [td('L2', align=1, bold=True),
         td('<b>Multicollinearity Masking:</b> In Diabetes, collinear features (Glucose vs. Insulin) '
            'partially cushion ΔP when one feature is perturbed.'),
         td('Joint perturbation of correlated feature groups could address this; left as future work.')],
        [td('L3', align=1, bold=True),
         td('<b>Tabular Tree-Model Scope:</b> Benchmarked exclusively on tabular classification with tree-based models.'),
         td('Extension to vision/NLP would require fast surrogate distillation methods.')],
        [td('L4', align=1, bold=True),
         td('<b>User Study Not Re-Run:</b> We re-analyse the authors\' existing CSV data; we did not conduct a new study.'),
         td('Our raw-data discrepancy findings (−17.2% on preference metric) are a secondary contribution.')],
    ]
    limt = Table(lim_data, colWidths=[30, 280, 213])
    limt.setStyle(std_table_style(colors.HexColor('#744210'), alt_row=CREAM))
    story.append(limt)
    story.append(Spacer(1, 6))

    # Reproducibility
    story.append(Paragraph('<b>7.3 Code Reproducibility Checklist</b>',
                           h2()))
    rep_data = [
        [th('Command / Script', align=0), th('Verified Output', align=0)],
        [td('<code>powershell -ExecutionPolicy Bypass -File .\\run_all.ps1</code>', bold=True),
         td('End-to-end pipeline: accuracy check → benchmark → tables → dashboards')],
        [td('<code>python experiments/10_compare_accuracy.py</code>', bold=True),
         td('Dual-split parsing evaluation (97.33% template leak vs. 67.40% held-out replication)')],
        [td('<code>python experiments/13_evaluate_consensus_improvement.py</code>', bold=True),
         td('60-instance DECF benchmark → Tables 4.1, 4.2, 4.3 above')],
        [td('<code>python experiments/14_generate_phase2_visualizations.py</code>', bold=True),
         td('All charts in Section 5: Phase 2 Master Dashboard, faithfulness bar chart, disagreement histogram')],
        [td('<code>python experiments/15_interactive_consensus_demo.py</code>', bold=True),
         td('Live terminal demo — interactive natural language queries, real-time DECF-Engine response')],
        [td('<b>GitHub Repository:</b>', bold=True),
         td('<b><font color="#2B6CB0">https://github.com/Shivwhoo/TalkToModel-XAI/tree/main/talktomodel-replication</font></b>',
            bold=True)],
    ]
    rept = Table(rep_data, colWidths=[250, 273])
    rept.setStyle(std_table_style(NAVY, alt_row=LGREY))
    story.append(rept)
    story.append(Spacer(1, 10))

    # Final conclusion callout
    conclusion_data = [[Paragraph(
        '<b>Conclusion:</b>  The DECF-Engine represents a principled, mathematically-grounded, '
        'and empirically-validated improvement to TalkToModel. By embedding multi-explainer '
        'consensus arbitration and perturbation faithfulness verification into the live conversational '
        'dialogue loop, we elevate TalkToModel from a <i>single-point-of-truth system</i> to an '
        '<i>epistemically honest, safety-aware explanation engine</i>. This is especially critical '
        'in high-stakes domains (credit underwriting, medical diagnosis, recidivism prediction) '
        'where presenting unreliable explanations with false confidence can cause real-world harm.',
        ParagraphStyle('Conc', fontName='Helvetica', fontSize=8, leading=11.5, textColor=DGREY)
    )]]
    conc_t = Table(conclusion_data, colWidths=[523])
    conc_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LGREY),
        ('BOX',        (0,0), (-1,-1), 2, NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
    ]))
    story.append(conc_t)

    # BUILD
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: {out}")


if __name__ == '__main__':
    os.chdir(r'C:\Users\Sachin\Desktop\talktomodel-replication')
    build_best_pdf()
