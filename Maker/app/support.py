from PIL import Image

def crop_img(filepath, x, y, w, h):
    img = Image.open(filepath)
    img = img.crop((x, y, x+w, y+h))
    img.save(filepath)
