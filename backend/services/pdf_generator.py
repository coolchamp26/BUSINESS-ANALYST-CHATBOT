import io
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Canvas to calculate total pages dynamically and add page numbers.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress page number on cover page
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header
        self.drawString(54, 750, "FlowArchitect AI — Business Process Assessment")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 742, letter[0] - 54, 742)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL — Prepared by FlowArchitect AI")
        self.line(54, 48, letter[0] - 54, 48)
        self.restoreState()

def generate_pdf_report(analysis_data: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    # Styles
    styles = getSampleStyleSheet()
    
    # Custom colors
    primary_color = colors.HexColor("#1e1b4b")  # Dark Indigo
    secondary_color = colors.HexColor("#0f766e")  # Teal
    accent_color = colors.HexColor("#4f46e5")  # Indigo
    dark_gray = colors.HexColor("#1e293b")
    text_color = colors.HexColor("#334155")
    bg_light = colors.HexColor("#f8fafc")
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=primary_color,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        leading=22,
        textColor=secondary_color,
        spaceAfter=150
    )
    
    metadata_style = ParagraphStyle(
        'CoverMetadata',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        textColor=dark_gray,
        spaceAfter=5
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_color,
        spaceAfter=10
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_color,
        leftIndent=15,
        spaceAfter=6
    )

    story = []

    # --- COVER PAGE ---
    story.append(Spacer(1, 100))
    story.append(Paragraph("FLOWARCHITECT AI", ParagraphStyle('CoverBrand', parent=title_style, fontSize=14, textColor=accent_color, spaceAfter=10)))
    story.append(Paragraph("Business Process Audit & Automation Blueprint", title_style))
    story.append(Paragraph("A comprehensive virtual consulting brief outlining operational inefficiencies, technology stack recommendations, ROI projections, and implementation roadmap.", subtitle_style))
    
    meta_table_data = [
        [Paragraph("Client Company:", metadata_style), Paragraph(analysis_data.get("company_name", "Valued Client"), body_style)],
        [Paragraph("Industry Focus:", metadata_style), Paragraph(analysis_data.get("industry", "Business Services"), body_style)],
        [Paragraph("Organization Size:", metadata_style), Paragraph(analysis_data.get("company_size", "Not specified"), body_style)],
        [Paragraph("Assessment Date:", metadata_style), Paragraph("June 5, 2026", body_style)],
    ]
    meta_table = Table(meta_table_data, colWidths=[150, 350])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # --- SECTION 1: EXECUTIVE SUMMARY ---
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Spacer(1, 5))
    
    summary = analysis_data.get("business_summary", {})
    story.append(Paragraph(f"This assessment was conducted by the FlowArchitect AI consulting engine to analyze operational processes at <b>{analysis_data.get('company_name')}</b>. The audit evaluated existing bottlenecks, manual friction points, and opportunities to adopt artificial intelligence and automated workflows.", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Key Core Processes Analysed:", h2_style))
    for proc in summary.get("key_processes", []):
        story.append(Paragraph(f"• {proc}", bullet_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Current Software & Systems Tooling:", h2_style))
    story.append(Paragraph(summary.get("existing_tools", "No legacy software declared."), body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Primary Operational Bottlenecks Detected:", h2_style))
    story.append(Paragraph(summary.get("operational_bottlenecks", "No major bottlenecks reported."), body_style))
    story.append(Spacer(1, 15))

    # --- SECTION 2: OPERATIONAL PATHOLOGY (PAIN POINTS) ---
    story.append(Paragraph("2. Operational Friction & Pain Point Analysis", h1_style))
    story.append(Paragraph("The consulting agents isolated friction across five critical operational segments:", body_style))
    story.append(Spacer(1, 10))
    
    pain_points = analysis_data.get("pain_points", {})
    pain_data = [
        [Paragraph("<b>Friction Segment</b>", metadata_style), Paragraph("<b>Identified Operational Bottlenecks</b>", metadata_style)],
        [Paragraph("Manual Workload", body_style), Paragraph(pain_points.get("manual_work", "No manual bottlenecks noted."), body_style)],
        [Paragraph("Customer Communications", body_style), Paragraph(pain_points.get("customer_communication", "No communication bottlenecks noted."), body_style)],
        [Paragraph("Sales Pipeline Inefficiencies", body_style), Paragraph(pain_points.get("sales_inefficiencies", "No sales pipeline bottlenecks noted."), body_style)],
        [Paragraph("Customer Support Overload", body_style), Paragraph(pain_points.get("support_inefficiencies", "No customer support bottlenecks noted."), body_style)],
        [Paragraph("Analytics & Reporting Delays", body_style), Paragraph(pain_points.get("reporting_challenges", "No analytics bottlenecks noted."), body_style)]
    ]
    pain_table = Table(pain_data, colWidths=[150, 350])
    pain_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(pain_table)
    story.append(PageBreak())

    # --- SECTION 3: READINESS & RECOMMENDATIONS ---
    story.append(Paragraph("3. Department Automation Readiness Scores", h1_style))
    story.append(Paragraph("Departmental readiness profiles reflect the urgency and integration compatibility of existing workflows. Lower scores indicate higher urgency to automate due to high manual friction.", body_style))
    story.append(Spacer(1, 10))
    
    readiness = analysis_data.get("readiness_scores", {})
    readiness_data = [[Paragraph("<b>Department</b>", metadata_style), Paragraph("<b>Readiness Score (0-100)</b>", metadata_style), Paragraph("<b>Status Assessment</b>", metadata_style)]]
    for dept, val in readiness.items():
        status = "Critically Manual" if val < 40 else ("Developing" if val < 70 else "Optimized")
        readiness_data.append([
            Paragraph(dept, body_style),
            Paragraph(f"{val} / 100", body_style),
            Paragraph(status, metadata_style if status == "Critically Manual" else body_style)
        ])
    
    readiness_table = Table(readiness_data, colWidths=[150, 150, 200])
    readiness_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(readiness_table)
    story.append(Spacer(1, 20))

    story.append(Paragraph("4. Recommended AI Automation Opportunities", h1_style))
    recs = analysis_data.get("recommendations", [])
    
    for i, rec in enumerate(recs):
        rec_title = f"Opportunity #{i+1}: {rec.get('title')}"
        story.append(Paragraph(rec_title, h2_style))
        story.append(Paragraph(f"<b>Category:</b> {rec.get('category')}  |  <b>Priority:</b> {rec.get('priority')}  |  <b>Effort:</b> {rec.get('effort')}", metadata_style))
        story.append(Paragraph(rec.get("description", ""), body_style))
        
        # Display blueprint detail
        bp = rec.get("blueprint", {})
        if bp:
            bp_data = [
                [Paragraph("<b>Step Type</b>", metadata_style), Paragraph("<b>Implementation Details</b>", metadata_style)],
                [Paragraph("<b>Trigger</b>", body_style), Paragraph(bp.get("trigger", ""), body_style)],
                [Paragraph("<b>Process Path</b>", body_style), Paragraph("<br/>".join([f"{idx+1}. {step}" for idx, step in enumerate(bp.get("process", []))]), body_style)],
                [Paragraph("<b>Integrations</b>", body_style), Paragraph(", ".join(bp.get("tools", [])), body_style)],
                [Paragraph("<b>Difficulty / Timeline</b>", body_style), Paragraph(f"{bp.get('difficulty', 'Medium')} / {bp.get('setup_time', 'N/A')}", body_style)]
            ]
            bp_table = Table(bp_data, colWidths=[120, 380])
            bp_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,-1), bg_light),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(Spacer(1, 5))
            story.append(bp_table)
        story.append(Spacer(1, 15))
        
    story.append(PageBreak())

    # --- SECTION 4: ROI FORECASTS & TECH STACKS ---
    story.append(Paragraph("5. Automation Tech Stack & Pricing Model", h1_style))
    story.append(Paragraph("To establish these workflows, our Automation Agent recommends the following tools, ensuring minimal setup overlap and optimized recurring subscription footprints:", body_style))
    story.append(Spacer(1, 10))
    
    stacks = analysis_data.get("tech_stack", [])
    stack_data = [[
        Paragraph("<b>Workspace Area</b>", metadata_style),
        Paragraph("<b>Recommended Technology</b>", metadata_style),
        Paragraph("<b>Monthly Cost</b>", metadata_style),
        Paragraph("<b>Setup Duration</b>", metadata_style)
    ]]
    
    total_cost = 0
    for item in stacks:
        cost_val = item.get("cost", 0)
        total_cost += cost_val
        stack_data.append([
            Paragraph(item.get("category", ""), body_style),
            Paragraph(item.get("tool", ""), body_style),
            Paragraph(f"INR {cost_val}", body_style),
            Paragraph(item.get("setup_time", ""), body_style)
        ])
        
    # Total row
    stack_data.append([
        Paragraph("<b>Total Projected Software Cost</b>", metadata_style),
        Paragraph("", body_style),
        Paragraph(f"<b>INR {total_cost} / month</b>", metadata_style),
        Paragraph("", body_style)
    ])
    
    stack_table = Table(stack_data, colWidths=[150, 150, 100, 100])
    stack_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_light),
        ('GRID', (0,0), (-1,-2), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (0,-1), (-1,-1), 1.5, primary_color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(stack_table)
    story.append(Spacer(1, 20))

    story.append(Paragraph("6. Business Impact & ROI Forecasts", h1_style))
    story.append(Paragraph("Predictive estimates modeled based on automated workflows resolving support channels and pre-qualifying leads:", body_style))
    story.append(Spacer(1, 10))
    
    roi = analysis_data.get("roi_prediction", {})
    roi_data = [
        [Paragraph("<b>Performance Metric</b>", metadata_style), Paragraph("<b>Before Automation</b>", metadata_style), Paragraph("<b>After Automation (Forecast)</b>", metadata_style)],
        [Paragraph("Monthly Lead Flow", body_style), Paragraph(str(roi.get("current_leads", 0)), body_style), Paragraph(str(roi.get("predicted_leads", 0)), body_style)],
        [Paragraph("Conversion Rate", body_style), Paragraph(f"{roi.get('current_conversion', 0)}%", body_style), Paragraph(f"{roi.get('predicted_conversion', 0)}%", body_style)],
        [Paragraph("Monthly Support Overhead", body_style), Paragraph(f"INR {roi.get('current_support_cost', 0)}", body_style), Paragraph(f"INR {roi.get('predicted_support_cost', 0)}", body_style)],
        [Paragraph("Weekly Team Hours Reclaimed", body_style), Paragraph("0 Hours", body_style), Paragraph(f"{roi.get('hours_saved_weekly', 0)} Hours", metadata_style)],
        [Paragraph("Net Monthly Savings", body_style), Paragraph("N/A", body_style), Paragraph(f"INR {roi.get('monthly_cost_savings', 0)}", metadata_style)]
    ]
    
    roi_table = Table(roi_data, colWidths=[200, 150, 150])
    roi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(roi_table)
    story.append(PageBreak())

    # --- SECTION 5: IMPLEMENTATION ROADMAP ---
    story.append(Paragraph("7. Implementation Roadmap & Timeline", h1_style))
    story.append(Paragraph("The recommended phased rollout timeline is designed to tackle quick wins first to establish confidence and ROI before scaling complex integrations.", body_style))
    story.append(Spacer(1, 10))
    
    roadmap = analysis_data.get("roadmap_plan", {})
    
    story.append(Paragraph("Phase 1: Quick Wins (Weeks 1-2)", h2_style))
    for step in roadmap.get("phase1", []):
        story.append(Paragraph(f"<b>{step.get('title')} ({step.get('timeline')})</b>", metadata_style))
        story.append(Paragraph(f"Action: {step.get('action')}<br/>Deliverable: {step.get('deliverables')}", body_style))
        story.append(Spacer(1, 5))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Phase 2: CRM & Core Systems Integration (Weeks 3-5)", h2_style))
    for step in roadmap.get("phase2", []):
        story.append(Paragraph(f"<b>{step.get('title')} ({step.get('timeline')})</b>", metadata_style))
        story.append(Paragraph(f"Action: {step.get('action')}<br/>Deliverable: {step.get('deliverables')}", body_style))
        story.append(Spacer(1, 5))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Phase 3: Advanced AI & Agent Orchestration (Weeks 6-8)", h2_style))
    for step in roadmap.get("phase3", []):
        story.append(Paragraph(f"<b>{step.get('title')} ({step.get('timeline')})</b>", metadata_style))
        story.append(Paragraph(f"Action: {step.get('action')}<br/>Deliverable: {step.get('deliverables')}", body_style))
        story.append(Spacer(1, 5))
        
    story.append(Spacer(1, 25))
    story.append(Paragraph("End of Consulting Deliverable.", ParagraphStyle('EndText', parent=body_style, alignment=1, fontName='Helvetica-Oblique', textColor=colors.HexColor("#64748b"))))

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer
