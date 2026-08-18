import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(company_name, ticker, current_price, pe_ratio, volatility, sentiment, risks, opportunities):
    """
    Generates a professional downloadable PDF financial report.
    """
    filename = f"{ticker}_Research_Report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor("#1f4e79"),
        spaceAfter=10
    )
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#2e75b6"),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor("#333333"),
        spaceAfter=6
    )

    # Document Header
    story.append(Paragraph(f"FinMind AI — Executive Research Report", title_style))
    story.append(Paragraph(f"<b>Company:</b> {company_name} ({ticker})", body_style))
    story.append(Paragraph(f"<b>Report Generated via FinMind AI Platform</b>", body_style))
    story.append(Spacer(1, 10))
    
    # Key Financial Metrics Table
    story.append(Paragraph("Key Financial Metrics", heading_style))
    data = [
        ["Metric", "Value"],
        ["Current Stock Price", f"₹{current_price:,.2f}" if isinstance(current_price, (int, float)) else str(current_price)],
        ["Trailing P/E Ratio", str(pe_ratio)],
        ["Annualized Volatility (Risk)", f"{volatility:.2f}%" if isinstance(volatility, (int, float)) else "N/A"],
        ["Market Sentiment Outlook", str(sentiment)]
    ]
    
    t = Table(data, colWidths=[200, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor("#2e75b6")),
        ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f2f2f2")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    # Risk Signals Section
    story.append(Paragraph("Evaluated Risk Signals", heading_style))
    for r in risks:
        story.append(Paragraph(f"• {r}", body_style))
        
    story.append(Spacer(1, 6))
    
    # Opportunity Signals Section
    story.append(Paragraph("Evaluated Opportunity Signals", heading_style))
    for o in opportunities:
        story.append(Paragraph(f"• {o}", body_style))
        
    doc.build(story)
    return filename