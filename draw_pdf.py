from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
# 第一页使用 letter 尺寸
pdf_filename = 

def cover(pdf_filename, pages, txt_boxs):
    pdf_canvas = canvas.Canvas(pdf_filename, pagesize=(pages[0]['w'], pages[0]['h']))
    for tb in txt_boxs:
        pdf_canvas.rect(tb['x'], tb['y'], tb['w'], tb['h'])
    pdf_canvas.drawString(pages[0]['w'], pages[0]['h'], "Page 1 - Letter Size Content")
    pdf_canvas.showPage()