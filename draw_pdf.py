from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import json

'''
<ITEXT CH="11登的"/>
<para/>
<ITEXT CH="居中"/>
<para ALIGN="1"/>
<ITEXT CH="左对齐"/>
<para ALIGN="0"/>
<ITEXT CH="右对齐"/>
<para ALIGN="2"/>
<ITEXT CH="两端对齐"/>
<para ALIGN="3"/>
<ITEXT CH="两端对齐有缩进"/>
<para ALIGN="3" FIRST="24"/>
<ITEXT CH="分散对齐"/>
<trail ALIGN="4"/>
'''

class PDF_Canvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cover(self, pages, txt_boxs):
        self.setPageSize((pages[0]['w'], pages[0]['h']))
        for tb in txt_boxs:
            if tb['pg'] != 0: continue
            self.draw_multiline_text(tb['x'], tb['y'], tb['texts'])
        self.drawString(100, 100, "Page 1 - Letter Size Content")
        self.showPage()

    def draw_multiline_text(self, x, y, lines):
        current_y = y
        for line in lines:
            current_x = x
            for part in line['text']:
                fs = self.get_formatted_string(part)
                fs.drawOn(self, current_x, current_y)
                current_x += fs.width
            current_y -= max(fs.height for fs in [self.get_formatted_string(part) for part in line['text']])

    def get_formatted_string(self, part):
        text = part['text']
        style = self.get_paragraph_style(part)
        return Paragraph(text, style=style)

    def get_paragraph_style(self, part):
        style = ParagraphStyle("custom_style", fontName=part['font'], fontSize=part['size'], textColor=part['fcolor'])
        if 'inherit bold' in part['feat']:
            style.bold = True
        return style

if __name__ == '__main__':
    with open('pages.json', 'r', encoding='utf-8') as f:
        pages = json.load(f)
    with open('texts.json', 'r', encoding='utf-8') as f:
        texts = json.load(f)
    pdf = PDF_Canvas('output.pdf')
    pdf.cover(pages, texts)
    pdf.save()