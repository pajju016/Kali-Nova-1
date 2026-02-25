import os
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

from core.app_state import app_state


class ReportGenerator:

    REPORT_DIR = "reports"

    @staticmethod
    def generate():

        if not os.path.exists(ReportGenerator.REPORT_DIR):
            os.makedirs(ReportGenerator.REPORT_DIR)

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M_report.pdf")
        filepath = os.path.join(ReportGenerator.REPORT_DIR, filename)

        doc = SimpleDocTemplate(filepath)
        elements = []

        styles = getSampleStyleSheet()

        title_style = styles["Heading1"]
        normal_style = styles["Normal"]

        # Title
        elements.append(Paragraph("Kalinova Security Assessment Report", title_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Date
        elements.append(Paragraph(f"Generated: {datetime.now()}", normal_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Open Ports
        elements.append(Paragraph("Open Ports Detected:", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))

        if app_state.open_ports:
            port_list = [ListItem(Paragraph(str(p), normal_style)) for p in app_state.open_ports]
            elements.append(ListFlowable(port_list, bulletType='bullet'))
        else:
            elements.append(Paragraph("No open ports detected.", normal_style))

        elements.append(Spacer(1, 0.3 * inch))

        # Risk Level
        elements.append(Paragraph("Risk Level:", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))

        risk_color = colors.green

        if app_state.global_risk == "MEDIUM":
            risk_color = colors.orange
        elif app_state.global_risk == "HIGH":
            risk_color = colors.red

        risk_style = ParagraphStyle(
            name="RiskStyle",
            parent=styles["Normal"],
            textColor=risk_color
        )

        elements.append(Paragraph(app_state.global_risk, risk_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Suggestions
        elements.append(Paragraph("Recommendations:", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph(app_state.suggestion, normal_style))

        doc.build(elements)

        return filepath