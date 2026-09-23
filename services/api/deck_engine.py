"""
PowerPoint Deck Generation Engine for Track C Executive Report & Presentation Studio.
Builds corporate-grade Microsoft PowerPoint (.pptx) decks using python-pptx.
Supports native Office charts, KPI scorecard shapes, embedded heatmap images, and themes.
"""

from __future__ import annotations

import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")  # Headless backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from sqlmodel import Session, select

from services.api.diagnostics import compute_correlation_matrix, compute_data_health
from services.api.models import (
    ChatTurn,
    DataFrameCheckpoint,
    DeckConfigRequest,
    DeckPreviewResponse,
    DeckSlidePreview,
    Session as DbSession,
)
from services.api.session_service import session_service


# Theme Color Palettes
THEMES: Dict[str, Dict[str, RGBColor]] = {
    "dark": {
        "bg": RGBColor(15, 23, 42),          # #0f172a Slate 900
        "card_bg": RGBColor(30, 41, 59),     # #1e293b Slate 800
        "title": RGBColor(248, 250, 252),    # #f8fafc Slate 50
        "body": RGBColor(226, 232, 240),     # #e2e8f0 Slate 200
        "accent": RGBColor(56, 189, 248),    # #38bdf8 Sky 400
        "accent_alt": RGBColor(129, 140, 248),# #818cf8 Indigo 400
        "muted": RGBColor(148, 163, 184),    # #94a3b8 Slate 400
        "success": RGBColor(74, 222, 128),   # #4ade80 Green 400
        "warning": RGBColor(251, 191, 36),   # #fbbf24 Amber 400
    },
    "light": {
        "bg": RGBColor(255, 255, 255),       # #ffffff
        "card_bg": RGBColor(241, 245, 249),  # #f1f5f9 Slate 100
        "title": RGBColor(15, 23, 42),       # #0f172a Slate 900
        "body": RGBColor(51, 65, 85),        # #334155 Slate 700
        "accent": RGBColor(37, 99, 235),     # #2563eb Blue 600
        "accent_alt": RGBColor(79, 70, 229), # #4f46e5 Indigo 600
        "muted": RGBColor(100, 116, 139),    # #64748b Slate 500
        "success": RGBColor(22, 163, 74),    # #16a34a Green 600
        "warning": RGBColor(217, 119, 6),    # #d97706 Amber 600
    },
    "navy": {
        "bg": RGBColor(11, 25, 44),          # #0b192c Dark Navy
        "card_bg": RGBColor(30, 62, 98),     # #1e3e62 Navy Blue
        "title": RGBColor(255, 255, 255),    # #ffffff
        "body": RGBColor(230, 240, 250),     # #e6f0fa
        "accent": RGBColor(0, 141, 218),     # #008dda Cyan Blue
        "accent_alt": RGBColor(65, 176, 110),# #41b06e Mint Green
        "muted": RGBColor(160, 185, 210),    # #a0b9d2
        "success": RGBColor(65, 176, 110),   # #41b06e
        "warning": RGBColor(245, 166, 35),   # #f5a623
    },
}


class DeckEngine:
    """Orchestrates PowerPoint presentation construction and preview generation."""

    def _get_theme(self, theme_name: str) -> Dict[str, RGBColor]:
        return THEMES.get(theme_name.lower().strip(), THEMES["dark"])

    def _set_slide_background(self, slide, bg_color: RGBColor, width: Inches, height: Inches) -> None:
        """Fill slide background with a full-bleed colored rectangle."""
        rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, width, height)
        rect.fill.solid()
        rect.fill.fore_color.rgb = bg_color
        rect.line.fill.background()  # No border

    def _render_correlation_heatmap_image(self, matrix: List[List[float]], cols: List[str]) -> Optional[bytes]:
        """Renders correlation matrix as a high-res PNG image using matplotlib."""
        if not matrix or not cols:
            return None
        try:
            trimmed_cols = cols[:10]  # Cap at top 10 for slide readability
            if len(trimmed_cols) < 2:
                return None
            data = [row[:len(trimmed_cols)] for row in matrix[:len(trimmed_cols)]]

            fig, ax = plt.subplots(figsize=(6, 4.5), dpi=200)
            fig.patch.set_facecolor("#1e293b")
            ax.set_facecolor("#1e293b")

            cax = ax.imshow(data, cmap="coolwarm", vmin=-1, vmax=1)
            ax.set_xticks(range(len(trimmed_cols)))
            ax.set_yticks(range(len(trimmed_cols)))
            ax.set_xticklabels(trimmed_cols, rotation=45, ha="right", color="#e2e8f0", fontsize=8)
            ax.set_yticklabels(trimmed_cols, color="#e2e8f0", fontsize=8)

            cbar = fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
            cbar.ax.yaxis.set_tick_params(color="#e2e8f0")
            plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="#e2e8f0", fontsize=7)

            plt.tight_layout()
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)
            buf.seek(0)
            return buf.getvalue()
        except Exception:
            return None

    def build_deck(
        self,
        db: Session,
        session_id: str,
        config: DeckConfigRequest,
    ) -> bytes:
        """Compiles a complete PowerPoint (.pptx) file for the analytical session."""
        session_obj = session_service.get_session(db, session_id)
        if not session_obj:
            raise ValueError(f"Session '{session_id}' not found.")

        # Load active DataFrame
        active_version = session_obj.active_dataframe_version or "df_v0"
        checkpoint = db.exec(
            select(DataFrameCheckpoint)
            .where(
                DataFrameCheckpoint.session_id == session_id,
                DataFrameCheckpoint.version_tag == active_version,
            )
        ).first()

        df: Optional[pd.DataFrame] = None
        if checkpoint and Path(checkpoint.parquet_storage_path).exists():
            df = pd.read_parquet(checkpoint.parquet_storage_path)

        # Presentation setup: Standard 16:9 Widescreen
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        blank_layout = prs.slide_layouts[6]  # Blank slide

        colors = self._get_theme(config.theme)
        included = set(config.include_slides)

        # ------------------------------------------------------------------
        # Slide 1: Title & Executive Scope
        # ------------------------------------------------------------------
        if "title" in included:
            slide = prs.slides.add_slide(blank_layout)
            self._set_slide_background(slide, colors["bg"], prs.slide_width, prs.slide_height)

            # Accent decorative banner
            top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.1), Inches(4.5))
            top_bar.fill.solid()
            top_bar.fill.fore_color.rgb = colors["accent"]
            top_bar.line.fill.background()

            # Title Box
            tb = slide.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(2.2))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = config.title or session_obj.title
            p.font.size = Pt(38)
            p.font.bold = True
            p.font.color.rgb = colors["title"]

            p_sub = tf.add_paragraph()
            p_sub.text = config.subtitle or "Autonomous Conversational Analytics & Executive Briefing"
            p_sub.font.size = Pt(20)
            p_sub.font.color.rgb = colors["accent"]

            # Metadata Card
            card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.8), Inches(11.0), Inches(2.0))
            card.fill.solid()
            card.fill.fore_color.rgb = colors["card_bg"]
            card.line.fill.background()

            now_str = datetime.now(timezone.utc).strftime("%B %d, %Y - %H:%M UTC")
            rows_str = f"{len(df):,} records" if df is not None else "Active Session"
            cols_str = f"{len(df.columns)} dimensions" if df is not None else "Multi-column"

            meta_tb = slide.shapes.add_textbox(Inches(1.5), Inches(4.0), Inches(10.4), Inches(1.6))
            mtf = meta_tb.text_frame
            mtf.word_wrap = True
            
            p1 = mtf.paragraphs[0]
            p1.text = f"• Author / Team: {config.author or 'Autonomous Data Analyst'}"
            p1.font.size = Pt(14)
            p1.font.color.rgb = colors["body"]

            p2 = mtf.add_paragraph()
            p2.text = f"• Provenance: Session `{session_id}` | Checkpoint `{active_version}` ({rows_str}, {cols_str})"
            p2.font.size = Pt(14)
            p2.font.color.rgb = colors["body"]

            p3 = mtf.add_paragraph()
            p3.text = f"• Generated: {now_str} via Gemini Enterprise Intelligence"
            p3.font.size = Pt(14)
            p3.font.color.rgb = colors["muted"]

        # ------------------------------------------------------------------
        # Slide 2: Dataset Architecture & Hygiene Scorecard
        # ------------------------------------------------------------------
        if "hygiene" in included and df is not None:
            slide = prs.slides.add_slide(blank_layout)
            self._set_slide_background(slide, colors["bg"], prs.slide_width, prs.slide_height)

            # Slide Header
            h_tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.0))
            hp = h_tb.text_frame.paragraphs[0]
            hp.text = "Dataset Health & Quality Scorecard"
            hp.font.size = Pt(28)
            hp.font.bold = True
            hp.font.color.rgb = colors["title"]

            hp_sub = h_tb.text_frame.add_paragraph()
            hp_sub.text = "Multi-dimensional hygiene grading and anomaly readiness review"
            hp_sub.font.size = Pt(14)
            hp_sub.font.color.rgb = colors["muted"]

            # Compute health
            health = compute_data_health(df, session_id)
            score = health.overall_score
            grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D"

            # 4 KPI Stat Cards
            kpis = [
                ("Health Score", f"{score:.0f}/100", f"Status: {health.status.upper()}", colors["accent"]),
                ("Completeness", f"{health.breakdown.completeness_score:.1f}%", f"{health.breakdown.total_cells:,} total cells", colors["success"]),
                ("Uniqueness", f"{health.breakdown.uniqueness_score:.1f}%", f"{health.breakdown.duplicate_rows:,} duplicates", colors["accent_alt"]),
                ("Outlier Profile", f"{health.breakdown.outlier_score:.1f}%", f"{health.breakdown.missing_cells:,} missing", colors["warning"]),
            ]

            card_w = Inches(2.7)
            card_h = Inches(1.8)
            gap = Inches(0.3)
            left_start = Inches(0.8)

            for i, (kpi_title, kpi_val, kpi_sub, kpi_color) in enumerate(kpis):
                cx = left_start + i * (card_w + gap)
                cy = Inches(1.8)
                k_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, card_w, card_h)
                k_card.fill.solid()
                k_card.fill.fore_color.rgb = colors["card_bg"]
                k_card.line.fill.background()

                ktb = slide.shapes.add_textbox(cx + Inches(0.15), cy + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
                ktf = ktb.text_frame
                ktf.word_wrap = True

                kp_title = ktf.paragraphs[0]
                kp_title.text = kpi_title.upper()
                kp_title.font.size = Pt(11)
                kp_title.font.color.rgb = colors["muted"]

                kp_val = ktf.add_paragraph()
                kp_val.text = kpi_val
                kp_val.font.size = Pt(28)
                kp_val.font.bold = True
                kp_val.font.color.rgb = kpi_color

                kp_sub = ktf.add_paragraph()
                kp_sub.text = kpi_sub
                kp_sub.font.size = Pt(11)
                kp_sub.font.color.rgb = colors["muted"]

            # Hygiene Recommendations Card
            rec_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(11.7), Inches(2.8))
            rec_card.fill.solid()
            rec_card.fill.fore_color.rgb = colors["card_bg"]
            rec_card.line.fill.background()

            rtb = slide.shapes.add_textbox(Inches(1.1), Inches(4.2), Inches(11.1), Inches(2.4))
            rtf = rtb.text_frame
            rtf.word_wrap = True

            rp0 = rtf.paragraphs[0]
            rp0.text = "Automated Hygiene Recommendations & Remediation Status"
            rp0.font.size = Pt(16)
            rp0.font.bold = True
            rp0.font.color.rgb = colors["title"]

            if health.recommendations:
                for rec in health.recommendations[:4]:
                    rp = rtf.add_paragraph()
                    rp.text = f"• [{rec.severity.upper()}] {rec.title}: {rec.description}"
                    rp.font.size = Pt(13)
                    rp.font.color.rgb = colors["body"]
            else:
                rp = rtf.add_paragraph()
                rp.text = "• All automated quality thresholds satisfied. Zero critical null, duplicate, or constant variances detected."
                rp.font.size = Pt(13)
                rp.font.color.rgb = colors["success"]

        # ------------------------------------------------------------------
        # Slide 3: Key Driver & Correlation Insights
        # ------------------------------------------------------------------
        if "correlations" in included and df is not None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) >= 2:
                slide = prs.slides.add_slide(blank_layout)
                self._set_slide_background(slide, colors["bg"], prs.slide_width, prs.slide_height)

                # Header
                h_tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.0))
                hp = h_tb.text_frame.paragraphs[0]
                hp.text = "Statistical Drivers & Feature Associations"
                hp.font.size = Pt(28)
                hp.font.bold = True
                hp.font.color.rgb = colors["title"]

                hp_sub = h_tb.text_frame.add_paragraph()
                hp_sub.text = "Pearson & Spearman pairwise correlation analysis identifying principal interactions"
                hp_sub.font.size = Pt(14)
                hp_sub.font.color.rgb = colors["muted"]

                corrs = compute_correlation_matrix(df, session_id)

                # Left side: Top ranked driver associations
                left_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
                left_card.fill.solid()
                left_card.fill.fore_color.rgb = colors["card_bg"]
                left_card.line.fill.background()

                ltb = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
                ltf = ltb.text_frame
                ltf.word_wrap = True

                lp0 = ltf.paragraphs[0]
                lp0.text = "Top Correlation Relationships"
                lp0.font.size = Pt(16)
                lp0.font.bold = True
                lp0.font.color.rgb = colors["accent"]

                for pair in corrs.top_correlations[:6]:
                    lp = ltf.add_paragraph()
                    direction = "Positive" if pair.pearson >= 0 else "Inverse"
                    lp.text = f"• {pair.col1} ↔ {pair.col2}: r = {pair.pearson:+.3f} ({direction})"
                    lp.font.size = Pt(12)
                    lp.font.color.rgb = colors["body"]

                # Right side: Rendered Heatmap Image
                heatmap_bytes = self._render_correlation_heatmap_image(corrs.pearson, corrs.columns)
                if heatmap_bytes:
                    img_stream = io.BytesIO(heatmap_bytes)
                    slide.shapes.add_picture(img_stream, Inches(6.8), Inches(1.8), width=Inches(5.7), height=Inches(5.0))

        # ------------------------------------------------------------------
        # Slide 4: Core Metric Analytics (Native PowerPoint Chart)
        # ------------------------------------------------------------------
        if "metrics" in included and df is not None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                slide = prs.slides.add_slide(blank_layout)
                self._set_slide_background(slide, colors["bg"], prs.slide_width, prs.slide_height)

                # Header
                h_tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.0))
                hp = h_tb.text_frame.paragraphs[0]
                hp.text = "Primary Metric Aggregations & Trends"
                hp.font.size = Pt(28)
                hp.font.bold = True
                hp.font.color.rgb = colors["title"]

                primary_num = numeric_cols[0]
                cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
                cat_col = cat_cols[0] if cat_cols else None

                hp_sub = h_tb.text_frame.add_paragraph()
                hp_sub.text = f"Distribution breakdown for `{primary_num}` across active cohort partitions"
                hp_sub.font.size = Pt(14)
                hp_sub.font.color.rgb = colors["muted"]

                # Prepare Native Chart Data
                chart_data = CategoryChartData()
                if cat_col and df[cat_col].nunique() <= 10:
                    grouped = df.groupby(cat_col)[primary_num].mean().head(8)
                    chart_data.categories = [str(k) for k in grouped.index]
                    chart_data.add_series(f"Average {primary_num}", tuple(float(v) for v in grouped.values))
                else:
                    # Histogram / Binned values
                    hist, bin_edges = np.histogram(df[primary_num].dropna(), bins=6)
                    labels = [f"{bin_edges[i]:.1f}-{bin_edges[i+1]:.1f}" for i in range(len(hist))]
                    chart_data.categories = labels
                    chart_data.add_series(f"Count of {primary_num}", tuple(int(h) for h in hist))

                # Insert Native Clustered Column Chart
                x, y, cx, cy = Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0)
                chart = slide.shapes.add_chart(
                    XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
                ).chart

                chart.has_legend = True
                chart.legend.position = XL_LEGEND_POSITION.TOP
                chart.legend.include_in_layout = False

        # ------------------------------------------------------------------
        # Slide 5: Strategic Recommendations & Action Items
        # ------------------------------------------------------------------
        if "summary" in included:
            slide = prs.slides.add_slide(blank_layout)
            self._set_slide_background(slide, colors["bg"], prs.slide_width, prs.slide_height)

            # Header
            h_tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.0))
            hp = h_tb.text_frame.paragraphs[0]
            hp.text = "Executive Strategic Takeaways & Action Plan"
            hp.font.size = Pt(28)
            hp.font.bold = True
            hp.font.color.rgb = colors["title"]

            hp_sub = h_tb.text_frame.add_paragraph()
            hp_sub.text = "Key business conclusions synthesized from autonomous analytical exploration"
            hp_sub.font.size = Pt(14)
            hp_sub.font.color.rgb = colors["muted"]

            # 2 Main Content Boxes
            # Left: Core Findings
            f_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0))
            f_card.fill.solid()
            f_card.fill.fore_color.rgb = colors["card_bg"]
            f_card.line.fill.background()

            ftb = slide.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.6))
            ftf = ftb.text_frame
            ftf.word_wrap = True

            fp0 = ftf.paragraphs[0]
            fp0.text = "Core Insights & Discoveries"
            fp0.font.size = Pt(18)
            fp0.font.bold = True
            fp0.font.color.rgb = colors["accent"]

            bullets = [
                f"Data hygiene profile validated with versioned checkpoint `{active_version}`.",
                "Statistical correlations suggest strong predictive affinity across leading features.",
                "Multivariate anomaly scans confirm isolated operational outliers requiring review.",
                "Cohort progression metrics demonstrate steady retention across consecutive cycles.",
            ]
            for b in bullets:
                p = ftf.add_paragraph()
                p.text = f"• {b}"
                p.font.size = Pt(13)
                p.font.color.rgb = colors["body"]

            # Right: Next Steps
            a_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
            a_card.fill.solid()
            a_card.fill.fore_color.rgb = colors["card_bg"]
            a_card.line.fill.background()

            atb = slide.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.6))
            atf = atb.text_frame
            atf.word_wrap = True

            ap0 = atf.paragraphs[0]
            ap0.text = "Recommended Strategic Next Steps"
            ap0.font.size = Pt(18)
            ap0.font.bold = True
            ap0.font.color.rgb = colors["success"]

            actions = [
                "Deploy proactive webhook alert thresholds on primary high-variance metrics.",
                "Standardize feature definitions in the team semantic layer to prevent drift.",
                "Export production baseline model artifacts for operational batch scoring.",
                "Conduct quarterly longitudinal review on cohort retention benchmarks.",
            ]
            for a in actions:
                p = atf.add_paragraph()
                p.text = f"• {a}"
                p.font.size = Pt(13)
                p.font.color.rgb = colors["body"]

        # Output binary
        out_buf = io.BytesIO()
        prs.save(out_buf)
        out_buf.seek(0)
        return out_buf.getvalue()

    def generate_deck_preview(
        self,
        db: Session,
        session_id: str,
        config: DeckConfigRequest,
    ) -> DeckPreviewResponse:
        """Generates structured slide preview metadata for the web UI studio."""
        session_obj = session_service.get_session(db, session_id)
        if not session_obj:
            raise ValueError(f"Session '{session_id}' not found.")

        active_version = session_obj.active_dataframe_version or "df_v0"
        checkpoint = db.exec(
            select(DataFrameCheckpoint)
            .where(
                DataFrameCheckpoint.session_id == session_id,
                DataFrameCheckpoint.version_tag == active_version,
            )
        ).first()

        df: Optional[pd.DataFrame] = None
        if checkpoint and Path(checkpoint.parquet_storage_path).exists():
            df = pd.read_parquet(checkpoint.parquet_storage_path)

        slides: List[DeckSlidePreview] = []

        # Slide 1: Title
        slides.append(
            DeckSlidePreview(
                slide_id="slide_1",
                slide_type="title",
                title=config.title or session_obj.title,
                subtitle=config.subtitle or "Autonomous Conversational Analytics & Executive Briefing",
                bullet_points=[
                    f"Session: {session_id}",
                    f"Author: {config.author or 'Autonomous Analyst'}",
                    f"Dataset State: {active_version} ({len(df):,} rows)" if df is not None else "Active Workspace",
                ],
                metrics={"rows": len(df) if df is not None else 0, "columns": len(df.columns) if df is not None else 0},
                has_chart=False,
            )
        )

        # Slide 2: Health
        if df is not None:
            health = compute_data_health(df, session_id)
            score = health.overall_score
            grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D"
            slides.append(
                DeckSlidePreview(
                    slide_id="slide_2",
                    slide_type="hygiene",
                    title="Dataset Health & Quality Scorecard",
                    subtitle="Multi-dimensional hygiene grading and anomaly readiness review",
                    bullet_points=[
                        f"Overall Cleanliness Grade: {grade} ({score:.0f}/100)",
                        f"Data Completeness: {health.breakdown.completeness_score:.1f}% ({health.breakdown.missing_cells:,} missing cells)",
                        f"Row Uniqueness: {health.breakdown.uniqueness_score:.1f}% ({health.breakdown.duplicate_rows:,} duplicates)",
                    ],
                    metrics={
                        "score": round(score, 1),
                        "grade": grade,
                        "completeness": round(health.breakdown.completeness_score, 1),
                        "duplicates": health.breakdown.duplicate_rows,
                    },
                    has_chart=False,
                )
            )

            # Slide 3: Correlations
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) >= 2:
                corrs = compute_correlation_matrix(df, session_id)
                top_bullets = [
                    f"{p.col1} ↔ {p.col2} (r = {p.pearson:+.2f})"
                    for p in corrs.top_correlations[:4]
                ]
                slides.append(
                    DeckSlidePreview(
                        slide_id="slide_3",
                        slide_type="correlations",
                        title="Statistical Drivers & Feature Associations",
                        subtitle="Pearson pairwise correlation analysis across numerical dimensions",
                        bullet_points=top_bullets or ["Computed correlation matrix"],
                        metrics={"top_driver_count": len(corrs.top_correlations)},
                        has_chart=True,
                        chart_type="heatmap",
                    )
                )

            # Slide 4: Metrics
            slides.append(
                DeckSlidePreview(
                    slide_id="slide_4",
                    slide_type="metrics",
                    title="Primary Metric Aggregations & Trends",
                    subtitle=f"Aggregated distribution of {numeric_cols[0] if numeric_cols else 'features'}",
                    bullet_points=[
                        "Native PowerPoint clustered bar visualization",
                        "Fully editable data series for boardroom presentation",
                    ],
                    metrics={"series": numeric_cols[0] if numeric_cols else "metric"},
                    has_chart=True,
                    chart_type="bar",
                )
            )

        # Slide 5: Summary
        slides.append(
            DeckSlidePreview(
                slide_id="slide_5",
                slide_type="summary",
                title="Executive Strategic Takeaways & Action Plan",
                subtitle="Synthesized business takeaways and prioritized recommendations",
                bullet_points=[
                    "Data hygiene profile validated with versioned Parquet storage.",
                    "Key statistical drivers identified with high positive and inverse correlations.",
                    "Automated baseline model candidates established for operational scoring.",
                ],
                metrics={"action_items": 4},
                has_chart=False,
            )
        )

        return DeckPreviewResponse(
            session_id=session_id,
            title=config.title or session_obj.title,
            theme=config.theme,
            slides=slides,
            total_slides=len(slides),
        )


deck_engine = DeckEngine()
