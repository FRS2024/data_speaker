"""
Executive PDF Brief Compiler for Track C Executive Report & Presentation Studio.
Builds corporate-grade PDF documents using ReportLab.
Features KPI scorecard callouts, formatted schema tables, executive narratives, and running headers/footers.
"""

from __future__ import annotations

import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlmodel import Session, select

from services.api.diagnostics import compute_correlation_matrix, compute_data_health
from services.api.models import (
    DataFrameCheckpoint,
    Session as DbSession,
)
from services.api.session_service import session_service


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw running 'Page X of Y' footers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Top Header (Page 2+)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "Gemini Data Speaker — Executive Analytics Brief")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Running Bottom Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_text)
        self.drawString(54, 36, "Confidential — For Internal Executive Decision Support Only")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, letter[0] - 54, 46)

        self.restoreState()


class PdfEngine:
    """Compiles multi-page executive PDF reports."""

    def build_pdf_report(
        self,
        db: Session,
        session_id: str,
        title: Optional[str] = None,
        author: Optional[str] = "Autonomous Data Analyst",
    ) -> bytes:
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

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54,
        )

        styles = getSampleStyleSheet()

        # Custom Corporate Typography Styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#0F172A"),
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#2563EB"),
        )
        h1_style = ParagraphStyle(
            "H1",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=14,
            spaceAfter=6,
        )
        h2_style = ParagraphStyle(
            "H2",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#334155"),
            spaceBefore=8,
            spaceAfter=4,
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#334155"),
        )
        meta_style = ParagraphStyle(
            "Meta",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#64748B"),
        )

        story = []

        # 1. Header Banner
        report_title = title or session_obj.title
        story.append(Paragraph(report_title, title_style))
        story.append(Paragraph("Executive Analytics & Data Health Intelligence Brief", subtitle_style))
        story.append(Spacer(1, 8))

        now_str = datetime.now(timezone.utc).strftime("%B %d, %Y - %H:%M UTC")
        meta_text = (
            f"<b>Author:</b> {author} &nbsp;|&nbsp; "
            f"<b>Session ID:</b> <code>{session_id}</code> &nbsp;|&nbsp; "
            f"<b>Version:</b> <code>{active_version}</code> &nbsp;|&nbsp; "
            f"<b>Date:</b> {now_str}"
        )
        story.append(Paragraph(meta_text, meta_style))
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceBefore=4, spaceAfter=14))

        # 2. Executive Summary Callout
        story.append(Paragraph("1. Executive Summary & Quality Scorecard", h1_style))
        
        row_count_str = f"{len(df):,}" if df is not None else "0"
        col_count_str = f"{len(df.columns)}" if df is not None else "0"
        
        summary_p = (
            f"This executive briefing evaluates active dataset checkpoint <code>{active_version}</code> containing "
            f"<b>{row_count_str} rows</b> across <b>{col_count_str} dimensions</b>. "
            f"Exploratory profiling, statistical interaction analyses, and automated quality heuristics have been executed "
            f"to establish operational data readiness and strategic takeaways."
        )
        story.append(Paragraph(summary_p, body_style))
        story.append(Spacer(1, 10))

        # KPI Scorecard Cards
        if df is not None:
            health = compute_data_health(df, session_id)
            score = health.overall_score
            grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D"
            kpi_data = [
                [
                    Paragraph(f"<b>Overall Health</b><br/><font size='16' color='#2563EB'><b>{score:.0f}/100</b></font><br/>Grade {grade}", body_style),
                    Paragraph(f"<b>Completeness</b><br/><font size='16' color='#16A34A'><b>{health.breakdown.completeness_score:.1f}%</b></font><br/>{health.breakdown.missing_cells:,} missing", body_style),
                    Paragraph(f"<b>Row Uniqueness</b><br/><font size='16' color='#7C3AED'><b>{health.breakdown.uniqueness_score:.1f}%</b></font><br/>{health.breakdown.duplicate_rows:,} duplicates", body_style),
                    Paragraph(f"<b>Outlier Ratio</b><br/><font size='16' color='#D97706'><b>{health.breakdown.outlier_score:.1f}%</b></font><br/>{health.breakdown.total_rows:,} total rows", body_style),
                ]
            ]
            kpi_table = Table(kpi_data, colWidths=[126, 126, 126, 126])
            kpi_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]))
            story.append(kpi_table)
            story.append(Spacer(1, 14))

        # 3. Schema Architecture Table
        story.append(Paragraph("2. Schema Architecture & Column Profiles", h1_style))
        if df is not None:
            schema_rows = [
                [
                    Paragraph("<b>Column</b>", body_style),
                    Paragraph("<b>Type</b>", body_style),
                    Paragraph("<b>Nulls</b>", body_style),
                    Paragraph("<b>Null %</b>", body_style),
                    Paragraph("<b>Distinct</b>", body_style),
                ]
            ]
            for col in df.columns[:15]:  # Display top 15 columns
                s = df[col]
                null_c = int(s.isnull().sum())
                null_pct = (null_c / len(df)) * 100.0 if len(df) > 0 else 0.0
                card = int(s.nunique())
                schema_rows.append([
                    Paragraph(f"<code>{col}</code>", body_style),
                    Paragraph(str(s.dtype), meta_style),
                    Paragraph(f"{null_c:,}", meta_style),
                    Paragraph(f"{null_pct:.1f}%", meta_style),
                    Paragraph(f"{card:,}", meta_style),
                ])

            schema_table = Table(schema_rows, colWidths=[160, 84, 80, 80, 100])
            schema_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ]))
            story.append(schema_table)
            story.append(Spacer(1, 14))

        # 4. Key Driver & Correlation Insights
        if df is not None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) >= 2:
                story.append(Paragraph("3. Statistical Driver Associations", h1_style))
                corrs = compute_correlation_matrix(df, session_id)
                corr_rows = [
                    [
                        Paragraph("<b>Dimension A</b>", body_style),
                        Paragraph("<b>Dimension B</b>", body_style),
                        Paragraph("<b>Pearson r</b>", body_style),
                        Paragraph("<b>Strength / Direction</b>", body_style),
                    ]
                ]
                for p in corrs.top_correlations[:6]:
                    strength = "Strong Positive" if p.pearson >= 0.6 else "Moderate Positive" if p.pearson >= 0.3 else "Inverse" if p.pearson <= -0.3 else "Weak"
                    corr_rows.append([
                        Paragraph(f"<code>{p.col1}</code>", body_style),
                        Paragraph(f"<code>{p.col2}</code>", body_style),
                        Paragraph(f"<b>{p.pearson:+.3f}</b>", body_style),
                        Paragraph(strength, meta_style),
                    ])
                corr_table = Table(corr_rows, colWidths=[150, 150, 84, 120])
                corr_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ]))
                story.append(corr_table)
                story.append(Spacer(1, 14))

        # 5. Strategic Recommendations & Action Items
        story.append(Paragraph("4. Strategic Recommendations & Action Items", h1_style))
        recs = [
            "<b>1. Automated Remediation Deployment:</b> Implement winsorization on skewed dimensions and enforce schema constraints.",
            "<b>2. Baseline Model Integration:</b> Promote high-performing tree ensembles to batch scoring pipelines for predictive segmentation.",
            "<b>3. Monitoring & Threshold Triggers:</b> Set proactive anomaly threshold alerts to trigger webhooks when distributional drift exceeds 5%.",
            "<b>4. Semantic Metric Harmonization:</b> Synchronize calculated measures with the team semantic metric dictionary.",
        ]
        for r in recs:
            story.append(Paragraph(r, body_style))
            story.append(Spacer(1, 4))

        # Build document with NumberedCanvas
        doc.build(story, canvasmaker=NumberedCanvas)
        buf.seek(0)
        return buf.getvalue()


pdf_engine = PdfEngine()
