import colorsys

def hsv_to_rgb_normalized(h_65535, s_255, v_255):
    h = h_65535 / 65535.0
    s = s_255 / 255.0
    v = v_255 / 255.0

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)