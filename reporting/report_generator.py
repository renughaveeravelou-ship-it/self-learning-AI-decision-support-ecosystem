from copilot.executive_copilot import executive_summary
import os

def generate_report(output_filename="Executive_Report.pdf"):
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
    except ImportError as exc:
        raise RuntimeError(f"reportlab is required to generate PDFs: {exc}")

    # Save in the same folder as this script, or root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    pdf_path = os.path.join(root_dir, output_filename)

    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    content = []

    # Title
    content.append(Paragraph("Executive AI Report", styles["Title"]))
    content.append(Spacer(1, 12))

    # Body
    summary_text = executive_summary()
    for line in summary_text.split("\n"):
        if line.strip():
            content.append(Paragraph(line, styles["BodyText"]))
            content.append(Spacer(1, 6))

    doc.build(content)
    print(f"Executive Report Generated: {pdf_path}")
    return pdf_path
