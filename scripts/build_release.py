from pathlib import Path
import re, zipfile
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

OUT=Path("dist"); OUT.mkdir(exist_ok=True)
S=getSampleStyleSheet()
S.add(ParagraphStyle(name="TitleBook",parent=S["Title"],fontSize=25,leading=30,textColor=colors.HexColor("#183153"),spaceAfter=18))
S.add(ParagraphStyle(name="SectionBook",parent=S["Heading2"],fontSize=14,leading=18,textColor=colors.HexColor("#147D83"),spaceBefore=15,spaceAfter=8))
S.add(ParagraphStyle(name="BodyBook",parent=S["BodyText"],fontSize=9,leading=13,spaceAfter=7))
S.add(ParagraphStyle(name="CodeBook",fontName="Courier",fontSize=7,leading=10,backColor=colors.HexColor("#F1F5F7"),leftIndent=8,spaceAfter=9))
def build(src,dest,title):
    story=[]; block=[]; code=False
    def flush():
        if block:
            for i in range(0,len(block),42):
                story.append(Preformatted("\n".join(block[i:i+42]),S["CodeBook"],maxLineLength=92))
            block.clear()
    for line in Path(src).read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            if code: flush()
            code=not code
            continue
        if code:
            block.append(line)
            continue
        if line.startswith("# "): story.append(Paragraph(escape(line[2:]),S["TitleBook"]))
        elif line.startswith("## "): story.append(Paragraph(escape(line[3:]),S["SectionBook"]))
        elif line.startswith("### "): story.append(Paragraph(escape(line[4:]),S["Heading3"]))
        elif line.strip() and not line.startswith("---"):
            txt=escape(line).replace("**","").replace("`","")
            story.append(Paragraph(txt,S["BodyBook"]))
    flush()
    def footer(canvas,doc):
        canvas.setFont("Helvetica",8);canvas.setFillColor(colors.HexColor("#183153"))
        canvas.drawString(42,28,"HOW SQL THINKS  |  JAGJOT BHARDWAJ")
        canvas.drawRightString(553,28,str(doc.page))
    SimpleDocTemplate(str(dest),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=48,bottomMargin=48,title=title,author="Jagjot Bhardwaj").build(story,onFirstPage=footer,onLaterPages=footer)
build("book/How_SQL_Thinks.md",OUT/"How_SQL_Thinks_Reader.pdf","How SQL Thinks")
build("book/Answer_Key.md",OUT/"How_SQL_Thinks_Answer_Key.pdf","How SQL Thinks - Answer Key")
with zipfile.ZipFile(OUT/"How_SQL_Thinks_Complete_Package.zip","w",zipfile.ZIP_DEFLATED) as z:
    for path in ["book/How_SQL_Thinks.md","book/Answer_Key.md","practice/seed.sql","practice/practice.py"]:
        z.write(path)
    for path in [OUT/"How_SQL_Thinks_Reader.pdf",OUT/"How_SQL_Thinks_Answer_Key.pdf"]:
        z.write(path,path.name)
