import sqlite3
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import json

dpsf_path = '期刊杂志-大16开骑马钉-文学杂志期刊模板240115-1352.dpsf'
conn = sqlite3.connect(dpsf_path)
# 创建游标
cursor = conn.cursor()
# 执行查询
cursor.execute('SELECT data FROM root WHERE name = "doc"')
xml_data = cursor.fetchall()[0][0]
root = ET.fromstring(xml_data)
document_element = root.find('DOCUMENT')

def read_pages(document_element):
    raw_pages = document_element.findall('PAGE')
    pages = {}
    for pg in raw_pages:
        t = {
        'x': float(pg.get('PAGEXPOS')),
        'y': float(pg.get('PAGEYPOS')),
        'w': float(pg.get('PAGEWIDTH')),
        'h': float(pg.get('PAGEHEIGHT'))
        }
        num = pg.get('NUM')
        pages[num] = t

    return pages


def read_texts(document_element):
    raw_text_box = document_element.findall('PAGEOBJECT[@PTYPE="4"]')
    #raw_text_box = document_element.findall('PAGEOBJECT')
    text_boxs = []
    for tb in raw_text_box:
        text_box = {
            'x': float(tb.get('XPOS')),
            'y': float(tb.get('YPOS')),
            'w': float(tb.get('WIDTH')),
            'h': float(tb.get('HEIGHT')),
            'pg': int(tb.get('OwnPage')),
        }
        
        if raw_text := tb.find('StoryText'):
            texts = []
            for e in raw_text:
                if e.tag == 'ITEXT':
                    text = e.get('CH', '')
                elif e.tag == 'para':
                    align = int(e.get('ALIGN', '3'))
                    idt =  float(e.get('FIRST', '0'))
                    texts.append({'text': text, 'align': align, 'idt': idt})
                elif e.tag == 'trail':
                    align = int(e.get('ALIGN', '3'))
                    idt =  float(e.get('FIRST', '0'))
                    texts.append({'text': text, 'align': align, 'idt': idt})
            
            text_box['text'] = texts
        else:
            continue
        a = any(isinstance(v, Element) for v in text_box.values())
        if a:
            raise Exception(f"{text_box} is not a valid text box")
        text_boxs.append(text_box)

    return text_boxs

if __name__ == '__main__':
    tbs = read_texts(document_element)
    pgs = read_pages(document_element)
    with open('texts.json', 'w', encoding='utf-8') as f:
        try:
            json.dump(tbs, f, ensure_ascii=False, indent=4)
        except:
            f.write(str(tbs))
    with open('pages.json', 'w', encoding='utf-8') as f:
        json.dump(pgs, f, ensure_ascii=False, indent=4)