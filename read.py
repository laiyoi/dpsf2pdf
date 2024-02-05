import sqlite3
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import json
from utils import get_xywh, hex_cmyk_to_hex_rgb, get_vector_path

dpsf_path = '无图.dpsf'
conn = sqlite3.connect(dpsf_path)
# 创建游标
cursor = conn.cursor()
# 执行查询
cursor.execute('SELECT data FROM root WHERE name = "doc"')
xml_data = cursor.fetchall()[0][0]
root = ET.fromstring(xml_data)
#document_element = root.find('DOCUMENT')

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
        num = int(pg.get('NUM'))
        pages[num] = t

    return pages

def read_vectors(document_element):
    raw_vectors = document_element.findall('PAGEOBJECT[@PTYPE="12"]')
    vectors = []
    for vec in raw_vectors:
        full = {
            **get_xywh(vec),
            'pg': int(vec.get('OwnPage')),
            'path': vec.get('path_md5')
        }
        parts = []
        for raw_part in vec.findall('PAGEOBJECT'):
            part = {
                **get_xywh(raw_part),
                'path': get_vector_path(raw_part.get('path_md5'))
            }
            colors = []
            for e in raw_part:
                color = e.get('NAME')
                colors.append(color)
            part['colors'] = colors
            parts.append(part)
        full['parts'] = parts
        vectors.append(full)
    return vectors


def read_imgs_info(document_element):
    raw_imgs = document_element.findall('PAGEOBJECT[@PTYPE="2"][@PFILE]')
    imgs = []
    for raw_img in raw_imgs:
        img = {
            **get_xywh(raw_img),
            'pg': int(raw_img.get('OwnPage')),
            'path': raw_img.get('PFILE'),
        }
        imgs.append(img)
    return imgs
    

def read_texts(document_element):
    raw_text_box = document_element.findall('PAGEOBJECT[@PTYPE="4"]')
    #raw_text_box = document_element.findall('PAGEOBJECT')
    text_boxs = []
    for tb in raw_text_box:
        text_box = {
            **get_xywh(tb),
            'pg': int(tb.get('OwnPage')),
        }
        
        if raw_text := tb.find('StoryText'):
            texts = []
            for e in raw_text:
                if e.tag == 'ITEXT':
                    text = e.get('CH', '')
                    size = float(e.get('FONTSIZE', '12'))
                    color = e.get('FCOLOR', '000000')
                    if color[0] == '#':
                        color = color[1:]
                    elif color[0] == '@':
                        color = hex_cmyk_to_hex_rgb(color[1:])
                    else:
                        color = '000000'
                    feat = e.get('FEATURES', '')
                elif e.tag == "para" or (e.tag == "trail"):
                    align = int(e.get('ALIGN', '3'))
                    idt =  float(e.get('FIRST', '0'))
                    texts.append({'text': text, 'size': size, 'color': color,
                                'feat': feat, 'align': align, 'idt': idt})
            text_box['text'] = texts
        else:
            continue
        a = any(isinstance(v, Element) for v in text_box.values())
        if a:
            raise Exception(f"{text_box} is not a valid text box")
        text_boxs.append(text_box)

    return text_boxs

if __name__ == '__main__':
    document_element = ET.parse('无图.xml').find('DOCUMENT')
    tbs = read_texts(document_element)
    pgs = read_pages(document_element)
    imgs = read_imgs_info(document_element)
    vectors = read_vectors(document_element)
    with open('texts.json', 'w', encoding='utf-8') as f:
        try:
            json.dump(tbs, f, ensure_ascii=False, indent=4)
        except:
            f.write(str(tbs))
    with open('pages.json', 'w', encoding='utf-8') as f:
        json.dump(pgs, f, ensure_ascii=False, indent=4)
    with open('images.json', 'w', encoding='utf-8') as f:
        json.dump(imgs, f, ensure_ascii=False, indent=4)
    with open('vectors.json', 'w', encoding='utf-8') as f:
        json.dump(vectors, f, ensure_ascii=False, indent=4)