from xml.etree.ElementTree import Element

def get_xywh(a: Element):
    b = {
        'x': float(a.get('XPOS')),
        'y': float(a.get('YPOS')),
        'w': float(a.get('WIDTH')),
        'h': float(a.get('HEIGHT'))
        }
    return b

def hex_cmyk_to_hex_rgb(hex_cmyk: str):
    def hex_to_float(value):
        return int(value, 16) / 255.0

    # 提取透明度和 CMYK 分量
    c = hex_to_float(hex_cmyk[:2])
    m = hex_to_float(hex_cmyk[2:4])
    y = hex_to_float(hex_cmyk[4:6])
    k = hex_to_float(hex_cmyk[6:])

    # 转换为 RGB
    r = int(255 * (1 - c) * (1 - k))
    g = int(255 * (1 - m) * (1 - k))
    b = int(255 * (1 - y) * (1 - k))

    # 转换为十六进制 RGB
    hex_rgb = "#{:02X}{:02X}{:02X}".format(r, g, b)
    return hex_rgb

def get_vector_path(path_name):
    cursor.execute('SELECT data FROM vector WHERE name = ?', (path_name,))
    return cursor.fetchall()[0][0].decode('utf-8')